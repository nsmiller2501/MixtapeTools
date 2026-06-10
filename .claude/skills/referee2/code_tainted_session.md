## Step -1: Tainted-session catch (run before anything else)

**Why this exists.** Referee2 only produces a credible audit if the auditing Claude has not previously touched the work being audited. A Claude that built a pipeline cannot objectively review its own choices. If you, the assistant currently reading this skill, have prior context in this session that touched the project being audited, your audit is contaminated before it begins.

**Detection.** Before doing any code-audit work, inspect this session's context. Treat the session as **tainted** if any of the following is true:

- You have read, edited, or run files in the project being audited earlier in this session
- You have substantively discussed the project's content (its data, code, results, identification, etc.) earlier in this session

**Casual or unrelated prior turns do NOT count as taint.** Greetings, off-topic questions, and work on a different project are fine. The threshold is "did prior work touch *this* project?" When in doubt, treat as tainted.

**If the session is tainted, present the user with this two-choice catch:**

> ⚠️ Referee2 requires a fresh session to produce a credible audit — Claude cannot objectively review work it has previously touched (see "Why they are separated" in referee2 docs).
>
> This session has prior context that may compromise audit independence. Two options:
>
> **(a) Subagents** — I keep this parent session only as orchestrator, then spawn fresh role-specific subagents for Agent 0, Agent A, and Agents B/C. Convenient (no session restart), but any unstated context from our earlier conversation will not reach the subagents.
>
> **(b) Cancel** — You start a brand new session and re-invoke `/referee2`. Highest fidelity, since you provide the full invocation in a clean context.
>
> Which? (a / b)

There is no "(c) proceed anyway" option. Proceeding in a tainted main session produces an invalid audit; the menu is bounded by what produces a valid one. If the user reasons in conversation that the prior context was unrelated and asks to proceed anyway, exercise judgment per the detection threshold above (B) — the catch fired because of judgment, and judgment can clear it.

### If the user picks (a) Subagents — parent orchestration

When the user picks subagents, you (the parent) do not delegate the whole referee2 protocol to one subagent. Subagents cannot be assumed to spawn other subagents. The parent stays in charge of orchestration and spawns each role-specific fresh subagent itself:

1. Discover and confirm the scope bundle. Default to audited entrypoints, sourced/imported code, configs, required inputs, and source-of-truth output artifacts. If the user narrows scope, honor and record that guardrail.
2. Check for resumable artifacts. Resume Agent A only when Agent 0 findings exist with no blockers and source state is unchanged. Resume B/C only when Agent A spec, expected outputs, notes, and restricted manifest exist and source state is unchanged. If source state changed, start a new round from Agent 0.
3. Write the full scope manifest for a new round at `correspondence/referee2/YYYY-MM-DD_roundN_scope.md`. Infer `roundN` from existing files for today's date. Include path, file size, modified time, and hashes where feasible for original code/config/source-output artifacts.
4. Read active overrides from `correspondence/referee2/referee2_overrides.md`, if it exists. Create the ledger lazily only when the first override is needed.
5. Spawn Agent 0 and wait for the gate result.
6. Gate only on material blockers. If Agent 0 finds uncovered blockers, stop for user review and use the blocking menu below. If it finds only nonblocking clarifications or documentation nits, proceed and pass relevant flag artifact paths to Agent A.
7. Spawn Agent A and wait for `ready_for_BC=yes`. For large multi-script projects, the parent may instead fan out bounded per-script Agent A extraction workers, then spawn a lead Agent A to synthesize their artifacts into the final spec and expected-output extracts. This fanout is parent-owned; per-script workers must not spawn subagents. The parent passes extraction artifact paths to the lead Agent A, not parent-written summaries.
8. Write the restricted B/C manifest at `correspondence/referee2/YYYY-MM-DD_roundN_restricted_manifest.md`, listing allowed pre-first-run files, sealed target paths, and prohibited files.
9. Verify B/C handoff availability. If B and C cannot run as separate isolated subagents, stop with `Status: partial-audit-replication-blocked` and preserve Agent A artifacts for later resume.
10. Spawn Agents B and C and wait for their triage results. If Agent A was fanned out, B/C should be fanned out on the same script or script-group units: each Agent A extraction unit gets one B replicator and one C replicator in the assigned replication languages.
11. Run output automation checks only if the user explicitly requested rerun/reproducibility checking. This is parent-owned diagnostic evidence, not Agent A work.
12. Aggregate role-subagent outputs and write the final report.

