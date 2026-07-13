# Isolation: Default Marker Mode

The parent runs install/cache/convert steps. If `cache_text.py check <markdown_path>` finds a cached neutral extract, the parent runs `cache_text.py pull <markdown_path> <text_path>` and skips extraction. Otherwise the parent prepares the extraction substrate and launches one paper reader. The reader follows the manifest's execution mode, then runs one synthesis bottleneck.

```text
Prepare converted marker markdown for bounded extraction.

Markdown input: <markdown_path>
Text output:    <text_path>
Manifest:       <cache-dir>/substrate/manifest.json
Schema:         ~/.claude/skills/read-pdf/extraction_schema.md
Worker prompt:  ~/.claude/skills/read-pdf/fanout_worker.md
Synthesis:      ~/.claude/skills/read-pdf/fanout_synthesis.md

Process:
1. Parent runs:
   python3 ~/.claude/skills/read-pdf/scripts/prepare_substrate.py <markdown_path>
2. Parent launches one paper reader.
3. For `single_reader`, that reader processes bundles sequentially and writes one durable note file per bundle. For `fanout`, it launches one bounded worker per bundle.
4. After every expected note exists, synthesis reads manifest + worker notes, gap-rereads specific chunks only when needed, and atomically writes <text_path> via a validated temp file.
5. Parent runs:
   python3 ~/.claude/skills/read-pdf/scripts/cache_text.py push <markdown_path> <text_path>

Report when done: page count if available, figures/tables found, one-sentence content summary.
```

After the subagent returns, the parent reads `_text.md` only.
