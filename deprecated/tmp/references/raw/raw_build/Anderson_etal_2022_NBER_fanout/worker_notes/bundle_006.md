# Worker notes: bundle_006

## Source chunks
- `/Users/noahmiller/.cache/claude-pdf-converter/cache/marker/5bf20b375d03a20fdc24387b2574c0eaf2d3d6096e98640dd57b1a84215b3917/substrate/chunks/chunk_013-a3-additional-robustness-checks-part-2.md` — A3. Additional Robustness Checks part 2

## Local extraction
- Research question / motivation evidence: None new; chunk is pure robustness appendix.
- Method / identification evidence: All tables use 2SLS local-linear RD with bandwidth = 20; running variable is pollution index; instrument is advisory indicator crossing the RD threshold. Observations at district-by-day level, population weighted. SE clustered by running variable or day of sample (table-specific, noted below).
- Target parameter evidence: FRD (fuzzy RD) coefficient on advisory indicator; dependent variables are respiratory or cardiovascular disease expenditures in cents per capita (11.5 KRW = 0.01 USD), by age group (Minors 0–19, Adults 20–64, Older Adults 65+, All).
- Data evidence: Seven major Korean cities: Gwangju, Daejeon, Daegu, Busan, Seoul, Ulsan, Incheon. Alert system management cost data from 2017–2018 municipal budgets (Table A12, A13).
- Statistical methods / specifications:
  - Partial table at top (continuation of prior chunk, no table number visible): quadratic RV, quadratic temperature, alternative time FE (year × month replaced by year + month FEs) — SE clustered by RV or day of sample.
  - Table A9: 32 2SLS regressions adding PM10, PM2.5, PM10+PM2.5, and AQI covariates (averaged across day); SE clustered by day of sample.
  - Table A10: 8 2SLS regressions, FRD coefficients fixed; reports SEs under 6 alternative clustering levels — province × day-of-week, province × day-of-sample, region × day-of-week, region × day-of-sample, district × day-of-week, district.
  - Table A11: 32 2SLS regressions — spillover test (advisory shifted to nearest alert region) and falsification tests (running variable shifted down by 20, 30, 50 units).
- Findings:
  - Partial table (spec modifications): respiratory illness "All" estimates range from −5.045 (alt. time FE) to −6.167 (baseline implied); cardiovascular "All" ranges −3.076 to −3.128. Estimates stable across quadratic RV, quadratic temperature, and alternative time FE.
  - Table A9 (pollution covariates added): respiratory "All" −5.353 to −5.510; cardiovascular "All" −3.076 to −3.174. Coefficients essentially unchanged by adding pollution controls.
  - Table A10 (clustering): respiratory "All" FRD = −5.829; cardiovascular "All" FRD = −3.259. SEs vary by cluster level but qualitative inference unchanged across all six alternatives.
  - Table A11 (spillover + falsification): spillover estimates near zero and insignificant for all age groups in both illness types (respiratory All = 0.147 (1.743); cardiovascular All = 0.074 (1.067)). All falsification placebo estimates (−20, −30, −50) near zero and insignificant — supports validity of RD threshold.
  - Table A13 (system costs): alert system management costs across 7 cities total $2,014,558 (2017) and $2,833,940 (2018 USD).
- Contributions: Collectively these appendix tables rule out: omitted pollution-covariate confounding, sensitivity to clustering choice, geographic spillovers, and spurious discontinuities at other cutoffs.
- Replication feasibility: Budget/cost data (Tables A12–A13) drawn from municipal records, 7 cities; may require FOIA-type request from Korean city governments. RD analysis tables require same district-by-day dataset as main results.

## Formal-object inventory
- Tables:
  - [Partial, no label visible] — Spec modifications (quadratic RV, quadratic temperature, alternative time FE); respiratory and cardiovascular, 4 age groups; SEs clustered by RV and by day of sample.
  - Table A9 — Robustness Check: Addition of Air Pollution Covariates (PM10, PM2.5, PM10+PM2.5, AQI); 32 2SLS regressions; SE clustered by day of sample.
  - Table A10 — Robustness Check: Standard Errors with Different Clusters; 8 2SLS regressions; 6 clustering schemes.
  - Table A11 — Robustness Check: Spillover Effect and Falsification Tests; 32 2SLS regressions; spillover + placebo at −20, −30, −50.
  - Table A12 — List of Budget Items Related to Alert System; 7 cities; itemized municipal budget line items.
  - Table A13 — Costs of the Air Pollution Alert System Management; 7 cities; total 2017 = $2,014,558, 2018 = $2,833,940.
- Figures: None.
- Equations/specifications: No new equations; specs match main text (2SLS local-linear, bandwidth 20, controls: RV, RV × above-threshold indicator, temperature, precipitation, year-by-month and day-of-week FEs).
- Other formal objects: None.

## Bibliographic candidates
- doi: not present in this chunk
- authors: not present in this chunk
- title: not present in this chunk
- year: not present in this chunk
- venue: not present in this chunk

## Unresolved gaps
- The partial table at the top of the chunk has no table number or heading visible — it is a continuation from the previous chunk (bundle_005 or earlier); the table label and full caption are missing here.
- Table A13 contains a typo "Toal" (should be "Total") in the row label — likely a transcription artifact; actual total values ($2,014,558 and $2,833,940) appear consistent with summing city rows.
- No references section present in this chunk; DOI and full bibliographic metadata must come from front_matter bundles.
