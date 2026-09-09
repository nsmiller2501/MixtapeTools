---
name: adjudicate-run
description: Drive the sequential per-state adjudication loop for the county-heating digitization (Issue #64) — dispatch one state subagent at a time, verify its exit criteria independently, manage the RULING and PROCESS queues, and stop on a PROCESS item. Use when asked to start, resume, or continue an adjudication run.
---

# Adjudication run — the orchestrator

You drive the loop described in Issue #64. You dispatch **one state at a time**, in sequence. You
do not adjudicate cells yourself.

Work from
`/Users/noahmiller/Library/CloudStorage/Dropbox/02_research_projects/Redlining_HomeHeatingCooling_claude/.claude/worktrees/issue-9-county-heating`.

## Why sequential

Parallel fan-out was considered and rejected. It multiplies the project's actual failure mode
(agents confidently *closing* things they got wrong), it destroys the accretive property that let
each state's lessons teach the next, and a usage limit mid-wave loses every in-flight state at
once. **Do not "optimize" this back to parallel.** If it seems obviously faster, read Issue #64.

## Start of run

1. Read `code/data/county_heating_digitization/adjudication/run_status.md` — the authority on what is finished. Git history is not; a
   state commits *provisionally*.
2. **Check `code/data/county_heating_digitization/adjudication/queue_process.md` for OPEN entries. If any exist, do not dispatch.**
   Report them to Noah and stop.
3. Check `code/data/county_heating_digitization/adjudication/queue_ruling.md` for `RULED` entries. If any exist, run the re-open pass
   (below) before dispatching new states.
4. Pick the next state from `run_status.md`'s ordering. Re-run `triage40.py -q` (or `triage50.py`)
   first — the recorded failure counts are a planning number, not a contract.

## Dispatch

One subagent per state, via the `adjudicate-state` skill with `<decade> <state>`. Run it in the
background and continue when it completes.

Ordering is **1940's remaining 16 → 1950 pathfinder → 1950's 42**, ascending by identity-failure
count within each. The reason for keeping decades separate is that Noah's adjudication attention is
the scarce resource, and mixing Table 28 (counties as rows, 1200 dpi, four identities) with
Table 27 (counties as columns, 800 dpi, six identities) in one morning is a context-switch tax on
the human — who is the quality ceiling here.

## On each report — verify, do not believe

**Re-run the exit criteria yourself.** They are all cheap and machine-checkable, and an agent that
has just spent a long session reading degraded glyphs is exactly the one most likely to report
"audit clean" from memory.

1940: `triage40.py <st>` · `assemble_1940.py <st>` · `audit_county_units.py 1940` · PA final
byte-identical.
1950: `triage50.py <st>` · `assemble_1950.py <st>` · `audit_county_units.py 1950` ·
`crosscheck_gwee_tan.py 1950 <st>`.

If something does not reproduce, fix it or re-dispatch that state — do not proceed past it.

Then:

- Fold the report's queue entries into the right queue if the subagent has not.
- Update `run_status.md`.
- Apply any change the subagent requested to the four **orchestrator-owned** files
  (`audit_county_units.py`, `notes/archive/county_heating_digitization/county_heat_extraction_rules.md`,
  `check_county_heat_extract.py`, `code/data/county_heating_digitization/adjudication/LESSONS.md`) — but only for items Noah has
  **ruled** on. An unruled request is a PROCESS entry, and PROCESS entries stop the run.
- A **new error shape** must get retro-sweep debt recorded in `run_status.md`: which already-closed
  states predate it.

## Stopping

Stop when states or budget are exhausted, **or** a PROCESS item lands — whichever comes first.
Everything worked after an unruled PROCESS item would be adjudicated under a rule Noah has not
seen, so finishing the current state and stopping is correct even if budget remains.

On stop, report: states closed this run, total corrections, RULING queue depth, any PROCESS item
and why it stopped things, and what the next state would be.

## The re-open pass

After Noah rules on RULING entries, one subagent can handle all affected states in a batch — no
re-reading is required, only applying rulings.

**The normal input is a filled-in ruling CSV**, `code/data/county_heating_digitization/adjudication/rulings/<yr>_<st>_human.csv`, in the
sidecar's own schema — so applying it is an append of the rows whose `corrected_value` is
non-empty, not a transcription. Check it before hand-editing anything:

- Every row's `(county, pdf_page, column)` must match a real extract row, or it is a typo — the
  assembler reports unmatched sidecar rows and you should treat that as an error, not a no-op.
- A row whose `corrected_value` equals its `extracted_value` is a **confirmation**, not a change.
  Record it as a documented no-change rather than dropping it silently; it is evidence the cell was
  read, which is exactly what a future sweep wants to know.
- Re-run `triage{40,50}` before and after so the residual movement is visible and reported.

Per affected state: append to `<st>_manual_fixes.csv` → re-run `assemble_*.py` → re-run the audit
(and the Gwee & Tan cross-check for 1950) → commit → set the queue entries to `APPLIED` → set the
state to `final` in `run_status.md` if nothing is left OPEN.

**If a ruling contradicts a cell the subagent recorded as print-verified, that is a signal, not an
exception.** It has happened repeatedly that a confident single-glyph call on a 300 ppi column was
simply wrong. When it does, note it in the state's lesson file — it is the highest-value line in
that file.

## Notes

- Both fan-outs are complete. **Never re-dispatch a page that already has an extract** — it spends
  budget re-buying data we own. There is **no outstanding reader dispatch in the ticket**: 1940
  OH p138's extract was committed in `b9cff90` and verified on disk 2026-08-03.
- Subagents commit their own state, so their work is durable the moment they finish, independent of
  whether you survive to receive the report. Do not take commit ownership back.
- Deferred sub-tasks, not part of the main loop: DC in both decades (Table 12, not 27/28).
