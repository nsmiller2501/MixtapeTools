# Worker notes: bundle_005

## Source chunks
- chunk_012-a3-additional-robustness-checks.md — A3. Additional Robustness Checks

## Local extraction
- Research question / motivation evidence: None new in this chunk; robustness section only.
- Method / identification evidence: FRD (fuzzy regression discontinuity) with local-linear 2SLS throughout. Running variable is threshold-normalized PM concentration. Bandwidth varied across 16, 20, 24. Quadratic RV specifications also tested (Table A8). Alternative clustering schemes tested (Table A10). Falsification via placebo thresholds (subtract 20, 30, or 50 units from PM10/PM2.5).
- Target parameter evidence: Advisory indicator effect on per-capita respiratory and cardiovascular disease expenditures (cents per capita, 11.5 KRW = 0.01 USD), across age groups: Minors (0–19), Adults (20–64), Older Adults (65+), All.
- Data evidence: District-by-day observations, population weighted. South Korea. Panel RD design (atypical for RD). Weather controls: temperature, precipitation. Fixed effects: year-by-month and day-of-week (or year + month separately as robustness). Standard errors clustered by day of sample (baseline); alternative clusterings tested in Table A10.
- Statistical methods / specifications: 2SLS local-linear regressions; quadratic RV specification (Table A8); optimal bandwidths via Calonico, Cattaneo and Titiunik (2014, 2015) reported in Table A5; various sample restrictions for asymmetry/nighttime robustness (Table A7); spillover test via nearest-neighbor alert region (Table A11); placebo thresholds (Table A11).
- Findings:
  - Manipulation test: No missing density above RD threshold in daily or hourly running variable distributions (Figures A1, A2).
  - Control continuity: No discontinuity in temperature or precipitation at RD threshold (Figure A3).
  - Asymmetry robustness (Table A7): Excluding later alert days or alert days with RV < 0 does not change qualitative results.
  - Nighttime exclusion (Table A7): Dropping district-days with alerts issued between 6AM–9PM or 8AM–8PM yields similar-magnitude estimates.
  - Quadratic RV (Table A8): Health expenditure effects of similar magnitude and significance as main results. Example respiratory: Minors −18.220 (SE 11.167), Adults −7.586 (SE 3.221), Older Adults −7.718 (SE 4.404), All −9.607 (SE 4.337).
  - PM as dependent variable (Table A4): No discontinuous change in ambient PM10 or PM2.5 at RD threshold (coefficients near zero, large SEs), supporting interpretation that effects reflect avoidance behavior not ambient pollution reduction.
  - Air quality controls (Table A9): Adding PM10, PM2.5, both, or AQI has virtually no impact on RD estimates.
  - Clustering robustness (Table A10): All significant coefficients from Tables 4 and 5 remain significant across all clustering combinations.
  - Spillover test (Table A11): No statistically significant effect of neighboring region alerts on own-region outcomes — no spillover attenuation.
  - Falsification (Table A11): Placebo thresholds (−20, −30, −50 units) yield statistically insignificant estimates.
  - Dynamic effects by bandwidth (Table A6): 3-day rolling sum of resp./cardio. expenditures estimated at BW 16, 20, 24. Resp. (All): −14.688, −16.125, −12.693; Cardio. (Older Adults): −25.911, −30.388, −26.687 — consistent across bandwidths.
- Contributions: None new stated here; this section supports validity of main identification.
- Replication feasibility: Dependent on access to South Korean district-level health claims data and PM monitoring data. Bandwidth calculations use Calonico-Cattaneo-Titiunik (2014, 2015) rdrobust package (standard). Tables A1–A3 describe data context (global alert systems, Korean medical institution types, out-of-pocket payment schedule).

## Formal-object inventory
- Tables:
  - Table A1: Examples of air quality alert systems worldwide (China, South Korea, US, Canada, Australia, Mexico, Singapore, UK) with regions covered and estimated population covered.
  - Table A2: Types of medical institutions in South Korea (Tertiary/Secondary/Primary tiers).
  - Table A3: Out-of-pocket payment schedules for outpatient visits in South Korean healthcare system by institution type, age, location.
  - Table A4: FRD results using PM10 and PM2.5 as dependent variables at BW 16, 20, 24 — coefficients and SEs; all insignificant.
  - Table A5: Optimal bandwidths (Calonico et al.) for 16 outcome × age-group combinations; range ~17 to ~34.
  - Table A6: Dynamic effects (3-day rolling sum) with BW 16, 20, 24 for respiratory and cardiovascular outcomes by age group.
  - Table A7: Robustness to asymmetric alert threshold — excluding later alert days, RV<0 alert days, nighttime-only alerts (9PM–6AM and 8PM–8AM windows); respiratory and cardiovascular by age group.
  - Table A8: FRD coefficients with quadratic RV specification (partially shown — respiratory panel visible; cardiovascular panel likely continues beyond chunk).
- Figures:
  - Figure A1: Histogram of daily running variable; red line at RD threshold = 0; no missing density above threshold.
  - Figure A2: Histogram of hourly running variable; red line at RD threshold = 0; no missing density.
  - Figure A3: Continuity of control variables (temperature and precipitation) plotted against running variable in [−40, 40]; bins of width 5; population-weighted averages; no discontinuity at threshold.
- Equations/specifications: None explicitly labeled; 2SLS local-linear structure described in table notes throughout.
- Other formal objects: None.

## Bibliographic candidates
- doi: not present in this chunk
- authors: not present in this chunk
- title: not present in this chunk
- year: not present in this chunk
- venue: not present in this chunk

## Unresolved gaps
- Table A8 cardiovascular panel and any additional rows beyond the respiratory panel are cut off — chunk ends at line 170 mid-table; full quadratic-RV cardiovascular estimates not visible.
- Tables A9, A10, A11 are referenced in the text but not reproduced in this chunk; their numerical results are summarized in prose only.
- Figure images are embedded as `![](_page_N_Figure_N.jpeg)` references; actual histogram and scatter shapes not readable from markdown.
- Calonico, Cattaneo and Titiunik (2014, 2015) citations appear as in-text links (#page-17-10, #page-17-11) — full bibliographic details not in this chunk.
