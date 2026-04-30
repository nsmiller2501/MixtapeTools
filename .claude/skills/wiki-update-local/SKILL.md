---
name: wiki-update-local
description: Ingest new PDFs from a project's references/raw/ folder into the project's wiki, using local PDF→markdown conversion (via /read-pdf) for high-fidelity tables, figures, and equations. Filters for relevance to the project's research focus. Creates `references/raw/`, `references/wiki/`, and `references/CLAUDE.md` on first invocation if absent. Use when the user adds new papers to references/raw/ and asks to update the wiki, or says "ingest new references", "update the wiki", or similar.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(python3:*), Bash(mv:*), Bash(cp:*), Bash(mkdir:*), Bash(touch:*), Agent
argument-hint: [optional focus or theme for this batch]
---

# wiki-update-local: Ingest references via local PDF conversion

Maintains a project's reference wiki by ingesting newly-added PDFs from `references/raw/`, summarizing each through the lens of the project's research focus, and updating the wiki atomically per-paper.

This skill is the **local-converter counterpart to `wiki-update`**: it relies on the `/read-pdf` skill (docling/marker via a local venv) to produce high-fidelity markdown — preserving table structure, extracting figures as PNG clips, and rendering equations as LaTeX math mode — before any synthesis happens. The trade-off versus `wiki-update`: a one-time installer step (handled lazily by `/read-pdf`), in exchange for materially better tables, figures, and equation handling.

## When this skill is invoked

The user has added one or more PDFs to `references/raw/` and wants the wiki updated. The optional argument is a free-form focus string (e.g., "focus on IV strategies and instrument validity") that applies to this batch in addition to the project's standing context.

## Pre-flight (main session)

Run all checks before any ingest work. If anything fails, stop and ask the user.

### 0. Lazy scaffolding (first invocation in a project)

Before the other pre-flight checks, self-bootstrap the wiki structure if it's absent. All steps are idempotent — re-invocations against an already-scaffolded project are no-ops.

**a. Check for `references/`.** If `./references/` does not exist:

1. Create the directory tree:
   ```bash
   mkdir -p references/raw references/wiki references/wiki/figures
   ```
2. Render `references/CLAUDE.md` from the template at `~/.claude/skills/wiki-update-local/templates/references_CLAUDE.md`, substituting `{{PROJECT_NAME}}` with the current project's name (use the basename of the project root — typically the current working directory).
3. Initialize `references/wiki/index.md`:
   ```markdown
   # Wiki Index — [project-name]

   | Page | Description |
   |------|-------------|
   ```
4. Initialize `references/wiki/log.md`:
   ```markdown
   # Wiki Log — [project-name]

   | Date | Source | Changes |
   |------|--------|---------|
   ```

If `./references/` already exists, skip a–d. Do not clobber any existing files.

**b. Append a wiki-references entry to the project's root `CLAUDE.md` (idempotent).** If `./CLAUDE.md` exists at the project root and does NOT already contain a reference to `references/CLAUDE.md` (grep for the literal string `references/CLAUDE.md`), append a single index entry pointing to it so future Claude sessions know the wiki exists. Suggested format:

```markdown
- See `references/CLAUDE.md` for wiki conventions and the project's reference library.
```

