# Protocol M — Wiki Synthesis from Marker Extract

*Input:* validated `references/raw/<basename>_text.md`, marker cache directory, canonical paper basename, and optional citation-overlap JSON.

Neutral extraction is already complete. Read `_text.md`, current wiki context, and `common.md`; keep worker notes and marker chunks outside this context. If `_text.md` has a project-critical gap, return a targeted recovery request rather than opening extraction scratch.

## Copy relevant figures

For each project-relevant figure listed in `_text.md`:

1. Identify the paper figure number from the caption and include its destination in the write plan.
2. After snapshot approval, run:
   `python3 ~/.claude/skills/wiki-update/scripts/copy_marker_figure.py <cache-dir>/markdown.md <absolute-project-root>/references/wiki/figures --basename <basename> --figure <M>`
3. Verify the printed destination exists.
4. Use the helper-printed `figures/<basename>_figN.<ext>` path in wiki markdown.

Less-relevant figures receive a one-line description and page reference without a copy. Read a copied image only when `_text.md` does not support the wiki description.

## Write wiki artifacts

Follow the plan-snapshot-apply contract and relevance rules in `common.md`. Use citation-overlap candidates only when they provide substantively useful wiki links.

## Return additions

```text
Figures copied: [list of {source_cache_path, dest_wiki_path, paper_figure_label}]
Equation fallback used: <true/false> (with count and any `[unreadable equation]` instances)
Targeted recovery requests: [list of {missing_item, likely_source_location}]
```
