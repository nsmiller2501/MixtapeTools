# /session

A lightweight session lifecycle skill for research and coding projects. The intent is to make it easy to pick up exactly where you left off across Claude Code sessions, and to ensure that progress is reliably recorded when you're done.

## Commands

**`/session start`** — orients Claude for a new session. Reads the most recent progress log from `progress_logs/`, then reads the key files listed in that log. Returns a brief status report: current state, open blockers, and next priorities. Also activates caveman mode for the session.

**`/session end`** — closes out the session. Writes a dated progress log to `progress_logs/YYYY-MM-DD_session.md` summarizing what was done, what's pending, and which files are worth reading next time. Then scans `agent_memory/` for any files that should be updated based on decisions or changes made during the session.

## Why this exists

Claude Code sessions are stateless — each conversation starts cold. Without a discipline around session logging, context gets lost and each session wastes time re-deriving the current state. This skill is the infrastructure for maintaining continuity: a consistent format for progress logs, and a ritual for reading them at the start and writing them at the end.
