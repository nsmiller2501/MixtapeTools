# Fanout Extraction Implementation Spec

Status: draft implementation plan
Date: 2026-05-19

## Goal

Replace whole-paper marker-mode reading with fanout-first extraction for academic PDFs. The design should reduce Read-limit failures and prompt cache amplification while preserving a neutral `_text.md` source of truth and project-specific wiki updates.

## Core Invariants

- `read-pdf` owns marker conversion and the reusable extraction substrate.
- `wiki-update` consumes the `read-pdf` substrate and adds project-wiki behavior.
- `_text.md` is project-neutral regardless of whether it was produced by `read-pdf` or `wiki-update`.
- Wiki pages are project-oriented and pass through the project-relevance gate.
- Chunk workers extract local evidence only; the synthesis bottleneck owns paper-level interpretation.
- Fanout workers run sequentially by default so a usage-limit failure loses at most one active worker bundle.

## Implementation Plan

### 1. Add `read-pdf/scripts/prepare_substrate.py`

Input: marker `markdown.md`.

Outputs beside the marker cache:

```text
chunks/
  chunk_001-title-abstract-introduction.md
  chunk_002-background-methods.md
  ...
manifest.json
```

Responsibilities:

- Split converted markdown into chunks.
- Prefer clean section/subsection boundaries.
- Enforce a hard chunk ceiling; split oversized sections at the safest paragraph, table, equation, or figure boundary.
- Merge tiny adjacent sections where safe.
- Generate sanitized chunk filenames from structural headings.
- Generate a structural manifest with source path, chunk paths, headings, line/character ranges, page anchors, figure/table references, and deterministic DOI candidates.
- Generate a worker-bundle plan by grouping adjacent chunks under a hard worker-source ceiling.
- Perform no scholarly interpretation and no summarization.

### 2. Add Fanout Prompt Docs Under `read-pdf`

Add:

- `fanout_worker.md`
- `fanout_synthesis.md`

Worker prompt responsibilities:

- Receive a bundle-specific assignment excerpt, not the full manifest.
- Read assigned bundle chunks in one tool turn when possible.
- Write one durable local note file per bundle.
- Use position-specific instructions:
  - front-matter worker: bibliographic candidates, abstract, introduction framing, stated contributions
  - body worker: local evidence only, skip bibliographic reconstruction unless new or contradictory metadata appears
  - back-matter worker: appendix evidence, robustness material, replication/data availability clues
- Maintain an unfiltered formal-object inventory: tables, figures, equations, specifications, algorithms, propositions, and similar objects.
- Avoid paper-level conclusions.

Synthesis prompt responsibilities:

- Read full manifest and all worker notes.
- Write neutral `_text.md`.
- Gap-directed source rereads only: if worker notes omit a needed table, figure, equation, or claim, reread the specific source chunk and report why.
- For `wiki-update`, write neutral `_text.md` first, then apply project context to wiki pages.

### 3. Upgrade Neutral Extraction Schema

Update `read-pdf/extraction_schema.md` and align `wiki-update/common.md` around one neutral extract shape:

- Bibliographic metadata
- Plain-English synthesis
- Research question
- Audience
- Method / identification strategy
- Target parameter
- Data
- Statistical methods / specifications
- Findings
- Contributions
- Replication feasibility
- Tables
- Figures
- Equations / formal objects

Policy difference:

- `read-pdf`: project-neutral; synthesis decides what is important for understanding, building on, or replicating the paper.
- `wiki-update`: `_text.md` remains neutral; wiki pages apply the project-relevance gate.

### 4. Update `read-pdf` Marker Isolation

Update `isolation_read.md`:

1. Parent runs install/cache/convert.
2. Parent runs `prepare_substrate.py`.
3. Parent launches worker subagents sequentially for each worker bundle.
4. Parent launches synthesis bottleneck after all worker notes exist.
5. Parent reads final `_text.md` only.

Keep split mode as the separate legacy vision-batch path unless later work unifies it.

### 5. Update `wiki-update` Protocol M

Protocol M should:

- Use the `read-pdf` substrate and fanout worker notes for marker markdown.
- Stop asking one subagent to read the whole `markdown.md`.
- Stop embedding `protocol_m.md` and `common.md` verbatim in prompts; pass file paths plus a compact checklist.
- Use one synthesis bottleneck to write:
  - neutral `references/raw/<basename>_text.md`
  - project-oriented wiki pages/index/log updates
  - proposed destructive diffs, if any
- Preserve journal-and-rollback semantics for wiki writes.

### 6. Add `wiki-update/scripts/citation_overlap.py`

Inputs:

- new paper marker `markdown.md`
- `references/references.bib`

Output:

- `references/raw/raw_build/<basename>_citation_overlap.json`

Rules:

- If `references/references.bib` is missing or empty, emit an empty candidate set.
- Extract candidate references mechanically from the new paper's references section.
- Compare only against existing BibTeX entries.
- Output only overlap candidates, not the full bibliography.
- Use deterministic match labels such as:
  - `doi_exact`
  - `title_exact_normalized`
  - `title_substring_normalized`
  - `author_year_exact`
  - `author_year_fuzzy`
  - `bib_key_string_seen`
