---
name: session
description: Manages start-of-session and end-of-session lifecycle for research and coding projects. On `start`, activates terse mode and orients by reading the latest progress log and key files; on `end`, writes a dated progress log and updates `agent_memory/` files. Use when the user says `/session start`, `/session end`, "start a session", "wrap up the session", or similar — pass `start` or `end` as the sub-command.
---

## Args
- `start` — orient for a new session
- `start --tasks` — orient as above, then also summarize the task list
- `end` — close out the session with a progress log

---

## start

1. Call the `caveman` skill via the Skill tool before doing anything else.
2. Run `~/.claude/skills/session/scripts/latest_progress_log.sh` to find the most recent file in `progress_logs/`.
3. Read it. Then read every file (at the line ranges) listed under `## Key Files` in that log.
4. Report in 3–5 bullets: current state, blockers, next priorities.
5. If `--tasks` was passed: read `agent_memory/tasklist.md` and append a **Task list** section summarizing every item.

---

## end

1. Determine filename: `YYYY-MM-DD_<session_slug>.md` using today's date. Append `_2`, `_3` on collision.
2. Write progress log — see [FORMAT.md](./FORMAT.md). Use Obsidian task boxes exactly for all task items: `- [ ]` for outstanding tasks and `- [x]` for completed tasks.
3. Scan `agent_memory/` for files needing updates based on this session (decisions made, terms defined, plans changed, tasks completed). Update them. Treat `agent_memory/tasklist.md` as read-only except for marking existing completed task boxes from `- [ ]` to `- [x]`.
4. Confirm: log written at `progress_logs/<filename>`, files updated.
