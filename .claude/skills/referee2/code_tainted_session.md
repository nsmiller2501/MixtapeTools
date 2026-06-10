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

1. Parent performs path enumeration/scope confirmation using only paths, not project narrative.
2. Parent writes or reuses the full scope manifest and reads active override ledger state.
3. Parent spawns Agent 0 and waits for the gate result.
4. If Agent 0 blocks, parent reports blockers to the user and stops.
5. If Agent 0 does not block, parent spawns Agent A and waits for `ready_for_BC=yes`. For large multi-script projects, the parent may instead fan out bounded per-script Agent A extraction workers, then spawn or retain a lead Agent A to synthesize their artifacts into the final spec and expected-output extracts. This fanout is parent-owned; per-script workers must not spawn subagents. The parent passes extraction artifact paths to the lead Agent A, not parent-written summaries of those artifacts.
6. Parent writes the restricted B/C manifest.
7. Parent spawns Agents B and C and waits for their triage results. By default, fanout subagents run sequentially to reduce usage-cap risk; if the user supplied `--parallel`, the parent may run same-stage fanout subagents in parallel. If the parent used Agent A fanout, B/C should be fanned out on the same script or script-group units: each Agent A extraction unit gets one B replicator and one C replicator in the assigned replication languages.
8. Parent aggregates role-subagent reports and writes the final report.

The discipline is still **transcription, not interpretation**. Quote verbatim. Do not paraphrase substantive project behavior in any role prompt.

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
