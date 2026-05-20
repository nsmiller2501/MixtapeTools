# Fanout Synthesis Prompt

Use this prompt after all worker bundles have durable notes.

## Inputs

- `manifest.json`
- all worker note paths
- output `_text.md` path
- `extraction_schema.md`
- optional wiki-update context and wiki paths

## Task

Read the manifest and every worker note. Write one coherent, project-neutral `_text.md` using `extraction_schema.md`. If running under `wiki-update`, write the neutral `_text.md` first, then apply project context only to wiki pages.

## Rules

- Treat worker notes as local evidence, not final interpretation.
- Do gap-directed rereads only: reread source chunks when notes omit a needed table, figure, equation, result, or ambiguous claim.
- Do not read the full marker `markdown.md`.
- Preserve exact coefficients, standard errors, sample details, equation labels, and table/figure captions when available.
- Keep `_text.md` project-neutral. Project relevance gates belong only to wiki-facing pages.

## Outputs

For `read-pdf`:
- `<basename>_text.md`

For `wiki-update`:
- `references/raw/<basename>_text.md`
- source page and concept/wiki pages
- non-destructive index updates
- proposed destructive diffs, if needed
- return-value summary required by `wiki-update/common.md`
