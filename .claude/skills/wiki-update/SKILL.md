---
name: wiki-update
description: Ingests new PDFs from `references/raw/` into a project wiki and refreshes its bibliography. Use when the user asks to ingest references or update the wiki.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(pdftotext:*), Bash(python3:*), Bash(mv:*), Bash(cp:*), Bash(mkdir:*), Bash(rm:*), Bash(touch:*), Agent
argument-hint: [optional focus or theme for this batch]
---

# wiki-update: Ingest new references into the project wiki

Maintains a project's reference wiki by ingesting newly-added PDFs from `references/raw/`, summarizing each through the lens of the project's research focus, and updating the wiki atomically per-paper.

**Ingest path is auto-detected per paper.** Use a local `references/raw/<basename>_text.md` when present (Protocol E). Otherwise, reuse a cached neutral extract (Tier M-cache), run bounded marker extraction (Protocol M), or use split-PDF extraction after converter failure (Protocol S). Every extraction path follows `read-pdf/extraction_schema.md`; project relevance enters only after the neutral extract exists.

**`pdftotext` is not an ingest source.** It is allowed only for narrow pre-flight tasks: first-page filename proposals when the converter is unavailable, metadata checks needed for `/bib-update`, and other explicit bootstrap/diagnostic checks that do not synthesize wiki content. Once a paper is assigned to Protocol M, M-cache, or E, do not use `pdftotext` to read, summarize, validate, or supplement substantive content. Wait for the selected input (`manifest.json` plus bounded chunks, or `_text.md`) and read that source only.

## When this skill is invoked

The user has added one or more PDFs to `references/raw/` and wants the wiki updated. The optional argument is a free-form focus string (e.g., "focus on IV strategies and instrument validity") that applies to this batch in addition to the project's standing context.

## Pre-flight (main session)

Run all checks before any ingest work. If anything fails, stop and ask the user.

### 0. Lazy scaffolding (first invocation in a project)

Run the scaffold script — idempotent, safe to re-run:

```bash
~/.claude/skills/wiki-update/scripts/scaffold_wiki.sh
```

It creates `references/{raw,wiki,wiki/figures}/`, renders `references/CLAUDE.md` from the template (substituting the project name), initializes empty `wiki/index.md` and `wiki/log.md`, and appends a `references/CLAUDE.md` pointer to the project root `CLAUDE.md` if one exists. All steps no-op when the target already exists.

After this self-bootstrap, the rest of the pre-flight (steps 1–6 below) runs as before.

### 1. Locate the wiki

Check that `./references/raw/` and `./references/wiki/` both exist relative to the current working directory. If either is still missing after the lazy-scaffolding step, ask the user where the wiki lives. Do not search parent directories.

Read `./references/CLAUDE.md` for project-specific wiki conventions (page format, citation rules, naming). These conventions take precedence over anything in this skill if they conflict — this skill defines *workflow*, not *format*.

### 2. Verify project context is filled in

Read `./CLAUDE.md` (the project root file). Check the "Research Question," "Data Sources," and "Identification Strategy" fields (or their equivalents). If any are still placeholder text — bracketed phrases like `[What are you trying to answer?]`, `[What data are you using?]`, or otherwise unfilled — **stop and ask the user to fill them in first**. Explain that relevance filtering depends on this context.

The optional `[focus]` argument supplements but does not replace the project CLAUDE.md context.

### 3. Discover new papers

Read `./references/wiki/log.md` to find previously-ingested filenames. List files in `./references/raw/` that do not appear in the log.

**Non-PDF files:** If any non-PDF files are present in `raw/`, surface them before continuing:

```
Non-PDF files found in references/raw/: <filenames>
These were skipped for ingest. Move them elsewhere if they don't belong, or tell me if any should be treated differently.
```

Include skipped filenames in the end-of-run summary under "Skipped (non-PDF)."

Proceed with PDF files only, in filename-sorted order. If no new PDFs are found, report that and exit.

