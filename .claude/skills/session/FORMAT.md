# Progress Log Format

Use this format only when `/session end` determines that a progress log is warranted. The configured tracker remains the authoritative work queue.

## Required sections

### Summary

Concise context that cannot be reconstructed from the tracker, PRs, commits, or durable project memory.

### Next Steps

Use Obsidian task boxes exactly. For tracker-backed work, each actionable task must reference its authoritative issue:

```markdown
- [ ] Continue #42 after the restricted extract arrives
- [ ] Triage the untracked robustness idea from `notes/meeting.md`
```

An untracked item is intake, not ready work. Do not restate issue acceptance criteria or build an independent queue.

### Completed Tasks

When useful, record completed tasks with checked Obsidian boxes and issue or PR references:

```markdown
- [x] Implemented and validated #41 in PR #57
```

If `agent_memory/tasklist.md` exists, treat it as read-only except for marking an already-listed task complete.

### Key Files

List only files needed to recover the supplementary context, using `path:start-end` line ranges:

```text
agent_memory/key_decisions.md:1-40
plans/analysis_plan.md:55-80
```

## Optional sections

Add Decisions, Open Questions, or other context only when useful.

### Tracker Updates

Link each issue or PR updated or drafted, and record any remaining blocker. Tracker state overrides this snapshot.
