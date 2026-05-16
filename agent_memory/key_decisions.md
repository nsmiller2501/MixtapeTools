# Key Decisions — MixtapeTools Skill Development

Durable decisions for Claude/Codex skill architecture. These are tracked in git and should survive branch deletion, rollbacks, and session-log churn. Append new entries; do not rewrite history except to fix factual errors.

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-16 | Keep `progress_logs/` ignored; use tracked `agent_memory/` for durable project memory. | Progress logs are session continuity artifacts and branch-local scratch history. Tracking them would couple living logs to branch rollbacks. Durable decisions should be promoted here instead. |
| 2026-05-16 | Keep `/handoff` and `/session end` as separate skills. | `/session end` is project-rooted, writes dated progress logs, and updates `agent_memory/`; `/handoff` is an ephemeral baton-pass outside the project-memory lifecycle. |
| 2026-05-16 | Make `/read-pdf` canonical and keep `/split-pdf` as compatibility wrapper. | The two skills shared an output contract and duplicated schema/isolation docs. `/read-pdf --split` preserves the legacy vision-batch backend while reducing maintenance drift. |
| 2026-05-16 | Keep one `/referee2` router; split code mode internally by phase. | `referee2.md` is the right shared persona/common resource for deck, code, and future referee-audit types. The real load problem was the 53KB code-mode protocol, now a small `code.md` index plus progressive-disclosure phase files. |
