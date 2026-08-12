---
name: digitize-unit
description: Adjudicate one unit of a digitization project end to end — print verification, sidecar corrections, assemble, audit, commit, lesson file. Use when dispatched by digitize-adjudicate with a unit id. Not for extraction; wave 1 is complete before this runs.
---

# Adjudicate one unit

`ARGUMENTS`: `<unit>` — e.g. `1940 nm`, `district-7`.

You are a **per-unit subagent** in the sequential wave-2 loop. You own exactly one unit.
When you finish it you commit and return; you do not start another.

## Read first

From the project root:

1. `digitization/MANUAL.md` — in full. Orientation, schema, identities, tooling, the loop,
   exit criteria, queue protocol. **§1's hard constraints are authoritative** — runs may
   execute unattended, so nothing else will stop you.
2. `digitization/PRINT_READING.md` — in full. The glyph and measurement epistemology.
3. `digitization/LESSONS.md` — in full. This project's operative rules, deduped.
4. `digitization/lessons/` — any file for a unit worked recently in your series. Recent
   precedent, usually the most useful thing after the three above.

Archived planning documents are archive: grep them for a specific precedent when you want
one; do not read them cover to cover.

## Your authority

**You may** fix any cell you have print-verified, and you should — that is the job.

**You may not** bank a NO-CHANGE, a misprint claim, or an "unreadable record"
(PRINT_READING §3, §9). Those go on the RULING queue and you move to the next record. Do not
treat this as a formality to route around: on the project this system comes from, misprints
ran 9 claimed / 3 real, three records banked as unclosable were later read correctly in a
single message, and one record banked with three no-changes had ten wrong cells. Queueing
costs nothing and blocks nobody.

If you find yourself writing "no reading can close this" — that sentence is a queue entry.

## Queue an item WITH its artifact

**You are the only one who will ever have the geometry cheaply.** Follow MANUAL §8 for every
RULING entry before you move on: render the record to its durable numbered path with labels
and extracted values attached, record the geometry so it can be re-cut without rediscovery,
and — once per unit with a non-empty queue — emit the ruling template CSV. A queue entry
whose image does not exist is not done.

## Loop

Follow MANUAL §6. The shape, per page: native resolution first; boundary counts against the
extract (the only check that sees a record slip); confirm every rendered record by its
anchor field; **sweep the whole page** — including pages with an empty queue, because
sum-preserving errors are found no other way and a clean sweep is a result; re-cut every
sweep hit on its own record before it goes in the sidecar.

Then per flagged record: arithmetic candidates → render at adjudication resolution → the
test that separates *that* pair → prefer the reading that closes the identity → or queue it.

**Append each verified correction to the sidecar immediately, not batched.** Triage applies
the sidecar exactly as the assembler does, so if you are killed mid-unit the next agent
inherits a shorter queue and loses only your unwritten reasoning.

## Finish

1. Run the exit criteria (MANUAL §7) and record the actual output. The orchestrator re-runs
   them, so a claim that does not survive re-running will be caught.
2. Commit **only** your own paths, in the MANUAL's commit format.
3. Write `digitization/lessons/<unit>.md` per MANUAL §9.
4. Update your row in `digitization/run_status.md` — `provisional (N queued)`, or `final`
   if the queue is empty.
5. Return a report: records checked, corrections and where they clustered, queue entries
   with one-line reasons, exit-criteria output verbatim, and any operative rule you think
   belongs in `LESSONS.md` — raised on the PROCESS queue, not by editing the file.

**Report honestly.** If an audit did not come back clean, say so and paste it. A
provisional-close design has no other way to see that.
