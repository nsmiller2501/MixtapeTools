## Parent Reporting

This file is for parent aggregation and report filing after role subagents
return. Discrepancy classification belongs to `agent_BC.md`; preserve B/C's
category labels when aggregating.

### The Five Audits

Perform the five audits summarized in `code_role_context.md`:

1. Code Audit
2. Cross-Language Replication
3. Directory & Replication Package Audit
4. Output Automation Audit
5. Econometrics Audit

Use the scope calibration table in `code_role_context.md` to determine intensity.

### Critical Rule: NEVER Modify Author Code

You READ, RUN, and CREATE your own audit artifacts. You NEVER edit the author's code. Audit independence requires separation.

### Output
1. Spec file at `code/replication/YYYY-MM-DD_roundN_spec_<scope>.md` (written by Agent A)
2. Expected-output extraction file at `code/replication/YYYY-MM-DD_roundN_expected_outputs_<scope>.<csv|json>` plus `YYYY-MM-DD_roundN_expected_outputs_<scope>_notes.md` (written by Agent A)
3. Full scope manifest and restricted B/C manifest in `correspondence/referee2/`
4. Agent 0 findings at `correspondence/referee2/YYYY-MM-DD_roundN_agent0_findings.md`
5. First-run lock files at `correspondence/referee2/YYYY-MM-DD_roundN_<language>_first_run_lock.md`
6. Replication scripts in `code/replication/referee2_replicate_*.{R,do,py}` (written by Agents B and C)
7. Preserved first-run outputs, optional revised outputs, and revision logs
8. Comparison tables showing each replication's outputs vs. expected outputs
9. Discrepancy diagnoses with source classification (per the triage table)
10. Formal referee report in `correspondence/referee2/`

---

**Final report structure after completed B/C handoff:**

```markdown
## Spec
[Path to the seven-section spec; do not paste the full spec unless the user asked for inline detail]

## Substantive discrepancies (likely real findings)
[List with deep-dive diagnosis]

## Ancillary spec violations (replication errors)
[List — fix-and-rerun within this run if time permits, else flag]

## Sensitivity findings (results depend on assumptions absent from original code)
[List with: which spec section, what default I assumed, what alternative would do]

## Open questions for the user (cannot be resolved without input)
[List of spec gaps where my default may be wrong; user can resolve in a follow-up invocation]

## Other audit findings
[Code audit, directory audit, output automation audit, econometrics audit findings]
```

**Resolution loop.** After the parent aggregates role-subagent results, the parent surfaces the report to the user. If the user wants to resolve open questions, they update the code and/or provide spec answers, then re-invoke referee2 in the same parent session. New fresh role subagents run against the updated state. Per Step -1's "Iterative re-invocation" rule: new role-subagent prompts must NOT include the prior audit's findings — only the current code, current spec, and scope.

**Resume loop.** If a prior round stopped with `partial-audit-replication-blocked`, a later invocation may resume from the next missing role rather than rerun completed stages. If Agent 0 completed but Agent A did not, resume at Agent A. If Agent A completed but B/C did not, resume at B/C. The parent must ask the user before resuming and must verify unchanged source state using file paths and timestamps or hashes from the prior scope/spec artifacts. Resume prompts receive only the artifacts needed for the next role; they do not receive prior report narrative or the reason the handoff failed.

---

## Filing the Report

### Report Format
Use this formal referee report template:
- Summary
- Status: `passed`, `blocked-on-user-review`, `partial-audit-replication-blocked`, `proceeding-with-nonblocking-flags`, `human-figure-comparison-required`, or `failed-substantive-discrepancy`
- Status is the audit workflow state, not the substantive referee verdict.
- Findings by audit
- Major Concerns (must be addressed)
- Minor Concerns (should be addressed)
- Questions for Authors
- Verdict
- Verdict is the substantive referee judgment: Accept, Minor Revisions, Major Revisions, or Reject. If status is `blocked-on-user-review`, write `Verdict: Not reached`.
- Prioritized Recommendations

### File Locations
- Full scope manifest: `correspondence/referee2/YYYY-MM-DD_roundN_scope.md`
- Restricted B/C manifest: `correspondence/referee2/YYYY-MM-DD_roundN_restricted_manifest.md`
- Agent 0 findings: `correspondence/referee2/YYYY-MM-DD_roundN_agent0_findings.md`
- First-run lock files: `correspondence/referee2/YYYY-MM-DD_roundN_<language>_first_run_lock.md`
- Override ledger: `correspondence/referee2/referee2_overrides.md`
- Report: `correspondence/referee2/YYYY-MM-DD_roundN_report.md`
- Deck (if producing one): `correspondence/referee2/YYYY-MM-DD_roundN_deck.tex`
- Replication scripts: `code/replication/referee2_replicate_*.{R,do,py}`

If these directories don't exist, create them.

---

## Remember

The replication scripts you create are permanent artifacts. They prove the results were independently verified — or they prove they weren't. Either outcome is valuable. Do the work.
