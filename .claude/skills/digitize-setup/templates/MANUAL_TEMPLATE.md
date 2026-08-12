# Digitization manual — {{PROJECT_NAME}}

**This document is stable.** It changes only via a PROCESS ruling from {{HUMAN_NAME}}. If you
are a per-unit subagent, read this in full plus `digitization/LESSONS.md` and
`digitization/PRINT_READING.md`, and nothing else unless this manual sends you there.

<!-- If the project runs in spot-check mode (no identities), say so here in bold, with the
     sampling rate, before anything else. -->

---

## 0. What the work is

{{ONE_PARAGRAPH: what the source is, what the output data is, current phase — extraction
in progress, or extraction complete and adjudication remaining.}}

The work per unit, once extraction is complete, is **adjudication**: take the records the
identities flag, read them against the print at high resolution, write verified corrections to
a sidecar, assemble, audit, commit.

**Do not re-dispatch a page that already has an extract.** It spends budget re-buying data we
own. Check any deferred-item list against the repository before believing it — a stale entry
costs a whole re-extraction.

---

## 1. Hard constraints

These are not style preferences. Runs may execute unattended, so nothing else will stop you.

1. **Renders go only to {{RENDER_DIR}}, never inside {{SYNCED_OR_WATCHED_DIRS}}.**
   <!-- Census example: rendering inside a Dropbox-synced worktree triggered a sync storm
        that pegged the machine. Use a prefix unique to your unit. -->
