# The two-wave architecture — what the substrate must serve

Every design choice below was bought with a real failure in the 1940/1950 census
county-heating digitization. The substrate you generate exists to enforce them.

## Readers are blind

Wave-1 readers transcribe what is printed. Their prompts carry the schema, the page, and
transcription rules — **never the identities, never any arithmetic relationship, never an
instruction to check that anything adds up.**

The evidence: a 1940 re-extraction pass was given the four identities plus an explicit
anti-fabrication clause and told to re-zoom failing columns. Identity failures collapsed from
45/72 to 9/72 — by fabrication. Adjudication against the print found whole columns rewritten
into internal consistency: one county's wood-heating count moved 3985→995 with gas moved
49→2985, a row shift satisfying all four identities that would have put 2,985 gas-heated units
in a 1940 rural county. The anti-fabrication clause was present verbatim and did not survive
being placed next to an arithmetic target.

**Identities are wave 2's QC instrument, never a reader's instruction.** The same logic bounds
adjudicators: arithmetic ranks the queue; only the print settles a cell.

## Adjudication is sequential

One unit at a time. Parallel wave-2 fan-out multiplies the actual failure mode (agents
confidently *closing* things they got wrong), destroys the accretive property that lets each
unit's lessons teach the next, and a usage limit mid-wave loses every in-flight unit at once.
Wave 1 parallelizes freely — readers are blind and independent, and a lost reader costs one
page, not a unit's judgment.

## The human is the quality ceiling

Adjudicators may fix what they have print-verified. They may **not** bank a NO-CHANGE, a
misprint claim, or an "unreadable column" — the census record on exactly those judgments:
misprints ran 9 claimed / 3 real; three columns banked as unclosable were read correctly by
the human in one message; one column banked with three no-changes had ten wrong cells.

Two queues carry everything an agent cannot settle:

- **RULING** — cell-level, needs the human's eye on one column. Never blocks the run.
- **PROCESS** — rule-level: a new error shape, a change to an orchestrator-owned file, a
  judgment call about the substrate itself. **An OPEN entry stops the run** — everything
  worked after it would be adjudicated under a rule the human has not seen.

A small set of files is **orchestrator-owned** (the audit script, LESSONS.md, the extraction
rules): subagents propose changes on the PROCESS queue and never edit them.

## Work is durable and provisional

Corrections append to a **sidecar** immediately, never batched — a subagent killed mid-unit
leaves the next one a shorter queue. Extracts are never edited. Units close *provisionally*
(commit + lesson file + run_status row); the queue file, not git history, is the authority on
finished. A **new error shape** records retro-sweep debt: which already-closed units predate
it and are in principle suspect.