If `./CLAUDE.md` does not exist (e.g., the project wasn't scaffolded by `/newproject`), skip this step silently.

After self-bootstrap, the rest of the pre-flight runs as below.

### 1. Locate the wiki

Check that `./references/raw/` and `./references/wiki/` both exist relative to the current working directory. If either is still missing after the lazy-scaffolding step, ask the user where the wiki lives. Do not search parent directories.

Read `./references/CLAUDE.md` for project-specific wiki conventions (page format, citation rules, naming). These conventions take precedence over anything in this skill if they conflict — this skill defines *workflow*, not *format*.

### 2. Verify project context is filled in

Read `./CLAUDE.md` (the project root file). Check the "Research Question," "Data Sources," and "Identification Strategy" fields (or their equivalents). If any are still placeholder text — bracketed phrases like `[What are you trying to answer?]`, `[What data are you using?]`, or otherwise unfilled — **stop and ask the user to fill them in first**. Explain that relevance filtering depends on this context.

The optional `[focus]` argument supplements but does not replace the project CLAUDE.md context.

### 3. Discover new papers

Read `./references/wiki/log.md` to find previously-ingested filenames. List PDFs in `./references/raw/` that do not appear in the log. These are the papers to ingest, in filename-sorted order.

If there are non-PDF files in `raw/`, surface them to the user before continuing:

```
Non-PDF files found in references/raw/: <filenames>
These were skipped for ingest. Move them elsewhere if they don't belong, or tell me if any should be treated differently.
```

Include these filenames in the end-of-run summary under a "Skipped (non-PDF)" section so the record is persistent. Do not silently ignore them.

If no new papers are found, report that and exit.

### 4. Normalize filenames

Each new PDF must conform to the project naming convention before ingest. This runs in the **main session** (not subagents) so renames can be batched and approved once.

**Convention:**
- 1 author → `Last_Year_Venue.pdf`
- 2 authors → `Last1_Last2_Year_Venue.pdf`
- 3+ authors → `Last1_etal_Year_Venue.pdf`
- Venue slug: standard econ journal abbreviation (`AER`, `JPE`, `QJE`, `JEEM`, `JHE`); `NBER` / `SSRN` / `IZA` for known WP series; `WP` for generic working papers; chapter abbrev or `Book` for book chapters.

**Skip condition.** A filename that matches the regex
```
^[A-Z][a-zA-Z]+(_[A-Z][a-zA-Z]+|_etal)?(_[A-Z][a-zA-Z]+){0,2}_\d{4}_[A-Z][A-Za-z]+\.pdf$
```
is treated as already-conforming and passed through untouched. Files not matching the regex go through the propose-and-approve flow below.

**Proposal flow (per non-conforming file):**

1. Run `/read-pdf` on the PDF to get a markdown rendering (this also primes the converter cache for the ingest step that follows). Run:
   ```bash
   python3 ~/.claude/skills/read-pdf/convert.py "<pdf-path>"
   ```
   Capture the printed markdown path. Read the first ~2000 characters of `markdown.md` — this includes the title page, authors, and (typically) the journal/year.
2. If the markdown is empty or unparseable (conversion failed), mark the file as **unparseable** and flag for manual handling. Do not attempt a rename.
3. Otherwise, extract author names, title keywords, year, and venue indicators from the markdown. Apply the convention to propose a new filename.

**Batched approval.** After proposals for all non-conforming files are ready, present to the user as one block:

```
Proposed renames (N files):
  <current-name>  → <proposed-name>
  <current-name>  → <proposed-name>
  ...

Already conform (skipped): K files

Unparseable (needs manual decision):
  ⚠ <current-name>  — conversion failed: <error>
    Keep as-is / Provide name?

Approve all / Edit (per-file) / Reject all?
```

- **Approve all** → apply all renames via `mv`.
- **Edit** → drop into per-file review; for each, user can approve, edit, or skip.
- **Reject all** → proceed with no renames.

**Collision handling** (before any `mv`):
- If a proposed name matches an existing file in `references/raw/` → block and ask user to provide an alternative.
- If two proposals in the same batch collide with each other → flag both, require user to disambiguate (typically by appending a title word).

Never silently overwrite. Never proceed past a collision without user input.

**After renames are applied**, re-list new PDFs under their new names before continuing. The cache is keyed by content hash, so renames do not invalidate prior conversions.

### 5. Pre-scan for cached synthesis

For each new paper, classify its reuse tier:

- **Tier 1 — synthesis exists**: `references/raw/<basename>_text.md` is present from a prior `/wiki-update-local` run. Subagent skips both conversion and synthesis; writes wiki pages directly from the existing extract.
- **Tier 2 — fresh ingest**: Subagent runs `/read-pdf`'s `convert.py` (which is itself cached by PDF content hash, so re-conversions across machines or projects are free), then synthesizes the structured extract, then writes wiki pages.

The default is to reuse without asking. Report once in your initial status message: "Reuse tiers: N at tier 1 (synthesis cached), M at tier 2 (fresh ingest)."

### 6. Read the wiki index

Load `./references/wiki/index.md` once. Pass it into each per-paper subagent so it can match new concepts against existing pages and avoid creating duplicates (see "Concept page disambiguation" below).

## Per-paper ingest (subagent)

Spawn one Agent per paper, sequentially. The main session must not read `<basename>_text.md` directly — that defeats the point of using subagents to bound context.

### Subagent prompt structure

The prompt to each Agent must be self-contained — the agent has no memory of this conversation. Include:

- Absolute path to the PDF
- Reuse tier (1 or 2) and the tier-appropriate paths:
  - Tier 1: absolute path to the existing `<basename>_text.md`
  - Tier 2: nothing extra (the agent runs the converter)
- Absolute paths to `references/raw/`, `references/wiki/`, `references/wiki/figures/`, `references/CLAUDE.md`
- The current `wiki/index.md` contents (for disambiguation)
- Project context block: research question, data sources, identification strategy (extracted from `./CLAUDE.md`)
- The optional batch focus string (if provided as the skill argument)
- The substantive-change rule (see below) — verbatim
- The conversion + extraction protocol (see below) — verbatim
- Instructions to write all non-destructive changes directly, and return proposed destructive edits as unified diffs

### Conversion + extraction protocol (passed to subagent verbatim)

**Tier 1** — A `<basename>_text.md` extract was provided. Read it. Skip to wiki writing.

**Tier 2** — No prior synthesis exists. Run the converter:

```bash
python3 ~/.claude/skills/read-pdf/convert.py "<absolute-pdf-path>"
```

Capture the printed path to `markdown.md`. The output lives at `~/.cache/claude-pdf-converter/cache/<sha>/`. Read both:

- `<cache-dir>/markdown.md` — the verbatim conversion with inline `![](figures/fig_N.png)` references
- `<cache-dir>/meta.json` — backend, page count, figure count, and `equation_extraction_mode`

If `meta.json:equation_extraction_mode == "image_fallback"`, equations were clipped as `<cache-dir>/figures/eq_*.png` rather than transcribed inline. Before synthesis, transcribe each equation image to LaTeX via a vision sub-agent (one image per sub-agent call to keep each call cheap):

```
Read the image at <eq-png-path>. It is a single equation clipped from an academic paper.
Transcribe it as LaTeX, in display math mode ($$ ... $$). Output only the LaTeX —
no commentary, no surrounding text. If the equation is not legible, output the literal
string "[unreadable equation]".
```

Edit `markdown.md` in the cache directory to replace each `![](figures/eq_N.png)` with the transcribed LaTeX. (The cache markdown is treated as scratch — overwriting it is fine, the next call to `convert.py` would regenerate from scratch on a hash miss anyway.)

After equations are handled, synthesize the structured extract directly into `references/raw/<basename>_text.md` — see structure below. Then proceed to wiki writing.

**Note:** Do **not** invoke `/read-pdf` as a slash command from inside this subagent. The slash invocation re-enters Claude unnecessarily and adds latency; the script is the contract. Bash-invoking `convert.py` directly is correct.

### Structure of `<basename>_text.md`

The structured extract is the durable, project-local artifact for each paper. Layout:

```markdown
## Plain-English synthesis
[200-word cap, see below]

## 1. Research question
...
## 2. Audience
...
[continue through all 11 dimensions below]
```

### Plain-English synthesis block (top of `_text.md`)

Hard cap: ~200 words. No jargon. Cover:

- Research question (1 sentence)
- Motivation / why it matters (1–2 sentences)
- What they estimate and how, in plain terms (2–3 sentences)
- What they found (1–2 sentences)
- The take-away — what someone should walk away believing or doing differently (1 sentence)

This block is the answer to "what's this paper about?" for someone who will not read the rest. Anyone with a college degree should be able to read it without a glossary. If you find yourself writing "endogeneity" or "LATE" or "first-stage F-stat," rewrite in plainer terms.

### Structured-extraction dimensions

1. **Research question** — what the paper asks, why it matters
2. **Audience** — sub-community of researchers who care
3. **Method / identification strategy** — how they answer the question
4. **Target parameter** — the estimand in plain terms (e.g., "ATE of schooling on log wages, conditional on age and state-by-year FE"). Distinct from method (the technique) and identification (the assumptions).
5. **Data** — sources, unit, sample size, time period
6. **Statistical methods / specifications** — econometric techniques, key specifications, **key equations** (extract verbatim in LaTeX math mode from `markdown.md` — do not paraphrase the equations)
7. **Findings** — key coefficients, standard errors
8. **Contributions** — what is learned that we didn't know
9. **Replication feasibility** — data availability, replication archive
10. **Tables (project-relevance gated)** — see Tables protocol below
11. **Figures (project-relevance gated, two-tier)** — see Figures protocol below

### Tables protocol (project-relevance gated)

Apply the project-relevance filter from "Relevance filtering" below. For tables that are *directly relevant* to the project's research focus, extract them in machine-readable markdown — and because the converter has already produced pipe-syntax tables in `markdown.md`, this is mostly a copy-paste with light cleanup. For tables that are not directly relevant, do not extract — a one-line description with a page reference suffices.

For relevant tables, use this format:

```
**Table N:** <verbatim caption> (p. 12)

| Variable | (1) | (2) | (3) |
|---|---|---|---|
| Schooling | 0.087*** | 0.091*** | 0.085*** |
|           | (0.012)  | (0.013)  | (0.011)  |
| ...       | ...      | ...      | ...      |
| N         | 12,450   | 12,450   | 12,450   |
| R²        | 0.34     | 0.36     | 0.38     |

Notes: <verbatim notes from the paper, including SE clustering, FE structure, etc.>
```

Preserve column headers verbatim, numerical values verbatim (including SEs in parentheses and significance stars), and the paper's notes verbatim. Pipe-syntax markdown only — no HTML tables. **Table notes** (the small-print explanations beneath a table) are part of the table's content and must be captured — they are distinct from page footnotes.

### Figures protocol (project-relevance gated, two-tier)

Apply the project-relevance filter. For figures not directly relevant to the project's research focus, write a one-line description with a page reference and stop — do not copy the image into the wiki.

For each relevant figure:

1. **Identify the converter's filename for it.** `markdown.md` references figures as `![](figures/fig_N.png)` where `N` is the converter's detection order. Match each `fig_N.png` to its paper figure number ("Figure 3") via the surrounding caption text in the markdown.
2. **Copy the image** from the cache to the wiki:
   ```bash
   cp ~/.cache/claude-pdf-converter/cache/<sha>/figures/fig_<N>.png \
      <abs-path>/references/wiki/figures/<paper-stem>_fig<M>.png
   ```
   where `<M>` is the paper's figure number (not the converter's detection order). This makes the wiki self-contained — referenced images live alongside the wiki and survive cache eviction.