### 4. Normalize filenames

Each new PDF must conform to the project naming convention before ingest. This runs in the **main session** (not subagents) so renames can be batched and approved once.

**Convention:**
- 1 author → `Last_Year_Venue.pdf`
- 2 authors → `Last1_Last2_Year_Venue.pdf`
- 3+ authors → `Last1_etal_Year_Venue.pdf`
- Venue slug: standard econ journal abbreviation (`AER`, `JPE`, `QJE`, `JEEM`, `JHE`); `NBER` / `SSRN` / `IZA` for known WP series; `WP` for generic working papers; chapter abbrev or `Book` for book chapters.

**Skip condition.** A filename matching
```
^[A-Z][a-zA-Z]+(_[A-Z][a-zA-Z]+|_etal)?(_[A-Z][a-zA-Z]+){0,2}_\d{4}_[A-Z][A-Za-z]+\.pdf$
```
is already-conforming and passed through untouched. Non-conforming files go through the propose-and-approve flow below.

**Extracting text for name proposal:**

For each non-conforming file, extract enough text to propose a name. Choose the method based on what's available:

- **If `~/.claude/skills/read-pdf/convert.py` exists:** run
  ```bash
  python3 ~/.claude/skills/read-pdf/convert.py "<pdf-path>"
  ```
  Capture and retain the printed path to `markdown.md`. Read the first ~2000 characters of `markdown.md` — this covers title, authors, year, and venue. This also primes the converter cache for the ingest step that follows (the cache is SHA-keyed, so renaming the PDF after this point does not invalidate it).

- **Otherwise:** run `pdftotext -l 1 "<pdf-path>" -` and read the output.

If either method returns empty or <50 chars of non-whitespace, mark the file as **unparseable** and flag for manual handling.

This `pdftotext` fallback is for filename proposal only. Do not reuse its output for paper synthesis, wiki page writing, tables, figures, or relevance filtering.

**Batched approval.** After proposals for all non-conforming files are ready, present as one block:

```
Proposed renames (N files):
  <current-name>  → <proposed-name>
  ...

Already conform (skipped): K files

Unparseable (needs manual decision):
  ⚠ <current-name>  — extraction failed: <reason>
    Keep as-is / Provide name?

Approve all / Edit (per-file) / Reject all?
```

- **Approve all** → apply all renames via `mv`.
- **Edit** → per-file review; for each, user can approve, edit, or skip.
- **Reject all** → proceed with no renames.

**Collision handling** (before any `mv`): proposed name matches existing file → block and ask user to provide an alternative. Two proposals in the batch collide with each other → flag both, require disambiguation (e.g., appending a title word).

Never silently overwrite. Never proceed past a collision without user input.

After renames are applied, re-list new PDFs under their new names before continuing.

### 5. Pre-scan: classify each paper into an ingest tier

For each new paper (using its post-rename canonical name), determine its ingest protocol. This classification runs entirely in the main session — each subagent receives exactly one protocol with no branching.

**Check order (stop at the first match):**

1. **Tier E — Local cached extract:** `references/raw/<basename>_text.md` exists. No conversion needed.

2. **Tier M-cache — Cached neutral extract in converter cache:** `~/.claude/skills/read-pdf/convert.py` exists. Reuse the `markdown.md` path retained during filename normalization; if none was produced, run `convert.py` once. If conversion succeeds and:
   ```bash
   python3 ~/.claude/skills/read-pdf/scripts/cache_text.py check "<markdown.md path>"
   ```
   prints a cache path. Copy it locally with:
   ```bash
   python3 ~/.claude/skills/read-pdf/scripts/cache_text.py pull "<markdown.md path>" "references/raw/<basename>_text.md"
   ```
   Then proceed directly to wiki synthesis. No worker fanout or read-pdf synthesis is needed.

