---
name: session
description: Manages start-of-session orientation and end-of-session closeout for tracker-backed research and coding projects. Use when the user says `/session start`, `/session end`, "start a session", or "wrap up the session" — pass `start` or `end` as the sub-command.
---

## Args

- `start` — orient from the configured tracker and durable project memory
- `start --issues` — compatibility alias for tracker-first orientation
- `start --tasks` — orient as above, then summarize the legacy markdown task list
- `end` — close out tracker state and durable project memory; write a progress log only when warranted

## Tracker contract

Read the tracker contract named by the project instructions. If none is named, check `agent_memory/research-tracker.md`, then `agent_memory/tracker.md`.

The configured tracker is the authoritative work queue. Issues hold actionable work and remaining steps; PRs and commits hold implementation evidence; `agent_memory/` holds durable project knowledge. Progress logs are supplementary context, not another queue.

## start

1. Read the project instructions, tracker contract, and relevant durable files in `agent_memory/`. Completion: you know the substrate, lifecycle vocabulary, artifact boundaries, and durable constraints.
2. If the substrate is GitHub Issues, query relevant open work using the contract's vocabulary: an explicitly named or assigned issue first, then assigned issues, ready work, and blocked work. Keep the query narrow and report it. Completion: every reported work item came from current tracker state.
3. Read the latest progress log only when the project has no configured tracker, the user requests log context, or the tracker contract makes logs part of startup. Treat issue references in a log as pointers back to current tracker state. Read relevant `## Key Files` ranges from that log. Completion: stale log text has not overridden the tracker.
4. If `--tasks` was passed, read `agent_memory/tasklist.md` and label its contents as legacy intake or local work according to the tracker contract. Completion: markdown tasks are not presented as a second authoritative queue.
5. Report in 3–5 bullets: current state, blockers, next priorities, and the issue or local task that is the natural session target. Completion: the recommended target is ready under the configured lifecycle.

## end

1. Read the tracker contract and classify the session as issue-scoped or exploratory/integration. Completion: every actionable next step has one authoritative destination.
2. Update tracked `agent_memory/` files for durable decisions, terminology, constraints, or plans changed during the session. Treat `agent_memory/tasklist.md` as read-only except for marking an existing task complete. Completion: durable knowledge needed outside the current issue or worktree will merge with the project.
3. For issue-scoped work, draft the tracker or PR update with outputs, validation, blockers, remaining steps, and artifact or commit links. Post updates according to the tracker contract; ask before closing an issue unless the user explicitly requested closure. Completion: another agent can continue from the issue or PR without the worktree or chat.
4. Write a progress log only for exploratory work, integration/orchestration work, a user request, or material context that the tracker and durable files cannot represent. Use [FORMAT.md](./FORMAT.md). Completion: any log adds context without creating a parallel task queue.
5. Confirm tracker/PR updates, durable files changed, and whether a progress log was written or intentionally skipped.
