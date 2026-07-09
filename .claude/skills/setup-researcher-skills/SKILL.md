---
name: setup-researcher-skills
description: "Configure a research repo for researcher-oriented planning skills: tracker substrate, labels, artifact boundaries, and agent-memory conventions. Use before adapting or running research planning skills such as grill-with-docs, to-spec, to-tickets, wayfinder, triage, or implement."
---

# Setup Researcher Skills

Create the per-repo contract that research planning skills read before writing specs, tickets, maps, progress logs, or project memory.

This is prompt-driven setup. Explore first, propose defaults, confirm, then write. Do not configure GitHub, create labels, or migrate tasks unless the user explicitly asks.

## Process

### 1. Explore

Read the repo before asking:

- `git remote -v`, `.git/config`, whether `gh` is authenticated, existing GitHub issues (`gh issue list --state all`), and existing labels (`gh label list`).
- `CLAUDE.md`. Project repos use this as the single source of truth; do not create or maintain `AGENTS.md`.
- `agent_memory/`, especially `CONTEXT-MAP.md`, `tasklist.md`, `key_decisions.md`, `codebook.md`, and `sample_restrictions.md`.
- `progress_logs/`, `plans/`, `meetings/`, `notes/`, and existing issue/PR references in commits.
- Existing `agent_memory/research-tracker.md` or prior tracker convention docs.

Outcome: a short summary of the current substrate and the missing convention pieces.

### 2. Resolve Decisions

Resolve these decisions. If the repo evidence makes the defaults obvious, present the recommended set together and ask for one confirmation. If any answer is unclear or high-impact, ask that decision by itself and wait.

1. **Tracker substrate** — GitHub Issues, local markdown, or hybrid. Default to GitHub Issues when the repo has a GitHub remote and the user is open to issue tracking; otherwise hybrid local markdown.
2. **Artifact boundaries** — define what belongs in GitHub Issues, `meetings/`, `notes/`, `agent_memory/`, `plans/`, `progress_logs/`, and commits/PRs.
3. **Labels and issue types** — choose the minimal vocabulary for research work. Prefer labels only where agents will query them.
4. **Issue lifecycle** — define what makes an issue ready, claimed, blocked, complete, or closed without action.
5. **Markdown task bridge** — if the user has note/todo aggregation, define the minimum fields required before a task from `meetings/` or `notes/` becomes an issue.

### 3. Draft

Show the user the exact edits before writing:

- The `## Agent skills` block for `CLAUDE.md`.
- The complete `agent_memory/research-tracker.md` body.

Use the bundled [github-research-tracker.md](./agent_memory/templates/github-research-tracker.md) template when GitHub Issues is the substrate. Use the bundled [local-research-tracker.md](./agent_memory/templates/local-research-tracker.md) template for local or hybrid markdown.

Do not summarize the tracker doc in place of showing it. Stop after the draft and ask for explicit permission to write.

### 4. Write

Only write after the user confirms the draft or says to proceed.

Edit the root instruction file:

- If `CLAUDE.md` exists, edit it.
- If `CLAUDE.md` does not exist, ask before creating it.
- Do not create `AGENTS.md`; Codex is configured to read `CLAUDE.md` when `AGENTS.md` is absent.

Add or update one `## Agent skills` block. Do not duplicate the block and do not disturb unrelated project instructions.

Write `agent_memory/research-tracker.md`. Keep it concise and operational; downstream skills should be able to answer "where do I write this?" and "what state is this work in?" without asking.

### 5. Verify

Check:

- `CLAUDE.md` points to `agent_memory/research-tracker.md`.
- The tracker doc names the substrate, artifact boundaries, labels/types, lifecycle, and markdown task bridge.
- No task migration happened unless explicitly requested.

Report the created/updated paths and the chosen substrate.