The discipline is still **transcription, not interpretation**. Quote verbatim. Do not paraphrase substantive project behavior in any role prompt.

#### Blocking menu and override ledger

If Agent 0 finds uncovered blockers, present this bounded menu and stop until
the user chooses:

```markdown
Agent 0 found blocking divergences. Referee2 cannot proceed to Agent A until each blocker is resolved or explicitly overridden.

For each blocker, choose one:
1. I will fix the code/comment outside referee2, then rerun.
2. Mark as intentional and add an active override.
3. Proceed with unresolved risk and add an active override.
4. Cancel the audit for now.
```

Option 1 stops referee2. The user fixes code/comments outside referee2 and
reruns.

Options 2 and 3 append entries to `correspondence/referee2/referee2_overrides.md`.
Override IDs use `REFEREE2_FLAG[OVR-YYYY-MM-DD-###]`; choose the next unused
number for the date. Overrides are always user-decided and agent-entered: draft
and append the ledger entry only after the user explicitly chooses an override
for a specific Agent 0 blocker.

Ledger template:

```markdown
# Referee2 Override Ledger

If source code/comments are later changed so an override no longer applies, mark the entry `Status: retired` and explain the retirement reason. Agents read only active overrides for blocking decisions.

## REFEREE2_FLAG[OVR-YYYY-MM-DD-001]
Status: active
Tier: blocking-user-overridden | blocking-unresolved-user-proceed
Date created: YYYY-MM-DD
Date retired:
Created from finding: REFEREE2_FLAG[A0-YYYY-MM-DD-###]
Scope path: <path>
Issue fingerprint: <short stable description>
User decision: <verbatim or concise user decision>
Do not block if: <condition under which this override still applies>
Still block if: <condition under which this override no longer applies>
Spec flag required: yes
```

Agent 0 reads active overrides to avoid re-blocking adjudicated issues. Agent A
reads active overrides only to encode localized `REFEREE2_FLAG[...]` assumptions
in the spec. Agents B and C never read the override ledger.

#### Subagent model defaults and user overrides

The parent session's model is already fixed when the user invokes the skill; the skill cannot downgrade or upgrade the parent. It can choose model tiers only when spawning role subagents, subject to the host tool's available model names.

Default subagent model tiers and effort:

| Role | Default model tier / effort | Rationale |
|---|---|---|
| Agent 0 | frontier reasoning model, adaptive effort (`low`, `medium`, or `high`) | Materiality judgments, econometric stakes, comment/code divergence, and scope ambiguity are high-risk; the parent should choose effort from structural risk signals before spawning Agent 0. |
| Agent A, single lead translator | frontier reasoning model, `medium` effort | Full-pipeline compression into a prose/math spec is high-risk when one agent handles the whole scope. |
| Per-script Agent A extraction workers | frontier reasoning model, `low` effort | Bounded script transcription is mostly extraction; the lead Agent A owns synthesis. |
| Agents B/C | frontier/coding-capable model, `low` effort | Replication work needs coding reliability and bounded reasoning, usually with lower marginal value from higher effort. |

Agent 0 adaptive effort rule:

- Use `low` for small, clear, single-file/script audits.
- Use `medium` for ordinary referee2 code audits.
- Use `high` for multi-script scopes, stale-output risk, comment/code ambiguity, unclear scope, or high-stakes empirical claims.

The parent should make this choice from structural signals only: scope size, language count, output-artifact state, invocation ambiguity, and similar metadata. Do not pre-audit substantive code behavior in the parent session.

