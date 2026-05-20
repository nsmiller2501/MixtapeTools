## Bibliographic metadata
doi: 10.1257/aer.20180279
authors: [Deryugina, Heutel, Miller, Molitor, Reif]
title: The Mortality and Medical Costs of Air Pollution: Evidence from Changes in Wind Direction
year: 2019
venue: American Economic Review
venue_type: journal

## Plain-English synthesis
Deryugina et al. estimate how short-run fine particulate pollution affects elderly mortality, hospital use, and medical spending in the United States. Their main problem is that pollution is not randomly assigned and monitor readings can measure exposure with error. They use daily changes in local wind direction as instruments for daily county PM2.5, letting the wind-pollution relationship vary across spatial monitor groups. The design relies on wind direction changing pollution but not directly changing elderly health once the model controls flexibly for weather, place, season, and time. Wind direction strongly predicts PM2.5; the first stage is stronger on higher-wind-speed days, which supports the interpretation that the identifying variation comes from transported pollution rather than purely local emissions. They find that a one-day PM2.5 increase raises deaths, emergency visits, hospitalizations, and inpatient spending, while planned admissions do not respond. They also show robustness to alternative instrument bins, monitor-group sizes, weather controls, fixed effects, instrument lags, LIML, placebo wind instruments, and simultaneous instrumentation for PM2.5, CO, and ozone. For an ozone alert project, the most useful contribution is the scalable wind-IV template and the assumptions needed to defend it.

## 1. Research question
Deryugina et al. ask what acute PM2.5 exposure does to elderly mortality, health care use, and medical costs in the United States.

They also ask which elderly beneficiaries are most vulnerable to acute pollution exposure, but that heterogeneity and life-years component is secondary for the present project.

## 2. Audience
The paper targets environmental economists, health economists, applied microeconometricians, and policy analysts who need causal estimates of pollution damages.

For this project, the most relevant audience is researchers designing pollution-health specifications with wind-based instruments and rich administrative health data.

## 3. Method / identification strategy
The paper instruments daily county PM2.5 with changes in local wind direction. The key assumption is that, after flexible fixed effects and climate controls, daily wind direction affects mortality and health care use only through air pollution.

The first stage is:

$$
PM2.5_{cdmy}
= \sum_{g \in G} \sum_{b=0}^{2} \beta_b^g \mathbf{1}[G_c=g] \times WINDDIR_{cdmy}^{90b}
+ X'_{cdmy}\sigma + \alpha_c + \alpha_{sm} + \alpha_{my} + \epsilon_{cdmy}.
$$

The excluded instruments are interactions between monitor-group indicators and wind-direction-bin indicators. Daily wind direction is divided into 90-degree bins; the omitted bin is $[270,360)$, and the included bins are $[0,90)$, $[90,180)$, and $[180,270)$.

The authors use $k$-means to classify pollution monitors into 100 spatial groups based on location, yielding 93 PM2.5 monitor groups in the final PM2.5 sample. The coefficient on wind direction is allowed to vary by monitor group.

The design is intended to emphasize pollution variation that moves similarly across a broader area, which the authors interpret as more likely to be nonlocal transported pollution than monitor-specific local-source variation.

The preferred outcome equation is:

$$
Y_{cdmy}
= \beta PM2.5_{cdmy} + X'_{cdmy}\gamma + \alpha_c + \alpha_{sm} + \alpha_{my} + \epsilon_{cdmy}.
$$

The main dependent variables are three-day totals measured over day $d$ and the following two days.

## 4. Target parameter
The main coefficient $\beta$ is the effect of a one-day increase in daily PM2.5 on three-day mortality, hospital use, and spending.

Under the IV interpretation, the estimate is a local average treatment effect for pollution variation shifted by wind-direction changes. The authors explicitly discuss the monotonicity condition needed for a LATE interpretation.

For this project, the analogous target would be the health effect of ozone shock variation shifted by wind-direction instruments, net of local ozone norms, alert status, and flexible weather/time controls.

