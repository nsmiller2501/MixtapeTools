# Isolation: Default Marker Mode

The parent runs install/cache/convert steps, then launches a subagent for markdown reading and extraction.

```text
Read a converted markdown file and produce structured extraction notes.

Markdown input: <markdown_path>
Text output:    <text_path>
Schema:         ~/.claude/skills/read-pdf/extraction_schema.md

Process:
1. Read <markdown_path> using the Read tool.
2. Extract the bibliographic metadata block and 8 research dimensions as specified in extraction_schema.md.
3. Write the final structured extraction to <text_path>, with the ## Bibliographic metadata block first.

Report when done: page count if available, figures/tables found, one-sentence content summary.
```

After the subagent returns, the parent reads `_text.md` only.
