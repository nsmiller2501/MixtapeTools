---
name: analysis-review
description: Lightweight independent review of Stata, R, Python, and research pipeline changes for empirical errors before closing a ticket. Use after implementing analysis work, before issue closure, or when the user asks for a focused research code review.
---

# Analysis Review

Review empirical code and outputs for research errors. This is the lightweight tier; use `referee2 code` for full independent replication or high-stakes final audits.

## Independence

Prefer a fresh-context subagent when available. Give it only:

- the source issue/spec/ticket
- changed files or diff
- relevant `agent_memory/` context
- commands run and validation output
- produced tables, figures, logs, or datasets needed for review

Do not pass the implementing agent's rationale except where it is part of the ticket or recorded decision. If no subagent is available, run the review as a separate pass and state that it was not independent.

## Review Checklist

Find concrete defects, not stylistic preferences.

- **Scope match**: change satisfies the ticket/spec and does not add unrequested analysis.
- **Sample integrity**: filters, exclusions, missingness, panel balance, and units of observation match the stated design.
- **Merge integrity**: join keys, duplicate handling, unmatched observations, and many-to-many merges are explicit and checked.
- **Timing**: treatment, exposure, controls, and outcomes use the intended periods and avoid look-ahead.
- **Variable construction**: transformations, winsorization, deflation, logs, weights, and denominators match `CONTEXT.md`, `NOTES.md`, specs, or ADRs.
- **Estimation**: fixed effects, clustering, weights, standard errors, and sample restrictions match the stated empirical design.
- **Output truthfulness**: tables, figures, and exported datasets reflect the code just run; labels and notes do not overclaim.
- **Reproducibility**: commands run from a clean checkout/session with documented dependencies, seeds, paths, and generated artifacts.
- **Language-specific hazards**: Stata globals/macros and sort order; R factor levels and recycling; Python index alignment, dtype coercion, and chained assignment.

## Output

Lead with findings ordered by severity. Use file paths and line numbers when available.

For each finding:

```markdown
- [severity] <title> — <file:line>
  Evidence: <what proves the problem>
  Impact: <how it can change the analysis>
  Fix: <minimal corrective action>
```

If no issues are found, say so and list residual risk: checks not run, artifacts not inspected, or assumptions inherited from the ticket.

## Boundary With Referee2

Use this skill for ordinary ticket closure. Escalate to `referee2 code` when the user wants independent replication, cross-language audit, or a cold-read review of a completed empirical pipeline.
