# Climate Norm / Weather Shock Decomposition

**Summary**: The norm/shock decomposition splits observed meteorological conditions into a slowly-moving climate norm (long-run average) and a transitory weather shock (deviation from that norm). Popularized for econometric climate-impact measurement by Bento et al. (2023), who showed via the [[frisch-waugh-lovell-decomposition]] that estimating both components jointly in one regression recovers the short-run and long-run effects as the weather-shock and climate-norm coefficients respectively.

**Sources**: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf

**Last updated**: 2026-05-19

---

## Construction of the climate norm

**General form (Eq. 11)**:

$$
\bar{x}_{i\bar{p}} \equiv \frac{1}{J}\sum_{j=1}^{J < y}\omega_j \bar{x}_{imj}
$$

a lagged weighted average of monthly averages $\bar{x}_{imj}$ for location $i$, month $m$, and year $j$ (all years strictly before the current year $y$). Weights $\omega_j$ accommodate myopic, bounded, or rational agent assumptions.

**Preferred specification (Eq. 12)** in Bento et al. (2023):

$$
\bar{x}_{i\bar{p}} = \frac{1}{30}\sum_{j=y-30}^{y-1}\bar{x}_{imj}
$$

Equal weights over the preceding 30 calendar years, consistent with the WMO "climate normal" convention. Lagged at least 1 year to allow agents to observe and respond before the current ozone season.

**Approximation quality**: Correlation between $\bar{x}_{i\bar{p}}$ (30-yr MA) and $\bar{x}_{imy}$ (location-by-month-by-year FE) $> 0.95$; correlation between corresponding weather shocks $> 0.90$ (source: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf).

## Construction of the weather shock

$$
\text{Shock}_{it} = x_{it} - \bar{x}_{i\bar{p}}
$$

The deviation of the contemporaneous value from the climate norm. Mean-zero by construction around the norm.

## JMP project mapping

The JMP project follows this decomposition for daily ozone $\rho_{it}$:

$$
\rho_{it} = P_{im} + \epsilon_{it}
$$

where $P_{im}$ is a 5-year backward moving average of ozone for the same county-month (lagged ≥1 year), and $\epsilon_{it}$ is the daily transitory shock. Note the JMP project uses a **5-year** rather than 30-year window — a shorter window that may better reflect agents' working knowledge of their local air quality environment than a 30-year norm. The shorter window is also constrained by ozone monitor data availability from 1980.

The JMP estimating equation:

$$
h_{it} = \beta^S(\rho_{it} - P_{im}) + \beta^N P_{im} + \beta_A^S(\rho_{it} - P_{im})A_{it} + \beta_A^N P_{im}A_{it} + \beta_A A_{it} + X_{it}'\gamma + \alpha_{is} + \delta_{ky} + \nu_{it}
$$

where the norm-shock gap $\beta^S - \beta^N$ recovers the net health benefit of ex-ante defensive action (the analogue of $\hat{\beta}_W - \hat{\beta}_C$ in Bento et al.).

## Robustness of the norm construction

Bento et al. (2023) show the adaptation measure $\hat{\beta}_W - \hat{\beta}_C$ is stable across MA windows of 3–30 years (range: 0.495–0.542 ppb/°C). The slight increase in the shock coefficient when using very short windows reflects attenuation bias (measurement error in the permanent component is larger for short MAs); the slight decrease when moving from 20 to 30 years reflects panel-driven attenuation bias (Blanc & Schlenker 2017). The 30-year window is approximately "optimal" for the ozone application.

## Conceptual interpretation

| | Weather shock $x_{it} - \bar{x}_{i\bar{p}}$ | Climate norm $\bar{x}_{i\bar{p}}$ |
|---|---|---|
| What varies | Day-to-day within location-season-year | Across years (rolling update) and across locations |
| Behavioral assumption | Agent has not had time to adapt | Agent has had time to adapt |
| Coefficient interpretation | Short-run effect, exclusive of adaptation | Long-run effect, inclusive of adaptation |
| FE analogue | Panel FE coefficient | Cross-section coefficient |
| Adaptation indicator | $\hat{\beta}_W - \hat{\beta}_C > 0$ implies partial adaptation | $\hat{\beta}_C = 0$ implies full adaptation |

## Related pages

- [[frisch-waugh-lovell-decomposition]]
- [[bento-miller-mookerjee-severnini-2023-jeem]]
- [[ex-ante-ex-post-adaptation]]
- [[adapting-wind-iv-to-ozone-shocks]]
