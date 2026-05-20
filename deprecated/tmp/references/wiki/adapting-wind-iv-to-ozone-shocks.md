# Adapting Wind IV To Ozone Shocks

**Summary**: Deryugina et al. provide a practical wind-IV template that can be adapted to an ozone norm/shock design, but ozone requires extra care around chemistry, alerts, and seasonal policy timing (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## Direct Adaptation

The closest adaptation is to use wind-direction instruments for the transitory ozone shock $\epsilon_{it}$ while controlling for the ozone norm $P_{im}$ (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. show that daily wind direction can instrument acute pollution exposure in a county-day design with high-dimensional fixed effects and flexible weather controls (source: Deryugina_etal_2019_AER.pdf). Their approach is attractive because it does not require a complete source-by-source map of emissions and transport pathways (source: Deryugina_etal_2019_AER.pdf).

## Candidate First Stage

For the JMP design, a wind first stage could instrument the ozone shock rather than total ozone (source: Deryugina_etal_2019_AER.pdf). A project-specific first stage could be:

$$
\epsilon_{it}
= \sum_{g \in G} \sum_b \pi_b^g \mathbf{1}[G_i=g] \times WINDDIR_{it}^b
+ f(W_{it}) + \mu_{is} + \lambda_{st} + \eta_{it},
$$

where $\epsilon_{it}$ is the ozone shock, $W_{it}$ includes weather and visibility controls, $\mu_{is}$ captures county-by-season fixed effects, and $\lambda_{st}$ captures state-by-year or other policy-time fixed effects (source: Deryugina_etal_2019_AER.pdf). This is an adaptation rather than the exact Deryugina et al. specification because the paper instruments PM2.5 levels, not an ozone norm/shock decomposition (source: Deryugina_etal_2019_AER.pdf).

## Alerts as a Channel

The ozone alert project must separate intrinsic avoidance from alert-induced avoidance, so alert status cannot be treated as an omitted channel (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. emphasize acute pollution variation and do not estimate alert-policy effects, so their exclusion argument must be modified when alerts respond to forecasted or realized ozone conditions (source: Deryugina_etal_2019_AER.pdf). In an alert model, wind direction may affect health through realized ozone and through alert issuance if agencies use wind-related forecasts, so the specification needs alert controls and alert interactions by design (source: Deryugina_etal_2019_AER.pdf).

## Data Requirements

The wind-IV adaptation requires daily county ozone from monitors or fused exposure data, wind vector fields, weather controls, fixed effects, and health outcomes (source: Deryugina_etal_2019_AER.pdf). The Deryugina et al. implementation uses NARR wind components interpolated to monitors before aggregation to county-day, which is a practical template for building county-day wind direction and wind speed (source: Deryugina_etal_2019_AER.pdf). The ozone project also requires AQAD alert data and a pre-specified norm construction, such as a backward county-by-calendar-month norm (source: Deryugina_etal_2019_AER.pdf).

## Diagnostics to Carry Over

The ozone adaptation should report first-stage $F$-statistics for the shock, not just total ozone, because the identifying variation is meant to isolate transitory deviations from norms (source: Deryugina_etal_2019_AER.pdf). It should show wind-direction first-stage plots in selected regions, because Deryugina et al. use these plots to demonstrate that geography-specific wind-pollution relationships are plausible (source: Deryugina_etal_2019_AER.pdf). It should estimate first stages by wind-speed decile, because Deryugina et al. use that diagnostic to distinguish nonlocal transport from local-source accumulation (source: Deryugina_etal_2019_AER.pdf). It should vary wind bins, spatial groups, season interactions, instrument lags, weather controls, and fixed effects, following Deryugina et al.'s robustness structure (source: Deryugina_etal_2019_AER.pdf).

## Ozone-Specific Risks

Ozone is formed photochemically, so temperature, sunlight-related conditions, seasonality, and precursors may be more central confounders than in a PM2.5-focused design (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. show that adding ozone to a PM2.5 wind-IV model changes first-stage strength and yields negative ozone coefficients in some specifications, which warns against treating co-pollutant interpretation as automatic (source: Deryugina_etal_2019_AER.pdf). The project should therefore pre-specify whether wind instruments target ozone alone, ozone plus co-pollutants, or a policy-relevant exposure bundle (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[wind-direction-instruments]]
- [[monitor-group-first-stage]]
- [[wind-iv-identification-assumptions]]
- [[wind-iv-late-monotonicity]]
- [[multi-pollutant-wind-iv]]
- [[deryugina-etal-2019-aer]]
