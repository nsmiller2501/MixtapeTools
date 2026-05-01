# `/wiki-update-local` — Reference wiki ingest with local PDF conversion

**Skill location:** [`.claude/skills/wiki-update-local/SKILL.md`](../../.claude/skills/wiki-update-local/SKILL.md)

---

## What This Skill Does

You drop one or more PDFs into a project's `references/raw/` folder, run `/wiki-update-local`, and the skill ingests each paper into a structured wiki at `references/wiki/`. For each paper it:

1. Converts the PDF to clean markdown via [`/read-pdf`](../read-pdf/README.md) — preserving table structure, extracting figures as PNG clips, and rendering equations as LaTeX math mode.
2. Writes a structured 11-dimension extract (`<basename>_text.md`) alongside the PDF, with a 200-word plain-English synthesis at the top.
3. Updates the wiki: creates new concept pages, appends to existing ones, embeds extracted figures, and adds backlinks. Destructive edits to existing pages are returned as diffs for user approval rather than applied silently.
4. Atomically logs the ingest in `wiki/log.md` only after wiki edits succeed — failed runs leave nothing partially committed.

The wiki is shaped by per-project conventions in `references/CLAUDE.md`, which the skill reads first and treats as authoritative.

---

## Why It Exists

There are two PDF-ingest paths into a project wiki:

| Skill | PDF parsing | Best for |
|---|---|---|
| `/wiki-update` (forthcoming, separate) | Uses Claude Code to "read" the pdf image as-is | First-time users, no local install, token intensive |
| `/wiki-update-local` (this skill) | `/read-pdf`'s local converter (docling/marker) | Faithful tables, figures, equations |

`/wiki-update-local` exists because table fidelity, figure extraction, and equation transcription matter for econ wikis. PDF-image rendering loses table structure (Claude can read the values but not preserve them as machine-readable markdown), can describe figures but cannot extract them as files, and turns long derivations into expensive image tokens. Local layout-aware conversion solves all three:

- **Tables** come through as pipe-syntax markdown — copy-paste into the wiki.
- **Figures** are pixel-accurate PNG clips, copied into `references/wiki/figures/` and embedded inline. No more CLIP placeholders to manually fill in.
- **Equations** are rendered as LaTeX math mode (`$$ ... $$`) inline in the source markdown — verbatim, not paraphrased. (If a backend struggles on a particular paper's math, the converter falls back to clipping equations as images, and a vision sub-agent transcribes them to LaTeX before synthesis.)

The trade-off: a one-time install of the local converter venv (~500 MB, 1–3 min, handled lazily by `/read-pdf`). After that, conversions are cached by content hash — re-ingesting the same PDF is free.

---

## How It Works

```
project-root/
├── CLAUDE.md                          # research question, data, identification (must be filled in)
└── references/
    ├── CLAUDE.md                      # wiki conventions (rendered from skill template on first run)
    ├── raw/                           # immutable source PDFs + per-paper structured extracts
    │   ├── Smith_2024_AER.pdf
    │   ├── Smith_2024_AER_text.md     # written by this skill — reusable cross-session
    │   └── ...
    └── wiki/
        ├── index.md                   # table of contents — appended on each ingest
        ├── log.md                     # append-only ingest log
        ├── figures/                   # extracted figure clips (copied from /read-pdf cache)
        │   └── Smith_2024_AER_fig3.png
        └── <concept-pages>.md         # one per concept; updated by ingest, linked via [[wiki-links]]
```

### Usage

```
/wiki-update-local
/wiki-update-local "focus on IV strategies and instrument validity"
```

The optional argument is a free-form focus string applied to this batch in addition to the project's standing context (research question, data, identification strategy, all read from `./CLAUDE.md`).

### What gets extracted (11 dimensions)

For each paper, the structured extract covers:

1. Research question
2. Audience
3. Method / identification strategy
4. **Target parameter** — the estimand in plain terms (distinct from method)
5. Data — sources, unit, sample size, time period
6. Statistical methods / specifications — including **key equations verbatim** in LaTeX
7. Findings — coefficients, SEs
8. Contributions
9. Replication feasibility
10. **Tables** — pipe-syntax markdown, only for project-relevant tables
11. **Figures** — Tier A (data figures, structured optical decomposition) or Tier B (schematics, image embed only)

Plus a `Bibliographic metadata` block at the top (DOI, authors, title, year, venue) for use by a forthcoming bib-pipeline skill.

### Pre-flight checks (before any ingest)

- **Lazy scaffolding** — creates `references/raw/`, `references/wiki/`, `references/wiki/figures/`, `references/CLAUDE.md`, `wiki/index.md`, `wiki/log.md` on first invocation. Idempotent on re-runs.
- **Project context check** — refuses to proceed if `./CLAUDE.md` has unfilled placeholder fields (research question, data sources, identification strategy). Relevance filtering depends on these.
- **Filename normalization** — proposes `Last_Year_Venue.pdf`-style renames for any non-conforming PDFs and asks for batched approval before applying.
- **Reuse tier classification** — Tier 1 (synthesis cached in `_text.md`) or Tier 2 (fresh ingest, but the converter's content-hash cache often makes this fast anyway).

### Per-paper subagent isolation

Each paper is ingested by a dedicated subagent so that converted markdown and extracted figures don't accumulate in the main session's context across papers. The main session orchestrates: spawning subagents, surfacing user-approval prompts, and writing the log entry only after wiki edits succeed.

---

## What This Skill Does NOT Do

- **No `references.bib` assembly.** A separate skill (forthcoming, on its own feature branch) handles BibTeX generation from the metadata block in each `_text.md` extract via a CrossRef / OpenAlex / GROBID cascade. `wiki-update-local` records the metadata so that skill has what it needs, but does no network lookups itself.
- **No PDF download.** Drop them into `references/raw/` first.
- **No silent fallback** if the converter fails. The skill surfaces converter errors and skips that paper for the run rather than substituting `pdftotext` output (which would produce subtly wrong wiki entries).

---

## Acknowledgments

Inspired by Andrej Karpathy's [LLM Wiki](https://karpathy.bearblog.dev/llm-wiki/) pattern — a structured, interlinked knowledge base maintained by an LLM, curated by a human. The Tier A / Tier B figure protocol, the project-relevance gate, and the substantive-change rule are workflow refinements specific to academic-paper ingest at scale.

The local-conversion path exists because of [docling](https://github.com/docling-project/docling) and [marker](https://github.com/VikParuchuri/marker) — open-source layout-aware PDF parsers whose authors did the actual hard work.
