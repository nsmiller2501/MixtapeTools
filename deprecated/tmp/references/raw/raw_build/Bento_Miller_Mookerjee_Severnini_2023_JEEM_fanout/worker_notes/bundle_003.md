# Worker notes: bundle_003

## Source chunks
- chunk_006-3-2-data-3-3-empirical-strategy.md — *3.2. Data* / *3.3. Empirical strategy*
- chunk_007-4-results-span-id-page-11-0-span-4-1-impacts-of-temperature-on-ambient.md — **4. Results** / *4.1. Impacts of temperature on ambient ozone concentration*

## Local extraction
- Research question / motivation evidence: How does temperature (decomposed into climate norms and weather shocks) affect ambient ozone concentration, and how much adaptation by economic agents offsets the long-run climate effect?
- Method / identification evidence: Temperature decomposed into (1) climate norm = lagged 30-year monthly moving average (Eq. 12) and (2) weather shock = deviation of daily temperature from that norm. Main estimating equation is Eq. (13): `Ozone_it = β_W Temp_it^W + β_C Temp_ip̄^C + X_it'δ + φ_is + ε_it`, with monitor-by-season-by-year fixed effects (φ_is). Adaptation measure = β̂_W − β̂_C. Benchmarked against standard panel fixed-effects (column 2) and cross-sectional approaches (column 3).
- Target parameter evidence: β_W (weather shock effect on ozone), β_C (climate norm effect on ozone), and implied adaptation = β̂_W − β̂_C. Full adaptation would imply β̂_C = 0.
- Data evidence: Weather: NOAA Global Historical Climatology Network, daily max temperature and total precipitation, 1950–2013, 20,000+ stations. Matching algorithm: two closest stations within 30 km of each ozone monitor (covers 97.25% of daily ozone obs, 97.91% of monitors); expanded to five stations within 80 km covers >99.99%. Ozone: EPA air quality monitoring stations, daily readings, unbalanced panel, 1980–2013. Final unbalanced sample: ozone monitors 1980–2013. Analysis focuses on daily max temperature vs. daily max ozone concentration, ozone season = April–September.
- Statistical methods / specifications: OLS panel regression (Eq. 13) with monitor-by-season-by-year FE. Controls include decomposed precipitation (norm + shock). Robustness: balanced panel, 3/5/10/20-year MAs, daily MAs, extended lag lengths, monitor-by-season-by-year-by-weekday/end FE, Ozone Action Day checks. Standard errors clustered at county level (columns 1–2); heteroskedastic robust (column 3). N = 5,139,523 (columns 1–2); 2,712 (column 3).
- Findings: Col (1) unifying approach: temperature shock → +1.678 ppb ozone per °C (SE 0.063***); climate norm → +1.164 ppb per °C (SE 0.051***); implied adaptation = 0.514 ppb (SE 0.041***). Col (2) panel FE: max temperature → +1.659 ppb (SE 0.063***). Col (3) cross-section: avg max temperature → +1.166 ppb (SE 0.106***). Shock and norm estimates replicate col (2) and col (3) respectively, consistent with Frisch–Waugh–Lovell. Climate penalty under RCP 8.5: +1.9 ppb by 2050 (1.6°C increase), +5.6 ppb by 2100 (4.8°C increase); wrongly using shock coefficient gives 2.7–8 ppb. R² = 0.481 (col 1), 0.542 (col 2), 0.352 (col 3).
- Contributions: Demonstrates that the unifying decomposition approach recovers both weather-shock and climate-norm effects in one regression; shows cross-sectional approach can over-estimate adaptation by >100% on balanced sample; provides adaptation measure (β_W − β_C = 0.514 ppb) as causal estimate.
- Replication feasibility: Data sources are public (NOAA GHCN, EPA air quality monitors). Matching algorithm detailed in Appendix A.2. Robustness tables in Appendices B and C. Large N (5.1M obs) but replication feasible from public sources.

## Formal-object inventory
- Tables: Table 1 — "Climate impacts and adaptation — our unifying approach vs. Prior approaches" (p. 12); columns: (1) Unifying, (2) Fixed-Effects, (3) Cross-Section; outcomes: daily max ozone levels (ppb); N = 5,139,523 / 5,139,523 / 2,712; R² = 0.481 / 0.542 / 0.352.
- Figures: Fig. 2 (p. 9) — Climate norms and shocks, US 1980–2013, Panel A = norm, Panel B = shock (unbalanced panel of weather stations, April–September). Fig. 3 (p. 11) — Decomposition of temperature norms & shocks, Los Angeles 2013, Panel A = preferred decomposition, Panel B = standard FE decomposition.
- Equations/specifications: Eq. (12) — definition of climate norm x̄_ip̄ = (1/30)Σ x̄_imj for j = y−30 to y−1 (30-year monthly MA lagged 1 year). Eq. (13) — main econometric model: Ozone_it = β_W Temp_it^W + β_C Temp_ip̄^C + X_it'δ + φ_is + ε_it. References Eq. (6) (generalized model, prior chunk) and Eq. (2) (standard FE approach, prior chunk).
- Other formal objects: Appendix A: Figs A1–A9, Tables A1–A3. Appendix B.1: Tables B2, B4. Appendix C: derivation of within-season and across-year variation in climate norm under monitor-by-season-by-year FE.

## Bibliographic candidates
- doi: (not present in these chunks)
- authors: (not present in these chunks — see front matter)
- title: (not present in these chunks — see front matter)
- year: 2023 (implied by JEEM citation in bundle id; not directly stated in these chunks)
- venue: Journal of Environmental Economics and Management (JEEM, implied by bundle id)

## Unresolved gaps
- Eq. (6) referenced repeatedly (chunk_006, p. 10; chunk_007, p. 12 Table 1 notes) but defined in a prior chunk — confirm β_W and β_C sign conventions match Eq. (6) setup.
- Eq. (2) (standard FE approach) referenced in Fig. 3 caption but defined in a prior chunk.
- Cross-sectional bias direction: chunk_007 (p. 12) notes upward and downward biases may coexist (Griliches 1977); balanced-sample result showing >100% over-estimation is in Appendix B.1 Table B2 (not in assigned chunks).
- DOI and full author list not present in these chunks; rely on front-matter bundle.
- Ozone Action Day robustness result mentioned (chunk_006, p. 10, fn 39) but not tabulated in assigned chunks — in Appendix B.
- Precipitation decomposition controls included in X_it (fn 43) but coefficients not reported in Table 1; available upon request per text.
