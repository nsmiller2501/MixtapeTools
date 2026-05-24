# ADR Format

ADRs are **project-wide, hard-to-reverse, surprising** decisions. They live at `agent_memory/docs/adr/` regardless of which scope was being grilled when the decision crystallised.

Scope-local methodology decisions go in that scope's `NOTES.md` (see [NOTES-FORMAT.md](./NOTES-FORMAT.md)), not in an ADR. The bar for an ADR is deliberately high — fewer, more meaningful records.

ADRs use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the `agent_memory/docs/adr/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan `agent_memory/docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

Plus a fourth criterion specific to multi-scope projects:

4. **Project-wide impact** — the decision affects work outside the current grilling scope. A decision that only governs the current scope belongs in that scope's `NOTES.md` as a `## Decision`, not an ADR.

If a scope-local decision later turns out to apply project-wide, it can be promoted to an ADR at the grilling-resolution promotion step.

### What qualifies (software projects)

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X."
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.**

### What qualifies (research projects)

- **Identification strategy** that governs the whole paper. "We use a Bartik-style shift-share instrument, not direct trade exposure."
- **Sample frame** at the project level. "The analytic universe is Chinese manufacturing firms with > 100 employees in the 2010 registry." (Specific cuts on top of this may be `NOTES.md` Decisions or `sample_restrictions.md` entries instead.)
- **Cross-stage methodology commitments.** "Variables are deflated to 2010 RMB throughout the project using the official PPI." If acquire, build, and analyze must all respect a rule, it's an ADR.
- **Data-source commitments** with downstream lock-in. "Customs data is the canonical source for trade flows; we never use UN Comtrade as a substitute."
- **Deliberate deviations from the obvious approach.** "We don't IV with tariffs because of measurement issues in the 2008-2009 window."

## Relationship to NOTES.md

- A `## Decision` in `NOTES.md` may include an optional `Refs:` line pointing at a relevant ADR.
- The reverse is not maintained: ADRs hold no list of scope NOTES that reference them.
- During grilling resolution, if a scope-local `## Decision` turns out to clear the ADR bar (project-wide, hard-to-reverse, surprising), it may be promoted to a new ADR. The original NOTES entry stays put as the scope's record; the ADR holds the canonical project-wide statement.
