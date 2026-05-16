# Agent Isolation Protocol

**When read-pdf is invoked by another skill or workflow**, the reading and extraction step MUST run inside a subagent. The converted `markdown.md` can be large, and reading it in the parent context of an active workflow accumulates permanent token cost.

The conversion steps (install / SHA-256 cache check / convert.py if needed) are lightweight bash calls and run in the parent context. The `_text.md` collision check also stays in the parent. Only the markdown read + structured-extraction write goes into the subagent.

## Pattern

```
Read a converted markdown file and produce structured extraction notes.

Markdown input: <markdown_path>
Text output:    <text_path>

Process:
1. Read <markdown_path> using the Read tool.
2. Extract the bibliographic metadata block and 8 research dimensions as
   specified in extraction_schema.md (read that file before starting).
3. Write the final structured extraction to <text_path>, with the
   ## Bibliographic metadata block first, followed by the research notes.

Report when done: page count, figures/tables found, one-sentence content summary.
```

After the agent returns, the parent reads `_text.md` (plain text, not the large `markdown.md`) and continues its workflow.

**Standalone invocations** (user calls `/read-pdf` directly) read `markdown.md` in the main conversation and write `_text.md` directly — no subagent needed for a one-off read.
