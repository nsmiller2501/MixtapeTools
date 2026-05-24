# Cross-Cutting Files

Cross-cutting files are project-wide `.md` files at the top of `agent_memory/` that hold decisions which apply across many scopes. They are **not** owned by this skill — the user creates and curates them — but this skill reads them, references them during grilling, and offers to promote scope-local NOTES into them at grilling resolution.

## Common cross-cutting files

These are conventional in research projects. The skill does not require any of them to exist; it discovers whichever ones are present.

| File | Holds |
|------|-------|
| `sample_restrictions.md` | Sample inclusion/exclusion rules — what's in the analysis, what's dropped, why |
| `key_decisions.md` | Project-level methodology decisions worth foregrounding |
| `codebook.md` | Variable definitions, units, coding conventions |
| `dropped_analyses.md` | Approaches that were tried and abandoned, with reasons |

Projects may have others (e.g. `data_sources.md`, `identification.md`). Any top-level `.md` file in `agent_memory/` other than `CONTEXT.md`, `NOTES.md`, and `CONTEXT-MAP.md` is treated as cross-cutting.

## Discovery

The Python helper script `scripts/build-context-map.py` walks `agent_memory/` and registers all top-level cross-cutting files in `CONTEXT-MAP.md`. The skill does **not** re-scan on every invocation — discovery happens at:

1. CONTEXT-MAP creation (first time the script runs in this project).
2. CONTEXT-MAP refresh (any time the script is invoked).

When the skill reads `CONTEXT-MAP.md` at session start, it learns the cross-cutting file list from the map. If the user mentions a cross-cutting topic and no relevant file is registered, the skill can prompt the user to scan / create one, but should not silently create.

## Read freely

Whenever the grilling touches a topic that a known cross-cutting file covers (sample, codebook, etc.), the skill reads that file before forming questions. Example:

> User: "we'll restrict to firms with > 100 employees."
> Skill: [reads `sample_restrictions.md` first] "your sample_restrictions.md already excludes firms with < 50 employees. Tightening to > 100 — confirm, or are these two different cuts?"

Read access is cheap and discipline-preserving. Use it.

## Write only at promotion

Top-level cross-cutting files are **not** written to mid-session. Decisions made during grilling land in the scope's `NOTES.md` first. At grilling resolution, the skill walks back through this session's `NOTES.md` entries and nominates candidates for promotion.

### Promotion criteria

A `NOTES.md` entry is a candidate for promotion when:

- It applies outside the current scope (other stages or pipeline-wide).
- It modifies a rule that downstream code will need to respect (sample, variable definition, key methodology).
- The user would expect a future agent to discover it when reading top-level docs.

### Promotion protocol

At grilling resolution:

1. List nominated entries: "these scope NOTES look cross-cutting — promote any of them?"

   ```
   [1] acquire/firm_registry/NOTES.md  ## Decision: drop firms with no registry record
       → candidate for sample_restrictions.md
   [2] acquire/firm_registry/NOTES.md  ## Decision: use customs_id as join key
       → candidate for key_decisions.md (or new data_sources.md?)
   ```

2. User confirms each individually. Skip, promote, or rename target.
3. On promotion: append the entry to the target file. Do **not** remove from the scope `NOTES.md` — the scope retains a record, and the top-level file holds the canonical version. If desired, the scope entry can reference the cross-cutting file: `Promoted to: ../../sample_restrictions.md` on a final line.
4. After promotions, rerun the helper script to refresh CONTEXT-MAP.md (in case promotion created a new top-level file).

### Never auto-route

Do not silently write to top-level cross-cutting files. Even at promotion time, every write requires user confirmation. The cost of a wrong write here is high — these files are the project's foreground decisions, and noise pollutes them.
