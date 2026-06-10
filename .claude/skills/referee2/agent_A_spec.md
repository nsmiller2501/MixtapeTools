# Agent A: Standalone Spec Writer

Read `code_role_context.md` first. You are one referee2 role subagent.
Do not spawn further subagents. Do not perform Agent 0, B, or C work.

Use this role for one standalone analysis unit: a single script, entrypoint, or
independent script group that can be specified without a cross-unit synthesis
agent.

## Read

- Full scope manifest, restricted to your assigned unit when applicable
- Active override ledger, if present
- Original code, comments, configs, and source outputs for your assigned unit

## Task

Write a complete replication spec and expected-output artifacts for your unit.

- Treat executable code behavior as authoritative.
- Use comments for labels and interpretation only after verifying behavior.
- Include only sanitized B/C-facing `REFEREE2_FLAG[...]` assumptions in the spec.
- Do not copy Agent 0 evidence, materiality rationale, user decision text,
  override ledger text, or full provenance narrative into the spec.
- Do not write, edit, run, debug, or compare R/Python/Stata replication scripts.
- Do not rerun author code to regenerate or refresh source outputs.
- Do not edit author code.

If you discover your unit depends on another analysis unit in a way that changes
model, sample, variables, or outputs, stop and return `requires_lead_A=yes` with
the dependency path(s). Do not write a partial spec for B/C.

## Spec Rules

The spec is prose for substance plus math notation for models. Do not use
pseudo-code. The spec must declare input data paths, not source-output paths.
Output artifact paths belong in sealed comparison instructions.

The spec must contain:

- `Input data`: paths, unit of observation, required variables
- `REFEREE2_FLAG assumptions for replication`: implementation-relevant flags only
- `1. Model`: math notation, regressors, fixed effects, SE type, clustering
- `2. Sample construction`: universe, eligibility, exclusions, drop rules
- `3. Data dictionary and units`: variable roles, units/scales, ranges/support
- `4. Variable construction`: transformations, recodes, derived variables, order
- `5. Missingness and edge-case handling`: missingness, logs, ties, panel gaps
- `6. Target parameter`: estimand and plain-English interpretation
- `7. Identification`: identifying assumption, with equation where useful

If original code is silent on missingness, sample edge cases, or variable
construction defaults, write `ORIGINAL CODE SILENT`, pick a defensible default,
and document it. Do not refuse to proceed because of a gap.

## Expected Outputs

Existing output artifacts are the source of truth by default. Extract structured
expected outputs from existing tables, figures, result files, or numeric backing
files. Do not regenerate author outputs.

Write:

- `code/replication/YYYY-MM-DD_roundN_spec_<unit>.md`
- `code/replication/YYYY-MM-DD_roundN_expected_outputs_<unit>.csv` or `.json`
- `code/replication/YYYY-MM-DD_roundN_expected_outputs_<unit>_notes.md`

For table-like outputs, use columns where applicable:

```csv
output_id,model,term,statistic,value,unit,source_artifact,source_location,notes
```

For figures with no stable numeric target, create a
`REFEREE2_FLAG[FIG-YYYY-MM-DD-###]` with tier `figure-human-comparison`.

## Return

- `spec=<path> outputs=<path(s)> notes=<path> ready_for_BC=yes`
- or `requires_lead_A=yes dependencies=<path(s)>`
- Input data paths B/C need
- Sealed source-output paths B/C may open only after first-run outputs are saved
