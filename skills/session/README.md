# /session

Tracker-first session orientation and closeout for research and coding projects.

`/session start` reads the project's tracker contract and current tracker state before recommending a ready target. A progress log is supplementary and is read only when the project contract or user requests it, or no tracker exists.

`/session end` leaves issue-scoped continuity in the issue or PR and promotes durable knowledge to tracked `agent_memory/`. It writes a progress log only for exploratory, integration, or otherwise uncaptured context.

The result is one authoritative work queue that remains usable across chats, branches, and worktrees.
