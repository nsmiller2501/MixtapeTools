---
name: wiki-update
description: Ingest new PDFs from a project's references/raw/ folder into the project's wiki, following the project's wiki conventions and filtering for relevance to the project's research focus. Creates `references/raw/`, `references/wiki/`, and `references/CLAUDE.md` on first invocation if absent. Use when the user adds new papers to references/raw/ and asks to update the wiki, or says "ingest new references", "update the wiki", or similar.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(curl:*), Bash(pdftotext:*), Bash(mv:*), Bash(mkdir:*), Bash(touch:*), Agent
argument-hint: [optional focus or theme for this batch] [--rebuild-bib]
---

# wiki-update: Ingest new references into the project wiki

Maintains a project's reference wiki by ingesting newly-added PDFs from `references/raw/`, summarizing each through the lens of the project's research focus, and updating the wiki atomically per-paper.

## When this skill is invoked

The user has added one or more PDFs to `references/raw/` and wants the wiki updated. The optional argument is a free-form focus string (e.g., "focus on IV strategies and instrument validity") that applies to this batch in addition to the project's standing context.

## Pre-flight (main session)

Run all checks before any ingest work. If anything fails, stop and ask the user.

### 0. Lazy scaffolding (first invocation in a project)

Before the other pre-flight checks, self-bootstrap the wiki structure if it's absent. All steps are idempotent — re-invocations against an already-scaffolded project are no-ops.

**a. Check for `references/`.** If `./references/` does not exist:

1. Create the directory tree:
   ```bash
   mkdir -p references/raw references/wiki
   ```
2. Render `references/CLAUDE.md` from the template at `~/.claude/skills/wiki-update/templates/references_CLAUDE.md`, substituting `{{PROJECT_NAME}}` with the current project's name (use the basename of the project root — typically the current working directory).
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

If `./references/` already exists, skip a–b. Do not clobber any existing files.

**b. Append a wiki-references entry to the project's root `CLAUDE.md` (idempotent).** If `./CLAUDE.md` exists at the project root and does NOT already contain a reference to `references/CLAUDE.md` (grep for the literal string `references/CLAUDE.md`), append a single index entry pointing to it so future Claude sessions know the wiki exists. Suggested format (one line under any existing index section, or appended to the bottom of the file):

```markdown
- See `references/CLAUDE.md` for wiki conventions and the project's reference library.
```

