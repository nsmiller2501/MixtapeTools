---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates scoped documentation (CONTEXT.md, NOTES.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions. Supports nested scopes for research projects with multi-stage pipelines.
---

<what-to-do>

Interview the user relentlessly about every aspect of the plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies one decision at a time. For each question, propose your recommended answer.

Ask one question at a time. Wait for feedback before continuing.

If a question can be answered by exploring the codebase or reading existing docs, do that instead of asking.

</what-to-do>

<orchestration>

This skill orchestrates four phases. Each phase delegates to a helper file for the details. Read the helper when you enter the phase.

### Phase 1 — Resolve scope (entry)

Before the first question, determine the scope of this session. See [SCOPE-RESOLUTION.md](./SCOPE-RESOLUTION.md).

Outcome: a scope path (e.g. `acquire/firm_registry`, or `root` for single-purpose mode), confirmed with the user.

### Phase 2 — Load merged glossary + scan cross-cutting (entry, continued)

With scope locked, load the merged glossary across the scope tree (root → stage → ... → current scope) per [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). Surface any shadowing conflicts before grilling begins.

Scan top-level `agent_memory/*.md` for cross-cutting files (e.g. `sample_restrictions.md`, `key_decisions.md`, `codebook.md`, `dropped_analyses.md`) so you know what's available to read when topics touch them. See [CROSS-CUTTING.md](./CROSS-CUTTING.md).

### Phase 3 — Grill, write inline

Drive the interview. When a term is resolved, write it to the appropriate scope's `CONTEXT.md` immediately per [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). When a methodology decision crystallises, write it to that scope's `NOTES.md` per [NOTES-FORMAT.md](./NOTES-FORMAT.md). Offer an ADR only for project-wide, hard-to-reverse, surprising decisions per [ADR-FORMAT.md](./ADR-FORMAT.md).

When the user signals interest in a deeper sub-scope, ask explicitly before nesting — never descend on your own. See SCOPE-RESOLUTION.md for the descent protocol.

When the topic touches a known cross-cutting file, read it. Do not write to top-level cross-cutting files mid-session.

After any structural change (new scope directory at any depth, new cross-cutting file detected), run the deterministic helper to rebuild the map:

```bash
python3 ~/.claude/skills/grill-with-docs/scripts/build-context-map.py <path-to-agent_memory>
```

See [CONTEXT-MAP-FORMAT.md](./CONTEXT-MAP-FORMAT.md) for the map shape and helper contract.

### Phase 4 — Grilling resolution (promotion + handoff)

Trigger when one of these happens:

- **Implicit**: no open branches remain on the design tree.
- **Explicit**: user says "ready to write", "let's implement", "done grilling", "wrap grilling", or similar.
- **Ambiguous "wrap up"**: ask the user — "wrap grilling, or end the full `/session`?" — these are distinct (this skill governs grilling resolution only; `/session end` is a separate skill for the parent work session).

At resolution:

1. Walk back through scope `NOTES.md` entries written this session. For any that look genuinely cross-cutting (apply outside the current scope), nominate them for promotion to a top-level cross-cutting file per [CROSS-CUTTING.md](./CROSS-CUTTING.md). User confirms each promotion individually.
2. Refresh CONTEXT-MAP.md via the helper script.
3. Offer the natural next action: "shall we write the spec, plan the implementation, or hand off?"

</orchestration>

<supporting-info>

### File layout produced by this skill

```
agent_memory/
├── CONTEXT.md                       ← project-wide glossary (cross-cutting terms)
├── CONTEXT-MAP.md                   ← auto-generated tree + cross-cutting registry
├── NOTES.md                         ← project-wide methodology notes (rare; usually scoped)
├── sample_restrictions.md           ← user-owned cross-cutting files (optional, varies by project)
├── key_decisions.md
├── codebook.md
├── dropped_analyses.md
├── docs/
│   └── adr/                         ← project-wide hard-to-reverse decisions only
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
├── acquire/                         ← stage scope (lazy)
│   ├── CONTEXT.md                   ← stage-level glossary
│   ├── NOTES.md                     ← stage-level methodology notes
│   └── firm_registry/               ← sub-scope (lazy, user-confirmed)
│       ├── CONTEXT.md
│       └── NOTES.md
└── analyze/
    ├── CONTEXT.md
    └── structural/
        ├── CONTEXT.md
        └── NOTES.md
```

All directories and files are created **lazily**, only when the first write to that scope happens. The skill never pre-creates structure.

### What goes where

| Artifact | Location | When |
|----------|----------|------|
| Glossary term | `<scope>/CONTEXT.md` at the level where it's first relevant | When term is resolved |
| Methodology decision (scope-local) | `<scope>/NOTES.md` as `## Decision` | When user commits to an approach |
| Methodology note (lighter than decision) | `<scope>/NOTES.md` as `## Note` | Observations, open questions, context |
| Hard-to-reverse, project-wide decision | `agent_memory/docs/adr/NNNN-slug.md` | Rare. Three criteria in ADR-FORMAT.md |
| Cross-cutting claim (sample, codebook, etc.) | Top-level `agent_memory/<file>.md` | **Promotion step only**, at grilling resolution |

### Non-goals

- Do not maintain a graph of links between ADRs and NOTES. `NOTES.md` may reference an ADR one-way; ADRs hold no back-references.
- Do not edit `CONTEXT-MAP.md` by hand. The Python helper is the source of truth for structure; descriptions are user-editable text after the `—` separator.
- Do not write to top-level cross-cutting files mid-session. Read freely; write only at the promotion step.

</supporting-info>
