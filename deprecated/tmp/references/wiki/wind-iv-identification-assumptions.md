# Wind IV Identification Assumptions

**Summary**: The wind-IV design requires relevance, exclusion, and credible controls for weather and seasonal confounding (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. defend these assumptions with flexible controls, placebo checks, robustness exercises, and first-stage diagnostics (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## Relevance

The relevance condition is that wind direction must predict the endogenous pollutant after controls and fixed effects (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. show this graphically for the Bay Area and Boston and report large first-stage $F$-statistics in their main IV tables (source: Deryugina_etal_2019_AER.pdf). The first stage remains strong across alternative instrument lags and instrument aggregations (source: Deryugina_etal_2019_AER.pdf).

## Exclusion Restriction

The exclusion restriction is that daily wind direction affects mortality and health care use only through air pollution, after conditioning on fixed effects and climatic controls (source: Deryugina_etal_2019_AER.pdf). The authors control flexibly for maximum temperature, minimum temperature, precipitation, wind speed, and interactions among these weather measures (source: Deryugina_etal_2019_AER.pdf). They include wind speed as a control rather than an instrument because wind speed may directly affect mortality through evaporation from skin under some conditions (source: Deryugina_etal_2019_AER.pdf).

## Fixed Effects Logic

County fixed effects absorb time-invariant geographic differences in health and pollution (source: Deryugina_etal_2019_AER.pdf). State-by-month fixed effects absorb seasonal relationships among pollution, wind direction, and health that vary by state (source: Deryugina_etal_2019_AER.pdf). Month-by-year fixed effects absorb common time-varying shocks such as policy changes (source: Deryugina_etal_2019_AER.pdf).

## Behavioral Response Concern

The authors consider whether windy days could directly change elderly behavior, such as staying indoors or traveling less (source: Deryugina_etal_2019_AER.pdf). They argue that many high-first-stage observations occur under wind speeds described as a gentle breeze, and their estimates are robust to excluding observations with wind speed above 3.9 meters per second (source: Deryugina_etal_2019_AER.pdf).

## Placebo and Robustness Evidence

The planned non-ER admissions outcome is a placebo-style outcome because planned admissions should not respond to acute pollution shocks (source: Deryugina_etal_2019_AER.pdf). The IV estimate for planned non-ER admissions is small and insignificant, while ER-driven admissions and visits rise (source: Deryugina_etal_2019_AER.pdf). The authors also report that random placebo wind directions produce very small first-stage $F$-statistics, supporting the view that actual wind direction captures meaningful pollution variation (source: Deryugina_etal_2019_AER.pdf).

## Ozone-Project Warning

For an ozone alert project, the exclusion restriction must also address the fact that wind direction may forecast ozone episodes and therefore alerts, information, or behavior (source: Deryugina_etal_2019_AER.pdf). A defensible ozone design should treat alerts as policy variables rather than hidden channels and should control for alert status, alert interactions, weather, visibility, ozone norms, and transitory ozone shocks (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[wind-direction-instruments]]
- [[monitor-group-first-stage]]
- [[multi-pollutant-wind-iv]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[deryugina-etal-2019-aer]]
