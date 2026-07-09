---
name: to-spec
description: Turn the current conversation into a research spec without more interviewing. Use when the user asks to write a spec, research design, analysis plan, or PRD from already-resolved context.
disable-model-invocation: true
---

# To Spec

Synthesize what is already known. Do not interview unless a missing fact makes the spec unsafe to publish.

## Process

1. Read `CLAUDE.md` and `agent_memory/research-tracker.md` if present. Completion: you know where specs live and whether GitHub Issues or local markdown is the substrate.
2. Read relevant `agent_memory/CONTEXT.md`, scoped `CONTEXT.md`, `NOTES.md`, ADRs, and any referenced plan/issue. Completion: the spec uses the project's terms and respects recorded decisions.
3. Draft the spec below. Completion: every section is filled or explicitly marked "None".
4. Publish according to the tracker contract. For GitHub Issues, draft first and ask before creating or updating issues unless the user explicitly asked you to publish. For local markdown, write where `agent_memory/research-tracker.md` says specs belong.

## Research Spec Template

```markdown
# <Spec Title>

## Research Objective

What this work is trying to learn, decide, estimate, or produce.

## Design / Specification

The identification strategy, empirical design, model, or system design at the right level of detail.

## Data Inputs

Required datasets, source notes, units of observation, joins, filters, timing, and known caveats.

## Output Artifacts

Tables, figures, datasets, notes, code paths, or issue links this work should produce.

## Implementation Decisions

Committed choices about modules, interfaces, workflow, schemas, estimators, or analysis steps. Avoid brittle file paths unless the path is itself the artifact.

## Validation Criteria

How success will be checked: tests, row-count invariants, balance checks, replication targets, figure/table review, CI, or manual inspection.

## Out Of Scope

Nearby work intentionally excluded.

## Further Notes

Open questions, risks, references, and follow-up hooks.
```
