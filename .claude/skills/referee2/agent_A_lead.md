# Agent A: Integrated Lead Translator

Read `code_role_context.md` first. You are one referee2 role subagent.
Do not spawn further subagents. Do not perform Agent 0, B, or C work.

Use this role for integrated pipelines: runner/helper structures, staged data
flows, shared cleaning, shared derived data, or analysis units whose specs must
be made mutually consistent. The parent may give you original files directly or
extraction artifact paths from `agent_A_extract.md` workers.

## Read

- Full scope manifest
- Active override ledger, if present
- Original code, comments, configs, and source outputs listed in the manifest,
  unless extraction artifacts fully cover the assigned source files
- Per-script extraction artifacts if the parent used integrated fanout

The parent must pass extraction artifact paths directly. Do not rely on a
parent-written summary of extracted behavior.

## Task

Write one integrated replication spec and expected-output artifact set.

- Treat executable code behavior as authoritative.
- Make extraction artifacts talk to each other: data flow, order, shared
  variables, sample construction, path dependencies, and common outputs.
- Include only sanitized B/C-facing `REFEREE2_FLAG[...]` assumptions in the spec.
- Do not copy Agent 0 evidence, materiality rationale, user decision text,
  override ledger text, or full provenance narrative into the spec.
- Do not write, edit, run, debug, or compare R/Python/Stata replication scripts.
- Do not rerun author code to regenerate or refresh source outputs.
- Do not edit author code.

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

- `code/replication/YYYY-MM-DD_roundN_spec_<scope>.md`
- `code/replication/YYYY-MM-DD_roundN_expected_outputs_<scope>.csv` or `.json`
- `code/replication/YYYY-MM-DD_roundN_expected_outputs_<scope>_notes.md`

For table-like outputs, use columns where applicable:

```csv
output_id,model,term,statistic,value,unit,source_artifact,source_location,notes
```

The notes file must document source artifact(s), provenance, extraction choices,
stale-output concerns, and sealed-output instructions for B/C. Provenance should
state whether the existing artifact is treated as source of truth, whether rerun
was not requested, or whether a user-requested rerun matched/differed.

For figures with no stable numeric target, create a
`REFEREE2_FLAG[FIG-YYYY-MM-DD-###]` with tier `figure-human-comparison`.

## Return

- `spec=<path> outputs=<path(s)> notes=<path> ready_for_BC=yes`
- Input data paths B/C need
- Sealed source-output paths B/C may open only after first-run outputs are saved
