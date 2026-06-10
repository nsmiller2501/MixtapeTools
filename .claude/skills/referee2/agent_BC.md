# Agents B/C: Independent Replicators

Read `code_role_context.md` first. You are one referee2 role subagent.
Do not spawn further subagents. Do not perform Agent 0, Agent A, or the other
replicator's work.

## Core Rule

Implement from the spec only. Never read original code. Expected outputs and
source outputs are sealed until your first-run script completes and first-run
outputs are saved.

## Pre-First-Run Access

- Restricted manifest
- Spec file
- Input data files listed as allowed
- Path-assignment config files only if the restricted manifest permits them

Do not read original code, source outputs, expected-output extracts or notes,
prior referee2 reports, override ledger, or full scope manifest before first-run
outputs are saved.

## First Run

1. Write the replication script from the spec only.
2. Run it.
3. Save first-run outputs.
4. Write the round-specific first-run lock file.
5. Only then open expected-output extracts and source outputs.

Lock file:

```markdown
correspondence/referee2/YYYY-MM-DD_roundN_<language>_first_run_lock.md
```

Contents:

```markdown
# Referee2 First-Run Lock

Language: <R|Python|Stata>
Round: YYYY-MM-DD_roundN
Spec path: <path>
First-run script path: <path>
First-run output path: <path>
Timestamp first-run output saved: <timestamp>
Expected outputs opened before first-run: no
Source outputs opened before first-run: no
```

If the first attempt fails before output creation, preserve the failed script and
a failure log, do not write a first-run lock, fix only referee-owned replication
code or environment-access artifacts, and try again without opening sealed
outputs.

Preserve first-run artifacts if you make diagnostic revisions.

## Artifact Names

Use `code/replication/referee2_replicate_<language>_first_run.<ext>` for
scripts and `code/replication/referee2_<language>_first_run_outputs.<csv|json>`
for outputs. Revised artifacts use the same pattern with `_revised`; revision
logs use `code/replication/referee2_<language>_revision_log.md`. Figures append
`_<figure_slug>.<ext>`; numeric backing outputs use `_data.csv` or `_data.json`.

## Compare

Compare substantive outputs, not formatting. Do not revise solely to match table
layout, labels, stars, decimal display, column order, LaTeX formatting, or file
naming.

For each discrepancy:

1. Classify it immediately.
2. Conjecture the specific source.
3. Test the conjecture where feasible.
4. Report with category tag and evidence.

| Category | What it means | What to do |
|---|---|---|
| `Substantive` | Different model, estimator, identifying variation, or target parameter | Real finding. Deep dive. Likely a bug in original or replication. |
| `Ancillary, specified in spec` | You implemented the spec contrary to sections 2/3/4 or other explicit instructions | Auditor error. Fix the replication and rerun if feasible. |
| `Ancillary, absent from spec` | You used a different default for something the spec did not pin down | Sensitivity finding, not a bug. Report the assumption and plausible alternative. |
| `Match` | Outputs match within numerical precision | Report as match. |

Revision logs classify changes as `spec misread`, `package default mismatch`,
`spec gap`, `original-code discrepancy`, or `numerical/formatting issue`.

For figures without stable numeric targets, make qualitative comparisons only
after first-run artifacts are saved, and label them qualitative.

## Return

- First-run script/output paths
- `Expected outputs opened after first-run outputs saved: yes/no`
- Optional revised script/output paths and revision log
- Triage table
