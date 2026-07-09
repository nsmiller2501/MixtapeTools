---
name: to-tickets
description: Break a research spec, plan, issue, or conversation into tracker-ready tickets with blocking edges. Use after scope is clear and the user wants executable agent-sized work.
disable-model-invocation: true
---

# To Tickets

Break work into tracer-bullet tickets sized for one focused agent session. Prefer vertical slices of research progress over layer-by-layer chores.

## Process

1. Read `CLAUDE.md` and `agent_memory/research-tracker.md` if present. Completion: you know the tracker substrate, labels, lifecycle, and markdown bridge.
2. Gather the source plan/spec/issue/conversation and relevant `agent_memory/` context. Completion: each ticket can point to its source and use project vocabulary.
3. Draft tickets in dependency order. Completion: every ticket has a title, blocking edges, deliverable, and validation criteria.
4. Show the draft breakdown and ask for approval. Completion: the user confirms granularity and blocking edges.
5. Publish only after approval. For GitHub Issues, create one issue/sub-issue per ticket with tracker labels and native blocking links where available. For local markdown, write the tracker-contracted file.

## Ticket Shape

```markdown
## <Ticket Title>

**Source:** <spec/issue/note link or path>

**What it delivers:** <end-to-end research or engineering progress this ticket makes real>

**Blocked by:** <ticket titles or "None">

**Validation:**
- [ ] <observable check>
- [ ] <observable check>
```

## Slicing Rules

Each ticket should leave behind a verifiable artifact: passing tests, a checked dataset, a rendered table/figure, a written decision, or a closed investigation.

Wide mechanical changes are the exception. Use expand-contract sequencing: add the new form, migrate bounded batches, then remove the old form once no callers remain.
