# Agent Isolation Protocol

**When split-pdf is invoked by another skill or workflow** (any process that continues working after the PDF has been read), the PDF reading MUST run inside a subagent to prevent context bloat in the parent conversation.

**Why:** Each PDF page rendered by the Read tool produces image data in the conversation context. A 35-page PDF (9 chunks) can add 10-20MB of image data that accumulates permanently. After reading one or two large PDFs on top of prior work, the conversation hits the API request size limit and becomes unrecoverable: no subsequent Read calls succeed, and rewinding does not free sufficient space.

## Pattern

The parent skill handles splitting (Step 2's Python script) in its own context; this is lightweight. Then it launches an Agent to perform all the reading:

```
Read PDF split files and produce structured extraction notes.

Split directory: <split_dir>
Files (read in this order, 3 at a time): <file_list>
Notes output: <notes_path>
Text output: <text_path>

Process:
1. Read 3 PDF files at a time using the Read tool.
2. After each batch, update the notes file with extracted content.
3. Extract the bibliographic metadata block and 8 research dimensions as
   specified in extraction_schema.md (read that file before starting).
4. Write the final structured extraction to the text output path, with the
   ## Bibliographic metadata block first, followed by the research notes.

Report when done: pages read, figures/tables found, one-sentence content summary.
```

After the agent returns, the parent reads the output files (plain markdown, not PDF images) and continues its workflow.

**Standalone invocations** (user calls `/split-pdf` directly) use the interactive protocol in SKILL.md with reads in the main conversation and the pause-and-confirm protocol.