Respect explicit user effort choices. The user may add optional flags to the `/referee2` invocation:

```text
--Agent0=<low|medium|high>
--AgentA=<low|medium|high>
--AgentA-script=<low|medium|high>
--BC=<low|medium|high>
--parallel
```

`--BC=<low|medium|high>` applies to both B and C. B and C exist only to run different replication languages, so they use the same effort selection. User effort overrides are allowed even when the parent would choose a higher default. If the user requests a specific concrete model in the natural-language invocation, respect it when the host supports that model unambiguously; otherwise, keep the role's default model tier and apply the requested effort.

By default, parent-owned fanout runs sequentially: complete one per-script Agent A worker before starting the next, and complete each B/C replication unit before starting the next unit. This avoids spending large amounts of tokens on multiple one-shot subagents that may all fail if the user hits a usage cap mid-stage. If the user supplies `--parallel`, the parent may run same-stage fanout workers concurrently when the host supports it. `--parallel` does not change the isolation rule: each subagent still gets only its assigned role context and must not spawn further subagents.

If the requested effort or concrete model is unavailable, tell the user which role cannot use it and fall back to the nearest available option in the same tier. Do not silently ignore user choices.

Role-subagent prompt header template:

```
You are running one role in the referee2 protocol in a fresh subagent context.
The parent session is orchestrating the protocol. You must not spawn further
subagents.

The user invoked this skill via:

  User invocation (verbatim):
  > /referee2 <args>

  User's invocation message (verbatim, if anything beyond the bare command):
  > <full message text>

Mode: <deck|code>
Target: <absolute path to file or directory>
Role: <Agent 0|Agent A|Agent B|Agent C>

Read ~/.claude/skills/referee2/code.md first, then read only the code-mode
files listed there for your assigned role. Use code_role_context.md for shared
stance and audit boundaries. Execute your assigned role only.
Do not assume any prior context. The user's verbatim text above plus the
manifest/spec paths supplied by the parent are your only specification.
```

#### Path enumeration (when the user's invocation is vague)

If the user's invocation is not a precise path (e.g., "audit everything we worked on this session," "the new code," empty target), do NOT skip enumeration and let the role subagents flounder. Enumerate concrete paths from this session's tool history, then **confirm with the user before spawning Agent 0:**

> I'll audit these files with fresh referee2 subagents (enumerated from this session's tool use):
>
> ```
> /path/to/a.do
> /path/to/b.R
> /path/to/c.py
> ```
>
> Add, remove, or proceed?

After user confirms, include the confirmed list in the full scope manifest or Agent 0 prompt under a `Session-enumerated audit scope` heading.

**Hard rule for enumeration: paths only, no narrative.** Do NOT include "this script does X," "we use Y approach," or any editorialization. Path strings are objective transcription; everything else is interpretation that contaminates the subagent's independence. If the user's invocation IS a precise path already, skip enumeration entirely — they've specified scope.

### If the user picks (b) Cancel

Tell the user: "Understood — start a new terminal session and re-invoke `/referee2 <args>` there for the cleanest audit." Do not proceed.

### Iterative re-invocation in the same parent session

After a role-subagent run completes and the user addresses findings (updates code, fills spec gaps), the user may re-invoke referee2 in the same parent session for a second audit. This is fine — each role subagent is fresh by virtue of being a subagent, regardless of how many prior subagents the parent has spawned. The independence requirement is about the *auditor*, not the user-Claude collaboration.

**However:** when constructing the prompt for a follow-up role subagent, **NEVER include prior-audit findings in the prompt** unless the role is explicitly resuming from a prior artifact path. Each subagent audits the current state on its own terms — pass current code + current spec + scope, never prior-audit narrative. Two reasons:

- **Anchoring:** the new subagent would look for the same problems and possibly miss new ones
- **Confirmation:** the new subagent might rationalize that previous findings were "addressed" without independently verifying

Same discipline as path enumeration: transcribe the current state, never the audit history.

---
