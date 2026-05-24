# /grill-with-docs

Like `/grill-me`, but domain-aware and scope-aware.

Before the interview begins, the skill resolves the **scope** of the session — project-wide, a specific pipeline stage, a sub-module within a stage, or single-purpose mode for one-shot repos. With scope locked, it reads the merged glossary across the scope tree (root → stage → module) and any registered cross-cutting files, then grills with that context in mind.

When a term gets resolved during grilling, the skill writes it to the appropriate scope's `CONTEXT.md` immediately. When a methodology decision crystallises, it writes a `## Decision` entry to that scope's `NOTES.md`. Project-wide, hard-to-reverse decisions still go to top-level ADRs. Cross-cutting decisions (sample restrictions, codebook entries, etc.) are nominated for promotion to top-level files at grilling resolution — never written silently mid-session.

## Why scope-aware

A research project has nested concerns:

- The project as a whole (theory, identification, paper structure).
- Each pipeline stage (acquire, build, analyze, write).
- Sub-modules within each stage (firm-registry scrape vs. customs pull; descriptive vs. structural analysis).

Without scope-awareness, every grilling session writes to one `CONTEXT.md` at the repo root, and unrelated sessions pollute each other's context. With scope-awareness, a session about firm-registry acquisition writes only to `agent_memory/acquire/firm_registry/`, while terms genuinely shared project-wide (e.g. "Chinese firm") land at root and inherit cleanly down the tree.

## File layout

```
agent_memory/
├── CONTEXT.md                       # project-wide glossary
├── CONTEXT-MAP.md                   # auto-generated tree (helper script)
├── NOTES.md                         # project-wide notes (rare)
├── sample_restrictions.md           # cross-cutting (user-owned, optional)
├── key_decisions.md
├── codebook.md
├── dropped_analyses.md
├── docs/adr/                        # project-wide hard-to-reverse decisions
│   └── 0001-instrument-strategy.md
├── acquire/
│   ├── CONTEXT.md                   # stage glossary
│   ├── NOTES.md                     # stage methodology notes
│   └── firm_registry/
│       ├── CONTEXT.md
│       └── NOTES.md
└── analyze/
    └── structural/
        ├── CONTEXT.md
        └── NOTES.md
```

All paths created lazily. The skill never pre-creates structure.

## Helper files

- [SKILL.md](./SKILL.md) — orchestrator and phase contract
- [SCOPE-RESOLUTION.md](./SCOPE-RESOLUTION.md) — mode and scope on entry, descent protocol, slug rules
- [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) — glossary format and merge-up rules with conflict surfacing
- [NOTES-FORMAT.md](./NOTES-FORMAT.md) — `## Decision` and `## Note` taxonomy, optional one-way refs to ADRs
- [CROSS-CUTTING.md](./CROSS-CUTTING.md) — read-anytime / write-at-resolution protocol for top-level files
- [CONTEXT-MAP-FORMAT.md](./CONTEXT-MAP-FORMAT.md) — map shape and the deterministic helper script
- [ADR-FORMAT.md](./ADR-FORMAT.md) — project-wide hard-to-reverse decisions only
- [scripts/build-context-map.py](./scripts/build-context-map.py) — deterministic map rebuilder

## Single-purpose mode

For repos that aren't multi-stage research projects (e.g. a single library, a tool, an in-conversation design session like this one), the user can say "single-purpose", "no nesting", or "scope: root" at the start. The skill skips scope nesting entirely, writes only to `agent_memory/CONTEXT.md` and `agent_memory/NOTES.md`, and does not create `CONTEXT-MAP.md`. If the session unexpectedly grows in scope mid-conversation, an escape hatch lets the user promote to multi-scope.

---

*Originally by [Matt Pocock](https://github.com/mattpocock/skills). Cherry-picked into this repo on 2026-05-15 and substantially extended on 2026-05-24 with scope-awareness, glossary inheritance, NOTES.md taxonomy, and a deterministic CONTEXT-MAP rebuilder.*
