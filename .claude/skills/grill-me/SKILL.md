---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

# Grill Me

Use [`grilling`](../grilling/SKILL.md) as the interview loop.

This wrapper is for plain plan/design stress tests that do not need scoped `agent_memory/` writes. If the user wants the project glossary, notes, ADRs, or tracker updated as decisions crystallise, switch to `grill-with-docs`.
