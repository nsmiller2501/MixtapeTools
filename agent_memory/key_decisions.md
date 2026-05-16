# Key Decisions — MixtapeTools Skill Development

Durable decisions for Claude/Codex skill architecture. These are tracked in git and should survive branch deletion, rollbacks, and session-log churn. Append new entries; do not rewrite history except to fix factual errors.

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-16 | Keep `progress_logs/` ignored; use tracked `agent_memory/` for durable project memory. | Progress logs are session continuity artifacts and branch-local scratch history. Tracking them would couple living logs to branch rollbacks. Durable decisions should be promoted here instead. |
| 2026-05-16 | Keep `/handoff` and `/session end` as separate skills. | `/session end` is project-rooted, writes dated progress logs, and updates `agent_memory/`; `/handoff` is an ephemeral baton-pass outside the project-memory lifecycle. |
| 2026-05-16 | Make `/read-pdf` canonical and keep `/split-pdf` as compatibility wrapper. | The two skills shared an output contract and duplicated schema/isolation docs. `/read-pdf --split` preserves the legacy vision-batch backend while reducing maintenance drift. |
