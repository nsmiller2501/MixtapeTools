# CONTEXT.md Format

`CONTEXT.md` is a glossary. It defines the precise meaning of terms inside a given scope — nothing more. Methodology decisions go in `NOTES.md`. Project-wide hard-to-reverse decisions go in `agent_memory/docs/adr/`. This file is for **language**.

## Structure

```md
# {Scope Name}

{One or two sentences describing what this scope is and why it exists.}

## Language

**Analytic universe**:
The full set of units eligible to enter the main estimating sample before outcome availability or model-specific filters.
_Avoid_: sample, population

**Registry firm**:
A legal entity observed in the firm registry snapshot.
_Avoid_: company, establishment

**Exposure**:
The pre-period industry-share-weighted shock assigned to a firm.
_Avoid_: treatment, shock

## Relationships

- The **Analytic universe** contains zero or more **Registry firms**.
- Each **Registry firm** has at most one baseline **Exposure** in the main design.

## Example dialogue

> **Agent:** "Does **Exposure** mean observed firm imports or the shift-share measure?"
> **Researcher:** "Use **Exposure** only for the shift-share measure; observed imports are **trade flows**."

## Flagged ambiguities

- "sample" was used for both **Analytic universe** and the final estimating sample — resolved: these are distinct concepts.
```

## Rules for entries

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
- **Flag conflicts explicitly.** If a term is used ambiguously, call it out in "Flagged ambiguities" with a clear resolution.
- **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
- **Show relationships.** Use bold term names and express cardinality where obvious.
- **Only include terms specific to this scope's context.** General programming concepts (timeouts, error types) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this scope?
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.
- **Write an example dialogue.** A short conversation that demonstrates how the terms interact naturally and clarifies boundaries between related concepts.

## Glossary inheritance across nested scopes

When a session is scoped to a nested path like `acquire/firm_registry/`, multiple `CONTEXT.md` files apply at once:

```
agent_memory/CONTEXT.md                     ← project-wide glossary
agent_memory/acquire/CONTEXT.md             ← stage-wide glossary
agent_memory/acquire/firm_registry/CONTEXT.md   ← scope-local glossary
```

### Merge rules

At session entry, load the glossary in this order (shallowest → deepest):

1. `agent_memory/CONTEXT.md`
2. `agent_memory/<stage>/CONTEXT.md`
3. `agent_memory/<stage>/.../<current-scope>/CONTEXT.md`

For each term, **deepest wins** on conflict. The deeper scope's definition supersedes the shallower one for that scope's grilling session.

### Conflict surfacing — always

Whenever a term is defined at multiple levels with different meanings, surface the conflict **before grilling begins**:

> "Term **exposure** is defined at three levels:
> - root `CONTEXT.md`: import-weighted regional shock measure
> - `acquire/CONTEXT.md`: raw trade-flow exposure (no weighting)
> - `acquire/firm_registry/CONTEXT.md`: not defined
>
> The deepest definition (acquire) will govern this session unless you want to refine further. Override, align with root, or proceed?"

This is non-negotiable. Silent shadowing is the main failure mode of inheritance — surface every conflict, every time.

### Where new terms land

When a new term is resolved during grilling, write it to the **lowest scope where it's genuinely scope-specific**.

- If the term is project-wide ("Chinese firm" — used across acquire, build, analyze): write to root `CONTEXT.md`.
- If the term is stage-specific ("trade-flow exposure" — only used in acquire): write to `acquire/CONTEXT.md`.
- If the term is local to one module ("firm-registry snapshot date" — only matters for firm_registry): write to `acquire/firm_registry/CONTEXT.md`.

When in doubt, ask the user where the term lives. Default to the current scope (the deepest level being grilled) — it's easier to promote a term up the tree later than to clean up cross-contamination at root.

## Single-purpose mode

In single-purpose mode, the scope is `root`. All terms go to `agent_memory/CONTEXT.md`. No inheritance is involved (there is no parent). No `CONTEXT-MAP.md` is created. The file otherwise looks identical.
