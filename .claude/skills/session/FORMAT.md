# Progress Log Format

## Required sections (session-start relies on these)

### Summary
Concise current project state after this session.

### Next Steps
Outstanding tasks for the next session. Use Obsidian markdown task boxes exactly:

```markdown
- [ ] Finish the remaining validation pass
- [ ] Re-run the full pipeline after fixing the input file
```

Do not use numbered lists, bare bullets, GitHub issue syntax, or prose paragraphs for task items here. Background task aggregation depends on the literal `- [ ]` prefix.

### Completed Tasks
Tasks completed during this session, when useful to record. Use Obsidian checked task boxes exactly:

```markdown
- [x] Added cached extract handling
- [x] Verified wiki-update pulls `text.md` from cache
```

Use `- [x]` only for completed task items. Do not use "done:", strikethrough, or prose-only completion notes.

If `agent_memory/tasklist.md` exists, treat it as read-only except for marking already-listed completed tasks from `- [ ]` to `- [x]`. Do not append new tasks there during session end; put newly discovered outstanding tasks in the progress log's `Next Steps` section instead.

### Key Files
Files session-start should re-read to get oriented. Use `path:start-end` line ranges to keep reads targeted. One per line.

```
agent_memory/key_decisions.md:1-40
plans/analysis_plan.md:55-80
```

## Optional sections (agent's discretion)
Work Done, Decisions, Open Questions, etc. — add as needed.
