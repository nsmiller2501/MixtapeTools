# GitHub Research Tracker Template

Use this template for `agent_memory/research-tracker.md` when GitHub Issues is the work tracker.

```markdown
# Research Tracker

## Substrate

Work units live in GitHub Issues for this repository.

- Parent issues represent specs, maps, or multi-session research efforts.
- Sub-issues represent concrete tickets sized for one focused session.
- Native issue dependencies represent blocking edges.
- `meetings/` and `notes/` remain human-facing note surfaces, not the durable work queue.
- `agent_memory/tasklist.md` and `progress_logs/` checkboxes are intake/history surfaces during transition, not a second tracker.

## Artifact Boundaries

- **GitHub Issues**: actionable work, specs/maps, tickets, blockers, claims, and completion discussion.
- **`meetings/`**: research meeting notes. Tasks may be harvested from `# Tasks` sections but remain untriaged until promoted.
- **`notes/`**: freeform notes, seminar comments, conceptual scratch, and untriaged ideas.
- **`agent_memory/`**: durable project memory agents must consult: glossary, codebook, sample restrictions, key decisions, scoped context, and current task index if still used.
- **`plans/`**: longform specs or implementation plans when an issue body is too small; link from the issue.
- **`progress_logs/`**: session closeout and next steps; may reference issues but should not replace them.
- **Commits / PRs**: code history and review surface; reference issues in commit messages when useful.

## Labels

Use the smallest queryable vocabulary that downstream skills need.

- `kind:map` — multi-session wayfinding effort.
- `kind:spec` — parent spec or research design.
- `kind:ticket` — executable child issue.
- `kind:grilling` — HITL decision interview.
- `kind:research` — AFK source/code/data investigation.
- `kind:prototype` — toy data, simulation, outline, or concrete sketch.
- `kind:task` — mechanical/manual work.
- `kind:analysis` — executable empirical analysis, robustness check, figure, or table.
- `state:needs-grilling` — human decision needed before ticketing or implementation.
- `state:ready-for-agent` — agent can pick up without more human context.
- `state:ready-for-human` — needs human action or judgment.
- `state:blocked` — has an unresolved dependency.
- `state:wontfix` — closed without action.

## Lifecycle

1. Capture ideas in notes freely.
2. Promote to an issue only when it has a title, source link, and either a decision question or acceptance criteria.
3. Grill unclear issues before ticketing.
4. Break approved specs/maps into sub-issues with blocking edges.
5. Claim an issue by assignment before starting.
6. Close with a short resolution comment linking outputs, commits, tables, figures, plans, or progress logs.

## Markdown Task Bridge

A task from `meetings/`, `notes/`, `progress_logs/`, or `agent_memory/tasklist.md` can become a GitHub Issue only when it has:

- Title.
- Source note path or URL.
- Target repo.
- One of: `state:needs-grilling` question, or acceptance criteria.
- Optional suggested labels.

Unclear note tasks stay in their source markdown file until clarified.
```
