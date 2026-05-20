# Worker notes: bundle_003

## Source chunks
- `/Users/noahmiller/.cache/claude-pdf-converter/cache/marker/5bf20b375d03a20fdc24387b2574c0eaf2d3d6096e98640dd57b1a84215b3917/substrate/chunks/chunk_009-references.md` — REFERENCES

## Local extraction
- Research question / motivation evidence: None new in this chunk; references confirm focus on air quality information, avoidance behavior, and health outcomes.
- Method / identification evidence: First-stage (Table 3): 1(RV≥0) coefficients ~0.618–0.636 across bandwidths 16–20–24; F-stats 46.0–89.7; Adj-R² ~0.708–0.728. Local-linear RD, population-weighted, SE clustered by running variable and by day of sample.
- Target parameter evidence: Tables 4–5 report reduced-form and 2SLS estimates for respiratory and cardiovascular health expenditures (US cents per capita; 11.5 KRW = 0.01 USD). Table 6 referenced in figure notes but not present in this chunk.
- Data evidence: Summary statistics (Table 2): full sample 53,363 district-day obs; bandwidth-40 sample 10,547 obs. Outcome variables: respiratory and cardiovascular per-capita expenditures by age group (minors 0–19, adults 20–64, older adults ≥65). Running variable is threshold-normalized PM function. Covariates: PM10 (mean 44.5 µg/m³ full / 68.4 bw-40), PM2.5 (mean 25.1 / 41.8), precipitation (mean 3.1 mm), temperature (mean 13.8 °C).
- Statistical methods / specifications: Local-linear RD, bandwidth 20 for main results (Tables 4–5); controls include running variable, RV×above-threshold interaction, temperature, precipitation, year-by-month FE, day-of-week FE. SE double-clustered: parentheses = clustered by RV value; square brackets = clustered by day of sample.
- Findings:
  - Table 3 first stage: alert probability rises ~0.62 when RV crosses threshold (strong first stage).
  - Table 4 (respiratory, 2SLS, BW=20): Minors −15.03 (SE 4.71/5.67), Adults −3.78 (2.20/2.13), Older Adults −4.30 (2.75/2.80), All −5.83 (2.40/2.50) cents per capita.
  - Table 5 (cardiovascular, 2SLS, BW=20): Minors −0.040 (0.032/0.035), Adults −2.83 (0.976/0.767), Older Adults −9.64 (3.85/3.68), All −3.26 (1.09/1.01) cents per capita.
  - Figure 5: lower bounds on gross health benefits by age group, scaled by 70% public coverage rate.
  - Figure 6: cost-benefit comparison across Baseline, Scenario A (alert at every threshold crossing), and Scenario B (lower PM2.5 threshold adopted July 2018); system maintenance cost line shown for 2016–2017.
- Contributions: None new stated in this chunk.
- Replication feasibility: Alert threshold rules stated precisely (Table 1). Korean AirKorea data sourced from https://www.airkorea.or.kr/. NAVER keyword search data used for Figure 2. OECD and Korean government sources cited. R package rdrobust (Calonico et al. 2015) used for RD inference.

## Formal-object inventory
- Tables:
  - Table 1 (p. 26): PM10 and PM2.5 advisory issuance/cancellation thresholds and behavioral guidelines by target group. Source: AirKorea (accessed Sep 30, 2021).
  - Table 2 (p. 27): Summary statistics at full sample and bandwidth=40; expenditure means/SDs by disease type and age group; treatment and covariate descriptives.
  - Table 3 (p. 28): First-stage regression results for bandwidths 16, 20, 24.
  - Table 4 (p. 29): RD results for respiratory diseases — reduced form and 2SLS, by age group, BW=20.
  - Table 5 (p. 30): RD results for cardiovascular diseases — reduced form and 2SLS, by age group, BW=20.
  - Table 6: Referenced in Figure 5/6 notes but not reproduced in this chunk.
- Figures:
  - Figure 1 (p. 20): Alert clusters for 7 major South Korean cities (Busan, Daejeon, Daegu, Gwangju, Incheon, Seoul, Ulsan); districts color-coded by cluster.
  - Figure 2 (p. 21): Daily alert counts (red) and NAVER keyword searches for air quality terms (blue), search index max = 100.
  - Figure 3 (p. 22): Treatment discontinuity — P(PM advisory) vs. running variable; bin width = 5 units, population-weighted.
  - Figure 4 (p. 23): Outcome discontinuity — residualized per capita health expenditures (US cents) vs. running variable; residualized for DOW, year×month, holiday, district FEs.
  - Figure 5 (p. 24): Lower bounds on gross health benefits by age group from Tables 4 and 5 (left) and Table 6 (right), scaled by 70% public coverage.
  - Figure 6 (p. 25): Cost-benefit comparison across Baseline / Scenario A / Scenario B; maintenance cost lines for 2016–2017 using 2017 and 2018 reference years.
- Equations/specifications: No named equations in this chunk; local-linear RD specification described in Table 3/4/5 notes.
- Other formal objects: None.

## Bibliographic candidates
- doi: not stated in this chunk
- authors: not restated here; inferred from output path: Anderson et al.
- title: not restated here
- year: 2022 (from output path)
- venue: NBER (from output path)

## Unresolved gaps
- Table 6 is referenced in Figures 5 and 6 notes but is not present in this chunk — its contents (likely additional RD results or heterogeneity estimates) are unobserved.
- Figure images are not rendered (placeholder `![](_page_XX_Figure_2.jpeg)`) — visual content of all six figures is unavailable.
- Paper DOI not found in this chunk; should be confirmed from front-matter chunk.
- Running variable construction (threshold-normalized PM function) is described qualitatively in figure notes but the exact formula is not in this chunk.
