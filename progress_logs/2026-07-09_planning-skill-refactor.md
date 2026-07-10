# Planning Skill Refactor

## Summary

Adapted the Matt Pocock planning cluster into a research-economist workflow centered on `agent_memory/`, GitHub Issues as the preferred durable tracker, and lightweight empirical validation.

Ported/adapted:

- `grilling`: shared one-question-at-a-time interview loop.
- `grill-me`: thin wrapper around `grilling`.
- `grill-with-docs`: keeps existing scoped `agent_memory/` writes, now reuses `grilling` and reads the tracker contract.
- `domain-modeling`: research terminology and durable decision updates under `agent_memory/`.
- `research-triage`: low-context bridge from `agent_memory/tasklist.md` or user-named notes into specs/tickets/issues; `--first-run` is the only broad scan mode.
- `to-spec`, `to-tickets`, `wayfinder`: research-native planning flow using `agent_memory/research-tracker.md`.
- `session`: issue-aware start/end lifecycle while preserving local progress logs.
- `implement`: one approved issue/spec/ticket through implementation, validation, review, and tracker handoff.
- `analysis-review`: lightweight Stata/R/Python empirical review gate before closing implementation work.

Skipped/superseded:

- Upstream `research`: overlaps with `read-pdf`, `wiki-update`, `bib-update`, `bibcheck`, and project reference wiki flow.
- Upstream `triage`: superseded by `research-triage` for local-note intake and `session` for issue-aware lifecycle.
- Upstream `tdd` and `code-review`: adapted into `analysis-review`; empirical pipelines need validation gates more than SWE-style unit-test ceremony.
- Upstream `diagnosing-bugs`: keep as HITL prompting for now; repeated empirical pipeline diagnosis can become a later `analysis-diagnose` skill if needed.
- Upstream `resolving-merge-conflicts`: not a recurring coauthor workflow; current pain is branch/worktree hygiene.
- Upstream `ask-matt`, `setup-matt-pocock-skills`, `codebase-design`, `improve-codebase-architecture`: not needed for this research workflow after the adapted planning stack.

Kept in staging:

- `prototype`: possible future port for synthetic data, estimator sketches, toy timing examples, fake merge scenarios, or table/figure mockups. Do not port until repeated concrete use appears.

## Decisions

- GitHub Issues should become the implementation surface: an agent takes a ready issue, works on the appropriate branch, validates, runs `analysis-review`, commits when appropriate, and updates/closes the issue through `session end`.
- Only one agent should work on a given project's worktree at a time for now. Spread agents across projects instead.
- If branch/worktree collisions become common, revisit `implement` to require per-issue worktrees and an explicit merge-back protocol.
- Commit early and often before starting agent work; messy merge-conflict recovery is a symptom of branch hygiene, not a workflow to optimize prematurely.

## Next Steps

- [ ] Try the GitHub-Issues implementation flow on one research project.
- [ ] Revisit `prototype` only after a second concrete need for toy data, estimator sketching, or synthetic pipeline testing.
- [ ] Consider a worktree/branch hygiene patch to `implement` only if multiple agents per project become useful.

## Completed Tasks

- [x] Added research-native planning, triage, implementation, and review skills.
- [x] Added issue-aware session lifecycle.
- [x] Decided not to port upstream triage/research/debug/merge-conflict skills for now.

## Key Files

.claude/skills/research-triage/SKILL.md:1-90
.claude/skills/implement/SKILL.md:1-40
.claude/skills/analysis-review/SKILL.md:1-60
.claude/skills/session/SKILL.md:1-35
.claude/skills-staging/mattpocock-v1.1/prototype/SKILL.md:1-80
