# Referee 2 Code Mode

This file is the code-audit mode index. Load only the files needed for the current phase or role. Use `code_role_context.md` as the compact shared context for code-mode subagents; reserve `referee2.md` for full final-report context only when needed.

## Progressive Disclosure

For parent orchestration, read these files in order:

1. `code_tainted_session.md` — independence check, tainted-session catch, model overrides, path enumeration, and re-invocation rules.
2. `code_role_context.md` — compact code-audit stance, boundaries, scope calibration, audit areas, and evidence standard.
3. `code_reporting.md` — final audit outputs, aggregation rules, report format, and file locations.

For role subagents, load the narrowest set that covers the assigned role:

| Role | Required files |
|---|---|
| Agent 0 | `code_role_context.md`, `agent_0.md` |
| Agent A standalone spec writer | `code_role_context.md`, `agent_A_spec.md` |
| Agent A integrated extraction worker | `code_role_context.md`, `agent_A_extract.md` |
| Agent A integrated lead translator | `code_role_context.md`, `agent_A_lead.md` |
| Agent B/C | `code_role_context.md`, `agent_BC.md` |
| Parent final report aggregation | `code_role_context.md`, `code_reporting.md`; read `referee2.md` only if the local report template is insufficient |

If unsure which phase applies, read the files in the parent-orchestration order above. Do not skip `code_tainted_session.md` before any code audit work in the parent session.

## Files

- `code_tainted_session.md`
- `code_role_context.md`
- `agent_0.md`
- `agent_A_spec.md`
- `agent_A_extract.md`
- `agent_A_lead.md`
- `agent_BC.md`
- `code_reporting.md`