3. **Tier M — Converted markdown substrate / bounded extract:** conversion succeeded and no neutral extract was cached. Reuse the retained `markdown.md` path and prepare the read-pdf extraction substrate:

   ```bash
   python3 ~/.claude/skills/read-pdf/scripts/prepare_substrate.py "<markdown.md path>"
   ```

   Capture the printed `manifest.json` path. Its `execution_mode` selects one sequential paper reader by default or bounded fanout only above 100,000 projected working tokens. Readers consume chunk files rather than the whole `markdown.md`.

   If `references/references.bib` exists, also run the mechanical citation-overlap scan. All Protocol M scratch for a paper lives under the single directory `references/raw/raw_build/<basename>_fanout/`, so create it first:

   ```bash
   mkdir -p "references/raw/raw_build/<basename>_fanout"
   python3 ~/.claude/skills/wiki-update/scripts/citation_overlap.py \
     "<markdown.md path>" references/references.bib \
     --output "references/raw/raw_build/<basename>_fanout/citation_overlap.json"
   ```

   Pass the output JSON path to Protocol M wiki synthesis. These are candidate overlaps only; the wiki agent decides whether any are substantively useful for links.

   If `convert.py` exists but fails for a specific paper (conversion error), report the error, skip marker tiers for that paper, and fall through to tier S. Do not use `pdftotext` as a temporary or parallel substitute while conversion is running or after conversion fails.

4. **Tier S — Split-PDF pipeline:** Neither of the above. For each tier-S paper, run the read-pdf split backend from the main session so the subagent receives a populated splits directory:

   ```bash
   python3 ~/.claude/skills/read-pdf/scripts/split.py \
     references/raw/<basename>.pdf \
     --output-dir references/raw/raw_build/split_<basename>
   ```

   `split.py` is the pypdf splitter for tier-S ingestion. It is idempotent at the chunk-file level: if the output directory already contains the expected `<basename>_pp<X>-<Y>.pdf` files from a prior interrupted run, re-running rewrites them with identical content. Call the script directly so the populated split directory can be passed to the paper reader.

**Report tier breakdown once, before starting per-paper agents:**

```
Ingest tiers for this batch:
  E (local cached extract): N papers
  M-cache (cached neutral extract): N papers
  M (converted markdown): N papers
  S (full pipeline):      K papers

[If any converter failures:]
  ⚠ Converter failed for: <filenames> — falling back to E or S
```

### 6. Locate the wiki index

Retain the absolute path to `./references/wiki/index.md`. Each wiki agent reads the current file immediately before synthesis so earlier papers in the batch are visible.

---

## Per-paper ingest

Process papers sequentially. Use one extraction context per paper so a completed paper's source does not accumulate in the batch context.

- **Tier E:** start one wiki synthesis agent from the local `_text.md`.
- **Tier M-cache:** start one wiki synthesis agent from the copied `_text.md`, with cache figure paths available.
- **Tier M:** start one paper extraction agent. For `single_reader`, it reads bundles sequentially and writes a durable note after each; for `fanout`, it launches one bounded worker per bundle. It then synthesizes `references/raw/<basename>_text.md.tmp` using `read-pdf/extraction_schema.md`. The main session validates the temp file is non-empty and contains the bibliographic block, plain-English synthesis, and all 12 dimensions before moving it to the final path. Cache the validated neutral extract, then start one fresh wiki synthesis agent.
- **Tier S:** start one split reader agent that follows `read-pdf/isolation_split.md` and `read-pdf/extraction_schema.md`, validates and installs the neutral extract atomically, then start one fresh wiki synthesis agent using Protocol S.

Extraction agents write only neutral extraction scratch and `_text.md.tmp`; they do not receive project context or wiki paths. Wiki agents use the plan-then-apply journal protocol below.

Each agent prompt must be self-contained — the agent has no memory of this conversation.

All per-paper wiki-writing prompts include:

- Absolute paths: PDF, validated `_text.md`, `references/raw/`, `references/wiki/`, `references/wiki/figures/`, and `references/CLAUDE.md`
- The tier (M, M-cache, E, or S)
- Absolute path to the current `wiki/index.md`
- Absolute path to project root `CLAUDE.md`
- Optional batch focus string (if provided as the skill argument)
- Absolute path to exactly one protocol file: `protocol_m.md` for M and M-cache, `protocol_e.md` for E, or `protocol_s.md` for S.
- Absolute path to `~/.claude/skills/wiki-update/common.md`.
- Absolute path to `~/.claude/skills/wiki-update/wiki_synthesis.md`.
- For Tier M and M-cache only: cache `markdown.md` path, absolute cache figure directory, absolute project `references/wiki/figures` directory, `copy_marker_figure.py`, and citation-overlap JSON path if one was produced.

Tier M paper-reader prompts include `manifest.json`, `fanout_worker.md`, `fanout_synthesis.md`, `extraction_schema.md`, and output paths. For `single_reader`, the same agent processes every bundle. For `fanout`, bundle workers receive only `fanout_worker.md`, their bundle excerpt, assigned chunk paths, and output note path.

Tier M synthesis reads only `fanout_synthesis.md`, `extraction_schema.md`, `manifest.json`, worker note paths, and the temp `_text.md` path. It does not receive wiki paths, project context, protocol files, or citation-overlap JSON.

Do not embed the protocol or common files verbatim. Instead, the first instruction in each wiki-writing prompt must be:

```text
Before doing any paper work:
1. Read the protocol file at <absolute protocol path>.
2. Read the common file at <absolute common path>.
3. Follow those instructions exactly for this paper.
```

Wiki prompts pass paths rather than embedding index or project-context contents. Protocol M wiki synthesis uses `protocol_m.md`, `common.md`, `wiki_synthesis.md`, `_text.md`, citation-overlap JSON if present, and current wiki paths. It does not receive worker notes or marker chunks unless a specific extraction gap is approved for recovery.

This keeps spawned prompts small while still making the protocol explicit through normal file reads.

---

## Per-paper atomicity (main session)

For each paper, the main session uses a **plan-snapshot-apply** pattern. The wiki agent identifies every target before writing, the main session snapshots existing targets, and the same agent then applies the plan. The snapshot lives on disk rather than in orchestration context.

Distinguish three classes of file, each with its own safety mechanism:

- **Write-once durable artifacts** — the neutral `_text.md` and any brand-new wiki page. Protect `_text.md` by validated temp-file rename and record new wiki targets for deletion on failure.
- **Modified pre-existing files** — `index.md`, `log.md`, and existing pages gaining cross-links. These have a prior version worth restoring. Protect by **disk snapshot**: before editing, `cp` each into the paper's journal dir.
- **`log.md`** — written **last** (step 5), so it never leads the page writes.

**Phase 1 — plan:** The wiki agent reads the current index and relevant pages, resolves its intended edits, and returns:

```text
Existing targets to modify: [absolute paths]
New targets to create: [absolute paths]
Disambiguation questions: [...]
Proposed destructive edits: [...]
```

It does not write during this phase. Resolve disambiguation and destructive-edit approvals before continuing. Add `wiki/log.md` to the existing targets because the main session appends it after validation.

**Phase 2 — snapshot:** Create the journal and copy every existing target from the approved plan. Record new targets in `_new_files.txt`; their rollback is deletion. `_text.md` is outside this journal because extraction installed it atomically before wiki planning.

```bash
mkdir -p references/raw/raw_build/<basename>_fanout/_journal
# for each existing target, preserve its path relative to references/wiki:
mkdir -p references/raw/raw_build/<basename>_fanout/_journal/<relative-parent>
cp references/wiki/<relative-target> \
  references/raw/raw_build/<basename>_fanout/_journal/<relative-target>
# write each approved new target path to:
references/raw/raw_build/<basename>_fanout/_journal/_new_files.txt
```

