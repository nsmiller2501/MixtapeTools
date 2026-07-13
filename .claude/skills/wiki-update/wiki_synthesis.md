# Wiki Synthesis Prompt

Use this prompt after a project-neutral `_text.md` exists.

## Inputs

- `references/raw/<basename>_text.md`
- canonical paper basename
- `references/CLAUDE.md`
- project root `CLAUDE.md`
- current `references/wiki/index.md`
- relevant existing wiki page paths
- optional `references/raw/raw_build/<basename>_fanout/citation_overlap.json`
- optional cache `markdown.md` path, cache figure directory, absolute project `references/wiki/figures` directory, and `copy_marker_figure.py` path for Protocol M figure copies

Do not read worker notes, marker chunks, or the full marker `markdown.md`. If `_text.md` explicitly marks a gap that blocks wiki writing, return the gap to the main session instead of reopening fanout internals.

## Task

Read the current index from disk immediately before planning. Use the neutral `_text.md`, project context, index, and relevant existing pages to plan project-specific wiki artifacts. Return every existing target to modify and new target to create without writing. After the main session snapshots the approved plan, apply only that plan and return the summary required by `common.md`.

## Source Page Naming

Use the canonical source slug from the paper basename:

- `Last_Year_Venue` -> `last-year-venue.md`
- `Last1_Last2_Year_Venue` -> `last1-last2-year-venue.md`
- `Last1_etal_Year_Venue` -> `last1-etal-year-venue.md`

Do not expand `_etal` into all author names. Examples:

- `Bento_Miller_Mookerjee_Severnini_2023_JEEM` -> `bento-etal-2023-jeem.md`
- `Anderson_etal_2022_NBER` -> `anderson-etal-2022-nber.md`

## Concept Page Rules

- Read `wiki/index.md` first.
- Reuse near-matching existing concept pages. Do not create duplicate synonyms.
- If a near-match exists but fit is ambiguous, return a disambiguation question.
- New concept pages need short, stable slugs that name concepts, not paper-specific prose.

## Outputs

- write plan listing existing and new targets
- source page and concept/wiki pages after snapshot approval
- non-destructive index updates
- proposed destructive diffs, if needed
- copied Protocol M figures, if relevant and available
- return-value summary required by `common.md`
