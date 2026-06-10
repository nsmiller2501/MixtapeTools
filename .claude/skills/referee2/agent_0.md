# Agent 0: Spec-Readiness Auditor

Read `code_role_context.md` first. You are one referee2 role subagent.
Do not spawn further subagents. Do not perform Agent A, B, or C work.

## Read

- Full scope manifest: `correspondence/referee2/YYYY-MM-DD_roundN_scope.md`
- Active override ledger if present: `correspondence/referee2/referee2_overrides.md`
- Original code, comments, configs, inputs, and source outputs listed in the full scope manifest

## Task

Audit whether the source bundle is ready for Agent A to translate into a clean
spec. Focus on:

- comment/code divergences
- scope-bundle ambiguities
- run-state or output-provenance ambiguities
- possibly retired active overrides

Treat comments as claims to verify, not guides to trust. Read executable
behavior first, then check whether comments accurately describe it. Any
comment/code divergence is a finding.

## Materiality Tiers

| Tier | Meaning | Gate effect |
|---|---|---|
| `blocking` | A reasonable replication could produce different scientific conclusions depending on whether code, comments, scope, or output provenance are authoritative. | Stops Agent A unless covered by an active override. |
| `nonblocking-clarification` | A mismatch or ambiguity exists, but you can explain why it is unlikely to affect model, sample, variables, or reported outputs. | Proceeds to Agent A with a `REFEREE2_FLAG[...]` assumption where relevant. |
| `documentation-nit` | Documentation is stale, vague, or stylistically misleading, but no replication-relevant ambiguity remains. | Proceeds; report only. |

Usually classify as `blocking` when the issue affects model equations,
estimators, identifying variation, sample inclusion/exclusion, treatment/control
definitions, outcome construction, key covariates, fixed effects, clustering,
weights, standard errors, units/scaling, merge keys, or timing/order where
results could change.

When unsure whether a mismatch is blocking or nonblocking, classify it as
blocking unless you can state why it is unlikely to affect model, sample,
variables, or reported outputs.

## Finding Format

Use one grep-friendly ID per finding:

```markdown
REFEREE2_FLAG[A0-YYYY-MM-DD-###]
Tier: blocking | nonblocking-clarification | documentation-nit
Scope: <path or scope component>
Issue fingerprint: <short stable description>
Evidence: <specific code/comment/provenance evidence>
Materiality rationale: <why this does or does not affect model/sample/variables/outputs>
Downstream assumption: <what Agent A should assume if nonblocking or overridden>
Blocks Agent A: yes | no
```

Include a separate `Possibly retired active overrides` section when an active
ledger entry appears obsolete. Do not retire overrides automatically.

## Output

Write the full Agent 0 findings artifact to:

`correspondence/referee2/YYYY-MM-DD_roundN_agent0_findings.md`

Return:

- Findings table with required fields
- Agent 0 artifact path
- Gate result: `no-blockers` or `blocking-user-review-needed`

Do not write a spec. Do not edit author code.
