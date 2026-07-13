# Protocol S — Wiki Synthesis from Split-PDF Extract

*Input:* validated `references/raw/<basename>_text.md` produced by the split reader.

Neutral extraction is already complete under `read-pdf/extraction_schema.md`. Read `_text.md`, current wiki context, and `common.md`; do not reopen split PDFs or `notes.md` during wiki synthesis. Return a targeted recovery request if a project-critical gap blocks writing.

## Figures

Embed figure paths already present in `_text.md`. Convert each `CLIP REQUIRED` marker or existing CLIP placeholder into `references/wiki/figures/<basename>_figN.png`, include that new target in the write plan, and return it under `Pending CLIPs`. A CLIP embed uses:

```markdown
![<short description>](figures/<basename>_figN.png)
*<verbatim caption> ([<basename>](../log.md), p. 12)*
```

Ensure `references/wiki/figures/` exists before adding a CLIP path.

## Write wiki artifacts

Follow the plan-snapshot-apply contract and relevance rules in `common.md`.

## Return additions

```text
Pending CLIPs: [list of {target_path, source_paper, page_number, one_liner}]
Targeted recovery requests: [list of {missing_item, likely_source_location}]
```
