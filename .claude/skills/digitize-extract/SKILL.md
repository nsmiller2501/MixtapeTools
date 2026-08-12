---
name: digitize-extract
description: Wave 1 of the digitization workflow — fan blind reader subagents out over the page manifest until every page has a committed extract. Completeness checks only.
disable-model-invocation: true
---

# Digitize extract — the blind fan-out

You orchestrate wave 1. Readers transcribe; you track completeness. All quality judgment
belongs to wave 2 — a reader's job is to be cheap and blind, not careful.

Work from the project root; `digitization/MANUAL.md` §2 names the paths.

## The blindness rule

**A reader's prompt contains the schema, the page, and the transcription rules below —
nothing else.** In particular it never contains the identities, any arithmetic relationship
between fields, or any instruction to check that values add up. A reader given an arithmetic
target satisfies it by fabrication (MANUAL §4 records the case: an explicit anti-fabrication
clause did not survive being placed next to the target). If you are ever tempted to add a
consistency hint to fix a noisy reader, that noise is exactly what wave 2 exists to
adjudicate — dispatch the page as-is.

## Dispatch

Readers are independent, so parallel fan-out is fine — batch to whatever the machine and
budget bear. One reader per manifest page. Prompt template:

```
Digitize page <N> of <source file> into CSV.

Schema (one row per <record>): <field list>
Layout: <records are printed as columns/rows; where the record labels sit — from MANUAL §2,
geometry only, no arithmetic>

Rules:
- Transcribe exactly what is printed. A dash, dots, or blank cell is a valid reading —
  record it as <project's zero/missing convention>.
- Where you are unsure of a glyph, give your best reading and list the cell in
  low_confidence_cells. An honest flag is worth more than a confident guess.
- Write to <extract path for this page>. Commit with message "<convention>".
```

Readers commit their own pages — work is durable the moment a reader finishes, independent
of whether you survive to collect the report.

## Completeness checks — the only checks

After each batch:

1. Every manifest page has an extract file on disk (check the repository, not your notes).
2. Each extract's record count matches the manifest's expected count where one exists.
   A mismatch means a re-dispatch of that page with the discrepancy named — the reader may
   have missed a continuation column or picked up a stray sub-column. It does not mean the
   values are wrong; you cannot see that and are not trying to.
3. The extract parses: right columns, right order, one row per record.

Anything about *values* — identity failures, suspicious cells, low-confidence flags — is
wave-2 material. Record nothing about it beyond what the extracts themselves carry.

**Never re-dispatch a page that already has a parseable, count-correct extract.** It spends
budget re-buying data you own.

## Finish

Done when every manifest page has a committed, parseable, count-correct extract. Report:
pages extracted this run, re-dispatches and why, pages remaining. Next phase:
`digitize-adjudicate`.