**Phase 3 — apply and validate:** Send the approved plan back to the same agent. It applies only those targets and returns the normal summary. The main session verifies every planned target, appends the log entry, then cleans scratch:

   ```bash
   python3 ~/.claude/skills/wiki-update/scripts/clean_fanout.py \
     references/raw/raw_build --basename <basename>
   ```

   This removes the `<basename>_fanout/` directory and any Protocol S split PDFs, preserving only Protocol S's permanent `notes.md`. The neutral `_text.md` (in `references/raw/`) and copied figures (in `references/wiki/figures/`) are the durable, shareable artifacts and live outside `raw_build`.

**On failure before logging:** delete every path in `_new_files.txt`, restore every snapshotted file, and delete the `_text.md` only if this run created it. Leave the journal intact and omit the log entry so the next invocation retries cleanly.

The journal is removed with the rest of the paper's scratch after success. Retry starts from restored durable state rather than partially resuming wiki writes.

Finish and log each paper before starting the next.

---

## Post-log: update `references/references.bib`

After **all** papers have been ingested and logged, invoke `/bib-update` in append-only mode. It reads the `## Bibliographic metadata` blocks from each newly-ingested paper's `_text.md`, runs the DOI-direct → CrossRef → OpenAlex → LLM-fallback cascade, and appends new entries to `references/references.bib`. Papers already present in `.bib` are skipped automatically.

To regenerate `.bib` from scratch, run `/bib-update --rebuild-bib` as a separate, explicit step — not as part of a normal ingest run.

---

## End-of-run summary

After all papers are processed, report:

- Papers successfully ingested (with counts of pages created/modified, and for Protocol M: figures copied)
- Papers that failed (with brief reasons; user can re-invoke to retry)
- Any disambiguation decisions the user made
- Any equation-fallback transcriptions marked "[unreadable equation]" (so the user can manually fix them)
- **Pending figure clips (punch-list).** Aggregate every CLIP placeholder from all Protocol E and S subagents:

  ```
  Pending figure clips (N):
    1. references/wiki/figures/Smith_2024_AER_fig2.png
       Smith_2024_AER, p. 14 — "DAG of identification strategy"
    ...
  ```

  Open each PDF to the indicated page, clip the figure, save under the listed path. Wiki pages already reference these paths — broken-image placeholders resolve silently as each PNG is added.

---

## Rules

- **Treat source PDFs and completed `_text.md` extracts as immutable.** New extraction writes go through a validated temp file; existing extracts are reused. The converter cache at `~/.cache/claude-pdf-converter/` is scratch and may be overwritten.
- **`references/raw/raw_build/` is scratch, not a deliverable.** It holds only regenerable per-paper intermediates under the canonical `<basename>_fanout/` directory (Protocol M) and `split_<basename>/` (Protocol S). The main session removes a paper's scratch via `clean_fanout.py` once that paper ingests successfully. Never copy bundles or worker notes elsewhere, never invent alternate sub-folder names, and do not commit `raw_build/` contents — a coauthor without the local cache regenerates them from the PDF.
- **Use one bounded reader context per paper.** The batch context handles orchestration and approval; bundle-level fanout occurs only when the manifest projects more than 100,000 working tokens.
- **Never write the log entry before wiki edits complete.** The log is the source of truth for "what's been ingested" — it must lag behind, not lead.
- **Never invent project context.** If `CLAUDE.md` placeholders are unfilled, stop and ask. Do not guess the research question.
- **Project conventions in `references/CLAUDE.md` override this skill** if they conflict on format/naming/citation. This skill owns workflow only.
- **Never rename a PDF without user approval.** Even a single non-conforming file goes through the batched propose/approve flow. No silent `mv`. No overwriting an existing file.
- **Never fall back from the converter silently.** If `convert.py` errors on a PDF, report the error and proceed to tier E or S for that paper — do not substitute pdftotext output without telling the user.
- **Never use `pdftotext` for substantive ingest.** `pdftotext` is limited to first-page metadata/filename/bootstrap checks. It must not be used to summarize, validate, or supplement Protocol M or Protocol E content.
