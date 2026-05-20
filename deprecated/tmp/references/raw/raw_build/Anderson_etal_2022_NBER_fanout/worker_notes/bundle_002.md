# Worker notes: bundle_002

## Source chunks
- chunk_005-iv-results-a-contemporaneous-effects.md — IV. Results / *A. Contemporaneous effects*
- chunk_006-b-dynamic-effects-c-robustness.md — *B. Dynamic effects* / *C. Robustness*
- chunk_007-v-discussion.md — V. Discussion
- chunk_008-vi-conclusion.md — VI. Conclusion

## Local extraction

- Research question / motivation evidence: Not restated here; body chunks focus on results. Conclusion reframes contribution as providing lower bounds on welfare gains from air pollution alert system (AQAS) via avoidance behavior, distinct from studies that combine alerts with emission reductions.

- Method / identification evidence: Fuzzy regression discontinuity (FRD) on running variable (PM level); threshold crossing raises alert probability by ~60 pp. First-stage F-statistics 25–50 across bandwidths 16/20/24. No significant change in measured PM at threshold, so effects attributed purely to avoidance behavior. Equations referenced: (5) first stage, (6) reduced form, (7) 2SLS, (8) 3-day rolling sum for dynamic effects. Local linear regressions; no higher-order polynomials following Gelman and Imbens (2019). Bandwidth sensitivity shown in Table 9.

- Target parameter evidence: Reduced-form and 2SLS estimates of health expenditure reductions (respiratory and cardiovascular) at RD threshold, by age group (minors <20, adults 20–64, older adults >64, all ages). Dynamic effects captured by 3-day rolling sums. Lower bound on gross benefits from reduction in *public* healthcare expenditures (public share ≈ 30% of total; copay:coverage ratio ≈ 7:3).

- Data evidence: South Korean AQAS data 2016–2017, seven major cities. Health expenditure data include private copayments + public coverage. Alert data: 134 unique alerts; 80 lasted >1 day; average alert length ≈ 1.87 days. Tertiary hospital outpatient visits excluded from main analysis (<15% of total outpatient expenditures) but included in robustness check. Policy comparison: PM2.5 threshold lowered from 90 µg/m³ to 75 µg/m³ starting July 2018.

- Statistical methods / specifications: FRD (first-stage + reduced form + 2SLS); bandwidths h = 16, 20 (preferred), 24; local linear in running variable; robustness to quadratic running variable, quadratic temperature, PM10/PM2.5/AQI controls, alternative time fixed effects, alternative clustering levels. McCrary density test for running-variable manipulation. Falsification tests at placebo thresholds ±20, ±30, ±50 from true threshold. Spatial spillover test using adjacent region's maximum running variable.

- Findings:
  - Contemporaneous: Alert reduces respiratory-illness spending for minors by ~15¢/capita (≈30% of mean below threshold, t = −3.2); aggregate respiratory reduction significant (t = −2.4). Alert reduces cardiovascular spending for adults 20–64 by ~2.8¢/capita (≈23%, t = −2.9) and older adults by ~9.6¢/capita (≈14%, t = −2.5); aggregate cardiovascular reduction significant (t = −3.0).
  - Dynamic (3-day rolling sum, Eq. 8): Coefficient magnitudes 2.5–2.8× contemporaneous; consistent with multi-day alert duration (avg 1.87 days) plus lagged avoidance benefits. Sample trimmed to avoid double-counting (drops alert days preceded by an alert day); trimmed coefficients 2.2–2.5× contemporaneous, 8–19% smaller than untrimmed dynamic.
  - Benefit aggregation: Total health expenditure reduction 2016–2017 ≈ $41M (contemporaneous), ≈$52M (dynamic). Public-expenditure lower bounds: respiratory $18.4M, cardiovascular $10.2M (dynamic: $24.5M and $12.2M). System cost ≈ $4M (2016–2017). Benefit:cost ratio ≈ 7.1:1 (contemporaneous), 9.2:1 (dynamic); net benefit ≈ $24.6M ($32.7M dynamic).
  - Policy simulation: Full compliance (sharp RD) adds $5.7M in expenditure reductions. Lowering PM2.5 threshold to 75 µg/m³ would have reduced total health expenditures by $76.5M (109% increase over baseline).
  - Age heterogeneity: Minors benefit most for respiratory; adults and older adults benefit most for cardiovascular. Dollar magnitudes: minors $12.6M, prime-age adults $20.4M, older adults $8M.

