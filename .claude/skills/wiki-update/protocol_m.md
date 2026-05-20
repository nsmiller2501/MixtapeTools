# Protocol M — Converted Markdown Substrate

*Input:* path to `manifest.json` produced by `read-pdf/scripts/prepare_substrate.py`, path to the converter cache directory (for figures), canonical paper basename.

Protocol M reads only `manifest.json`, its chunk files, worker notes, `meta.json`, and cache-local figure/equation files. Do not read the whole converted `markdown.md`. Do not inspect the source PDF with `pdftotext` or any other text extractor for substantive synthesis, even if conversion is slow. If conversion or substrate preparation is still running, wait.

## Step 1: Check for equation fallback

Read `<cache-dir>/meta.json`. If `equation_extraction_mode == "image_fallback"`, equations were extracted as `<cache-dir>/figures/eq_*.png` rather than inline LaTeX. Before synthesis, transcribe each:

```
Read the image at <eq-png-path>. It is a single equation clipped from an academic paper.
Transcribe it as LaTeX, in display math mode ($$ ... $$). Output only the LaTeX —
no commentary, no surrounding text. If the equation is not legible, output "[unreadable equation]".
```

Edit the relevant chunk files in place to replace each `![](figures/eq_N.png)` with the transcribed LaTeX. The substrate is scratch and can be regenerated from `markdown.md`.

## Step 2: Extract bounded worker notes

The main session spawns one worker agent per `manifest.worker_bundles` entry, sequentially. Each worker receives its bundle excerpt, reads the assigned chunk paths only, follows `~/.claude/skills/read-pdf/fanout_worker.md`, and writes one durable note file under `references/raw/raw_build/<basename>_fanout/worker_notes/`.

If interrupted, completed worker notes are salvageable and should not be deleted.

## Step 3: Synthesize `_text.md`

After all worker notes exist, the main session spawns one synthesis agent. The synthesis agent reads `manifest.json` and all worker note files. It uses `~/.claude/skills/read-pdf/fanout_synthesis.md` plus `common.md` to produce `references/raw/<basename>_text.md` following the project-neutral `_text.md` structure (bib block, plain-English synthesis, structured dimensions, and formal-object inventories). Gap-reread specific chunk files only when worker notes omit a needed table, figure, equation, result, or ambiguous claim. Write or overwrite if a prior partial file exists.

For the bib metadata block, use DOI candidates from `manifest.json` and front-matter worker notes. Extract authors, title, year, and venue from the front-matter chunks and worker notes. Record null for any field not found. Do not read the whole `markdown.md` for metadata.

## Step 4: Copy and classify relevant figures

For each figure inventoried in `manifest.json` or worker notes:

1. Identify the paper figure number from surrounding caption text.
2. Apply the project-relevance filter. Non-relevant: one-line description + page ref only; do not copy.
3. For relevant figures:
   - Copy from cache to wiki: `cp <cache-dir>/figures/fig_N.png references/wiki/figures/<basename>_fig<M>.png` (where M is the paper's figure number). Before the first copy, run `mkdir -p references/wiki/figures` (idempotent).
   - Classify as Tier A (data figure: scatter, line, bar, coefplot, histogram, density, time series, RD/event-study plot) or Tier B (schematic: DAG, conceptual diagram, map, flowchart, theoretical model). Use the caption text; read the PNG only if the caption is genuinely ambiguous.

## Step 5: Write wiki pages

Use the substantive-change rule and relevance filtering in `common.md`.

For relevant figures embedded in wiki concept pages, use this format regardless of Tier A/B:

```markdown
**Figure N:** <verbatim caption> (p. 12)

![<short description>](../figures/<basename>_figN.png)

- Key visual finding: <one sentence — what the eye sees / the point of the figure>
- **Figure notes:** <verbatim notes printed below the figure in the paper, if any>
```

The Tier A/B distinction lives in `_text.md` only (full optical decomposition for Tier A; schematic one-liner for Tier B). Wiki pages use the same lightweight embed format for all figures.

## Return value additions for Protocol M

```
Figures copied: [list of {source_cache_path, dest_wiki_path, paper_figure_label}]
Equation fallback used: <true/false> (with count and any "[unreadable equation]" instances if true)
```
