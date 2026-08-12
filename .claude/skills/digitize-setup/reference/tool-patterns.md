# Tool patterns — the five roles and their invariants

Contracts, not implementations: write each tool for the project's actual table geometry.
Every invariant below was paid for with a real error in the census project.

## 1. Manifest

One row per page: source file, page number, unit, expected record count (from an external
reference where one exists, e.g. a harmonized county list). The manifest is what "complete"
means for wave 1.

## 2. Triage — the queue

`triage <unit>` applies the sidecar **exactly as the assembler does** (same code path or same
logic, verified once against it), then reports every failing record with the **signed
residual** of each broken identity.

- Signed residuals are the diagnostic (see PRINT_READING §6) — never report bare pass/fail.
- A blank derived cell goes to a separate `na` bucket, not the failure count.
- Confirmed misprints are expected permanent residuals — annotate, don't re-flag.
- `-q` summary mode for the orchestrator's planning pass; failure counts are a planning
  number, not a contract.

## 3. Assemble

`assemble <unit>`: extracts + sidecar → final per-unit CSV. Reports the record count and
**every sidecar row that matched no extract row** — an unmatched sidecar row is an error
(a typo in its key), never a silent no-op. A sidecar row whose corrected value equals the
extracted value is a documented *confirmation*, not a drop.

## 4. Audit

`audit <series>`: unit-level checks across all assembled units — record counts vs the
external reference, name/key-level diff, empty-page sweep. Machine-checkable and cheap, so
the orchestrator can re-run it after every unit.

- Make the pass/fail grep-able with an unambiguous marker (`<-- CHECK`) that cannot appear
  in prose notes.
- Known-discrepancy allowlists (`KNOWN_*`) are orchestrator-owned data: adjudicators queue
  additions, never write them.
- **Report coverage, not just verdicts**: a validator that silently compares 20% of a unit
  looks exactly like one that passes (a name-join failure once skipped 100 of 127 records in
  the largest unit and reported nothing wrong). `compared` far below the unit's record count
  is itself a failure.

## 5. Column render (+ boundary detection, sweep)

The adjudicator's eyes. Three cooperating pieces:

- **Boundary detection**: record windows from the page's **printed rules** (ink projections),
  never from the OCR/text layer. Always report the window count for the **count gate**:
  windows vs the extract's record count, the only check that sees a record slip. Merge rules
  closer than the glyph pitch (a tall digit stack masquerades as a rule); expect the
  outermost rule to print below threshold and pad the extrapolated window generously — a
  clipped units digit at a crop edge looks like a crop artifact, which is exactly how it
  gets waved past.
- **Column render**: one record tiled cell-by-cell beside its printed labels and the
  extracted values, with per-band **pixel heights** (separates a digit band from a dash band
  with no glyph judgment — the instrument for a tail slide). Full column width always
  (PRINT_READING §2, the dash-vs-digit rule).
- **Sweep**: whole-page render against a printed dump of the extract, budgeted in records
  per tile from the native ppi. Prefer full-width per-panel strips with the print's own stub
  labels attached where the page fits — every mapping failure so far has been a failure of
  tool-side row reconstruction, and the strip does not have that failure mode.

Cross-cutting:

- **A matching band count is not a correct mapping** — cancelling band errors (one split,
  one lost) keep the count right while every label sits one row off. Confirm mapping against
  the print via an anchor field.
- Row grids are not uniform (panel gaps vs body pitch); anchor on a robust per-page skew
  fit, not any single band.
- Cache renders by the full band key, or not at all — a stale cache silently invalidates a
  whole round of comparisons.
