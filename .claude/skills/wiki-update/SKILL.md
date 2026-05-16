---
name: wiki-update
description: Ingests new PDFs from a project's `references/raw/` folder into the project's wiki, summarizing each through the lens of the project's research focus and auto-detecting the best conversion path (marker → cached `_text.md` → split-pdf fallback). Scaffolds `references/raw/`, `references/wiki/`, and `references/CLAUDE.md` on first run, and calls `/bib-update` at the end to refresh `references/references.bib`. Use when the user adds new PDFs to `references/raw/` and says "ingest new references", "update the wiki", or similar.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(pdftotext:*), Bash(python3:*), Bash(mv:*), Bash(cp:*), Bash(mkdir:*), Bash(touch:*), Agent
argument-hint: [optional focus or theme for this batch]
---

# wiki-update: Ingest new references into the project wiki

Maintains a project's reference wiki by ingesting newly-added PDFs from `references/raw/`, summarizing each through the lens of the project's research focus, and updating the wiki atomically per-paper.

**Ingest path is auto-detected per paper.** If the read-pdf converter is installed, it runs first for high-fidelity markdown (Protocol M: best tables, figures, and equation handling). If only a cached `_text.md` extract exists, that feeds wiki writing directly (Protocol E). Otherwise the full split-PDF vision pipeline runs (Protocol S). All three paths produce the same wiki output — the difference is quality of table and figure capture.

**`pdftotext` is not an ingest source.** It is allowed only for narrow pre-flight tasks: first-page filename proposals when the converter is unavailable, metadata checks needed for `/bib-update`, and other explicit bootstrap/diagnostic checks that do not synthesize wiki content. Once a paper is assigned to Protocol M or Protocol E, do not use `pdftotext` to read, summarize, validate, or supplement substantive content. Wait for the selected input (`markdown.md` or `_text.md`) and read that source only.

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
  Capture the printed path to `markdown.md`. Read the first ~2000 characters of `markdown.md` — this covers title, authors, year, and venue. This also primes the converter cache for the ingest step that follows (the cache is SHA-keyed, so renaming the PDF after this point does not invalidate it).

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

1. **Tier M — Converted markdown:** `~/.claude/skills/read-pdf/convert.py` exists, **and** running it for this PDF succeeds (cache hit is instant; a miss triggers the full conversion here). Capture the returned `markdown.md` path and cache directory. If `convert.py` was already run during step 4 for this paper, it was cached — re-running is a no-op.

   If `convert.py` exists but fails for a specific paper (conversion error), report the error, skip tier M for that paper, and fall through to tier E or S. Do not use `pdftotext` as a temporary or parallel substitute while conversion is running or after conversion fails.

2. **Tier E — Cached extract:** `references/raw/<basename>_text.md` exists. No conversion needed.

3. **Tier S — Split-PDF pipeline:** Neither of the above. For each tier-S paper, run the split-pdf script from the main session so the subagent receives a populated splits directory:

   ```bash
   python3 ~/.claude/skills/split-pdf/scripts/split.py \
     references/raw/<basename>.pdf \
     --output-dir references/raw/raw_build/split_<basename>
   ```

   `split.py` is the canonical PyPDF2 splitter (shared with `/split-pdf`). It is idempotent at the chunk-file level: if the output directory already contains the expected `<basename>_pp<X>-<Y>.pdf` files from a prior interrupted run, re-running rewrites them with identical content. Do not invoke `/split-pdf` as a skill — its interactive pause-and-confirm flow cannot be answered from a subagent context. Call the script only.

**Report tier breakdown once, before spawning subagents:**

```
Ingest tiers for this batch:
  M (converted markdown): N papers
  E (cached extract):     M papers
  S (full pipeline):      K papers

[If any converter failures:]
  ⚠ Converter failed for: <filenames> — falling back to E or S
```

### 6. Read the wiki index

Load `./references/wiki/index.md` once. Pass it into each per-paper subagent so it can match new concepts against existing pages and avoid creating duplicates.

