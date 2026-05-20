# CLAUDE.md — JMP_revision

**Project:** JMP_revision
**Researcher:** Noah Miller
**Created:** 2026-03-18

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

**Policy-Induced Defensive Action: The Role of Information in Reducing the Healthcare Burden of Air Pollution.** The paper jointly estimates the health impacts of (i) *expected* long-run ozone (the pollution norm $P$) and (ii) *unexpected* daily ozone shocks ($\epsilon$), using the norm–shock gap $\beta^S - \beta^N$ to recover the sum effectiveness of agents' **intrinsic ex-ante defensive actions** — all behavioral and medical adjustments taken against anticipatable pollution. It then compares this with **policy-induced defensive action** from air-quality alert programs, testing whether the two channels substitute or complement and bounding the welfare value of the alert program.

The conceptual framework combines Grossman (1972) health-capital with the Carleton et al. (2024) climate-adaptation decomposition: an ex-ante defensive stock $k$ (chosen in a pre-period based on $P$) and contemporaneous defensive action $b$ (chosen after $\rho_t$ is realized). The envelope theorem identifies $\beta^S - \beta^N$ as the net health effect of $k$, accounting for any rational crowding-out of $b$ by $k$ in health production. The alert program is modeled as an information intervention that expands the agent's information set about $\epsilon_t$; following Anderson, Hyun, and Lee (2022), the alert coefficient $\beta_A$ on government-borne costs identifies the fiscal externality $\Delta E$ and provides a lower bound on the social welfare gain. OOP-cost estimates bound WTP from above.

An extension sketch considers three amendments (imperfect knowledge of $P$, joint choice of $k$ with information acquisition, salience/attention) under which alert-program *introduction* could shift $k^*$. The preferred route is to lead with the joint-choice extension, tied to the $k$–$b$ substitutability primitive $\phi = \partial^2 h/\partial k \partial b$, with the imperfect-$P$ channel as a footnote.

### Research Question

What are the respective health and fiscal benefits of individuals' intrinsic defensive actions vs. information-based alert policies against ambient ozone exposure? Specifically:

1. Do individuals intrinsically engage in ex-ante defensive actions?
2. Do air quality alerts induce additional defensive actions?
3. What is the welfare value of the alert programs?

### Data Sources

County-day panel, ozone season (April–September), 2004–2017, contiguous United States (~1.91M county-day observations across 879 counties).

- **Medicare MedPAR** fee-for-service inpatient claims — 4-day admissions count + cost of care, decomposed into government share (fiscal externality $\Delta E$) and out-of-pocket share (WTP upper bound)
- **EPA AQS** ozone (parameter 44201, daily 8-hr max; 1980–2017 used to construct backward-looking norms) plus co-pollutants PM2.5, CO, NO2, SO2
- **Di et al. (2019)** satellite-derived PM2.5 (1 km, 2000–2016)
- **EPA AirNow AQAD** air-quality alerts (binary $A_{it}$; CBSA reports mapped to counties)
- **NARR** wind fields (3-hourly, 32 km) — used to construct instruments
- **PRISM** temperature and precipitation (4 km, daily)
- **ASOS/AWOS** surface visibility (information-channel control)

### Identification Strategy

- **Frisch–Waugh–Lovell decomposition** (Bento et al. 2023): daily ozone $\rho_{it} = P_{im} + \epsilon_{it}$, where $P_{im}$ is a 5-year backward moving average for the same county × calendar month (lagged ≥1 year), and $\epsilon_{it}$ is the transitory shock.
- **Wind-direction IV** (Deryugina et al. 2019): daily wind direction instruments the shock; historical monthly wind-direction shares instrument the norm.
- County-by-season and state-by-year fixed effects; flexible weather controls (temperature × precipitation × wind-speed bins); visibility control to net out pollution-information from visible haze; three leads/lags of instruments; standard errors clustered at the county level; population-weighted by daily FFS beneficiaries.
- Key estimating equation: $h_{it} = \beta^S (\rho_{it} - P_{im}) + \beta^N P_{im} + \beta_A^S (\rho_{it}-P_{im}) A_{it} + \beta_A^N P_{im} A_{it} + \beta_A A_{it} + X'_{it}\gamma + \alpha_{is} + \delta_{ky} + \nu_{it}$.
- Mapping to model objects: $\beta^S - \beta^N$ = net health benefit of ex-ante defensive action; $\beta_A$ = infra-marginal level shift on alert days, with $\beta_A$ on government-share costs = $\Delta E$ (lower bound on $\Delta W$); program-activation interactions $\beta_P^S - \beta_P^N$ test whether alert-program introduction shifts $k^*$.

---

## Key Files

- **Main analysis**: `./code/analysis/README.md` [not yet written]
- **Data cleaning**: `./code/data/README.md`
- **Paper draft**: `./documents/manuscript.tex` [not yet written]
- **Presentation**: `./decks/jmp_presentation/jmp_presentation.tex`
- **Reference PDFs**: `./references/raw/` stores papers and other PDFs for `/split-pdf`, `/read-pdf`, `/bib-update`, and `/wiki-update`.
- **Central BibTeX file**: `./references/references.bib` (maintained by `/wiki-update`; cite from any `.tex` via `\bibliography{<relative-path>/references/references}`)
- **Reference wiki**: `./references/wiki/` is created and maintained lazily by `/wiki-update`.

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

- **Methodological decisions**: `agent_memory/key_decisions.md`
- **Dropped analyses**: `agent_memory/dropped_analyses.md`
- **Codebook (variable definitions)**: `agent_memory/codebook.md`
- **Sample restrictions**: `agent_memory/sample_restrictions.md`
- **Current status / next steps**: latest entry in `progress_logs/`
- **Referee 2 correspondence**: `correspondence/referee2/` (see `/referee2` skill)
- See `references/CLAUDE.md` for wiki conventions and the project's reference library.

---

## Notes for Claude

[add project specific quirks here, either manually or by telling claude to when discovering something in a session]
