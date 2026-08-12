---
name: digitize-setup
description: Scaffold a table-digitization project — interview the user about their scanned tables, then generate the digitization substrate (MANUAL, queues, sidecar convention, tool scripts) that the extract and adjudicate phases run on.
disable-model-invocation: true
---

# Digitize setup — interview, then scaffold

`ARGUMENTS`: a path (or glob) to the source PDFs/images.

You are building the **substrate** a digitization project runs on. The deliverable is not
extraction code that works everywhere — it is a `digitization/` directory whose MANUAL a fresh
subagent can read and then work a unit without asking anything. Read
[`reference/architecture.md`](reference/architecture.md) first for the two-wave design the
substrate must serve.

## 1. Inventory the sources

1. List the source files; open two or three representative pages.
2. `pdfimages -list` on each distinct source — record **native resolution** per source. This
   number governs everything downstream (render dpi, whether IoU-style glyph measurement will
   hold, sweep tile density).
3. Draft the **page manifest**: one row per page carrying source file, page number, which unit
   of work it belongs to, and (if knowable) the expected count of records on it.

Done when: manifest drafted and native resolutions recorded for every distinct source.

## 2. Interview

One question at a time, in the style of `grilling` — each answer fills a MANUAL slot. Cover,
in order:

1. **Geometry.** What is a printed row, a printed column, a record? (Census Table 27 example:
   a county is a printed *column*; the schema variables are the *rows*; one county is one row
   of the extract CSV.) Confirm against an actual page, not the user's memory — the census
   project carried a wrong axis claim through five states.
2. **Schema.** The exact field list, in extract-CSV order, plus a `low_confidence_cells`
   self-flag field.
3. **Identities — the hard gate.** What arithmetic must hold within one record? Parts→totals,
   cross-panel reprints, derived percents. Push: a second printing of the same quantity
   anywhere on the page is an identity. If the table truly has none, the project runs in
   **spot-check mode** — a fixed random sample of records per unit is print-verified instead
   of triage-flagged columns — and the MANUAL says so on its first page. Wave 2's power comes
   from identities; without them the user should expect materially weaker QC.
4. **Unit of work.** The chunk one adjudicator owns end-to-end (a state, a year, a district).
   Sized so one subagent session can close it.
5. **Series.** If multiple table vintages exist (decades, editions), what differs between them
   — resolution, identity count, layout. One geometry per work session; the human's attention
   is the quality ceiling.
6. **External cross-checks.** Any independent digitization, published totals, or reference
   file (e.g. NHGIS county lists) that can audit unit counts or pin specific fields.
7. **Environment constraints.** Where renders may go (never inside a synced/watched
   directory), what is git-tracked, commit message convention.

Done when: every MANUAL slot has an answer the user has confirmed.

## 3. Generate the substrate

Create in the project root:

```
digitization/
  MANUAL.md            # from templates/MANUAL_TEMPLATE.md — fill every {{SLOT}}
  PRINT_READING.md     # copy of reference/print-reading.md, verbatim
  LESSONS.md           # header only: "Operative rules, deduped. Orchestrator-owned."
  lessons/README.md    # the per-unit lesson-file template (in MANUAL_TEMPLATE §9)
  queue_ruling.md      # header + entry format (in MANUAL_TEMPLATE §8)
  queue_process.md     # header: "Rule-level items. An OPEN entry stops the run."
  run_status.md        # one row per unit: unit | status | queued | notes
  rulings/             # empty; ruling CSV templates land here
```

Sidecar convention: extracts are immutable; corrections go to
`<extract-dir>/<unit>_manual_fixes.csv` with schema
`unit,page,record,field,extracted_value,corrected_value,reason`.

Done when: `grep -r '{{' digitization/` returns nothing.

## 4. Build the tools

Five roles, contracts in [`reference/tool-patterns.md`](reference/tool-patterns.md): manifest,
**triage** (applies the sidecar exactly as the assembler does, reports signed residuals per
identity), **assemble**, **audit**, **column-render**. Write them for *this* table's geometry;
the reference gives the invariants that were paid for with real errors (count gates, geometry
from printed rules not the text layer, full-column-width crops).

Done when: each tool runs against one sample page and its output is shown to the user.

## 5. Hand off

Report: the substrate paths, the manifest size, the identity list (or spot-check mode), and
the next command — `digitize-extract`. Offer to commit the substrate.
