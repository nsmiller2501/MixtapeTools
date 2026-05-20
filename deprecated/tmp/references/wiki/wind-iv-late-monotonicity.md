# Wind IV LATE Monotonicity

**Summary**: Deryugina et al. explicitly discuss the monotonicity condition needed to interpret wind-IV estimates as a local average treatment effect (source: Deryugina_etal_2019_AER.pdf). In their setting, counties within a monitor group should respond to a given high-pollution wind direction in the same direction (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## LATE Interpretation

Deryugina et al. state that IV estimates are generally interpreted as local average treatment effects and that this interpretation requires a monotonicity assumption (source: Deryugina_etal_2019_AER.pdf). In their design, monotonicity requires PM2.5 to weakly increase in a county when wind comes from a high-pollution direction and weakly decrease when wind comes from a low-pollution direction (source: Deryugina_etal_2019_AER.pdf).

## What Monotonicity Means with Grouped Instruments

Because the instruments are wind-direction-bin indicators interacted with monitor-group indicators, the monotonicity condition applies within monitor groups and wind-angle bins (source: Deryugina_etal_2019_AER.pdf). The authors explain that every county in a monitor group should experience pollution changes in the same direction for a given 90-degree wind-angle bin (source: Deryugina_etal_2019_AER.pdf).

## Possible Violations

The authors identify three possible monotonicity threats: counties inside a monitor group may respond differently to the same wind direction, the pollution response may vary within a coarse 90-degree bin, and the wind-pollution relationship may differ by time of year (source: Deryugina_etal_2019_AER.pdf). These threats matter because they can make the set of compliers hard to interpret (source: Deryugina_etal_2019_AER.pdf).

## Robustness Strategy

The authors probe monotonicity by using 60-degree wind bins, using 50 or 200 monitor groups instead of 100, and interacting instruments with season (source: Deryugina_etal_2019_AER.pdf). Estimates remain similar across those alternatives, and the authors conclude that any monotonicity violations have little effect on interpreting their estimates as LATE (source: Deryugina_etal_2019_AER.pdf).

## Implication for Ozone Norm/Shock Design

For an ozone shock design, monotonicity should be stated for the shock component rather than total ozone if the norm is separately controlled (source: Deryugina_etal_2019_AER.pdf). The relevant condition would be that a high-ozone wind direction weakly shifts the transitory ozone shock in the same direction for counties within the chosen spatial group and time partition (source: Deryugina_etal_2019_AER.pdf). Seasonal interactions may be especially important for ozone because ozone chemistry and alert issuance are seasonal by construction (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[wind-direction-instruments]]
- [[monitor-group-first-stage]]
- [[wind-iv-identification-assumptions]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[deryugina-etal-2019-aer]]
