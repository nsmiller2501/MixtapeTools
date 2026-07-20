# MixtapeTools Tracker

## Substrate

GitHub Issues is the authoritative work queue for this repository.

- One issue represents one actionable skill-development or repository-maintenance unit.
- Assignment claims an issue; open/closed records active/finished work.
- Issue and PR links carry continuity across chats, branches, and worktrees.

## Artifact Boundaries

- **GitHub Issues**: scope, acceptance checks, blockers, ownership, and remaining work.
- **Pull requests and commits**: implementation, validation, and review evidence; reference the issue when useful.
- **`agent_memory/`**: durable architecture, terminology, decisions, and deliberately deferred ideas.
- **`progress_logs/`**: optional, gitignored context for exploratory or integration sessions; never the authoritative queue.
- **Skill files and READMEs**: current behavior and user-facing documentation.

## Labels

Use only labels that support agent queries:

- `kind:skill` — behavior or documentation of a skill.
- `kind:infra` — repository tooling, packaging, or shared configuration.
- `state:ready` — sufficiently scoped for implementation.
- `state:blocked` — waiting on a decision, dependency, or external input.

Use GitHub's assignee and open/closed state instead of additional claim or completion labels.

## Lifecycle

1. Open an issue when work has a concrete outcome and observable acceptance check.
2. Apply one kind label and a state label when either will be queried.
3. Claim work by assignment before implementation.
4. Record material blockers on the issue and apply `state:blocked`.
5. Close with a resolution comment linking outputs and validation; close rejected or duplicate work with a short reason.

## Intake Bridge

Ideas remain in `agent_memory/deferred_ideas.md` or other notes until they have a title, source, concrete outcome, and observable acceptance check. Promotion creates an issue; the source note may retain a link but does not become a second task queue.