3. **Classify and describe** the figure as Tier A or Tier B (below).

Classification heuristic: prefer the caption text. "Figure 3: scatterplot of X against Y" → Tier A. "Figure 5: schematic of identification strategy" or "DAG showing..." → Tier B. Fall back to reading the PNG directly only when the caption is genuinely ambiguous; in that case use a small vision sub-agent for classification.

**Tier A — Data figures** (scatter, line, bar, coefplot, histogram, density, time series, regression discontinuity plots, event study plots). The data IS the content. Extract as a structured block with the image embedded:

```
**Figure N:** <verbatim caption> (p. 12)

![<short description>](../figures/<paper-stem>_fig<N>.png)

- Type: <scatter / line / bar / coefplot / histogram / etc.>
- X-axis: <variable, units, range>
- Y-axis: <variable, units, range>
- Series / panels: <brief list>
- Key visual finding: <one sentence — what does the eye see?>
- Annotations: <text labels, reference lines, shaded regions, sample restrictions>
- **Figure notes:** <verbatim notes printed below the figure in the paper, if any>
```

The "Key visual finding" line is mandatory — it's what makes the figure useful in the wiki without re-opening the PDF. **Figure notes** (small-print explanations beneath a figure, often clustering / specification details) are captured separately from the caption and from page footnotes.

