---
name: grilling
description: Shared relentless interview loop for plans and designs. Use when the user wants to stress-test a plan, says grill/grilling, or another planning skill needs a one-question-at-a-time decision interview.
---

# Grilling

Use this as the canonical interview loop for `grill-me`, `grill-with-docs`, `wayfinder`, and other planning skills.

## Loop

1. State the current assumption or decision branch in one sentence.
2. Ask exactly one question.
3. Give your recommended answer and the tradeoff behind it.
4. Wait for the user's answer before moving to the next branch.

Completion criterion: every live branch of the design tree is either resolved, explicitly deferred, or named as out of scope, and the user confirms shared understanding.

## Legwork

If a fact can be found by reading the repo, docs, tracker, or referenced artifacts, look it up instead of asking. Decisions belong to the user; facts are agent legwork.

## Boundary

Do not enact the plan during grilling. Stop when shared understanding is reached or when the user explicitly switches from grilling to writing, ticketing, or implementation.
