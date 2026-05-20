# Anderson, Hyun, and Lee (2022) NBER

**Summary**: Establishes a lower-bound welfare framework for air-quality alert systems (AQAS) using a fuzzy RD at South Korea's PM alert threshold; finds alerts reduce government-borne health expenditures by $28.6M (contemporaneous) at a benefit-cost ratio of 7:1, with effects entirely via avoidance behavior (no ambient PM change at threshold). The fiscal externality $\Delta E$ identified here enters the JMP directly as the estimable component of $\Delta W$.

**Sources**: Anderson_etal_2022_NBER.pdf

**Last updated**: 2026-05-19

---

## Paper in brief

Anderson, Hyun, and Lee (2022) study South Korea's fine-particulate-matter alert system (PM2.5 and PM10 advisories issued to 51 million residents). They estimate the causal effect of alert issuance on per-capita health expenditures using a **fuzzy regression discontinuity**: when the running variable $rv_d = PM_d^{\text{2h-min-max}} - c$ crosses zero, the probability of an alert rises by ≈62 pp (strong first stage, F ≈ 46–90), but measured ambient PM does not jump — so any health expenditure changes must reflect avoidance behavior, not reduced actual pollution.

The paper's key conceptual contribution is a **welfare bounds framework**: social welfare gain decomposes as $\Delta W_i = \Delta U_i + \Delta E_i$. Because $\Delta U_i \geq 0$ (more accurate PM information weakly increases private utility), the estimated reduction in *publicly reimbursed* health costs $\Delta E_i$ is a lower bound on the total welfare gain. The JMP uses this logic: the alert coefficient $\beta_A$ on government-borne Medicare costs identifies $\Delta E$ and provides a conservative welfare lower bound.

## Identification

- **Design**: Fuzzy RD; running variable is threshold-normalized daily PM; treatment is alert issuance; instrument is the above-threshold indicator.
- **Sample**: South Korea, 2016–2017; 73 districts in 7 major cities; 2.3 million individuals (NHIS 10% sample); district-by-day observations ($N \approx 2{,}530$ at $h = 20$).
- **No PM discontinuity**: Table A4 confirms no jump in ambient PM10 or PM2.5 at the threshold → effects are purely behavioral (avoidance).
- **Bandwidth**: $h = 20$ preferred (CCT-optimal range 17–22); robustness at $h = 16$ and $h = 24$.

## Key estimates

**First stage** (Table 3): Alert probability rises 0.618–0.636 at threshold; F-stat 46–90; Adj. $R^2 \approx 0.71$–$0.73$.

**Respiratory effects** (Table 4, 2SLS, $h = 20$, US cents per capita):

| Age group | Coeff. | SE (RV) | SE (day) |
|---|---|---|---|
| Minors (0–19) | −15.03 | (4.71) | [5.67] |
| Adults (20–64) | −3.78 | (2.20) | [2.13] |
| Older Adults (≥65) | −4.30 | (2.75) | [2.80] |
| All ages | −5.83 | (2.40) | [2.50] |

Minors: ≈30% of mean below-threshold spending.

**Cardiovascular effects** (Table 5, 2SLS, $h = 20$, US cents per capita):

| Age group | Coeff. | SE (RV) | SE (day) |
|---|---|---|---|
| Adults (20–64) | −2.83 | (0.976) | [0.767] |
| Older Adults (≥65) | −9.64 | (3.85) | [3.68] |
| All ages | −3.26 | (1.09) | [1.01] |

Adults: ≈23% reduction; Older Adults: ≈14% reduction.

**Dynamic effects** (Table 6, 3-day rolling sum, $h = 20$, cents per capita): Effects 2.5–2.8× contemporaneous, consistent with multi-day alert duration (mean 1.87 days).

| | All ages |
|---|---|
| Respiratory | −16.1 (4.78) |
| Cardiovascular | −8.04 (2.66) |

**Aggregate welfare bounds** (2016–2017):
- Contemporaneous: total health expenditure reduction ≈$41M; public-share lower bound $28.6M (respiratory $18.4M + cardiovascular $10.2M).
- Dynamic: total ≈$52M; public lower bound $36.7M.
- System cost ≈$4M (Tables A12–A13).
- **BCR: 7.1:1** (contemporaneous); **9.2:1** (dynamic).
- **Net benefit: $24.6M** ($32.7M dynamic).

## Figures

**Figure 1:** Alert cluster map for 7 South Korean cities (p. 20)