**Tier B — Schematic figures** (DAGs, conceptual diagrams, maps, flow charts, theoretical model schematics, complex layouts where the layout itself is the content). Embed the image and a short verbal pointer — do not attempt structured optical decomposition:

```
**Figure N:** <verbatim caption> (p. 12)

![<short description>](../figures/<paper-stem>_fig<N>.png)

One-liner: <what the figure depicts at a glance>
**Figure notes:** <verbatim notes if any>
```

**Default to Tier B when uncertain.** A structured Tier-A block written for a schematic is misleading and wrong; a Tier-B embed for what could have been Tier-A just means a future reader looks at the image themselves.

After deep-reading is complete and `<basename>_text.md` is written, proceed to writing wiki pages. Apply the substantive-change rule and the relevance-filtering rule below.

### Substantive-change rule (passed to subagent verbatim)

The subagent applies non-destructive edits directly to the wiki. Destructive edits to existing pages must be returned to the main session as proposed diffs, **not** applied.

| Edit | Apply directly? |
|---|---|
| Create new wiki page | Yes |
| Append new section / bullet / paragraph to existing page | Yes |
| Add `[[backlink]]` (inline or under "Related pages") | Yes |
| Update `**Last updated**` date | Yes |
| Append a new source to `**Sources**` | Yes |
| Note a contradiction between sources (additive note) | Yes |
| Reorganize section order (no content lost) | Yes |
| Update `wiki/index.md` (append new entries, edit existing one-liners) | Yes |
| Copy an extracted figure into `references/wiki/figures/` | Yes |
| Edit the `**Summary**` field on an existing page | **Return as diff** |
| Delete any existing line | **Return as diff** |
| Modify the wording of an existing claim | **Return as diff** |