- Contributions: (1) First causal evidence of AQAS benefits beyond respiratory disease (cardiovascular effects for adults); (2) novel evidence that benefits extend to all adult age groups, not just children; (3) benefit-cost framework providing lower bounds on welfare gains; (4) shows pure avoidance-behavior mechanism (no PM change at threshold); (5) framework generalizable to other information-provision contexts (restaurant hygiene cards, electricity usage information).

- Replication feasibility: Core FRD specifications use standard local linear IV. Data are South Korean administrative health claims + government environmental expenditure reports; not publicly posted in paper but referenced via municipal government websites (Appendix Tables A12–A13). Bandwidth and specification sensitivity tables available in appendix. Alert timing robustness (dropped if cancelled before 9am or triggered after 7pm) reported.

## Formal-object inventory

- Tables:
  - Table 3: First-stage estimates of Eq. (5), bandwidths 16/20/24 (p. 28)
  - Table 4: Reduced-form and 2SLS estimates for respiratory disease, h = 20 (p. 29)
  - Table 5: Reduced-form and 2SLS estimates for cardiovascular disease, h = 20 (p. 30)
  - Table 6: Dynamic effects estimates, Eq. (8), 3-day rolling sum (p. 31)
  - Tables 7–8: Robustness — inclusion of tertiary outpatient visits (pp. 32–33)
  - Table 9: Robustness — bandwidth sensitivity + alert timing filter (p. 34)
  - Appendix Table A4: First-stage effect on average PM levels (no discontinuity)
  - Appendix Table A6: Dynamic effects across bandwidths 16/20/24
  - Appendix Table A7: Asymmetric alert issuance/cancellation threshold robustness
  - Appendix Tables A8–A9: Quadratic controls, AQI controls, alternative time FE
  - Appendix Table A10: Alternative clustering robustness
  - Appendix Table A11: Spatial spillover + placebo threshold tests
  - Appendix Tables A12–A13: Municipal government expenditure items and totals

- Figures:
  - Figure 3: Binned scatter, treatment probability vs. running variable (p. 22)
  - Figure 4: Binned scatter, health expenditures by running variable, 6 panels (respiratory/cardiovascular × minors/adults/older adults) (p. 23)
  - Figure 5: Lower bounds on gross benefits by age group (p. 24)
  - Figure 6: Net benefits under baseline + two policy scenarios (p. 25)
  - Appendix Figures A1–A2: Running variable density / manipulation tests
  - Appendix Figure A3: Covariate balance / discontinuity in controls

- Equations/specifications:
  - Eq. (5): First stage — alert probability on running variable + controls
  - Eq. (6): Reduced form — health expenditures on running variable indicator
  - Eq. (7): 2SLS — health expenditures instrumented by threshold crossing
  - Eq. (8): Dynamic FRD — 3-day rolling sum of health expenditures as dependent variable

- Other formal objects: Benefit-cost ratio calculations (p. 14–15); policy simulation parameterization (Scenarios A and B, p. 15).

## Bibliographic candidates
- doi: not stated in these chunks
- authors: not restated in these chunks (see front_matter bundle)
- title: not restated in these chunks
- year: not restated in these chunks
- venue: not restated in these chunks

## Unresolved gaps
- DOI/venue not present in any of these body/conclusion chunks — must be resolved from front_matter bundle.
- Appendix A2 (detail on cost data collection) referenced but not in assigned chunks; cost data sourcing may warrant checking.
- Replication data availability statement not located in these chunks; no data-availability section found in conclusion — may be in appendix or front matter.
- Public vs. private copayment ratio stated as "approximately 7:3" (private:public) in chunk_007; precise source for this ratio not cited inline — could affect lower-bound calculations.
- 2016 cost data assumed equal to 2017 ($2M); actual 2016 figure not available per authors (chunk_007, fn. 30).
