# Worker notes: bundle_001

## Source chunks
- chunk_001-nber-working-paper-series-bounds-benefits-and-bad-air-welfare-impacts.md — NBER Working Paper Series / Abstract / Introduction
- chunk_002-i-background-and-data.md — I. Background and data
- chunk_003-ii-theoretical-framework.md — II. Theoretical framework
- chunk_004-iii-regression-discontinuity-design.md — III. Regression discontinuity design

## Local extraction
- Research question / motivation evidence: What are the welfare impacts of air-quality alert systems (AQAS)? Despite AQAS covering >1.7 billion people worldwide, there has been little empirical welfare analysis. Paper focuses on South Korea's 2015 AQAS covering 51 million people. Also motivated by potential welfare consequences of air-quality data manipulation observed in other contexts.
- Method / identification evidence: Regression discontinuity (RD) design exploiting PM alert issuance thresholds. Running variable = daily maximum of 2-hour minimum PM values, normalized by respective thresholds (PM2.5: 90 µg/m³; PM10: 150 µg/m³), so treatment threshold = 0. Fuzzy RD (FRD) because alerts not mechanically determined by threshold (weather conditions also considered; issuance/cancellation thresholds differ). First-stage Eq.(5) and reduced-form Eq.(6); FRD LATE recovered via 2SLS (Eq. 7: τ̂_FRD = β̂₁/γ̂₁). Dynamic effects addressed via rolling 3-day sum specification Eq.(8). Default bandwidth h=20 (CCT-optimal range: 17–22; results shown at 16, 20, 24).
- Target parameter evidence: Lower bound on net social benefits of AQAS (net of avoidance behavior costs). Key insight: ΔW_i = ΔU_i + ΔE_i; since ΔU_i ≥ 0 (more accurate PM info weakly increases private utility), ΔE_i is a lower bound on social net benefits. ~70% of health expenditures are publicly reimbursed externalities. LATE = effect of alert on health expenditures for compliers near threshold.
- Data evidence: Daily per-capita health spending by district, 2016–2017, from National Health Insurance Service (NHIS) of South Korea (covers entire population). 10% random sample from 7 major cities (Seoul, Busan, Daegu, Daejeon, Incheon, Gwangju, Ulsan); combined population ~23 million (44% of South Korea); ~2.3 million individuals in sample. Spending by disease type: cardiovascular (ICD-10 "I") and respiratory (ICD-10 "J"); age groups: minors (0–19), adults (20–64), older adults (65+). 230 region-days / 1,427 district-days with alerts during 2016–2017; 73 districts, 14 alert regions. Excludes inpatient stays and tertiary outpatient visits from main analysis (temporal lag issues). Data access restricted to South Korean data centers; no processed data can be shared per NHIS rules.
- Statistical methods / specifications: Fuzzy RD with linear polynomial in running variable (baseline), quadratic as robustness check. Controls: temperature, precipitation (X₁ᵢₜ); year-month, day-of-week, holiday fixed effects (X₂ₜ); district fixed effects (δᵢ). Population-weighted regressions. Standard errors clustered by running-variable value or date (use whichever is larger for conservative t-stats). Adjusted R² ~0.8–0.9 in outcome regressions. Dynamic spec (Eq. 8) uses rolling 3-day sum Y⁺ᵢₜ = Σ_{s=0}^{2} Yᵢ,ₜ₊ₛ; omits days following an alert day to avoid double-counting in policy simulations. Robustness check trims days following alert days.
- Findings (from abstract): Alert issuance reduced youth respiratory expenditures by 30% and adult cardiovascular expenditures by 23%. Overall system reduced externalized health expenditures by $28.6 million (2016–2017); minimum benefit-cost ratio 7.1:1. Including dynamic impacts: $36.7 million in minimum benefits; benefit-cost ratio 9.2:1.
- Contributions: (1) First welfare analysis of AQAS (as opposed to general air-quality monitoring); uses health expenditures (not visit counts/deaths) + theoretical bounds framework to estimate net benefits net of avoidance behavior costs. (2) First RD design to study health outcomes from AQAS (prior work used time-series/panel variation). (3) Context more representative of developing/middle-income country pollution levels than prior literature.
- Replication feasibility: LOW — health spending micro-data restricted to South Korean NHIS data centers; NHIS prohibits sharing processed data. Alert data from KECO website (public). PM monitor data retrievable. Code/specifications fully described but cannot run on external machines.

## Formal-object inventory
- Tables: Table 1 (alert thresholds and recommended behaviors; p.26/A1); Table 2 (health spending data summary; p.27); Appendix Table A1 (alert system examples); Appendix Table A2 (medical institution type definitions); Appendix Table A3 (insurance coverage by treatment location); Appendix Table A4 (PM levels at RD threshold — confirms no discontinuity in PM itself); Appendix Table A5 (CCT optimal bandwidths, range 17–22); Appendix Table A7 (FRD results excluding issuance/cancellation threshold overlap cases); Tables 4 and 5 (main outcome regressions — referenced but not yet in these chunks)
- Figures: Figure 1 (PM alert regions within cities; p.20); Figure 2 (NAVER search keyword spikes on alert days; p.21)
- Equations/specifications:
  - Eq. (1): Utility function U_i(a_i, pm) = b_i(a_i) − s_i^{pvt} · p_s(a_i, pm)
  - Eq. (2): ΔU_i = [b_i(a_i(pm^{hi})) − b_i(a_i(pm^{avg}))] − s_i^{pvt}[p_s(a_i(pm^{hi}),c) − p_s(a_i(pm^{avg}),c)]
  - Eq. (3): W_i = U_i(a_i, pm) + E_i
  - Eq. (4): ΔW_i = ΔU_i + ΔE_i
  - Eq. (5): First-stage FRD regression (Alert_it on 1(PM̃≥0), PM̃, PM̃·1(PM̃≥0), controls, FEs)
  - Eq. (6): Reduced-form regression (Y_it on same RHS)
  - Eq. (7): τ̂_FRD = β̂₁/γ̂₁ (FRD LATE via 2SLS)
  - Eq. (8): Dynamic reduced-form using rolling 3-day Y⁺_it
- Other formal objects: Appendix A1 (theoretical generalization to non-PM running variable); Appendix A2 (running variable calculation details); IRB: Korea National Institute for Bioethics Policy IRB P01-201811-22-008

## Bibliographic candidates
- doi: not stated in these chunks; NBER working paper URL: http://www.nber.org/papers/w29637
- authors: Michael L. Anderson (UC Berkeley, ARE); Minwoo Hyun (UC Santa Barbara, Economics); Jaecheol Lee (UC Berkeley, ARE — corresponding author, ferleejc@berkeley.edu)
- title: Bounds, Benefits, and Bad Air: Welfare Impacts of Pollution Alerts
- year: January 2022
- venue: NBER Working Paper No. 29637; JEL: I12, I18, Q53

## Unresolved gaps
- Published journal version (if any) not identified in these chunks — may appear in back matter or references
- DOI for final published version not present; only NBER WP URL confirmed
- Tables 4 and 5 (main regression results with R² ~0.8–0.9) not in these chunks; quantitative effect sizes from abstract only
- Section V (policy simulations, benefit-cost calculations) not yet read — welfare bound magnitudes ($28.6M, $36.7M, BCR 7.1:1, 9.2:1) stated in abstract but derivation deferred to later sections
- pmavg = 22.7, pmhi = 66.7, c = 57.5 (footnote 15) — these are PM2.5 values near threshold; source/vintage of these descriptive stats not specified in these chunks
