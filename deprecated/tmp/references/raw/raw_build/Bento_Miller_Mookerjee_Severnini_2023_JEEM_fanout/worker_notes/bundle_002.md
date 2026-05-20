# Worker notes: bundle_002

## Source chunks
- chunk_004-2-3-decomposition-of-meteorological-variables-climate-norms-vs-weather.md — *2.3. Decomposition of meteorological variables: Climate norms vs. Weather shocks*
- chunk_005-3-empirical-application-climate-impacts-on-ambient-ozone-3-1-conceptua.md — **3. Empirical application: Climate impacts on ambient ozone** / *3.1. Conceptual framework*

## Local extraction
- Research question / motivation evidence: Chunk 005 applies the framework to measure climate impacts on ambient ozone and adaptation in this context. Ozone is chosen because: (1) meteorological conditions drive ozone formation (NOx + VOCs + sunlight + warmth → ozone via Leontief-like reactions); (2) nationwide high-frequency data available 1980–2013; (3) policy-relevant "climate penalty" on ozone with implications for public health and labor productivity.
- Method / identification evidence: Chunk 004 operationalizes the decomposition from Eq. (6) via a first-stage regression (Eq. 9): x_it = γ_imy + ε_it, where temperature in location i on day t is regressed on location-by-month-by-year FE. The FE coefficients constitute climate norms x̄_imy; residuals are de-seasonalized weather shocks (x_it − x̄_imy). A lagged weighted average (Eq. 11) replaces the contemporaneous monthly average to form x̄_ip̄ ≈ x̄_imy, with weight scalars ω_j accommodating agent adaptation timelines. Frisch–Waugh–Lovell theorem (Lovell 1963, Theorem 4.1) invoked to show the outcome variable need not be de-seasonalized if regressors are, permitting simultaneous estimation of both effects in Eq. (6).
- Target parameter evidence: The approach simultaneously estimates (a) the response to weather shocks (x_it − x̄_ip̄) and (b) the response to climate norms x̄_ip̄. Adaptation is identified as the difference between these two coefficients — i.e., the difference between points A′ and C in Fig. 1.
- Data evidence: Daily ozone measurements and meteorological data for the U.S. ozone season (typically April–September), 1980–2013. Nationwide network of weather monitors. Correlation between x̄_ip̄ and x̄_imy > 0.95; correlation between (x_it − x̄_ip̄) and (x_it − x̄_imy) > 0.90 (fn. 19).
- Statistical methods / specifications: First-stage decomposition regression Eq. (9) with location × month × year FE; Eq. (10) partitions Temp into Temp^C (climate norm) and Temp^W (weather shock); Eq. (11) defines the lagged weighted norm x̄_ip̄ = (1/J)∑_{j=1}^{J<y} ω_j x̄_imj. Flexible weighting ω_j allows myopic (only last year), bounded, or rational agent assumptions.
- Findings: (Conceptual/setup chunks — empirical results not yet reported.) Fig. 1 illustrates theoretical prediction: agent facing transitory shock of T^3 produces at A′ (higher ozone); agent facing permanent climate norm shift to T^3 adapts to schedule 2 and produces at C (lower ozone than A′, but higher than A). Adaptation is not costless.
- Contributions: Shows decomposition is agnostic about whether agents are rational, myopic, or inattentive (chunk 004, p. 5). Notes the decomposition is a first-order Taylor approximation of a potentially nonlinear temperature–outcome relationship; magnitude of temperature shocks (deviations from 30-year moving average) found to be relatively stable over time in the data.
- Replication feasibility: Data are described as publicly available (daily ozone + meteorological data, U.S., 1980–2013). First-stage FE regression is standard. Eq. (11) weights ω_j must be specified by researcher; paper mentions 30-year climate normal convention (WMO / Climatology Office 2003) and band-pass filter alternatives (Baxter–King 1999; Christiano–Fitzgerald 2003).

## Formal-object inventory
- Tables: None in these chunks.
- Figures: Fig. 1 (p. 7) — "Theoretical relationship between marginal cost of dirty production and temperature." Illustrates cost-minimizing production schedules 1 and 2 as a function of temperature T; left y-axis = cost of production, right y-axis = associated ozone concentration; x-axis = temperature. Points A (T^1, schedule 1), B (T^2, indifferent), C (T^3, schedule 2), A′ (T^3 shock without adaptation) marked. Dashed gray line = long-run equilibrium envelope.
- Equations/specifications:
  - Eq. (9): x_it = γ_imy + ε_it (first-stage FE decomposition; p. 4)
  - Eq. (10): Temp = Temp^C + Temp^W, i.e., x_it = x̄_imy + (x_it − x̄_imy) (p. 4)
  - Eq. (11): x̄_ip̄ ≡ (1/J)∑_{j=1}^{J<y} ω_j x̄_imj ≈ x̄_imy (lagged weighted climate norm; p. 4–5)
  - Eq. (6): Referenced but defined in earlier chunk (not in this bundle).
- Other formal objects: Lovell (1963) Theorem 4.1 quoted in full in fn. 20 (p. 4–5). Footnote 19 reports correlations: corr(x̄_ip̄, x̄_imy) > 0.95; corr((x_it − x̄_ip̄), (x_it − x̄_imy)) > 0.90.

## Bibliographic candidates
- doi: not visible in these chunks
- authors: not restated in these chunks (see front_matter bundle)
- title: not restated in these chunks
- year: not restated in these chunks
- venue: not restated in these chunks

## Unresolved gaps
- Eq. (6) is central (referenced 6+ times) but defined in an earlier chunk (chunk_003 or earlier) — not present in this bundle; synthesizer must pull definition from front_matter/earlier body bundle.
- Fig. 1 image renders as a placeholder (`![](_page_7_Figure_2.jpeg)`); actual figure not extractable from markdown — visual content described only via caption.
- Specific values of ω_j used in the paper's preferred decomposition are not stated here; presumably given in Section 3.2 or later (not in this bundle).
- "Appendix A.1" referenced (chunk 005, fn. 22) for ozone chemistry details — content not in this bundle.
- Robustness checks mentioned re: regulations not playing an important role in adaptation (fn. 27) — results not yet in these chunks.
