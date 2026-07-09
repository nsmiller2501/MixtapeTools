---
name: session
description: Manages start-of-session and end-of-session lifecycle for research and coding projects. On `start`, orients by reading the latest progress log and key files; on `end`, writes a dated progress log and updates `agent_memory/` files. Use when the user says `/session start`, `/session end`, "start a session", "wrap up the session", or similar — pass `start` or `end` as the sub-command.
---

## Args
- `start` — orient for a new session
- `start --tasks` — orient as above, then also summarize the task list
- `start --issues` — orient as above, then also summarize assigned/open tracker work
- `end` — close out the session with a progress log

---

## start

1. Read `CLAUDE.md` and `agent_memory/research-tracker.md` if present.
2. Run `~/.claude/skills/session/scripts/latest_progress_log.sh` to find the most recent file in `progress_logs/`.
3. Read it. Then read every file (at the line ranges) listed under `## Key Files` in that log.
4. If `--tasks` was passed: read `agent_memory/tasklist.md` and append a **Task list** section summarizing every item.
5. If `--issues` was passed, or the tracker contract names GitHub Issues as the substrate, summarize relevant open work from the tracker: assigned issues first, then issues labelled ready/blocked by the contract's vocabulary. Keep the query narrow and report the query used.
6. Report in 3–5 bullets: current state, blockers, next priorities, and the issue or local task that looks like the natural session target.

---

## end

1. Determine filename: `YYYY-MM-DD_<session_slug>.md` using today's date. Append `_2`, `_3` on collision.
2. Write progress log — see [FORMAT.md](./FORMAT.md). Use Obsidian task boxes exactly for all task items: `- [ ]` for outstanding tasks and `- [x]` for completed tasks.
3. Scan `agent_memory/` for files needing updates based on this session (decisions made, terms defined, plans changed, tasks completed). Update them. Treat `agent_memory/tasklist.md` as read-only except for marking existing completed task boxes from `- [ ]` to `- [x]`.
4. If the session worked on GitHub Issues, draft the issue update before posting. Include outputs, validation, blockers, next steps, and links to the progress log or artifacts. Ask before closing issues unless the user explicitly requested closure.
5. Confirm: log written at `progress_logs/<filename>`, files updated, tracker updates posted or left as drafts.
