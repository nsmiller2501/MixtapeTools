# Protocol M — Converted Markdown

*Input:* path to `markdown.md` (in the converter cache), path to the cache directory (for figures), canonical paper basename.

Protocol M reads only the converted `markdown.md`, `meta.json`, and cache-local figure/equation files. Do not inspect the source PDF with `pdftotext` or any other text extractor for substantive synthesis, even if conversion is slow. If conversion is still running, wait.

## Step 1: Check for equation fallback

Read `<cache-dir>/meta.json`. If `equation_extraction_mode == "image_fallback"`, equations were extracted as `<cache-dir>/figures/eq_*.png` rather than inline LaTeX. Before synthesis, transcribe each:

```
Read the image at <eq-png-path>. It is a single equation clipped from an academic paper.
Transcribe it as LaTeX, in display math mode ($$ ... $$). Output only the LaTeX —
no commentary, no surrounding text. If the equation is not legible, output "[unreadable equation]".
```

Edit `<cache-dir>/markdown.md` in place to replace each `![](figures/eq_N.png)` with the transcribed LaTeX. (The cache markdown is scratch — overwriting is fine; `convert.py` regenerates it on a hash miss.)

## Step 2: Synthesize `_text.md`

Read `markdown.md`. Produce `references/raw/<basename>_text.md` following the `_text.md` structure in `common.md` (bib block, plain-English synthesis, 11 structured dimensions). Write or overwrite if a prior partial file exists.

For the bib metadata block: scan `markdown.md` for the DOI regex `10\.\d{4,}/\S+`. Extract authors, title, year, and venue from the title page text. Record null for any field not found.

## Step 3: Copy and classify relevant figures

For each figure in `markdown.md` (referenced as `![](figures/fig_N.png)`):

1. Identify the paper figure number from surrounding caption text.
2. Apply the project-relevance filter. Non-relevant: one-line description + page ref only; do not copy.
3. For relevant figures:
   - Copy from cache to wiki: `cp <cache-dir>/figures/fig_N.png references/wiki/figures/<basename>_fig<M>.png` (where M is the paper's figure number). Before the first copy, run `mkdir -p references/wiki/figures` (idempotent).
   - Classify as Tier A (data figure: scatter, line, bar, coefplot, histogram, density, time series, RD/event-study plot) or Tier B (schematic: DAG, conceptual diagram, map, flowchart, theoretical model). Use the caption text; read the PNG only if the caption is genuinely ambiguous.

## Step 4: Write wiki pages

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
