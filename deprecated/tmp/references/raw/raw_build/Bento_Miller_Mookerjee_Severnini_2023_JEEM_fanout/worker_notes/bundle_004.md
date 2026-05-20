# Worker notes: bundle_004

## Source chunks
- chunk_008-span-id-page-13-0-span-4-2-measuring-adaptation-to-climate-change-4-3.md — *4.2. Measuring adaptation to climate change* / *4.3. Robustness checks*
- chunk_009-4-4-estimating-nonlinear-effects-of-temperature.md — *4.4. Estimating nonlinear effects of temperature*
- chunk_010-4-5-exploring-heterogeneity-5-concluding-remarks.md — *4.5. Exploring heterogeneity* / **5. Concluding remarks**

## Local extraction

- **Research question / motivation evidence:** Chunks 8–10 confirm the core question: how does climate change affect ambient ozone, and how much do economic agents adapt? Section 4.2 introduces the adaptation measure directly; Section 5 restates the four main findings.

- **Method / identification evidence:**
  - Adaptation measure = difference between weather-shock coefficient and climate-norm coefficient (βW − βC). Preferred spec: 30-year MA lagged 1 year as climate norm; deviations from MA as weather shock (Eq. 13, defined in earlier chunks).
  - Robustness: alternative MA lengths (3, 5, 10, 20 yr); alternative lag structures (10- and 20-year lags); Ozone Action Day (OAD) interaction for short-run adaptive response.
  - Nonlinear extensions: quadratic (Eq. 14), cubic, and 5 °C binned specifications. Marginal adaptation under quadratic given by Eq. 15; simplifies to Eq. 16 when weather shock ≈ 0.
  - Heterogeneity analyses in Appendix B.2: over time (Fig. B1, Table B8); by belief in climate change (Tables B9–B11); by NOx/VOC precursor limitation (Table B12).
  - FWL theorem invoked as the identification device enabling simultaneous short- and long-run estimation.

- **Target parameter evidence:**
  - Primary: adaptation = βW − βC = 0.51 ppb per 1 °C (from Section 4.1/4.2).
  - Ignoring adaptation overestimates "climate penalty" by ~44%.
  - Under RCP 8.5: overestimation of 0.82 ppb by mid-century, 2.47 ppb by end of century.

- **Data evidence:** Full sample N ≈ 5,139,523 obs (Table 2 cols 1–4). OAD subsample: 1,879,041 obs (2004–2013, ~35–36% of full sample). Panel is unbalanced (preferred; noted as more nationally representative vs. semi-balanced, Table B2).

- **Statistical methods / specifications:**
  - Main: county FE + time FE (λs), clustered SEs at county level.
  - Bootstrapped SEs in Table B5; state-level clustering doubles magnitude but does not change significance.
  - Measurement error robustness: Solon (1992) argument — longer MA windows reduce mismeasurement of permanent component; coefficients stable across 3–30 yr windows (Table 2 cols 1–4).
  - Blanc & Schlenker (2017) point on FE magnifying attenuation bias noted; mild attenuation seen moving from 20- to 30-yr MA.
  - OAD interaction: coefficient on Shock × Action Day = 0.068 (SE 0.188), statistically insignificant → negligible short-run adaptive response.

- **Findings:**
  1. 1 °C temperature shock → +1.68 ppb ozone (consistent with standard FE estimate).
  2. 1 °C increase in 30-yr MA → +1.16 ppb ozone.
  3. Adaptation = 0.51 ppb (statistically and economically significant); stable across MA-length robustness checks (range 0.495–0.542 ppb in Table 2).
  4. Nonlinear (binned) spec: ozone/temperature response increasing at increasing rate at low temps, increasing at decreasing rate at high temps. Agents exert extra adaptive effort at highest temperatures ("normal u" shape for marginal adaptation, Fig. 4 Panel E).
  5. Linear spec provides adequate first-order approximation; quadratic mis-specifies; cubic and binned are preferred for nonlinear analysis.
  6. No meaningful short-run adaptive response detected via OAD alerts.

- **Contributions:**
  - Unifying framework bridging cross-sectional and panel FE strands of climate-economy literature.
  - Direct, statistically testable adaptation measure derived from same fixed-effects equation.
  - Overcomes Lucas Critique problem of time/space extrapolation by comparing same economic agents.
  - Applied to ambient ozone: shows adaptation overestimation of ~44% matters for climate penalty projections.