### Concept page disambiguation (subagent)

Before creating a new concept page, the subagent checks `wiki/index.md` for existing pages covering the same concept — including obvious synonyms (e.g., "RDD" vs "regression discontinuity"). If a near-match exists but the agent isn't confident, it must **not** create a new page; instead, return the ambiguity to the main session as a question for the user.

### Relevance filtering (subagent)

Apply "compress, don't omit": sections of the paper directly relevant to the project's research focus get full treatment in the wiki. Less-relevant sections get a one-line description plus a page reference, so future-you can dig in if needed. Nothing is fully omitted.

### Embedding figures in wiki pages (subagent)

When a relevant figure was copied to `references/wiki/figures/`, the wiki concept page embeds it using this uniform format regardless of Tier A/B:

```markdown
**Figure N:** <verbatim caption> (p. 12)

![<short description>](../figures/<paper-stem>_fig<N>.png)

- Key visual finding: <one sentence — what the eye sees / the point of the figure>
- **Figure notes:** <verbatim notes printed below the figure in the paper, if any>
```

The Tier A/B distinction lives in `_text.md` only (full structured optical decomposition for Tier A; schematic one-liner for Tier B). Wiki pages get the same lightweight format for all figures — caption, embed, one-sentence takeaway, notes.

If a wiki page references a figure that the converter did not extract (rare — typically only when the backend missed a figure or the PDF page is purely text), fall back to a verbal description and page reference.

### Subagent return value

The subagent returns a structured summary to the main session:

```
Pages created: [list]
Pages modified non-destructively: [list with brief description]
Proposed destructive edits: [list of {page, unified diff, rationale}]
Disambiguation questions: [list of {concept, candidate existing pages}]
Proposed log entry: [single line for wiki/log.md]
Figures copied: [list of {source_cache_path, dest_wiki_path, paper_figure_label}]
Equation fallback used: <true/false> (with count if true)
Errors: [any issues encountered]
```

## Per-paper atomicity (main session)

For each paper, the main session uses a **journal-and-rollback** pattern to guarantee the wiki is never left in an inconsistent state.

**Before writing any wiki changes:**

1. Record a snapshot of every wiki page that the subagent intends to touch (pages to be created: note they don't exist yet; pages to be modified: read and save current content). This is the rollback journal.

**Then execute the write sequence:**

2. Spawn the subagent and wait for its return summary.
3. If there are disambiguation questions, ask the user; pass answers back via a follow-up SendMessage to the same agent (or apply decisions directly if simple).
4. Apply all non-destructive edits.
5. If there are proposed destructive edits, present them to the user as a single batched approval request (one prompt per paper, not one per edit). The user can approve all, reject all, or selectively approve. Apply approved edits.
6. **Last:** append the log entry to `wiki/log.md`.

**On failure at any step 2–6:**

Roll back: restore each touched page to its journaled state (delete pages that were newly created; restore original content for pages that were modified). Do not write the log entry. The next `/wiki-update-local` invocation will rediscover the paper as new and retry cleanly from a known-good state.

Do not implement partial-resume logic. The journal guarantees retry is always safe.

After each paper finishes, move to the next. Do not batch papers.

## End-of-run summary

After all papers are processed, report:

- Papers successfully ingested (with counts of pages created/modified, figures copied)
- Papers that failed (with brief reasons; user can re-invoke to retry)
- Any disambiguation decisions the user made (so they have a record)
- Any equation-fallback transcriptions that were marked unreadable (so the user can manually fix them)

## What this skill does NOT do

- **Does not download PDFs.** Drop them into `references/raw/` first.

## Rules

- **Never modify anything in `references/raw/`.** PDFs and their cached `_text.md` extracts are immutable.
- **Never read `markdown.md` or `_text.md` extracts in the main session.** Always delegate to a subagent. The main session's job is orchestration and approval.
- **Never write the log entry before wiki edits complete.** The log is the source of truth for "what's been ingested" — it must lag behind, not lead.
- **Never invent project context.** If `CLAUDE.md` placeholders are unfilled, stop and ask. Do not guess the research question.
- **Project conventions in `references/CLAUDE.md` override this skill** if they conflict on format/naming/citation. This skill owns workflow only.
- **Never rename a PDF without user approval.** Even a single non-conforming file goes through the batched propose/approve flow. No silent `mv`. No overwriting an existing file.
- **Never fall back from the converter silently.** If `convert.py` errors on a PDF, surface the error to the user and skip that paper for this run — do not substitute pdftotext output.
