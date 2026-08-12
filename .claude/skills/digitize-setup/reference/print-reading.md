# Print reading — the operative rules

General epistemology for adjudicating digitized cells against scanned print. Distilled from
~30 states of 1940/1950 census adjudication; **every rule here was paid for with a real
error.** Table-geometry facts stay in each project's LESSONS.md; everything here is about the
*face* and the *reader* and carries across projects.

Copied into each project as `digitization/PRINT_READING.md`. Orchestrator-owned: amendments
go through the PROCESS queue.

---

## 1. Each glyph test separates exactly ONE pair

Do not reuse a test on a pair it cannot see. Always stack the disputed digit against a known
reference **from the same column** at ×10 or more — same face, same ink, same scan exposure.

Example tests, built on the 1940 census Vol. II face — **face-dependent, so rebuild this
table for your own source** (the 1950 Vol. I face contested six pairs absent from it):

| pair | test |
|---|---|
| `3` vs `8` | left-wall stroke weight: a true `8` has a continuous full-weight left stem; a bridged `3`'s left wall is thin, notched or broken |
| `3` vs `9` | lower-bulb upturn; a `9` has an empty lower-left quadrant |
| `5` vs `6` | flat horizontal top bar; a `6` closes its bowl from a curved entry stroke |
| `2` vs `8` | wide flat baseline foot; an `8` shows two stacked counters |
| `1` vs `4` | baseline foot serif; a `4`'s stem simply terminates |

- **A test transfers to an unlisted pair exactly when the feature it keys on is ABSENT from
  the new counter-class** — and misleads when present. (`5`/`7` defeated the flat-top-bar
  test because a `7` also has one; `5`/`9` is settled by it unchanged.) Index tests by
  *feature*, not by pair.
- **Counting enclosed counters** settles the `6`/`8`/`0`/`9` family and is size- and
  exposure-invariant — **but it needs a control exactly like any metric**: count the
  *references* too. On an ink-spread 1-bit face, stroke breaks make the count a LOWER BOUND
  (a known `6` returning 0 counters means the instrument has failed; do not rank).
- **When a suspected misread duplicates an adjacent digit, the adjacent digit is the
  control** — same face, ink, exposure, and baseline for free. The best reference of all is
  a digit inside the disputed number itself.