If `./CLAUDE.md` does not exist (e.g., the project wasn't scaffolded by `/newproject`), skip this step silently.

After this self-bootstrap, the rest of the pre-flight (steps 1–6 below) runs as before.

### 1. Locate the wiki

Check that `./references/raw/` and `./references/wiki/` both exist relative to the current working directory. If either is still missing after the lazy-scaffolding step, ask the user where the wiki lives. Do not search parent directories.

Read `./references/CLAUDE.md` for project-specific wiki conventions (page format, citation rules, naming). These conventions take precedence over anything in this skill if they conflict — this skill defines *workflow*, not *format*.

### 2. Verify project context is filled in

Read `./CLAUDE.md` (the project root file). Check the "Research Question," "Data Sources," and "Identification Strategy" fields (or their equivalents). If any are still placeholder text — bracketed phrases like `[What are you trying to answer?]`, `[What data are you using?]`, or otherwise unfilled — **stop and ask the user to fill them in first**. Explain that relevance filtering depends on this context.

The optional `[focus]` argument supplements but does not replace the project CLAUDE.md context.

### 3. Discover new papers

Read `./references/wiki/log.md` to find previously-ingested filenames. List PDFs in `./references/raw/` that do not appear in the log. These are the papers to ingest, in filename-sorted order. Non-PDF files in `raw/` are skipped silently.

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

1. Extract first-page text: `pdftotext -l 1 "<pdf>" -`.
2. If output is empty or <50 chars of non-whitespace, mark the file as **unparseable** and flag it for manual handling in the approval batch. Do not attempt a rename.
3. Otherwise, read author names, title keywords, year, and venue indicators from the extracted text. Apply the convention to propose a new filename.

**Batched approval.** After proposals for all non-conforming files are ready, present to the user as one block:

```
Proposed renames (N files):
  <current-name>  → <proposed-name>
  <current-name>  → <proposed-name>
  ...

Already conform (skipped): K files

Unparseable (needs manual decision):
  ⚠ <current-name>  — could not extract first-page text
    Keep as-is / Provide name?

Approve all / Edit (per-file) / Reject all?
```

- **Approve all** → apply all renames via `mv`.
- **Edit** → drop into per-file review; for each, user can approve, edit the proposed name, or skip.
- **Reject all** → proceed with no renames (files keep their current names).

**Collision handling** (before any `mv`):
- If a proposed name matches an existing file on disk in `references/raw/` → block and ask user to provide an alternative.
- If two proposals in the same batch collide with each other → flag both, require user to disambiguate (typically by appending a title word, e.g., `Grossman_1972_JPE_HealthCapital.pdf`).

Never silently overwrite. Never proceed past a collision without user input.

**After renames are applied**, re-list new PDFs under their new names before continuing to step 5. This ensures subsequent tier classification and ingest use the canonical names.

### 5. Pre-scan for cached work (three-tier reuse)

For each new paper, classify its reuse tier so you can include it in the subagent prompt:

- **Tier 1 — extract exists**: `references/raw/<basename>_text.md` is present. Subagent skips both splitting and deep-reading; uses the extract directly.
- **Tier 2 — splits exist but no extract**: `references/raw/raw_build/split_<basename>/` contains PDF splits but no `_text.md`. Subagent skips splitting; reads the existing splits to produce `_text.md`, then proceeds.
- **Tier 3 — neither**: Subagent splits the PDF, then reads, then writes `_text.md`.

The default is to reuse without asking. Report once in your initial status message: "Reuse tiers: N at tier 1 (extracts cached), M at tier 2 (splits cached), K at tier 3 (full pipeline)."

### 6. Read the wiki index

Load `./references/wiki/index.md` once. Pass it into each per-paper subagent so it can match new concepts against existing pages and avoid creating duplicates (see "Concept page disambiguation" below).

## Per-paper ingest (subagent)

Spawn one Agent per paper, sequentially. The main session must not read PDF extracts directly — that defeats the purpose of using subagents to bound context.

### Subagent prompt structure

The prompt to each Agent must be self-contained — the agent has no memory of this conversation. Include:

- Absolute path to the PDF
- Reuse tier (1, 2, or 3) and the tier-appropriate paths:
  - Tier 1: absolute path to the existing `<basename>_text.md`
  - Tier 2: absolute path to the existing `raw_build/split_<basename>/` directory
  - Tier 3: nothing extra
- **Canonical build directory**: absolute path `<absolute-path-to-references>/raw/raw_build/`. The subagent must use this exact path for any new splits — do not let it derive its own. This prevents drift between subagent invocations.
- Absolute paths to `references/raw/`, `references/wiki/`, `references/CLAUDE.md`
- The current `wiki/index.md` contents (for disambiguation)
- Project context block: research question, data sources, identification strategy (extracted from `./CLAUDE.md`)
- The optional batch focus string (if provided as the skill argument)
- The substantive-change rule (see below) — verbatim
- The deep-read protocol (see below) — verbatim
- Instructions to write all non-destructive changes directly, and return proposed destructive edits as unified diffs

### Deep-read protocol (passed to subagent verbatim)

**Do not invoke `/split-pdf` as a slash command.** That skill has a per-batch user-confirmation gate ("Would you like me to continue?") which deadlocks in subagents because there is no user. Inline the logic instead:

**Tier 1** — A `<basename>_text.md` extract was provided. Read it. Skip to wiki writing.

**Tier 2** — Splits exist at `<provided split_dir path>`. Read them in batches of 3 sequentially without pausing or asking for confirmation. Maintain a `notes.md` inside that split_dir, updating it after each batch with the structured-extraction dimensions below. **If a `notes.md` already exists in the split_dir from a prior interrupted run, resume from it — read it first, then continue updating in place rather than starting fresh.** After all splits are read, write the final notes to `<absolute-path-to-references>/raw/<basename>_text.md`. **`notes.md` is permanent — do not delete it after writing `_text.md`.** Then proceed to wiki writing.

**Tier 3** — No prior work exists. Split the PDF into 4-page chunks using PyPDF2, writing chunks to `<canonical-build-dir>/split_<basename>/`. Then proceed exactly as Tier 2.

**`notes.md` discipline (applies to both Tier 2 and Tier 3):**

- **Append-mostly.** Each batch *adds* findings under the structured-extraction dimensions below. Do not rewrite or compress earlier content. The point is auditability — a future reader (or a resumed run) needs to see what came from which split.
- **Mark each batch boundary** with a comment line: `<!-- batch N: pp X-Y -->` immediately before the new content from that batch.
- **Permanent artifact.** `notes.md` lives in the `split_dir` indefinitely. Do not delete it as cleanup after writing `_text.md`. The `_text.md` is the persistent extract for downstream consumers; `notes.md` is the audit trail and the resume point.

Structured-extraction dimensions for `notes.md` and the final `_text.md` (per the project's wiki conventions):

1. Research question
2. Audience
3. Method / identification strategy
4. **Target parameter** — what specifically is the paper trying to estimate? The estimand, in plain terms (e.g., "ATE of schooling on log wages, conditional on age and state-by-year fixed effects"). Distinct from method (the technique) and identification (the assumptions).
5. Data (sources, unit, sample size, time period)
6. Statistical methods / specifications
7. Findings (key coefficients, standard errors)
8. Contributions
9. Replication feasibility (data availability, replication archive)
10. **Tables (project-relevance gated)** — see Tables protocol below
11. **Figures (project-relevance gated, two-tier)** — see Figures protocol below

**Plain-English synthesis block (top of `_text.md`):**

Before the structured-extraction sections, write a top-of-file `## Plain-English synthesis` block. Hard cap: ~200 words. No jargon. Cover:

- Research question (1 sentence)
- Motivation / why it matters (1–2 sentences)
- What they estimate and how, in plain terms (2–3 sentences)
- What they found (1–2 sentences)
- The take-away — what someone should walk away believing or doing differently (1 sentence)

This block is the answer to "what's this paper about?" for someone who will not read the rest. Anyone with a college degree should be able to read it without a glossary. If you find yourself writing "endogeneity" or "LATE" or "first-stage F-stat," rewrite in plainer terms.

**Tables protocol (project-relevance gated):**

Apply the project-relevance filter from "Relevance filtering" below. For tables that are *directly relevant* to the project's research focus, extract them in machine-readable markdown. For tables that are not directly relevant, do not extract — a one-line description with a page reference suffices.

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

Preserve column headers verbatim, numerical values verbatim (including SEs in parentheses and significance stars), and the paper's notes verbatim. Pipe-syntax markdown only — no HTML tables.

**Figures protocol (project-relevance gated, two-tier):**

Apply the project-relevance filter. For figures not directly relevant to the project's research focus, write a one-line description with a page reference and stop.

For relevant figures, classify into one of two tiers:

**Tier A — Data figures** (scatter, line, bar, coefplot, histogram, density, time series, regression discontinuity plots, event study plots). The data IS the content. Extract as a structured block:

```
**Figure N:** <verbatim caption> (p. 12)
- Type: <scatter / line / bar / coefplot / histogram / etc.>
- X-axis: <variable, units, range>
- Y-axis: <variable, units, range>
- Series / panels: <brief list>
- Key visual finding: <one sentence — what does the eye see?>
- Annotations: <text labels, reference lines, shaded regions, sample restrictions>
```

The "Key visual finding" line is mandatory — it's what makes the figure useful in the wiki without re-reading the PDF.

**Tier B — Schematic figures** (DAGs, conceptual diagrams, maps, flow charts, theoretical model schematics, complex layouts where the layout itself is the content). Do NOT attempt optical description. Write a CLIP placeholder:

```
> **Figure N (CLIP):** <verbatim caption> (p. 12)
> One-liner: <what the figure depicts at a glance>
> ACTION: clip from PDF, save to references/wiki/figures/<paper-stem>_fig<N>.png
```

The one-liner is mandatory and short — it's the only thing that lets future-you decide whether the clip is worth doing without reopening the PDF.

**Default to placeholder when uncertain.** Asymmetric cost: a structured block written for a schematic is misleading and wrong; a CLIP placeholder for what could have been a structured block just costs the user 10 seconds. When in doubt, CLIP.

**Figures directory creation.** Before writing any CLIP placeholder, the subagent should ensure `references/wiki/figures/` exists by running `mkdir -p <absolute-path-to-references>/wiki/figures`. `mkdir -p` is idempotent — no check needed.

**Also extract bibliographic metadata** (for the .bib step). Record these as a clearly-labeled block at the top of `_text.md`:

```
## Bibliographic metadata
doi: <10.xxxx/yyyy from first page if present, else null>
authors: [LastName1, LastName2, ...]
title: <verbatim title from title page>
year: <year>
venue: <journal/working paper series/etc., verbatim>
venue_type: journal | working_paper | book_chapter | other
```

The DOI check: scan the first split for the regex `10\.\d{4,}/\S+`. Record only if found; do not guess.

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
| Edit the `**Summary**` field on an existing page | **Return as diff** |
| Delete any existing line | **Return as diff** |
| Modify the wording of an existing claim | **Return as diff** |

### Concept page disambiguation (subagent)

Before creating a new concept page, the subagent checks `wiki/index.md` for existing pages covering the same concept — including obvious synonyms (e.g., "RDD" vs "regression discontinuity"). If a near-match exists but the agent isn't confident, it must **not** create a new page; instead, return the ambiguity to the main session as a question for the user.

### Relevance filtering (subagent)

Apply "compress, don't omit": sections of the paper directly relevant to the project's research focus get full treatment in the wiki. Less-relevant sections get a one-line description plus a page reference, so future-you can dig in if needed. Nothing is fully omitted.

### CLIP placeholders in wiki pages (subagent)

When a relevant figure was classified as Tier B (CLIP placeholder) in the deep-read, the wiki concept page that should reference it uses a standard markdown image link pointing to the (not-yet-existing) clipped file:

```markdown
![<short description>](../figures/<paper-stem>_fig<N>.png)
*<verbatim caption from paper> ([<paper-stem>](../log.md), p. 12)*
```

The image link will render as a broken-image placeholder in any markdown viewer until the user manually clips and saves the file. This is a feature, not a bug — the broken image is the visible TODO.

The subagent reports each CLIP placeholder it created in its return value (see below) so the main session can aggregate them into the end-of-run punch-list.

### Subagent return value

The subagent returns a structured summary to the main session:

```
Pages created: [list]
Pages modified non-destructively: [list with brief description]
Proposed destructive edits: [list of {page, unified diff, rationale}]
Disambiguation questions: [list of {concept, candidate existing pages}]
Proposed log entry: [single line for wiki/log.md]
Bibliographic metadata: {doi, authors, title, year, venue, venue_type}
Pending CLIPs: [list of {target_path, source_paper, page_number, one_liner}]
Errors: [any issues encountered]
```

## Per-paper atomicity (main session)

For each paper, the main session:

1. Spawns the subagent and waits for its return summary
2. If there are disambiguation questions, asks the user; passes answers back via a follow-up SendMessage to the same agent (or applies decisions directly if simple)
3. If there are proposed destructive edits, presents them to the user as a single batched approval request (one prompt per paper, not one per edit). The user can approve all, reject all, or selectively approve.
4. Applies approved destructive edits directly via Edit
5. **Last:** appends the log entry to `wiki/log.md`

If any step before #5 fails (subagent error, user interrupt, edit failure), do not write the log entry. The next `/wiki-update` invocation will rediscover the paper as new and retry from scratch. Partial wiki pages from the failed attempt will be **overwritten** on retry — this is intentional. Do not implement resume logic.

After each paper finishes, move to the next. Do not batch papers.

## Post-log: update `references/references.bib`

After **all** papers have been ingested and logged, the main session updates the central BibTeX file at `references/references.bib`. This step runs in the main session (not subagents) so network-fetch failures and unverified entries don't poison wiki writes.

### Mode

- **Default:** append-only. For each filename ingested in this run, add one entry. Skip any filename whose citation key already exists in `references.bib` — never overwrite.
- **`--rebuild-bib` flag:** iterate every filename in `wiki/log.md`, re-run the fetch cascade using cached `_text.md` metadata (never re-read PDFs), and overwrite `references.bib` after a single confirmation prompt. If a `_text.md` is missing, skip with a warning.

If `references/references.bib` does not exist, create it.

### Citation key

Use the filename stem verbatim (e.g., `Deryugina_etal_2019_AER`). If the fetched BibTeX has a different key, rewrite it. Key collision with an existing entry → surface as a conflict, do not overwrite.

### Fetch cascade (per paper, stop at first success)

**0. DOI from PDF.** The subagent returned a DOI in `Bibliographic metadata` if it found one on the first page. If present, fetch directly via content-negotiation:

```
curl -sLH "Accept: application/x-bibtex" "https://doi.org/<DOI>"
```

A successful response is accepted as-is (rewrite the key, done). No match test needed — the DOI is definitive.

**1. CrossRef title+author search.** Query `https://api.crossref.org/works?query.title=<urlencoded-title>&query.author=<first-author-last>&rows=5`. For each candidate, apply the **3-signal match test**:

- Year matches (±1 acceptable, flag in report)
- First author's last name matches (case-insensitive)
- Title fuzzy-match ≥85% after normalization (lowercase, strip punctuation, collapse whitespace)

Additionally require **three-way agreement** across filename (parsed as `Author_etal_Year_Venue`), subagent-returned metadata, and the API result — year and first-author must agree. Disagreement → reject this candidate.

On first candidate passing all tests: content-negotiate its DOI to get clean BibTeX.

**2. OpenAlex title+author search.** Query `https://api.openalex.org/works?search=<title>&filter=authorships.author.display_name.search:<first-author-last>`. Apply the same match test and three-way agreement. OpenAlex BibTeX may need minor post-processing.

**3. LLM-from-PDF fallback.** If all network sources fail or no candidates pass matching, construct a BibTeX entry from the subagent's returned metadata (doi, authors, title, year, venue, venue_type). Map `venue_type`:
- `journal` → `@article`
- `working_paper` → `@techreport` (institution = venue)
- `book_chapter` → `@incollection`
- other → `@misc`

Mark this entry as **unverified** and block for user approval (see Review below).

**Preprint/published divergence:** the filename's venue wins. If the filename says `Anderson_etal_2022_NBER` but an API returns a 2024 AER version, reject the API result and either re-query scoped to the WP series or fall through to LLM fallback.

### Review and append

Group results into three tiers and report to the user at the end:

```
BibTeX entries for this batch (N papers):

[auto-appended, no review]
✓ <key>  — CrossRef via DOI (<doi>)
...

[auto-appended, flagged for spot-check]
⚠ <key>  — CrossRef title-match (<fuzzy%>, year/author OK)
...

[REQUIRES APPROVAL]
? <key>  — LLM-from-PDF (unverified)
   <full entry printed>
   Approve / Edit / Skip?
...
```

- Tier 1 (DOI hits) and Tier 2 (fuzzy matches) are appended immediately.
- Tier 3 (LLM-unverified) is printed in full and blocks for per-entry approval. Do not append until approved.

### Failure handling

- `curl` timeout / network error on any single source → fall through to next source.
- All sources fail → LLM-from-PDF fallback → blocks for approval.
- JSON parse error from API → treat as failure, fall through.
- Content-negotiation returns empty body → fall through.

### Rebuild mode mechanics (`--rebuild-bib`)

When the flag is passed:

1. Confirm with user: "This will overwrite `references/references.bib` with entries for N papers from `log.md`. Proceed?"
2. Iterate filenames in `log.md` order.
3. For each, read the `## Bibliographic metadata` block from `references/raw/<basename>_text.md`. If missing, warn and skip.
4. Run the cascade as above, but seed it with the cached metadata (no subagent re-read).
5. Write all accepted entries to `references.bib`, overwriting. Hard-stop at any tier-3 entry to get approval.

## End-of-run summary

After all papers are processed, report:

- Papers successfully ingested (with counts of pages created/modified)
- Papers that failed (with brief reasons; user can re-invoke to retry)
- Any disambiguation decisions the user made (so they have a record)
- **Pending figure clips (punch-list).** Aggregate every CLIP placeholder reported by all subagents into a single list:

  ```
  Pending figure clips (3):
    1. references/wiki/figures/Smith_2024_AER_fig2.png
       Smith_2024_AER, p. 14 — "DAG of identification strategy"
    2. references/wiki/figures/Jones_2023_QJE_fig1.png
       Jones_2023_QJE, p. 8  — "Conceptual map of policy variation"
    3. references/wiki/figures/Lee_2022_NBER_fig4.png
       Lee_2022_NBER, p. 22 — "Treatment timing schematic"
  ```

  Open each PDF to the indicated page, clip the figure, save under the listed path. Wiki pages already reference these paths via markdown image links — the broken-image placeholders will resolve silently as each PNG is added.

## Rules

- **Never modify anything in `references/raw/`.** PDFs and their cached `_text.md` extracts are immutable.
- **Never read PDF extracts in the main session.** Always delegate deep reading to a subagent. The main session's job is orchestration and approval.
- **Never write the log entry before wiki edits complete.** The log is the source of truth for "what's been ingested" — it must lag behind, not lead.
- **Never invent project context.** If `CLAUDE.md` placeholders are unfilled, stop and ask. Do not guess the research question.
- **Project conventions in `references/CLAUDE.md` override this skill** if they conflict on format/naming/citation. This skill owns workflow only.
- **Never overwrite existing `.bib` entries.** Append-only in default mode. Key collisions surface as conflicts for the user. Only `--rebuild-bib` may overwrite, and only after explicit confirmation.
- **Never silently accept an LLM-generated BibTeX entry.** Tier-3 (unverified) entries must be printed in full and blocked for user approval.
- **Never rename a PDF without user approval.** Even a single non-conforming file goes through the batched propose/approve flow. No silent `mv`. No overwriting an existing file.
