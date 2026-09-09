---
name: adjudicate-state
description: Adjudicate one state of the county-heating digitization (1940 Table 28 or 1950 Table 27) end to end — gate-3 print verification, sidecar corrections, assemble, audit, commit, lesson file. Use when dispatched with a decade and state code, e.g. "1940 nm". Not for extraction; both fan-outs are complete.
---

# Adjudicate one state

`ARGUMENTS`: `<decade> <state>` — e.g. `1940 nm`, `1950 ma`.

You are a **per-state subagent** in the sequential loop described in Issue #64. You own exactly one
state. When you finish it you commit and return; you do not start another.

## Read first

From the worktree root
`/Users/noahmiller/Library/CloudStorage/Dropbox/02_research_projects/Redlining_HomeHeatingCooling_claude/.claude/worktrees/issue-9-county-heating`:

1. `code/data/county_heating_digitization/adjudication/MANUAL.md` — in full. Orientation, schema, identities, tooling, the loop, exit
   criteria, queue protocol.
2. `code/data/county_heating_digitization/adjudication/LESSONS.md` — in full. The operative rules, deduped.
3. `code/data/county_heating_digitization/adjudication/lessons/` — any file for a state worked recently in your decade. These are recent
   precedent and usually the most useful thing after the two above.

Do **not** read `plans/handoff_{1940,1950}_county_heat_production.md` cover to cover. They are
archive, ~24k and ~8k tokens, and everything operative in them is already in the two files above.
Grep them for a specific precedent when you want one.

## Hard constraints

Runs execute in bypass-permissions mode, so nothing else will stop you. `MANUAL.md` §1 is
authoritative; the four that bite hardest:

- **Renders only to `/private/tmp/<yr><st>/`.** Never inside the worktree — it once triggered a
  Dropbox sync storm that pegged the machine. Never a prefix another job might share.
- **Never edit an extract CSV.** Corrections go to `code/data/county_heating_digitization/agent_outputs/stage2_extracted/<yr>/<st>_manual_fixes.csv`.
  The sole exception is a county *name*, which a sidecar cannot express.
- **Never edit the four orchestrator-owned files** — `audit_county_units.py`,
  `notes/archive/county_heating_digitization/county_heat_extraction_rules.md`, `check_county_heat_extract.py`,
  `code/data/county_heating_digitization/adjudication/LESSONS.md`. Want a change? PROCESS queue, then continue.
- **`git add` by explicit path, never `-A`.** The worktree carries untracked `scratch/`, `tmp/`
  and staging files that must not be swept in.

## Your authority

**You may** fix any cell you have print-verified, and you should — that is the job.

**You may not** bank a NO-CHANGE, a misprint claim, or an "unreadable column." Those go on the
RULING queue and you move to the next column. Do not treat this as a formality to route around:
the project's running misprint score is **9 claimed, 3 real** (updated 2026-08-03), three columns banked as unclosable
were later read correctly in a single message, and one column banked with three no-changes had ten
wrong cells. Queueing costs nothing and blocks nobody.

If you find yourself writing "no reading can close this" — that sentence is a queue entry.

## Queue an item WITH its artifact, not just its description

**You are the only one who will ever have the column geometry cheaply.** You already know the
x-window, the band, and which printed column is which county. If you queue a residual without
those, the next reader rebuilds all of it from scratch — on 1940 NM that meant re-running `cols40`
and re-reading the `all_occ_units` row across both pages just to regenerate crops that already
existed under throwaway names.

So for **every** RULING entry, before you move on:

1. Render the column to a durable, named path:
   `data/intermediate/county_heating_digitization/adjudication_crops/<yr>_<st>/<NN>_<County>.png`, numbered in queue order, via
   `colread40`/`colread50` so each row carries its label and the extracted value. Add
   `<NN>b_<County>_<cell>.png` for any glyph you argued about, cropped beside its same-column
   references.
2. Record the **geometry** in the entry (x-window in points, band, column index) so it can be
   re-cut without rediscovery.
3. Keep working crops in `/private/tmp` — only these final review images go under
   `data/intermediate/county_heating_digitization/adjudication_crops/`, which is untracked, so they persist without entering git.

Then, once per state with a non-empty RULING queue, write
`code/data/county_heating_digitization/adjudication/rulings/<yr>_<st>_human_TEMPLATE.csv`: one row per variable per queued column, in the
sidecar's own schema (`state,pdf_page,county,column,extracted_value,corrected_value,reason`), with
`extracted_value` pre-filled **post-sidecar** and `corrected_value` blank. That is what the human
ruling is written into, and it means the ruling applies without transcription.

A queue entry whose image does not exist is not done.

## Loop

Follow `MANUAL.md` §6. The shape, per page:

1. `pdfimages -list` — native resolution. At 300–400 ppi expect the IoU controls to collapse and
   plan to decide cells on structure.
2. Column/row boundary detection. **Compare the count against the extract's row count.** A slip is
   invisible to every identity and this is the only check that sees it.
3. Confirm each rendered column by its printed `all_occ_units` before reading a disputed glyph.
4. **Sweep the whole page** against a printed dump of the extract — including pages with an empty
   queue. Most sum-preserving errors are found this way and nothing else finds them. A clean sweep
   is a result.
5. Re-cut every sweep hit on its own column before it goes in the sidecar. A strip locates
   disagreements; it never settles a glyph.

Then per queued column: arithmetic candidates → render at gate-3 resolution → the glyph test that
separates *that* pair → prefer the reading that closes the identity → or queue it.

**Append each verified correction to the sidecar immediately, not batched.** `triage{40,50}` applies
the sidecar exactly as the assembler does, so if you are killed mid-state the next agent inherits a
shorter queue and loses only your unwritten reasoning.

## Finish

1. Run the decade's exit criteria (`MANUAL.md` §7) and record the actual output. The orchestrator
   re-runs them, so a claim that does not survive re-running will be caught.
2. Commit **only** your own paths:
   ```
   <ST> <YR> county heating: adjudicated, N queued (#9)
   ```
3. Write `code/data/county_heating_digitization/adjudication/lessons/<yr>_<st>.md` from the template in `code/data/county_heating_digitization/adjudication/lessons/README.md`.
4. Update your row in `code/data/county_heating_digitization/adjudication/run_status.md` — `provisional (N queued)`, or `final` if the
   queue is empty.
5. Return a report: units, corrections and where they clustered, queue entries with one-line
   reasons, exit-criteria output verbatim, and any operative rule you think belongs in
   `LESSONS.md` (which you raise on the PROCESS queue, not by editing the file).

**Report honestly.** If an audit did not come back clean, say so and paste it. A provisional-close
design has no other way to see that.
