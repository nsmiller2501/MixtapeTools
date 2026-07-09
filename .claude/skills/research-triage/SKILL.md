---
name: research-triage
description: Harvest research tasks from tasklist.md or user-named notes into specs, tickets, or tracker drafts. Use when the user wants to turn meeting notes, notes, progress logs, or task lists into GitHub Issues or local tracker work.
---

# Research Triage

Promote research tasks from human-facing notes into the configured tracker without flooding context.

## Inputs

Default invocation reads only:

- `CLAUDE.md`
- `agent_memory/research-tracker.md`
- `agent_memory/tasklist.md`, if present
- files or directories the user names directly

`--first-run` is the only full-harvest mode. It scans likely intake surfaces: `meetings/`, `notes/`, `progress_logs/`, and `agent_memory/tasklist.md`.

If the user names a broad directory without `--first-run`, inspect only the newest or explicitly relevant files and say what boundary you used.

## Process

1. Read the tracker contract.
   Completion: you know the substrate, artifact boundaries, labels, lifecycle, and markdown task bridge.

2. Gather candidate tasks from allowed inputs.
   Completion: each candidate has source path or URL, nearby context, and original wording.

3. Classify each candidate.
   Completion: every candidate is in exactly one bucket:
   - **Already tracked**: duplicates or clearly belongs to an existing issue/spec/ticket.
   - **Keep in notes**: too vague, stale, or not actionable.
   - **Needs grilling**: decision question exists but needs human judgment.
   - **Ready for spec**: objective/design is coherent but work is too broad for tickets.
   - **Ready for tickets**: acceptance criteria or validation checks are clear enough.
   - **Ready for human**: requires coauthor judgment, external access, or manual action.

4. Present a promotion draft.
   Completion: the user sees source, recommended bucket, proposed title, suggested labels, and next action for each promotable item.

5. Ask before writing.
   Completion: no GitHub Issues, tracker files, specs, or tickets are created until the user approves.

6. Dispatch approved items.
   Completion: each approved item goes to the narrowest next skill:
   - `grill-with-docs` for **Needs grilling**.
   - `to-spec` for **Ready for spec**.
   - `to-tickets` for **Ready for tickets**.
   - tracker draft or issue creation according to `agent_memory/research-tracker.md`.

## Promotion Draft Shape

```markdown
## Promotion Draft

### Ready for tickets

1. <title>
   Source: <path-or-url>
   Why: <one sentence>
   Labels: <suggested labels>
   Validation: <observable check>

### Needs grilling

1. <title>
   Source: <path-or-url>
   Decision question: <question to resolve>

### Keep in notes

1. <title or quoted fragment>
   Source: <path-or-url>
   Reason: <why not promotable yet>
```

## Duplicate Check

Before recommending a new issue or ticket, check the configured tracker and local tracker files for likely duplicates by concept, not just exact wording.

## Context Discipline

Do not read every historical meeting, note, or progress log during normal invocation. Ask the user for a path, use `agent_memory/tasklist.md`, or require `--first-run`.
