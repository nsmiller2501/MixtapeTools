---
name: implement
description: Implement one approved research ticket, issue, or spec through code/data/output changes, validation, lightweight analysis review, and tracker handoff. Use when the user asks to implement a ready research task or GitHub issue.
---

# Implement

Execute one approved unit of research work. Do not use this to clarify vague work; send that to `grill-with-docs`, `to-spec`, `to-tickets`, or `wayfinder`.

## Process

1. Load the contract.
   Read `CLAUDE.md`, `agent_memory/research-tracker.md`, the source issue/spec/ticket, and relevant `agent_memory/` context. Completion: you can state the deliverable, validation criteria, out-of-scope items, and tracker update path.

2. Claim or confirm scope.
   If the work lives in GitHub Issues, claim it according to the tracker contract before editing. If no tracker exists, state the local source artifact. Completion: exactly one work unit is the session target.

3. Plan the validation first.
   Identify the checks that will prove the work: tests, Stata/R/Python assertions, row counts, merge cardinalities, rendered tables/figures, replication targets, or manual inspection. Completion: the validation list is concrete enough to fail.

4. Make the smallest implementation change.
   Edit only files needed for the ticket. Preserve existing pipeline shape unless the ticket requires changing it. Completion: every changed line traces to the work unit or its validation.

5. Run validation.
   Execute the narrow checks first, then broader pipeline checks when appropriate. Completion: each validation item is pass/fail/blocked with command or artifact evidence.

6. Run `analysis-review` when code or analysis artifacts changed.
   If the implementation touched Stata/R/Python code, data-build scripts, tables, figures, or exported research artifacts, the ticket is not complete until `analysis-review` signs off or records a blocker. Prefer a fresh-context subagent when available, giving it only the source work unit, changed files, relevant artifacts, and validation output. If no subagent is available, do a separate review pass yourself and label it as not independent. Completion: review findings are fixed, deferred with rationale, or recorded as blockers.

7. Handoff.
   Summarize changed artifacts, validation, review result, and remaining work. Update the tracker or leave a draft update for `session end` according to `agent_memory/research-tracker.md`.

## Commit Boundary

Commit only when the user asks, or when the repo's tracker/session contract explicitly requires commits at implementation end.