---

## Per-paper ingest (subagent)

Spawn one Agent per paper, sequentially. The main session must not read PDF extracts or markdown directly — delegate deep reading to subagents to bound context.

**Before spawning each subagent, record the journal** (for rollback on failure): for every wiki page the subagent intends to touch, note whether it exists and its current content if so. This is the rollback snapshot. On failure at any step, restore journaled state and do not write the log entry. The next invocation rediscovers the paper as new and retries cleanly.

Each subagent prompt must be self-contained — the agent has no memory of this conversation. Include:

- Absolute paths: PDF, input source (markdown.md, `_text.md`, or populated splits directory), `references/raw/`, `references/wiki/`, `references/wiki/figures/`, `references/CLAUDE.md`
- The tier (M, E, or S)
- Current `wiki/index.md` contents (for disambiguation)
- Project context block: research question, data sources, identification strategy (from `./CLAUDE.md`)
- Optional batch focus string (if provided as the skill argument)
- **The verbatim contents of exactly one protocol file** — read and embed `~/.claude/skills/wiki-update/protocol_m.md`, `protocol_e.md`, or `protocol_s.md` depending on the tier. Do not embed the other two.
- **The verbatim contents of `~/.claude/skills/wiki-update/common.md`** — shared `_text.md` structure, structured-extraction dimensions, tables and figures protocols, substantive-change rule, concept disambiguation, relevance filtering, and subagent return-value schema.

Embed both files verbatim in the subagent prompt; the subagent has no filesystem awareness of this skill directory.

---

## Per-paper atomicity (main session)

For each paper, the main session uses a **journal-and-rollback** pattern to guarantee the wiki is never left in an inconsistent state.

**Before spawning the subagent:**
Record a snapshot of every wiki page the subagent intends to touch — pages to be created (note they don't exist yet); pages to be modified (read and save current content). This is the rollback journal.

**Execute the write sequence:**
1. Spawn the subagent and wait for its return summary.
2. If there are disambiguation questions, ask the user; pass answers back via a follow-up SendMessage to the same agent (or apply decisions directly if simple).
3. Apply all non-destructive edits.
4. If there are proposed destructive edits, present them to the user as a single batched approval request (one prompt per paper). User can approve all, reject all, or selectively approve. Apply approved edits.
5. **Last:** append the log entry to `wiki/log.md`.

**On failure at any step 1–5:** roll back: restore each touched page to its journaled state (delete newly-created pages; restore original content for modified pages). Do not write the log entry. The next invocation will rediscover the paper as new and retry cleanly.

Do not implement partial-resume logic. The journal guarantees retry is always safe.

After each paper finishes, move to the next. Do not batch papers.

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

- **Never modify anything in `references/raw/`.** PDFs and their cached `_text.md` extracts are immutable. The converter cache at `~/.cache/claude-pdf-converter/` is scratch and may be overwritten.
- **Never read PDF extracts, markdown, or splits in the main session.** Always delegate deep reading to subagents. The main session's job is orchestration and approval.
- **Never write the log entry before wiki edits complete.** The log is the source of truth for "what's been ingested" — it must lag behind, not lead.
- **Never invent project context.** If `CLAUDE.md` placeholders are unfilled, stop and ask. Do not guess the research question.
- **Project conventions in `references/CLAUDE.md` override this skill** if they conflict on format/naming/citation. This skill owns workflow only.
- **Never rename a PDF without user approval.** Even a single non-conforming file goes through the batched propose/approve flow. No silent `mv`. No overwriting an existing file.
- **Never fall back from the converter silently.** If `convert.py` errors on a PDF, report the error and proceed to tier E or S for that paper — do not substitute pdftotext output without telling the user.
- **Never use `pdftotext` for substantive ingest.** `pdftotext` is limited to first-page metadata/filename/bootstrap checks. It must not be used to summarize, validate, or supplement Protocol M or Protocol E content.