2. **Never edit an extract CSV** (`{{EXTRACT_PATH_PATTERN}}`). Corrections go only to the
   sidecar `{{SIDECAR_PATH_PATTERN}}`. {{SIDECAR_EXCEPTIONS: anything a sidecar cannot
   express, e.g. a record's name/key itself}}
3. **Write only to your own unit's paths:** the sidecar, the assembled output, your lesson
   file, the two queue files (append only), and your own row of `run_status.md`.
4. **Orchestrator-owned files — do not edit:** {{ORCHESTRATOR_OWNED_FILES: the audit script,
   extraction rules, LESSONS.md, anything whose keys are shared across units}}. Want a
   change? PROCESS queue, then continue.
5. **`git add` by explicit path, never `-A`.** {{UNTRACKED_DEBRIS_NOTE}}
6. {{OTHER_CONSTRAINTS: sacred directories, tool prohibitions, etc.}}

---

## 2. Orientation

**Work from:** `{{PROJECT_ROOT}}`. {{BRANCH_AND_COMMIT_CONVENTION: e.g. every commit message
carries the ticket number}}

| | {{SERIES_A}} | {{SERIES_B if any}} |
|---|---|---|
| source | {{...}} | |
| records are printed as | {{ROWS or COLUMNS — verified against a page, not memory}} | |
| identities | {{N}} | |
| adjudication render dpi | {{...}} | |
| manifest | {{...}} | |
| extracts | {{...}} | |
| assembler | {{...}} | |

---

## 3. Schema and identities

```
{{FIELD_LIST_IN_EXTRACT_ORDER}}
```

{{NOTES: sampling/rounding conventions, how the print marks zero (dots/dashes), fields the
print carries that the schema does not, asymmetries between panels.}}

| id | identity |
|---|---|
| (a) | {{e.g. part fields → total field}} |
| (b) | {{...}} |

{{PER_IDENTITY_NOTES: which are load-bearing (a derived percent once caught a coordinated
shift that passed every count identity), which fields NO identity protects — name those
explicitly; they are the schema's weakest evidence and external cross-checks are their only
audit.}}

---

## 4. The rule that governs the whole design

**Never put the identities in a reader's prompt.** A reader given an arithmetic target will
satisfy it — the census project watched a pass with an explicit anti-fabrication clause
rewrite whole columns into internal consistency. Identities are your QC instrument, never a
reader's instruction. The same logic bounds *you*: arithmetic ranks the queue; only the print
settles a cell.

---

## 5. Tooling

<!-- One row per tool. The first row is always native-resolution inspection. -->

| tool | use |
|---|---|
| `pdfimages -list` | **first, always.** Native resolution — governs render dpi and whether glyph measurement controls will hold. |
| `{{TRIAGE_TOOL}}` | **the queue.** Applies the sidecar exactly as the assembler does, then reports every failing record with the **signed residual** of each broken identity. |
| `{{BOUNDARY_TOOL}}` | row/column windows from the page's own printed rules, **plus the count against the extract**. The only check that sees a dropped or duplicated record. |
| `{{COLUMN_RENDER_TOOL}}` | one record rendered beside its printed labels and extracted values, with per-band pixel heights. The instrument for a row slide. |
| `{{SWEEP_TOOL}}` | whole-page render against a printed dump of the extract. |
| {{OTHERS}} | |

{{TOOL_CAVEATS: known failure modes, discovered as they happen — candidates for LESSONS.md.}}

---

## 6. The loop

### Per page, before you argue about any single glyph

1. **Native resolution** (`pdfimages -list`).
2. **Boundary detection; compare the count against the extract's record count.** If they
   disagree, work out *which* record was dropped or duplicated before reading a glyph. No
   identity can see a slip — both mislabelled records are real print and internally
   consistent.
3. **Confirm every rendered record by its printed {{ANCHOR_FIELD: a field whose value is
   distinctive, e.g. the first/total row}}** against the extract before reading a disputed
   cell. Label mapping fails silently.
4. **Sweep the whole page** against a printed dump of the extract — including pages with no
   identity failures. Sum-preserving errors are found this way and nothing else finds them.
   A clean sweep is a result.
5. **Re-cut every sweep hit on its own record before it goes in the sidecar.** A strip
   locates disagreements; it never settles a glyph.

### Per flagged record

1. Arithmetic candidates first — a ranking, never a verdict.
2. Render the record with its own labels at the adjudication dpi.
3. Judge the glyph with the test that separates *that* pair (`PRINT_READING.md` §1).
4. Prefer the reading that closes the identity (`PRINT_READING.md` §4).
5. If you cannot close it — queue it (§8). You may not bank a NO-CHANGE.

### Write corrections as you verify them

Append each verified correction to the sidecar **immediately**, not batched. Triage applies
the sidecar exactly as the assembler does, so a subagent killed mid-unit leaves the next one
a shorter queue and loses only unwritten reasoning.

---

## 7. Exit criteria

1. All identities pass, or each failure is print-verified and documented in the sidecar, or
   queued.
2. `{{ASSEMBLER_CMD}}` produces the expected record count ({{COUNT_REFERENCE: vs manifest or
   external reference}}).
3. `{{AUDIT_CMD}}` clean for the unit — or the only discrepancy is one you have queued.
4. Every self-flag print-verified.
5. {{EXTERNAL_CROSSCHECK_CMD if any}} clean. {{REGRESSION_BASELINE if any: e.g. a
   byte-identical reference unit}}
6. Commit.

All criteria are cheap and machine-checkable **by design** — the orchestrator re-runs them.

---

## 8. Queues — what you may and may not conclude

**You may** fix any cell you have print-verified.

**You may not** bank a NO-CHANGE, a misprint claim, or an "unreadable record" — see
`PRINT_READING.md` §3 and §9 for why this judgment is reserved. Append to a queue and move
to the next record. Queueing costs nothing and blocks nobody.

### `queue_ruling.md` — never blocks anything

Anything that needs {{HUMAN_NAME}}'s eye on one record. **Queue the item WITH its artifact:**
you are the only one who will ever have the geometry cheaply. Before you move on:

1. Render the record to a durable, named path:
   `{{REVIEW_IMAGE_DIR}}/<unit>/<NN>_<record>.png`, numbered in queue order, via the
   column-render tool so each cell carries its label and extracted value. Add
   `<NN>b_<record>_<cell>.png` for any glyph you argued about, beside same-column references.
2. Record the **geometry** in the entry (window coordinates, band, index) so it can be re-cut
   without rediscovery.
3. Working crops stay in {{RENDER_DIR}}; only final review images go under
   `{{REVIEW_IMAGE_DIR}}` (untracked — they persist without entering git).

Entry format:

```markdown
### {{UNIT}} <record> (p<N>) — <one-line summary>
- **Residual(s):** a=−3, b=+6
- **Geometry:** <window / band / index — so it can be re-cut>
- **Review image:** <path>
- **Cells in play:** post-sidecar values, and which you changed
- **Tried:** candidates and why each was refuted; which test on which pair; measurement
  scores WITH their same-class controls; what the page sweep showed
- **Native ppi:** from `pdfimages -list`
- **Status:** OPEN
```

Report control numbers whether or not they discriminated — a score below the same-class
control is no verdict at all, and saying so is what makes the entry auditable.

**Also emit a ruling template** once per unit with a non-empty RULING queue:
`digitization/rulings/<unit>_human_TEMPLATE.csv`, one row per field per queued record, in the
sidecar's own schema, `extracted_value` pre-filled post-sidecar and `corrected_value` blank —
so the human read applies without transcription.

A queue entry whose image does not exist is not done.

### `queue_process.md` — stops the run

Anything that changes a **rule** rather than a cell: a new glyph test or an amendment; an
**error shape never seen before** (also record retro-sweep debt: which closed units predate
it); a change wanted to an orchestrator-owned file; a unit queue so large it implicates the
extract rather than the adjudication.

---

## 9. Closing a unit

Closure is **provisional**. In this order, so it is one commit:

1. Run the exit criteria and record actual output.
2. Write `digitization/lessons/<unit>.md`: unit universe (final count vs reference), face
   notes (which glyph confusions dominated, which test decided them, whether measurement
   controls held, native resolution), tooling failures and workarounds, error shapes —
   especially anything the identities could not see — and **operative rules**: one-line
   generalizations the orchestrator may fold into `LESSONS.md`. Everything else stays here
   as narrative evidence.
3. Update your row in `run_status.md` — `provisional (N queued)`, or `final` if nothing OPEN.
4. Commit: `{{COMMIT_MESSAGE_FORMAT}}` — N is the RULING count only.

**The queue file, not git history, is the authority on "finished."**

---

## 10. Order of work

{{UNIT_ORDERING: ascending by triage failure count is the default — cheap wins first, and
the failure counts are a planning number, not a contract; re-run triage before dispatch.
One table geometry per work session.}}

{{DEFERRED_AND_OUT_OF_SCOPE}}
