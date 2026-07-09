---
name: wayfinder
description: Plan a multi-session research effort as a shared map of decision tickets. Use when the work is too large or foggy for one session and needs a durable frontier before implementation.
disable-model-invocation: true
---

# Wayfinder

Wayfinding finds the route to a destination. It produces decisions and a frontier, not implementation, unless the map notes explicitly say otherwise.

## Tracker Contract

Read `CLAUDE.md` and `agent_memory/research-tracker.md` first. The tracker contract decides whether maps and tickets live in GitHub Issues or local markdown, which labels to use, how to claim work, and how to express blocking edges.

If no tracker contract exists, stop and ask whether to run `setup-researcher-skills` before charting.

## Map Shape

A map is the durable parent artifact for the effort.

```markdown
## Destination

<what is clear or complete when this map is done>

## Notes

<standing context, skills to consult, project constraints>

## Decisions So Far

- [<closed ticket title>](link-or-path) - <one-line gist>

## Not Yet Specified

<in-scope fog that cannot be ticketed precisely yet>

## Out Of Scope

<nearby work ruled outside this destination>
```

## Ticket Types

- `kind:grilling`: HITL decision interview using `grilling` or `grill-with-docs`.
- `kind:research`: AFK investigation of docs, code, data, or literature.
- `kind:prototype`: concrete sketch, toy analysis, simulation, or outline to react to.
- `kind:analysis`: empirical analysis, robustness check, figure, or table.
- `kind:task`: mechanical/manual work needed to unblock a decision.

## Chart A Map

1. Use `grilling` and, when project memory should change, `grill-with-docs` to name the destination. Completion: the user confirms what the map is finding its way to.
2. Map the first frontier breadth-first. Completion: each ticketable question is sharp, and remaining fog stays in `Not Yet Specified`.
3. Create or draft the map according to the tracker contract. Completion: the map has destination, notes, fog, out-of-scope, and no duplicated ticket detail.
4. Create or draft tickets in dependency order, then wire blocking edges. Completion: unblocked, unclaimed frontier work is visible in the tracker.
5. Stop. Charting and resolving tickets are separate sessions.

## Work Through A Map

Resolve at most one ticket per session.

1. Load the map, then choose the named ticket or the first unblocked, unclaimed frontier ticket.
2. Claim the ticket according to the tracker contract before work starts.
3. Resolve it with the skill named by its type. Completion: the ticket's decision or artifact is complete and linked.
4. Record the resolution in the ticket, close it, and append one context pointer to `Decisions So Far`.
5. Graduate newly-sharp fog into tickets, update blockers, and move newly out-of-scope work to `Out Of Scope`.
