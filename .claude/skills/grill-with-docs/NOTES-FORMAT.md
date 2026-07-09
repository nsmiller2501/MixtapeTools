# NOTES.md Format

`NOTES.md` lives alongside `CONTEXT.md` at each scope and holds **methodology** content — decisions, observations, open questions — for that scope. It is the ADR-light artifact: more permissive than an ADR (no "three criteria"), more durable than a chat transcript.

`CONTEXT.md` is a glossary. `NOTES.md` is everything else this scope needs future agents to know.

## Structure

```md
# Notes — {Scope Name}

## Decision: use Bartik-style exposure instrument

We're constructing exposure as $z_i = \sum_k s_{ik} \cdot g_k$ where $s_{ik}$ is firm $i$'s lagged industry share and $g_k$ is the national-level shock for industry $k$.

Alternative considered: direct trade-flow exposure at the firm level. Rejected because firm-level trade data has high measurement error pre-2010 and the lagged-shares construction inherits the exogeneity argument from the canonical literature.

Refs: [ADR-0003](../../../docs/adr/0003-instrument-strategy.md)

## Decision: drop firms with no entry in the registry snapshot

Firms appearing in customs records but absent from the 2010 firm registry are dropped. This affects ~3% of customs-recorded firms. The rationale is that the registry is the source of truth for the firm's existence at our analysis window — customs entries without registry backing are likely measurement artifacts or pre-incorporation activity.

## Note: registry snapshot date is end-of-2010

The registry snapshot we have is dated 2010-12-31. We assume firms present in that snapshot existed for at least Q4 2010. This is good enough for our analytical window (2011-2015) but would need re-examination for any pre-2010 work.

## Note: open question — how to handle firm-name changes across years?

Some firms appear under slightly different legal names in 2011 vs 2014. We have not decided how to deduplicate. Possible approaches: fuzzy match on name + tax ID, manual review of large firms, drop ambiguous matches. Defer to data-quality session.
```

## Entry types

Use one of two heading styles:

### `## Decision: ...`

A methodology commitment that downstream work will rely on. Examples: choice of instrument, sample restriction, identification strategy, variable construction, deduplication rule.

Body: 1–3 paragraphs. State the decision, the rationale, and the alternative(s) considered.

### `## Note: ...`

Lighter than a decision. Open questions, observations, contextual flags, "things to revisit", explanations of state that aren't a commitment yet.

Body: 1–2 paragraphs. State the note. If it's an open question, say what would resolve it.

Use `## Decision` when the user has committed. Use `## Note` when they haven't, or when the content is observational rather than a commitment.

## Optional references

A `## Decision` may end with a one-line reference to a related project-wide ADR:

```
Refs: [ADR-0003](../../../docs/adr/0003-instrument-strategy.md)
```

Rules:

- **Optional.** Only add when there's a genuinely related ADR.
- **One direction only.** `NOTES.md` may reference an ADR. ADRs hold no back-references to NOTES.
- **LLM-suggested, user-confirmed.** When writing a Decision, scan `agent_memory/docs/adr/` for slugs that look topically related. If one matches, ask the user before adding the ref.
- **Not maintained.** If an ADR renames or moves, the link rots. Accepted cost — the alternative is a graph maintenance burden that drifts anyway.
- **Relative paths**, computed from the scope's depth. The skill should write the correct relative path based on `<scope>/NOTES.md` → `agent_memory/docs/adr/<file>.md`.

`## Note` entries should not include `Refs:`. Notes are not commitments and shouldn't pretend to be linked to an ADR.

## Rules

- **Append-only by default.** Don't rewrite existing decisions during grilling — if a prior decision is being revised, add a new `## Decision` and reference the supersession in the body. Future readers benefit from seeing how thinking evolved.
- **One entry per decision.** Don't bundle multiple decisions into one heading. Each should be greppable on its own.
- **Use the scope's language.** Term names in `## Decision` bodies should match the merged glossary for that scope. If you need to introduce a new term, define it in `CONTEXT.md` first, then use it in `NOTES.md`.
- **Promotion candidates.** When you write a `## Decision` that seems to apply outside the current scope, flag it mentally as a promotion candidate for the grilling-resolution phase (see CROSS-CUTTING.md).

## Where NOTES.md lives

Every scope can have its own `NOTES.md`:

```
agent_memory/NOTES.md                              ← project-wide (rare)
agent_memory/acquire/NOTES.md                      ← stage-level
agent_memory/acquire/firm_registry/NOTES.md        ← scope-local
```

Created lazily — only when the first `## Decision` or `## Note` is being written to that scope. Empty `NOTES.md` files should not exist.
