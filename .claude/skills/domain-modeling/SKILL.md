---
name: domain-modeling
description: Build or sharpen research project terminology and durable decisions in agent_memory. Use when the user wants to pin down domain language, resolve glossary conflicts, or when another planning skill needs to update scoped project memory.
---

# Domain Modeling

Use this when changing the model, not merely reading it. Plain vocabulary lookup is ordinary repo legwork.

## Research Memory Contract

Before writing, read `CLAUDE.md` and `agent_memory/research-tracker.md` if they exist. They define the repo's tracker substrate and artifact boundaries.

Write durable model updates under `agent_memory/`:

- Glossary terms: `agent_memory/<scope>/CONTEXT.md`.
- Methodology notes and decisions: `agent_memory/<scope>/NOTES.md`.
- Hard-to-reverse, project-wide decisions: `agent_memory/docs/adr/`.

Use the `grill-with-docs` helper files for exact formats when present.

## During The Session

Challenge terms against existing `CONTEXT.md` files. When the user uses vague or overloaded language, propose one canonical term and list aliases to avoid.

Stress-test relationships with concrete research scenarios: sample construction, treatment definition, variable timing, units of observation, identifying variation, estimation sample, robustness, and output artifacts.

Check factual claims against code, data docs, notes, and the tracker when available. Surface contradictions immediately and ask which source should govern.

Write resolved terms and decisions inline as they crystallise. Create files lazily only when there is something to record.

Offer an ADR only when the decision is project-wide, hard to reverse, surprising without context, and the result of a real tradeoff.