![Alert cluster map](../figures/Anderson_etal_2022_NBER_fig1.jpeg)

- Key visual finding: 73 districts organized into 14 alert regions across 7 cities (Seoul, Busan, Daegu, Daejeon, Incheon, Gwangju, Ulsan).

**Figure 2:** Daily PM alert counts and NAVER keyword search index, 2016–2017 (p. 21)

![Alert counts and search keyword spikes](../figures/Anderson_etal_2022_NBER_fig2.jpeg)

- Key visual finding: NAVER keyword searches for air quality spike sharply on alert days, confirming that alerts successfully transmit information to the public.

**Figure 3:** P(PM advisory) vs. running variable — first-stage discontinuity (p. 22)

![RD first stage](../figures/Anderson_etal_2022_NBER_fig3.jpeg)

- Key visual finding: Sharp jump in advisory probability at $rv_d = 0$; essentially zero below, ≈62% above. Strong and credible first stage.

**Figure 4:** Residualized per-capita health expenditures vs. running variable — 6 panels (p. 23)

![RD outcome discontinuity](../figures/Anderson_etal_2022_NBER_fig4.jpeg)

- Key visual finding: Visible downward jumps in residualized spending at threshold for youth respiratory and adult/older-adult cardiovascular — visual confirmation of the 2SLS estimates.
- **Figure notes:** Residualized for DOW, year × month, holiday, and district FEs. Bin width = 5 RV units.

**Figure 5:** Lower bounds on gross health benefits by age group — contemporaneous and dynamic (p. 24)

![Welfare lower bounds by age group](../figures/Anderson_etal_2022_NBER_fig5.jpeg)

- Key visual finding: Adults (20–64) account for the largest share of benefits ($20.4M), led by cardiovascular; respiratory benefits concentrated in minors ($12.6M).
- **Figure notes:** Scaled by 70% public coverage rate. Based on Tables 4–5 (contemporaneous) and Table 6 (dynamic).

**Figure 6:** Cost-benefit comparison across Baseline, Scenario A (full compliance), and Scenario B (lower PM2.5 threshold to 75 µg/m³) (p. 25)

![Cost-benefit comparison](../figures/Anderson_etal_2022_NBER_fig6.jpeg)

- Key visual finding: All scenarios yield positive net benefits. Scenario B (lower threshold) generates $76.5M in expenditure reductions — 109% above baseline — with minimal additional cost.
- **Figure notes:** 2016 system cost assumed equal to 2017. Maintenance cost line at $4M.

## Welfare framework equations

$$
W_i = U_i(a_i, pm) + E_i \qquad \Delta W_i = \Delta U_i + \Delta E_i
$$

Since $\Delta U_i \geq 0$: $\quad \Delta E_i \leq \Delta W_i$ — public expenditure reduction is a conservative lower bound on total social welfare gain.

## Project connections

- **JMP direct application**: The $\beta_A$ coefficient on government-borne Medicare costs in the JMP's estimating equation identifies $\Delta E$, the fiscal externality, following this paper's bounds logic. See [[welfare-bounds-alert-programs]].
- **Avoidance mechanism**: Effects are purely via behavioral avoidance — no PM reduction at threshold. This validates the JMP assumption that alerts operate through the information/behavior channel $b_t(\epsilon_{it}, A_{it})$. See [[air-quality-alerts-and-avoidance-behavior]].
- **Identification analogy**: The FRD running variable is PM itself; the JMP uses ozone shocks + wind IV rather than an RD, but the alert-program component shares the same avoidance-behavior interpretive logic.
- **Contemporaneous vs. ex-ante distinction**: AHL2022 identifies the contemporaneous avoidance effect $b$ (ex-post adaptation triggered by the alert). The JMP's norm-shock gap $\beta^S - \beta^N$ captures the ex-ante stock $k$ built against the anticipated pollution environment. These are complementary channels. See [[ex-ante-ex-post-adaptation]].

## Replication feasibility

LOW. NHIS health microdata restricted to South Korean data centers; data cannot be shared externally. Alert and PM monitoring data are public (AirKorea). Code fully described; rdrobust package standard.

## Related pages

- [[welfare-bounds-alert-programs]]
- [[air-quality-alerts-and-avoidance-behavior]]
- [[forecasts-alerts-and-identification]]
- [[ex-ante-ex-post-adaptation]]
- [[health-production-and-adaptation]]
- [[bento-miller-mookerjee-severnini-2023-jeem]]
