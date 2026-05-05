# /bibcheck — Many-Agent Bibliography Audit

A verification skill for `.bib` files. Spawns many narrow-focus agents — one per citation, or one per field — to audit each bibliography entry against canonical sources (DOI, journal page, author working paper). Catches the silent errors that pass spell-check but kill peer review: mixed-up entries, wrong years, fabricated DOIs, journal misattributions.

---

## Why this exists

A single agent asked to audit 80 citations in one pass tends to drift. Early entries get careful treatment; later entries get pattern-matched. Whatever you call it — gradient decay, attention dilution, fatigue — the practical effect is that late-batch citations are checked less rigorously than early-batch citations, and the user cannot see which is which.

`/bibcheck` flips the structure. Each agent gets one small task, full attention budget, and a parallel sibling for the next entry. The bottleneck moves to orchestration, which is what cheap parallel agents are for.

This is the same principle behind `/referee2` (fresh agent reads cold), `/split-pdf` (parallel chunks instead of one giant PDF), and the package-audit experiment (96 zero-discretion agents instead of one general-purpose one).

---

## What it checks

For each entry, the audit verifies:

1. **Existence** — does the cited paper exist? Locate a DOI or canonical landing page.
2. **Field consistency** — do title, authors, year, journal, volume, issue, pages, and publisher all belong to the *same* paper? (Mixed-up entries are the most common silent error in inherited `.bib` files.)
3. **Field correctness** — wrong year, wrong abbreviation, wrong volume, wrong page range.
4. **Format integrity** — parseable BibTeX, no quietly-broken unicode in author names.

What it does **not** check:

- Whether the citation supports the claim it's attached to (that's a `/referee2` literature audit).
- Whether the cited paper's findings are correctly characterized in the manuscript text (same).
- Whether the manuscript is missing citations it should have.

`/bibcheck` is bounded: are the entries in this `.bib` accurate descriptions of papers that exist?

---

## Two modes

### Per-citation (default)

```
/bibcheck path/to/refs.bib
```

One agent per `@article{}`/`@book{}`/`@incollection{}` entry. Each agent fully audits its one entry: identify the paper from canonical sources, cross-check that all fields belong to the same paper, emit a one-sentence description and a corrected entry if needed. A final reviewer agent consolidates and adjudicates.

**Best for:** catching mixed-up entries (title of paper A paired with authors of paper B).

### Per-field

```
/bibcheck --by-field path/to/refs.bib
```

One specialist per field — title, year, journal, authors, volume/issue, pages, DOI. Each specialist reads the *whole* bibliography but only checks its one field. Specialists are launched as **separate `claude --dangerously-skip-permissions -p` subprocesses** so they do not share context, then the consolidator joins their outputs.

**Best for:** catching *systematic* transcription errors — a journal name consistently rendered wrong, working-paper years leaking into published-paper entries, swapped volume/issue numbers.

The two modes are complements. If a manuscript is going somewhere it cannot afford a citation error, run both.

---

## Outputs

```
<bib_dir>/bibcheck_<timestamp>/
  ├── input.bib              # copy of source
  ├── entries/               # split entries
  ├── reports/               # per-agent JSON
  ├── bibcheck_report.md     # consolidated audit
  └── corrected.bib          # drop-in replacement
```

The skill **never** auto-overwrites your source `.bib`. You review `bibcheck_report.md`, then move `corrected.bib` into place yourself.

---

## Arguments

| Argument | Effect |
|----------|--------|
| `<file>` | Path to a `.bib` (or a `.tex` whose `\bibliography{}` points to one) |
| `--by-citation` | Per-citation mode (default if omitted) |
| `--by-field` | Per-field mode |
| `--max-parallel N` | Cap concurrent subagents/subprocesses. Default 8 |

---

## Cost and rate-limit notes

`/bibcheck` issues one WebSearch (often 2–3) per citation in per-citation mode, plus an aggregator pass. For an 80-entry bibliography, expect ~80 light agent runs plus one consolidation. Per-field mode is heavier — each specialist does N web searches across the whole bibliography. Default `--max-parallel 8` keeps things sane on a Max plan; bump it if you have headroom or lower it if you are getting throttled.

---

## When to use which mode

| Situation | Mode |
|-----------|------|
| Inherited `.bib` from a coauthor or RA | per-citation first |
| Pre-submission audit on your own manuscript | per-citation, then per-field on the entries flagged unverifiable |
| Worried about systematic transcription errors (e.g., one journal abbreviated wrong everywhere) | per-field |
| 3+ entries came back unverifiable | re-run those specifically with per-field |

---

## Related skills

- `/referee2` — broader audit of an artifact, including a literature-review check (citation-claim fidelity)
- `/split-pdf` — if your starting point is a PDF rather than a `.bib`, run this first to extract the references section
