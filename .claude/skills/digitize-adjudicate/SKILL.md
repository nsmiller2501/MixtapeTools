---
name: digitize-adjudicate
description: Wave 2 of the digitization workflow — drive the sequential per-unit adjudication loop: dispatch one digitize-unit subagent at a time, verify its exit criteria independently, manage the RULING and PROCESS queues, stop on a PROCESS item.
disable-model-invocation: true
---

# Digitize adjudicate — the orchestrator

You drive the wave-2 loop. You dispatch **one unit at a time**, in sequence. You do not
adjudicate cells yourself.

Work from the project root; `digitization/MANUAL.md` is the substrate authority.

## Why sequential

Parallel fan-out multiplies the project's actual failure mode (agents confidently *closing*
things they got wrong), destroys the accretive property that lets each unit's lessons teach
the next, and a usage limit mid-wave loses every in-flight unit at once. **Do not "optimize"
this back to parallel** — wave 1 was the parallel phase, because readers are blind and a lost
reader costs one page, not a unit's judgment.

## Start of run

1. Read `digitization/run_status.md` — the authority on what is finished. Git history is
   not; units commit *provisionally*.
2. **Check `queue_process.md` for OPEN entries. If any exist, do not dispatch.** Report them
   to the user and stop.
3. Check `queue_ruling.md` for `RULED` entries. If any exist, run the re-open pass (below)
   before dispatching new units.
4. Pick the next unit from `run_status.md`'s ordering (MANUAL §10). Re-run triage first —
   recorded failure counts are a planning number, not a contract.

## Dispatch

One subagent per unit, via the `digitize-unit` skill with the unit id. Run it in the
background and continue when it completes.

## On each report — verify, do not believe

**Re-run the exit criteria (MANUAL §7) yourself.** They are cheap and machine-checkable by
design, and an agent that has just spent a long session reading degraded glyphs is exactly
the one most likely to report "audit clean" from memory. If something does not reproduce,
fix it or re-dispatch that unit — do not proceed past it.

Then:

- Fold the report's queue entries into the right queue if the subagent has not.
- Update `run_status.md`.
- Apply requested changes to the **orchestrator-owned files** (MANUAL §1) — but only for
  items the user has **ruled** on. An unruled request is a PROCESS entry, and PROCESS
  entries stop the run.
- A **new error shape** gets retro-sweep debt recorded in `run_status.md`: which
  already-closed units predate it.

## Stopping

Stop when units or budget are exhausted, **or** a PROCESS item lands — whichever comes
first. Everything worked after an unruled PROCESS item would be adjudicated under a rule the
user has not seen, so finishing the current unit and stopping is correct even with budget
remaining.

On stop, report: units closed this run, total corrections, RULING queue depth, any PROCESS
item and why it stopped things, and what the next unit would be.

## The re-open pass

After the user rules on RULING entries, one subagent handles all affected units in a batch —
no re-reading, only applying rulings.

**The normal input is a filled-in ruling CSV**, `digitization/rulings/<unit>_human.csv`, in
the sidecar's own schema — applying it is an append of the rows whose `corrected_value` is
non-empty, not a transcription. Check it first:

- Every row's key must match a real extract row, or it is a typo — the assembler reports
  unmatched sidecar rows and that is an error, not a no-op.
- A row whose `corrected_value` equals its `extracted_value` is a **confirmation**, not a
  change. Record it as a documented no-change — it is evidence the cell was read, which is
  exactly what a future sweep wants to know.
- Run triage before and after, so the residual movement is visible and reported.

Per affected unit: append to the sidecar → re-assemble → re-audit (and any external
cross-check) → commit → set queue entries to `APPLIED` → set the unit to `final` in
`run_status.md` if nothing is left OPEN.

**If a ruling contradicts a cell the subagent recorded as print-verified, that is a signal,
not an exception.** Confident single-glyph calls on degraded print have been simply wrong,
repeatedly. Note it in the unit's lesson file — it is the highest-value line in that file.
