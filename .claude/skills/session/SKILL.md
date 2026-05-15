---
name: session
description: Manages start-of-session and end-of-session lifecycle for research and coding projects. On `start`, activates terse mode and orients by reading the latest progress log and key files; on `end`, writes a dated progress log and updates `agent_memory/` files. Use when the user says `/session start`, `/session end`, "start a session", "wrap up the session", or similar — pass `start` or `end` as the sub-command.
---

## Args
- `start` — orient for a new session
- `end` — close out the session with a progress log

---

## start

1. Switch to caveman mode: drop articles, filler, pleasantries. Terse fragments OK. Technical terms stay exact.
2. Find most recent file in `progress_logs/` (sort by filename date descending).
3. Read it. Then read every file (at the line ranges) listed under `## Key Files` in that log.
4. Report in 3–5 bullets: current state, blockers, next priorities.

---

## end

1. Determine filename: `YYYY-MM-DD_session.md` using today's date. Append `_2`, `_3` on collision.
2. Write progress log — see [FORMAT.md](./FORMAT.md).
3. Scan `agent_memory/` for files needing updates based on this session (decisions made, terms defined, plans changed). Update them.
4. Confirm: log written at `progress_logs/<filename>`, files updated.