## 5. Data
Pollution data come from EPA Air Quality System monitor readings, aggregated from hourly monitor readings to daily county measures.

The paper uses PM2.5 as the main pollutant and also obtains ozone, carbon monoxide, sulfur dioxide, and nitrogen dioxide.

Wind speed and wind direction come from North American Regional Reanalysis daily reanalysis data on a 32-by-32 kilometer grid. The authors interpolate daily east-west and north-south wind components to each pollution monitor, convert them to wind direction and wind speed, and average to county-day.

The authors define wind direction as the direction the wind is blowing from.

Temperature and precipitation come from daily gridded weather data based on PRISM and weather stations, averaged to county-day.

Health outcomes come from Medicare administrative data for beneficiaries aged 65 to 100, with dates of death from enrollment files and hospital outcomes from MedPAR and outpatient claims.

The main PM2.5 estimation sample has 1,980,549 county-day observations and covers 902 counties with PM2.5 monitor data, representing about 70 percent of the elderly Medicare population.

## 6. Statistical methods / specifications
The preferred controls include county fixed effects, state-by-month fixed effects, month-by-year fixed effects, and flexible interactions among maximum temperature bins, minimum temperature bins, precipitation deciles, and wind-speed deciles.

The authors include two leads of weather controls to align with the three-day outcome window.

OLS specifications include two leads and two lags of PM2.5, while IV specifications include two leads and two lags of the instruments.

The authors cluster standard errors at the county level and weight per-capita outcomes by the relevant beneficiary population.

They do not use wind speed as an instrument because wind speed may directly affect mortality through evaporation from skin under some conditions.

They partial out high-dimensional fixed effects and controls using the Correia algorithm, noting that instruments are not partialled out by that algorithm and therefore increasing the number of instruments is computationally costly.

## 7. Findings
The preferred IV estimate is that a one-day $1$ microgram per cubic meter PM2.5 increase causes about $0.69$ additional deaths per million elderly beneficiaries over three days.

The IV estimates are larger than OLS estimates, which the authors interpret as evidence that observational pollution-health estimates can be biased.

For hospital outcomes, a $1$ microgram per cubic meter PM2.5 increase raises ER visits, ER-originating inpatient admissions, and inpatient ER spending, while planned non-ER admissions do not respond.

The PM2.5 mortality effect remains significant when the authors simultaneously instrument for PM2.5, CO, and ozone, though the first-stage $F$-statistic falls in the multi-pollutant specifications.

The wind-IV estimates are robust to alternative wind-direction bin widths, monitor-group counts, season interactions, fixed effects, weather controls, and instrument lags.

The first-stage $F$-statistic is lowest in low-wind-speed deciles and largest for higher-wind-speed samples, which supports the authors' claim that the design captures transported pollution.

## 8. Contributions
The main project-relevant contribution is a scalable wind-direction IV design that does not require hand-mapping each local pollution source.

The paper also provides concrete diagnostics for defending the design: first-stage maps/plots, wind-speed decile first stages, alternative instrument aggregations, placebo wind instruments, LIML, future-pollution falsification, multi-pollutant instrumentation, and monitor-continuity checks.

The paper is especially useful for adapting wind instruments to a county-day ozone shock design because it separates the construction of wind instruments from source-specific engineering models.

## 9. Replication feasibility
Replication requires EPA AQS pollution monitors, NARR wind vector fields, gridded temperature and precipitation, county-day population denominators, health outcomes, and enough monitor density to form spatial groups.

A close adaptation to the ozone alert project would require daily county ozone, a norm/shock decomposition, AirNow alert data, wind fields, weather controls, and health claims at county-day or finer resolution.

The wind-IV component is feasible if wind direction has a strong first stage for ozone shocks after conditioning on ozone norms, weather, fixed effects, and alert variables.

