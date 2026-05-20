# Bento, Miller, Mookerjee, and Severnini (2023) JEEM

**Summary**: Proposes a unifying regression framework — exploiting the Frisch–Waugh–Lovell theorem — that estimates short-run weather-shock effects and long-run climate-norm effects in a single equation, directly recovering an adaptation measure as their difference. Applied to ambient ozone in the U.S. 1980–2013, finds adaptation of 0.51 ppb/°C and shows ignoring it overestimates the "climate penalty" by ~44%.

**Sources**: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf

**Last updated**: 2026-05-19

---

## Bibliographic information

- **DOI**: 10.1016/j.jeem.2023.102843
- **Replication archive**: https://doi.org/10.3886/E192708V1 (openICPSR)
- **JEL codes**: Q53, Q54, C51

## Core contribution

The paper unifies two strands of the climate-economy literature: cross-sectional comparisons across climate zones and panel fixed-effects regressions exploiting day-to-day weather variation. The key insight is that both are embedded in a single regression via the [[frisch-waugh-lovell-decomposition]]:

$$
y_{it} = \alpha + \beta_W(x_{it} - \bar{x}_{i\bar{p}}) + \beta_C \bar{x}_{i\bar{p}} + \mu_i + \lambda_s + \nu_{it}
$$

- $\hat{\beta}_W$ recovers the panel FE estimate (no time for adaptation)
- $\hat{\beta}_C$ recovers the cross-sectional estimate (full adaptation absorbed)
- $\hat{\beta}_W - \hat{\beta}_C$ = the adaptation measure, testable with standard errors from this single regression

See [[climate-norm-weather-shock-decomposition]] for the implementation details.

## Empirical application: ambient ozone

Temperature affects ozone formation via photochemical reactions with NOx and VOCs. The paper estimates:

| Parameter | Estimate | SE |
|-----------|----------|----|
| $\hat{\beta}_W$ (temperature shock) | 1.678 ppb/°C | 0.063*** |
| $\hat{\beta}_C$ (climate norm, 30-yr MA) | 1.164 ppb/°C | 0.051*** |
| Adaptation ($\hat{\beta}_W - \hat{\beta}_C$) | 0.514 ppb/°C | 0.041*** |

Panel FE benchmark: 1.659 ppb (0.063), statistically identical to $\hat{\beta}_W$ ✓  
Cross-section benchmark: 1.166 ppb (0.106), statistically identical to $\hat{\beta}_C$ ✓

## Climate penalty projections

Using the norm-based $\hat{\beta}_C = 1.164$ (inclusive of adaptation) vs. the shock-based $\hat{\beta}_W = 1.678$ (exclusive of adaptation) under RCP 8.5 (1.6°C by 2050, 4.8°C by 2100):

| Scenario | Correct (norm) | Incorrect (shock) | Overestimate |
|----------|---------------|-------------------|--------------|
| 2050 | 1.9 ppb | 2.7 ppb | +0.82 ppb (+44%) |
| 2100 | 5.6 ppb | 8.0 ppb | +2.47 ppb (+44%) |

## Ozone Action Day null result

Interacting a binary OAD alert indicator with the temperature shock tests for short-run adaptive responses:

$$
\text{Shock} \times \text{Action Day}: \quad \hat{\beta} = 0.068, \quad \text{SE} = 0.188 \quad (\text{insignificant})
$$

No meaningful short-run adaptive response detected nationally. This is consistent with alerts being insufficient to trigger behavioral change at the aggregate level — a finding directly relevant to the JMP project's test of whether alert programs induce additional defensive action. See [[forecasts-alerts-and-identification]].

## Robustness

Adaptation estimate is stable across MA lengths (3–30 years): range 0.495–0.542 ppb/°C. Longer lag structures (10- and 20-year lags) yield 0.527–0.542 ppb/°C. See Table 2 in `_text.md`.

## Data and sample

- Ozone: EPA AQS, daily max concentration, monitor × day, 1980–2013, ozone season (April–September)
- Temperature: NOAA GHCN, 20,000+ stations; matched to ozone monitors within 30 km
- N = 5,139,523 monitor-day observations; 2,712 monitors in cross-section
- Unit of observation: ozone monitor × day (note: JMP project uses county-level data)

## Figures

**Figure 1:** Theoretical relationship between marginal cost of dirty production and temperature. (p. 7)

![Conceptual schematic: production schedules 1 and 2](figures/Bento_Miller_Mookerjee_Severnini_2023_JEEM_fig1.jpeg)

- Key visual finding: Agents facing a transitory temperature shock produce at A′ (higher ozone); agents facing a permanent norm increase adapt to production schedule 2 and produce at C (lower ozone than A′). Adaptation is not costless.

**Figure 2, Panel A:** Climate norms — US ozone-season temperature, 1980–2013. (p. 9)

![Time-series of US climate norms 1980–2013](figures/Bento_Miller_Mookerjee_Severnini_2023_JEEM_fig2a.jpeg)

- Key visual finding: Climate norms drift slowly upward over the sample period, consistent with gradual warming.

**Figure 2, Panel B:** Weather shocks — US ozone-season temperature deviations from norm, 1980–2013. (p. 9)

![Time-series of US weather shocks 1980–2013](figures/Bento_Miller_Mookerjee_Severnini_2023_JEEM_fig2b.jpeg)

- Key visual finding: Weather shocks are mean-zero and volatile, confirming the decomposition produces the intended distinct variation.

**Figure 3:** Decomposition of temperature norms & shocks, Los Angeles 2013. (p. 11)

![LA 2013 norm/shock decomposition, preferred vs. standard FE](figures/Bento_Miller_Mookerjee_Severnini_2023_JEEM_fig3.jpeg)

- Key visual finding: Preferred 30-yr MA decomposition and standard FE decomposition yield near-identical shocks, validating the approximation.

**Figure 4:** Comparing linear, binned, quadratic, and cubic specifications. (p. 17)

![Five-panel nonlinear ozone-temperature response comparison](figures/Bento_Miller_Mookerjee_Severnini_2023_JEEM_fig4.jpeg)

- Key visual finding: Marginal adaptation (Panel E) is U-shaped — greatest at highest temperatures. Linear spec provides a good average approximation.

## Related pages

- [[frisch-waugh-lovell-decomposition]]
- [[climate-norm-weather-shock-decomposition]]
- [[ex-ante-ex-post-adaptation]]
- [[forecasts-alerts-and-identification]]
- [[health-production-and-adaptation]]
- [[carleton-etal-2024-hesecc]]