- **When two glyphs touch, find a fused same-class control in the same column** (a disputed
  `0?` pair vs the column's own `00` from a `100`) — never split the run by hand.
- **Ink spread closes a `3`'s lobes with hairlines** — judging closure alone reads `3` as
  `8`. At low native resolution (≤300 ppi), expect structural tests to fail in *both*
  directions; treat them as unavailable, not merely weak, and lean on identity closure.
- **Do not assume the pair, and do not assume the direction.** Adjacent units ran
  `3`/`8`-dominant, `3`/`9`, `5`/`3`, `5`/`6`, `2`/`8`, and dash-as-digit. Five units ran
  errors overwhelmingly one way; the sixth split ~17/15. A directional prior is a hypothesis
  to test on the page in front of you, never a tiebreak.
- **Low native resolution is a prior about a face, not a verdict on it** — one 300 ppi source
  was legible at ×2.7 while another at the same ppi was brutal. Calibrate on the first
  render, and note two consecutive units have needed no glyph test at all: budget from the
  page, not the alarm.

## 2. Measurement: check the control before the ranking

Any similarity metric (IoU against labelled references, ink widths) must ship **every
reference-vs-reference pair as a control**. The control is the whole point.

- On a good column, same-class control sits high and cross-class low, and the verdict is
  unmissable.
- **An INVERTED control — cross-class scoring above same-class — is a hard refusal, not a
  weak ranking.** Report it and stop. It usually means segmentation swallowed something (a
  comma touching a digit).
- **A winner below the same-class control matched *nothing*.** Reporting "0.652 beats 0.549"
  against controls of ~0.75 once produced a false misprint claim on an ordinary error.
- **Controls collapse on low-resolution pages** — a high-dpi render of a 300 ppi source is
  pure upsampling. Structure carries those columns; the metric does not.
- **Never judge a glyph whose box was set by hand.** Boxes come from ink-run segmentation,
  never hand-guessed windows: a window off by part of a glyph stacks half of one digit
  against half of the next and *manufactures* the feature under test. Nothing enforces this
  — it is on you.
- **When the disputed glyph touches a neighbour, shape outranks width** — a bounding box
  swallows neighbour ink.
- **Cut bigger.** A ×5 cut is not a reading; a glyph read as a clean `2` at ×5 plainly
  carried two counters at ×12.
- **A tight per-cell crop destroys the dash-vs-digit test.** Zero-marks (em-dashes, dots)
  print at the LEFT of a cell; digits are right-aligned — horizontal position is half the
  evidence. Always cut the full column width, and run the dash-vs-digit pass *before*
  arguing any glyph. Report the page's dash density with any "no dash errors" claim — a
  clean negative at 3% density licenses almost nothing.
- **On a broken 1-bit face, go to native pixels, not higher dpi.** Upsampling visibly
  *manufactures* stroke continuity — it adds no information, but it adds plausibility.
- **The metric's other safe use is proving two glyphs are the SAME digit**, which survives a
  collapsed control.

## 3. A misprint claim is the last resort

Running census score: **9 claimed, 3 real**. Reserve a misprint claim for a residual *no
reading* can close. What made the real ones survive — the template a claim must match:

1. **Multiple independent reads converge** on the same values for every cell in the record
   (the settled case took four).
2. **A second printed cross-check sides with the printed value, not against it** (the printed
   percent was only consistent with the "misprinted" count).
3. **The alternative was a specific, falsifiable reading that was tested and failed** — not
   "something must be wrong". And refuting a candidate needs the same standard of proof as
   accepting one; one false claim came from a wrong refutation.

A confirmed misprint means the data stays **exactly as printed** and the unit keeps a
permanent triage residual — do not "fix" it, and do not let a later sweep re-open it.

**One reader's failure to close a record is never evidence of a misprint.** Under the queue
system you do not write the claim at all — you queue it, and the template above is the bar
the entry must clear.

### 3a. There is only ONE source, and it is the print

Never write "the print contradicts the extract" — false premise. Every crop, upscale and
re-render is a *derivation* of the one printed page, so a conflict is **two readers of one
source disagreeing**: the original extractor and you. Resolve it with the rules you already
have; if they fail, escalate. It is never a new error shape and never evidence of a misprint.
When you are certain the print disagrees with an extract that closes every identity, the base
rate says **you** are the misreader — in the founding case, one column both readers were
wrong (equal-and-opposite errors, identity closed on false values) and in two the extract was
simply right.

## 4. Prefer the reading that closes the identity

When a glyph is genuinely indeterminate, and (1) every other cell in the record
print-verifies cleanly, (2) the total is independently corroborated, and (3) **exactly one**
reading closes the identity — take that reading. This is **the default, not the tiebreaker**;
it has been under-applied about three times as often as over-applied. A glyph measurement
never overrides it.

**The boundary is sharp**: gate it to one cell, after the rest of the record is read, with
the glyph independently established as damaged. Two or more cells in doubt is not a reading —
it is a guess. But then the strong form applies:

**The identities do not merely veto readings — they GENERATE them.** When several cells are
ambiguous, **enumerate the assignment that closes all identities simultaneously, then verify
that assignment against the print** — never read cells one at a time asking of each whether
it closes. Across 94 human-ruled census records, 93 closed every count identity exactly; on
genuinely hard records the identity-closing reading is right ~99% of the time. And a
multi-identity closure across many moving cells on a scan too degraded for any glyph test
*is* the proof — that is not fabrication, because the values came from the print and the
identities checked them afterwards.

**Closure is necessary, not sufficient.** Compensating pairs close identities on wrong
values (§5). Solving tells you *which* reading to verify; it does not excuse verifying it.

- **A single-cell repair enumerator that permutes digits in place is blind to a
  dropped/added digit** — run a digit-count-aware pass before believing a "no single-cell
  repair exists" verdict.
- **Run external cross-checks EARLY** — as candidate eliminators, not just exit criteria.
  An independent digitization can pin a field no identity protects before any glyph is
  argued.
- **A validator that silently checks 20% of a unit looks exactly like a validator that
  passes.** Whenever a cross-check's `compared` count is far below the unit's record count,
  that is the finding — before any cell is read. An `unmatched` row is a finding until its
  cause is named (real non-matching unit, vintage change, reference-side misspelling,
  reference-side annotation — all four occurred). Two validators do not cover for each other.

## 5. Error shapes the identities cannot see

**Sum-preserving errors pass everything. Sweep every page against a printed dump of the
extract, including pages with no identity failures.** A clean sweep is a result, not a wasted
pass — it is also what calibrates the project's error rate.

| shape | signature |
|---|---|
| **Record slip** | Reader drops one printed record and keeps a neighbour, shifting every label after it. Both mislabelled records are real print and internally consistent — *all* identities close. The only check is counting printed records against extracted ones, then reading one anchor field across the page. Mandatory on every page. |
| **Tail slide** | A value duplicated/inserted in the short-tail rows, everything below pushed down, the last value dropped. Signature: a **small residual (±2 to ±5)** on a record whose tail is small values and dashes. Single-cell candidate generators are *actively misleading* here. Slides cluster by page — one found means read the tail of every record on that page. The mechanism is the junction (a zero-mark row following a digit row), not any particular panel: screen on the mechanism. |
| **Compensating pair** | Two cells moved equal and opposite. No identity fires. **A closing identity is not evidence that both its cells are right.** |
| **Transposition** | Two adjacent values swapped. Sum-preserving. |
| **Coordinated shift** | The same offset applied to a total and its parts. Only an independent second printing (derived percent, cross-panel reprint) catches it. |
| **Spurious/dropped digit** | Invisible to every glyph test — the disputed glyph is not on the page. Settle by **digit position**: values are right-aligned in fixed x-bands; compare occupied bands against a same-column number of known length. A residual that is a round multiple of a power of ten is reason to *count the glyphs* — the count, not the arithmetic, decides. |

## 6. Reading a residual

- **A small residual does not mean a small error** — ±3 was once produced by ten wrong
  cells that nearly cancelled. When a record's glyphs are degraded across the board, suspect
  the whole record.
- **A round residual (±50, ±100, ±500) says *n* digits moved in the same place value** —
  enumerate multi-cell readings before anything else.
- **Two identities missing by the same amount in opposite directions suggests a shared cell —
  as a hypothesis to check against the print, not a verdict.** It resolved three records by
  arithmetic alone, then the same signature appeared where the shared cell read unambiguously
  correct. Lead with it; never close on it.
- **A residual on only the derived-quantity identity, with counts clean, means the derived
  cell itself was misread** — at any size, down to the last printed digit.
- **When every single-cell candidate dies on the print, that is evidence for a multi-cell
  record — not for a misprint.**
- **Two readings closing the same identity is not a NO-CHANGE; it is an instruction to
  measure both.** If the measurement also refuses (controls collapse, winner below control),
  queue the pair with the control numbers.
- **Read a panel residual as a NET, not a cell** — one −10 concealed +10 and −20 in the same
  panel. Enumerate multi-cell solutions inside the failing panel before accepting a one-cell
  repair.
- Several records on one page failing by the same small residual, each closed by the same
  units-digit confusion, is a *face* finding. A pattern that survives full per-cell
  verification escalates once as a page-level question; one that dissolves cell by cell was
  never a page question at all. **Test the pattern; do not let it do the work** — two errors
  on the same printed row in nearby records had unrelated causes.

## 7. Derived quantities (percents, rates)

- **They stay as printed** — reconstructed from raw counts downstream. The derived identity
  is a QC instrument only; never "correct" a count from it.
- **But a *misread* derived cell is an ordinary error**: compute from print-verified counts;
  if the computed value matches the print and only the extract differs, fix the extract; if
  the print itself misses, keep the print.
- **A blank/dash derived cell means the identity is *unavailable*, not failed** — a separate
  triage bucket, not a failure, and not a queue entry.

## 8. Self-flags

- **Flags never localize.** A flagged cell was correct while the error sat elsewhere in the
  record; one flagged record print-verified clean end to end. Verify the whole record.
- **But flag *count* is a record-level alarm** — one with eleven flags had ten wrong cells.
- The absence of a flag protects nothing.

## 9. "Unreadable" is a statement about the agent, not the page

A NO-CHANGE is for a residual *no reading* can close — not for a record you personally cannot
read. Escalating has repeatedly cost one message and recovered ten to fifteen cells; under
the queue system it costs nothing at all: write the entry and move on. Two related traps:

- **A confident single-glyph call on a low-resolution record is worth much less than it
  feels** — errors keep being found in cells previously marked "print-verified". When a
  human ruling contradicts one, that is a signal, not an exception: it is the highest-value
  line in the unit's lesson file.
- **The page's text/OCR layer is not evidence, however complete it looks** — the rule is not
  "it is usually broken", it is "it is not evidence". (Exception: as a *ranking* input for a
  sweep, where every hit is print-verified anyway, it is a free independent read.)
