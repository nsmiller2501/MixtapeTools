# Scope Resolution

How to determine the scope of a grilling session before grilling begins.

## Mode is just a special case of scope

There are two effective modes:

- **Single-purpose**: scope is `root`. All writes go to `agent_memory/CONTEXT.md` and `agent_memory/NOTES.md`. No nesting. No `CONTEXT-MAP.md` created.
- **Multi-scope (research)**: scope is a path like `acquire/firm_registry`. Writes go to `agent_memory/<scope-path>/CONTEXT.md` and `agent_memory/<scope-path>/NOTES.md`. `CONTEXT-MAP.md` is maintained.

Mode is not a separate flag — it falls out of the scope answer. "single-purpose" is just a special scope answer that means "root".

## When to ask

At session entry, decide which of these applies:

1. **User supplied a scope in their invocation** (e.g. "grill me on the firm-registry acquisition step"). Confirm and proceed: "scope: `acquire/firm_registry/` — sound right?"
2. **User used a single-purpose phrase** (e.g. "single-purpose", "single scope", "no nesting", "flat", "scope: root", "this whole repo", "we're scoping one thing"). Confirm and proceed in single-purpose mode.
3. **Repo looks single-purpose** (no `code/`, `data/`, `references/` dirs; small library/tool shape). Suggest single-purpose: "this looks like a single-purpose repo — scope the session to root, or pick a scope?"
4. **Repo has multi-stage research shape** (presence of `code/01_*`, `data/raw`, `data/build`, `references/`, etc.). Ask the question: "scope this session to: project-wide (root), [detected stages], single-purpose mode, or a new scope name?"
5. **Ambiguous / unclear**: ask the question above.

Never silently assume scope. The cost of asking once is small; the cost of polluting CONTEXT.md across unrelated work is large.

## Slug generation

When user names a new scope, generate a directory-safe slug and report it:

- Lowercase.
- Spaces → underscores.
- Strip punctuation except `_` and `/` (for nested paths).
- Preserve numeric prefixes if the user provides them (e.g. `01_acquire`).
- Match conventions from the existing tree when possible — if `agent_memory/02_build/` exists, suggest `03_analyze` rather than `analyze`.

Default behavior: generate the slug, report it, proceed. Do not block on confirmation. Example: "creating scope `acquire/firm_registry/` — proceeding. Ask to rename if you'd prefer something else."

## Descent protocol (mid-session nesting)

When grilling reveals that the conversation has narrowed to a sub-scope (e.g. user has been grilling on `acquire/`, but the discussion has narrowed to a specific dataset within acquisition), **ask before descending**:

> "this is narrowing to firm-registry specifics. Create sub-scope `acquire/firm_registry/`, or keep these entries at the `acquire/` level?"

Never auto-nest. The user is the only one who decides when to create a new directory.

Unbounded depth is allowed. `acquire/firm_registry/2020_snapshot/legal_form/` is fine if the user confirms each descent. The skill should not push back on depth — the user knows whether they need it.

## Single-purpose escape hatch

If a single-purpose session unexpectedly grows in scope, the user can promote to multi-scope mid-session:

> User: "actually, scope this to a `prep` stage — we'll have an `analysis` stage later."

In that case:

1. Confirm the scope name and slug.
2. Create `agent_memory/CONTEXT-MAP.md` (it didn't exist in single-purpose mode).
3. Move existing root-level writes (`agent_memory/CONTEXT.md`, `agent_memory/NOTES.md`) into the new scope directory if appropriate, or keep them at root if they represent project-wide content. Confirm with the user which entries belong where.
4. Run the map helper to register the new structure.

Do not auto-promote a single-purpose session into multi-scope based on repo shape alone. Respect the user's explicit choice unless they say otherwise.

## What scope means for writes

Once scope is locked:

- New glossary terms go to `agent_memory/<scope-path>/CONTEXT.md`.
- New methodology decisions and notes go to `agent_memory/<scope-path>/NOTES.md`.
- Project-wide ADRs (rare) still go to `agent_memory/docs/adr/` regardless of scope.
- Top-level cross-cutting files (`sample_restrictions.md` etc.) are **read** anytime topic touches them, but **written** only at the promotion step at grilling resolution.