- **Replication feasibility:**
  - Sample period 1980–2013; N = 5,139,523 obs (unbalanced panel).
  - Data sources: EPA ozone monitors, temperature data, EPA OAD alerts (from 2004).
  - All robustness appendix tables (B1–B12) and figures (B1, Fig. 4) appear to be in the paper/appendix.
  - Binned spec details: 5 °C bins, lowest bin <20 °C, highest >35 °C, middle bin 25–30 °C (median 27.8 °C, mean 27.1 °C).

## Formal-object inventory

- **Tables:**
  - Table 2 (p. 14): Key robustness checks — 7 columns (alternative MA lengths cols 1–4; lagged adaptive response cols 5–6; OAD short-run col 7). Reports temperature shock, climate norm, implied adaptation, Shock × Action Day coefficients; N and R².
  - Table B1: Sensitivity to ozone/temperature monitor matching algorithm.
  - Table B2: Semi-balanced panel robustness.
  - Table B3: Exclusion of regions with targeted ozone-precursor policies.
  - Table B4: Four additional checks (daily MA, monthly aggregation, wind/sunlight controls, OTR exclusion/inclusion).
  - Table B5: Bootstrapped and state-level clustered SEs.
  - Table B6: Binned specification coefficients (col 1) and implied adaptation (col 2).
  - Table B7: Adaptation comparison across linear, binned, quadratic, cubic specs.
  - Tables B8–B11: Heterogeneity by time and belief in climate change.
  - Table B12: Attenuation by NOx/VOC precursor limitation.

- **Figures:**
  - Fig. 4 (p. 17): Comparing linear, binned, quadratic, cubic specs. Five panels: A (ozone vs. climate across temp distribution), B (ozone vs. weather), C (marginal climate impact), D (marginal weather impact), E (marginal adaptation — "normal u" for binned/cubic). Top/bottom 1% of temp distribution trimmed.
  - Figure B1: Heterogeneity in adaptive behavior over time (Appendix B.2).

- **Equations/specifications:**
  - Eq. 13: Main estimating equation (defined in earlier chunks; referenced throughout).
  - Eq. 14 (p. 15, anchor page-15-5): Quadratic extension — adds βW2(xit − x̄ip̄)² + βC2(x̄ip̄)².
  - Eq. 15 (p. 15, anchor page-15-2): Marginal adaptation under quadratic model = (βW − βC) + 2(βW2(xit − x̄ip̄) − βC2(x̄ip̄)).
  - Eq. 16 (p. 15, anchor page-15-4): Marginal adaptation at weather shock ≈ 0 = βW − βC − 2βC2(x̄ip̄).
  - Cubic model: adds βW3(xit − x̄ip̄)³ + βC3(x̄ip̄)³ terms; adaptation adds 3(βW3(xit − x̄ip̄)² − βC3(x̄ip̄)²).

- **Other formal objects:**
  - Footnote 50: Caveat that future climate penalty predictions require extrapolation; adaptation measure itself does not.
  - Footnote 51: OAD coefficient interpretation; sample size difference (cols 5–6 vs. col 7 in Table 2).
  - Footnote 52: Mathematical note on interaction effects in higher-order models.
  - Footnote 53: Marginal effect constrained within bin, varies across bins (piece-wise linear).
  - Footnotes 54–56: Temperature bin cutoffs; graphing assumptions (shock = 0 for climate panel; norm = 27.5 °C for shock panel); Table B7 reference.

## Bibliographic candidates
- doi: (not present in assigned chunks — defer to front-matter bundle)
- authors: (not restated in assigned chunks)
- title: (not restated in assigned chunks)
- year: (not restated in assigned chunks)
- venue: (not restated in assigned chunks)

## Unresolved gaps
- Eq. 10 and Eq. 13 (referenced repeatedly) are defined in earlier chunks, not in this bundle — confirm labels and exact forms from bundles 001–003.
- Fig. 4 image is present as a placeholder (`![](_page_17_Figure_2.jpeg)`) but not rendered — verify panels A–E content from synthesis or direct image read.
- Appendix B tables (B1–B12) and Figure B1 are referenced but not in assigned chunks — confirm whether they appear in a back_matter bundle.
- Specific heterogeneity results (Tables B9–B11 on climate-change beliefs; Table B12 on NOx/VOC) are noted but not described quantitatively in assigned chunks.
- Solon (1992) and Blanc & Schlenker (2017) cited for measurement-error arguments — full references not recoverable from this bundle; flag for citation-overlap check.
