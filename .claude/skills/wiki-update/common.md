# Common wiki-synthesis protocol

These rules are shared across Protocols M, E, and S after a project-neutral `_text.md` exists. Neutral extraction follows `read-pdf/extraction_schema.md`; this file does not redefine that contract.

---

## Evidence boundary

Use `_text.md` as the paper evidence. Apply project relevance while writing wiki pages, without rewriting the neutral extract. If a project-critical table, figure, equation, result, or ambiguous claim is missing, return a targeted recovery request naming the missing item and likely source location.

## Tables in wiki pages

For tables directly relevant to the project, reuse machine-readable content from `_text.md`. Less-relevant tables receive a one-line description with page reference. Preserve available column headers, values, standard errors, significance stars, and notes verbatim.

For relevant tables:

```
**Table N:** <verbatim caption> (p. 12)

| Variable | (1) | (2) | (3) |
|---|---|---|---|
| Schooling | 0.087*** | 0.091*** | 0.085*** |
|           | (0.012)  | (0.013)  | (0.011)  |
| N         | 12,450   | 12,450   | 12,450   |
| R²        | 0.34     | 0.36     | 0.38     |

Notes: <verbatim table notes — SE clustering, FE structure, etc.>
```

Pipe-syntax markdown only; table notes are part of the table.

## Figures in wiki pages

Less-relevant figures receive a one-line description with page reference. Protocol M copies relevant cached figures; Protocols E and S embed existing figure paths or forward CLIP placeholders.

```
**Figure N:** <verbatim caption> (p. 12)

![<short description>](figures/<basename>_figN.<ext>)

- Key visual finding: <one sentence>
- **Figure notes:** <verbatim notes, if available>
```

Wiki pages live directly under `references/wiki/`; figure links are relative paths beginning with `figures/`.

## Plan and substantive-change rule

First return every existing and new target without writing. After the main session snapshots the approved plan, apply non-destructive edits directly. Destructive edits to existing pages require approved unified diffs.

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

## Concept page disambiguation

Before creating a new concept page, check `wiki/index.md` for existing pages covering the same concept — including obvious synonyms (e.g., "RDD" vs "regression discontinuity"). If a near-match exists but you aren't confident, do **not** create a new page; return the ambiguity to the main session as a question for the user.

## Relevance filtering

Apply "compress, don't omit": sections directly relevant to the project's research focus get full treatment. Less-relevant sections get a one-line description plus page reference. Nothing is fully omitted.

## Wiki-agent return value

```
Existing targets modified: [list]
New targets created: [list]
Pages created: [list]
Pages modified non-destructively: [list with brief description]
Proposed destructive edits: [list of {page, unified diff, rationale}]
Disambiguation questions: [list of {concept, candidate existing pages}]
Proposed log entry: [single line for wiki/log.md]
Pending CLIPs: [list of {target_path, source_paper, page_number, one_liner}]
[Protocol M only] Figures copied: [list of {source_cache_path, dest_wiki_path, paper_figure_label}]
[Protocol M only] Equation fallback used: <true/false>
Errors: [any issues encountered]
```
