# CLAUDE.md Template for Research Projects

> Copy this file to your project root and fill in the sections below.

---

## Communication Guidelines

- Refer to the user as **Noah**
- Collaborators: [List collaborators and their roles]

---

## Estimation Philosophy

**Design before results.** During estimation and analysis:

- Do NOT express concern or excitement about point estimates
- Do NOT interpret results as "good" or "bad" until the design is intentional
- Focus entirely on whether the specification is correct
- Results are meaningless until we're confident the "experiment" is designed on purpose
- Objectivity means being attached to getting the design right, not to any particular finding

---

## Project Overview

[2-3 paragraph description of your project]

### Research Question

[What are you trying to answer?]

### Data Sources

[What data are you using? Time periods? Geographic coverage?]

### Identification Strategy

[How are you identifying causal effects? What's the source of variation?]

---

## Key Files

- **Main analysis**: `path/to/script.R` or `script.py`
- **Data cleaning**: `path/to/cleaning.R`
- **Paper draft**: `path/to/paper.tex`
- **Presentation**: `path/to/slides.tex`
- **Central BibTeX file**: `references/references.bib` (maintained by `/wiki-update`; cite from any `.tex` via `\bibliography{<relative-path>/references/references}`)

### Conventions

- **`data/raw/` is immutable** — never edit or delete source files. All cleaning and transformations happen in `code/` with outputs to `data/clean/`.
- Include random seeds for any stochastic analyses.

### Analysis output conventions

Unless the user explicitly specifies otherwise:

- **Tables** (from any analysis script) → `output/tables/` as standalone `.tex` fragments. No preamble, no `\documentclass` — just the `\begin{tabular}…\end{tabular}` or `\begin{table}…\end{table}` block, suitable for `\input{}`.
- **Figures** (from any analysis script) → `output/figures/` as `.pdf` (prefer vector over raster). Use a descriptive base name; specification variants as suffixes.
- **Compiled LaTeX documents** (a standalone `.tex` that `\input`s multiple tables and `\includegraphics`es multiple figures — e.g., `summary_stats.tex`, `conceptual_framework.tex`) → `documents/<topic>/<topic>.tex`, where `<topic>` is a short subject-derived folder name. Build artifacts (`.aux`, `.log`, `.synctex.gz`, compiled `.pdf`) live in the same subfolder. Reference tables/figures with relative paths like `\input{../../output/tables/tab_foo.tex}` and set `\graphicspath{{../../output/figures/}}`.
- Never create a new top-level folder for LaTeX output (no `code/analysis/latex/`, no ad-hoc `figs/`). If `output/{tables,figures}` and `documents/<topic>/` don't fit a use case, pause and ask.

---

## Indexes (detail lives in linked files)

Look here first when you need project history, codebook entries, or prior decisions. Do not duplicate this content into CLAUDE.md — update the linked file instead.

- **Methodological decisions**: `notes/key_decisions.md`
- **Dropped analyses**: `notes/dropped_analyses.md`
- **Codebook (variable definitions)**: `notes/codebook.md`
- **Sample restrictions**: `notes/sample_restrictions.md`
- **Current status / next steps**: latest entry in `progress_logs/`
- **Referee 2 correspondence**: `correspondence/referee2/` (see `/referee2` skill)

---

## Notes for Claude

[Any specific instructions, quirks, or reminders for this project]
