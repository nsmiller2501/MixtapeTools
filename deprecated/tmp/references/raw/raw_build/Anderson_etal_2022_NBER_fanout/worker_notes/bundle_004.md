# Worker notes: bundle_004

## Source chunks
- chunk_010-references-part-2.md — REFERENCES part 2 (actual content: robustness/appendix tables 6–9)
- chunk_011-online-appendix-a1-generalization-of-theoretical-framework-a2-addition.md — Online Appendix / A1. Generalization of Theoretical Framework / A2. Additional Data Notes

## Local extraction
- Research question / motivation evidence: A1 extends the main theoretical model to show results hold when the running variable is an arbitrary function of daily PM (not just average daily PM), specifically justifying use of maximum 2-hour-minimum PM as the running variable.
- Method / identification evidence: RD with local-linear regression; 2SLS where advisory indicator instruments for treatment. Running variable defined as daily max of 2-hour-minimum PM minus alert threshold c (c=150 for PM10; c=90 or c=75 post-2018-03-27 for PM2.5), rounded to nearest integer. Bandwidth 20 used in main specs; 16 and 24 tested in robustness.
- Target parameter evidence: LATE of pollution advisory on healthcare expenditures (respiratory and cardiovascular), by age group (minors 0–19, adults 20–64, older adults 65+, all).
- Data evidence: N=2,530 in main specs (BW=20); N=1,857 (BW=16); N=3,380 (BW=24); N=2,443 after dropping late/early advisories; N=2,228 in dynamic spec excluding prior-day advisory days. Unit: district-by-day, population-weighted. Expenditures measured in cents per capita (11.5 KRW = 0.01 USD). PM2.5 example values: pmavg=22.7, pmhi=66.7, pmc=57.5.
- Statistical methods / specifications: Local-linear 2SLS; controls: running variable, RV×above-threshold interaction, temperature, precipitation, year-by-month and day-of-week FEs; SEs clustered by running variable and by day of sample (both reported). Table 6 uses 3-day cumulative spending (day t to t+2) to capture dynamic effects. Tables 7–8 extend main results to include tertiary general hospital visits. Table 9 varies bandwidth (16, 20, 24) and drops late/early advisories (cancelled before 9am or triggered after 7pm).
- Findings:
  - Table 6 (dynamic, 3-day): Respiratory—minors −38.2 cents/capita (SE 11.6), adults −10.7 (3.95), older adults −13.0 (4.95), all −16.1 (4.78). Cardiovascular—minors near zero, adults −5.28 (1.91), older adults −30.4 (12.2), all −8.04 (2.66). Effects persist when excluding subsequent alert days.
  - Table 7 (respiratory, including tertiary hospitals): 2SLS all-age −5.54 cents/capita (SE 2.37). Minors −14.1 (4.66), adults −3.64 (2.18), older adults −4.10 (2.70).
  - Table 8 (cardiovascular, including tertiary hospitals): 2SLS all-age −3.43 (SE 1.17). Minors near zero, adults −3.02 (1.02), older adults −9.69 (3.93).
  - Table 9 (robustness): Respiratory results stable across bandwidths and sample restrictions; cardiovascular effects for older adults somewhat sensitive to bandwidth choice (BW=24: −4.47 vs BW=20: −9.69).
- Contributions: A1 provides formal justification that information-provision welfare analysis extends beyond average-PM running variable to the actual max-2h-min-PM running variable used. A2 documents exact running variable construction steps and cost evaluation methodology for alert system.
- Replication feasibility: Running variable construction fully documented in A2 (4-step procedure). Cost data drawn from city-level environmental expenditure reports (Appendix Tables A12, A13). Sufficient detail for replication given access to raw PM monitoring data and NHI claims.

## Formal-object inventory
- Tables:
  - Table 6: Dynamic Impacts — 2SLS 3-day spending, respiratory and cardiovascular, by age group (N=2,530 main; N=2,228 excluding prior-alert days)
  - Table 7: RD Results for Respiratory Diseases including tertiary general hospitals — reduced form and 2SLS, by age group (N=2,530)
  - Table 8: RD Results for Cardiovascular Diseases including tertiary general hospitals — reduced form and 2SLS, by age group (N=2,530)
  - Table 9: Robustness Checks — 2SLS, bandwidths 16/20/24 and without late/early advisories, respiratory and cardiovascular by age group
  - Appendix Table A12 (referenced, not shown): Air Pollution Alert System cost items by city
  - Appendix Table A13 (referenced, not shown): Total alert system costs by city
  - Appendix Table A9 (referenced, not shown): Robustness with alternative air quality variable controls
- Figures: None in these chunks.
- Equations/specifications:
  - A1 eq. (individual beliefs): pm̄_i = pmavg if f(pm)↑c, pmhi if f(pm)↓c
  - A1 eq. (utility): U_i = U_i(a_i(pmavg), pmc) below threshold; U_i(a_i(pmhi), pmc) above
  - A1 eq. (ΔU_i): ΔU_i = [b_i(a_i(pmhi)) − b_i(a_i(pmavg))] − s_i^pvt [p_s(a_i(pmhi), pmc) − p_s(a_i(pmavg), pmc)]
  - A2 eq. (1): PM_dh^{2h min} = min_h{PM_d(h−1), PM_dh}
  - A2 eq. (2): PM_d^{2h min max} = max_d{PM_dh^{2h min}}
  - A2 eq. (3): rv_d = PM_d^{2h min max} − c
  - A2 eq. (4): rv_d rounded to nearest integer
- Other formal objects: None.

## Bibliographic candidates
- doi: not in these chunks
- authors: not in these chunks
- title: not in these chunks
- year: not in these chunks
- venue: not in these chunks

## Unresolved gaps
- chunk_010 is labeled "references-part-2" in the filename but contains tables 6–9, not bibliography entries; actual references section content may be in a prior chunk or mislabeled — worth confirming against chunk index.
- Appendix Tables A9, A12, A13 are referenced but not present in assigned chunks; their content (alternative air quality controls, city-level alert system costs) is not available for extraction.
- PM2.5 threshold change date (March 27, 2018: c changes from 90 to 75) noted in A2 but implications for sample splits or subperiod robustness not shown in these chunks.
- chunk_011 ends mid-section (after A2 cost evaluation paragraph); further appendix sections (A3+) are not included in this bundle.
