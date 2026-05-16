# Deferred Ideas — MixtapeTools Skill Development

Ideas intentionally postponed, rejected, or left for a later usage window. Use this for decisions that should remain visible even if the branch where they were tested is abandoned.

- **Remove `/split-pdf` wrapper** (defer after 2026-05-16): Keep wrapper for now to preserve slash-command muscle memory. When ready, delete the skill in place; the canonical split workflow lives under `/read-pdf --split`, and the wrapper has no remaining dependencies that require a larger migration.
- **Split `/referee2` into sibling skills** (deferred after 2026-05-16): Keep one router for now. Revisit only if future referee-audit types make routing ambiguous or mode triggers become too broad for one skill.
- **Refine `newproject` agent-memory taxonomy** (revisit after 2026-07-16): Decide whether `agent_memory/key_decisions.md` should remain a broad catch-all for all durable decisions, or split into narrower files such as methodology decisions, project conventions, workflow decisions, and naming/scope decisions. Wait until several projects have accumulated real entries, then inspect whether natural boundary definitions are obvious.