- Add a deterministic priority score for sorting; do not emit scholarly relevance judgments.
- Cap prompt excerpt to top 10 candidates; cap JSON to a reasonable maximum such as 50.

## A/B Testing Spec

### Question

Does fanout-first extraction reduce token/cache cost and failure risk without materially degrading `_text.md` or wiki quality relative to whole-paper ingest?

### Test Inputs

Use fixed cached marker outputs rather than fresh uncached conversion. This isolates extraction architecture from marker runtime variability.

Run at least two papers:

- Bento et al. JEEM: short but token-heavy, methods/results/figures stress case.
- Anderson et al. NBER: longer working paper with appendix/reference stress.

For each paper, pin:

- source PDF
- cached `markdown.md`
- project `CLAUDE.md`
- `references/CLAUDE.md`
- starting `references/wiki/index.md`
- starting `references/wiki/log.md`
- starting `references/references.bib`

### Test Procedure

1. Create a throwaway wiki project.
2. Run the current whole-paper `wiki-update` implementation.
3. Archive:
   - `references/raw/<basename>_text.md`
   - all touched `references/wiki/*.md`
   - `references/wiki/index.md`
   - `references/wiki/log.md`
   - copied figures
   - subagent transcript JSONL
   - cached input token totals, non-cached input tokens, and output tokens
4. Reset the throwaway wiki to the identical starting state.
5. Run the fanout implementation against the same cached marker output.
6. Archive the same artifacts.
7. Compare cost, reliability, and quality.

### Cost Metrics

Collect from JSONL transcripts where available:

- total cached input tokens
- total non-cached input tokens
- total output tokens
- number of subagents
- number of tool turns
- wall-clock time
- failure point if a usage limit or platform interruption occurs
- salvageable artifacts left on disk after failure

### Quality Rubric

Score each output 1-5 on:

- Coverage: captures research question, method, data, findings, contribution, target parameter, replication details.
- Specificity: includes equations, sample details, variables, coefficients, standard errors, table/figure references where relevant.
- Faithfulness: avoids unsupported claims and preserves uncertainty.
- Organization: `_text.md` is coherent and not a stitched chunk log.
- Formal objects: tables, figures, equations, and propositions are inventoried and treated appropriately.
- Wiki usefulness: pages are concise, project-relevant, linked, and source-cited.
- Cross-reference handling: citation-overlap candidates are used only when substantively useful.
- Duplication control: avoids repeated bibliography, intro-summary repetition, and conflicting claims.

### Acceptance Criteria

Fanout is acceptable if:

- cached input token use falls materially relative to whole-paper ingest;
- no Read-limit failure occurs on marker `markdown.md`;
- `_text.md` remains project-neutral and coherent;
- wiki pages remain project-relevant;
- no critical method, data, result, table, figure, or equation is lost relative to whole-paper ingest;
- failures leave completed worker notes that can be resumed or salvaged.

### Review Method

Use a structured side-by-side review, not an impressionistic "which reads better" judgment. Record concrete misses and false additions. If fanout loses nuance, decide whether the issue belongs in worker instructions, synthesis instructions, or chunking/bundling.

## Comparison Against `write-a-skill` Design

### What Matches

- Deterministic operations become scripts:
  - `prepare_substrate.py`
  - `citation_overlap.py`
- Long instructions are split out of `SKILL.md`:
  - fanout worker prompt
  - fanout synthesis prompt
  - extraction schema
- Progressive disclosure improves:
  - parent prompt passes compact excerpts and paths
  - workers read only assigned bundle context
  - synthesis reads full manifest and notes
- References stay one level deep from the loaded skill docs.
- The skill descriptions should remain trigger-oriented and under 1024 characters.

### Risks To Watch

- `SKILL.md` files may exceed the recommended 100 lines unless fanout details live in separate reference files.
- `wiki-update` currently embeds protocol/common files verbatim; this conflicts with progressive disclosure and should be replaced with path-based loading plus compact checklists.
- Too much manifest content in prompts can recreate context bloat; pass excerpts, keep full metadata on disk.
- If worker prompts include the full final schema, workers may overclaim from partial context. Use local-note schema instead.
- If citation-overlap output includes too much bibliography detail, it becomes another bulky source. Emit only capped candidates.

### Needed Skill-Structure Changes

For `read-pdf`:

```text
read-pdf/
  SKILL.md
  extraction_schema.md
  agent_isolation.md
  isolation_read.md
  fanout_worker.md
  fanout_synthesis.md
  scripts/
    prepare_substrate.py
```

For `wiki-update`:

```text
wiki-update/
  SKILL.md
  common.md
  protocol_m.md
  scripts/
    citation_overlap.py
```

`SKILL.md` should route workflows and link to these files; detailed fanout behavior should not live inline.

### Open Implementation Questions

- Exact soft target and hard ceiling for chunk and worker-bundle sizes.
- Manifest schema details and whether to include both line and character offsets.
- Whether `prepare_substrate.py` should be idempotent by comparing source mtime, source hash, or manifest version.
- Resume behavior when some worker notes exist and others are missing.
- Exact transcript parser for token accounting in the A/B test.