Key risks for ozone are photochemical formation, sunlight and temperature confounding, co-transport with ozone precursors, and the possibility that wind direction may predict alert issuance through forecasted air quality rather than only realized ozone.

## 10. Tables (project-relevance gated)
### Table 1. Summary statistics
Main sample: county-day observations from 1999 to 2013, with PM2.5 mean $10.48$ micrograms per cubic meter, standard deviation $7.13$, and 1,980,549 observations. Useful for understanding scale but not central to the wind-IV adaptation.

### Table 2. OLS and IV mortality by age group
Relevant because it reports the main mortality IV estimates and first-stage strength. The all-elderly IV estimate is about $0.69$ additional deaths per million for a one-day $1$ microgram per cubic meter PM2.5 increase over a three-day outcome window.

### Table 3. OLS and IV hospital outcomes
Relevant as a placebo/outcome template. IV estimates show PM2.5 increases ER-driven use and spending, while non-ER planned admissions are small and insignificant.

### Table 8. Multi-pollutant IV with CO and ozone
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

Notes: dependent variable is three-day mortality per million. All specifications instrument included pollutants with wind direction and include county, month-by-year, state-by-month fixed effects, flexible weather controls, two weather-control leads, and two leads/lags of instruments.

### Table 9. Robustness to instrument choices
| Specification | PM2.5 estimate | SE | Wind bins | Monitor groups | Season interactions | F-statistic | Observations |
|---|---:|---:|---:|---:|---|---:|---:|
| Smaller wind bins | 0.690 | 0.054 | 60 degrees | 100 | No | 197 | 1,980,549 |
| Fewer monitor groups | 0.719 | 0.056 | 90 degrees | 50 | No | 554 | 1,980,549 |
| More monitor groups | 0.652 | 0.063 | 90 degrees | 200 | No | 161 | 1,980,547 |
| Season interactions | 0.603 | 0.067 | 90 degrees | 100 | Yes | NA | 1,980,549 |

### Table 10. Robustness to fixed effects and weather controls
The PM2.5 mortality IV estimate remains positive across specifications with no weather controls, separate weather controls, full weather controls, and alternative fixed-effect structures. Reported estimates range from $0.270$ to $0.712$ deaths per million.

### Table 11. Robustness to instrument lags
| Lags | Mortality estimate | SE | Mortality F-statistic | Mortality observations | Life-years lost estimate | SE | Life-years F-statistic |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.602 | 0.077 | 389 | 1,980,549 | 2.737 | 0.488 | 392 |
| 1 | 0.730 | 0.061 | 304 | 1,980,549 | 3.267 | 0.477 | 310 |
| 3 | 0.687 | 0.061 | 298 | 1,977,622 | 2.997 | 0.487 | 304 |
| 4 | 0.683 | 0.061 | 298 | 1,974,768 | 2.993 | 0.485 | 304 |
| 5 | 0.680 | 0.061 | 297 | 1,971,974 | 2.978 | 0.480 | 303 |

## 11. Figures (project-relevance gated)
### Figure 2. Bay Area wind direction and PM2.5
Relevant because it shows wind direction is a strong local predictor of PM2.5 in 10-degree bins after fixed effects and flexible weather controls. Copied to wiki figure file `Deryugina_etal_2019_AER_fig2.png`.

### Figure 3. Boston wind direction and PM2.5
Relevant because it shows the wind-pollution relationship can differ by geography in ways consistent with upwind pollution sources. Copied to wiki figure file `Deryugina_etal_2019_AER_fig3.png`.

### Figure 7. First-stage strength by wind speed
Highly relevant because first-stage $F$-statistics are lowest on low-wind-speed days and largest on higher-wind-speed days, supporting the nonlocal transport interpretation. Copied to wiki figure file `Deryugina_etal_2019_AER_fig7.png`.

### Low-priority figures
Figures on PM2.5 trends, life expectancy prediction, mortality windows, and treatment-effect heterogeneity are useful background but less central to this project's wind-IV and ozone-alert design.
