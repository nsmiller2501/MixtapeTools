# Local Research Tracker Template

Use this template for `agent_memory/research-tracker.md` when work stays in local markdown, or as a fallback section for hybrid repos.

~~~markdown
# Research Tracker

## Substrate

Work units live in local markdown.

- `plans/` holds specs, maps, and longform implementation plans.
- `agent_memory/tasklist.md` holds the current task index when no issue tracker is configured, or during transition to GitHub Issues.
- `progress_logs/` records session closeout and next steps.
- `meetings/` and `notes/` remain human-facing note surfaces, not authoritative task state.

## Artifact Boundaries

- **`plans/`**: durable specs/maps/ticket breakdowns.
- **`agent_memory/`**: durable project memory agents must consult: glossary, codebook, sample restrictions, key decisions, scoped context, and task index.
- **`meetings/`**: research meeting notes. Tasks may be harvested from `# Tasks` sections but remain untriaged until promoted.
- **`notes/`**: freeform notes, seminar comments, conceptual scratch, and untriaged ideas.
- **`progress_logs/`**: session closeout and next steps; link back to plans/tasks.
- **Commits / PRs**: code history and review surface.

## Local Ticket Format

Write ticket sets as `plans/<slug>_tickets.md`:

```markdown
# Tickets: <work name>

## Frontier

- [ ] <ticket title> — blocked by: none

## <Ticket title>

**Kind:** grilling | research | prototype | task | analysis
**Blocked by:** none | <ticket title>
**Done when:** <checkable completion criterion>

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Lifecycle

1. Capture ideas in notes freely.
2. Promote to `plans/` or `agent_memory/tasklist.md` only when the task has a title, source link, and either a decision question or acceptance criteria.
3. Grill unclear tasks before ticketing.
4. Work the frontier: any unchecked ticket whose blockers are done.
5. Mark complete only when the `Done when` criterion is satisfied.
6. Record session outcomes in `progress_logs/`.

## Markdown Task Bridge

A task from `meetings/` or `notes/` can become a local ticket only when it has:

- Title.
- Source note path or URL.
- Target project.
- One of: decision question, or acceptance criteria.
- Optional destination: `plans/` or `agent_memory/tasklist.md`.

Unclear note tasks stay in their source markdown file until clarified.
~~~
