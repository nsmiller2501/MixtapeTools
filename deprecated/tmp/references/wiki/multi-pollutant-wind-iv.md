# Multi Pollutant Wind IV

**Summary**: Deryugina et al. use wind direction to instrument PM2.5 jointly with CO and ozone (source: Deryugina_etal_2019_AER.pdf). The exercise is important for ozone work because co-transported pollutants can change interpretation and weaken first stages (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## Motivation

Deryugina et al. note that ozone and carbon monoxide can be co-transported with PM2.5, and that pollutants are not perfectly co-transported because they can have different sources and atmospheric transport patterns (source: Deryugina_etal_2019_AER.pdf). They therefore test whether PM2.5 mortality estimates change after controlling for wind-instrumented CO and ozone (source: Deryugina_etal_2019_AER.pdf).

## Table 8 Evidence

| Panel / sample | Spec | PM2.5 | CO | Ozone | F-statistic | Observations |
|---|---:|---:|---:|---:|---:|---:|
| All beneficiaries | PM2.5 only | 0.490 (0.109) |  |  | 137 | 652,218 |
| All beneficiaries | PM2.5 + CO | 0.337 (0.108) | 0.025 (0.008) |  | 35 | 652,218 |
| All beneficiaries | PM2.5 + ozone | 0.642 (0.099) |  | -0.310 (0.106) | 56 | 652,218 |
| All beneficiaries | PM2.5 + CO + ozone | 0.394 (0.137) | 0.023 (0.009) | -0.093 (0.118) | 29 | 652,218 |
| FFS beneficiaries | PM2.5 only | 0.699 (0.118) |  |  | 134 | 590,263 |
| FFS beneficiaries | PM2.5 + CO | 0.572 (0.134) | 0.018 (0.010) |  | 34 | 590,263 |
| FFS beneficiaries | PM2.5 + ozone | 0.903 (0.124) |  | -0.427 (0.148) | 53 | 590,263 |
| FFS beneficiaries | PM2.5 + CO + ozone | 0.779 (0.190) | 0.011 (0.011) | -0.328 (0.180) | 27 | 590,263 |

The table uses three-day mortality per million as the outcome and restricts the sample to county-days with simultaneous CO, ozone, and PM2.5 readings (source: Deryugina_etal_2019_AER.pdf). The PM2.5 effect remains significant across these specifications, which the authors interpret as evidence that their mortality results are primarily attributable to PM2.5 rather than CO or ozone (source: Deryugina_etal_2019_AER.pdf).

## Interpretation

The multi-pollutant specifications show that wind direction can provide separate instruments for multiple pollutants when pollutants are not perfectly co-transported (source: Deryugina_etal_2019_AER.pdf). The sharp decline in first-stage $F$-statistics after adding CO and ozone shows that joint instrumentation can be more demanding than single-pollutant instrumentation (source: Deryugina_etal_2019_AER.pdf). This is central for ozone work because ozone may need to be separated from PM2.5, CO, NO2, or precursor channels (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[wind-direction-instruments]]
- [[wind-iv-identification-assumptions]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[deryugina-etal-2019-aer]]
