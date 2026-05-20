# Monitor Group First Stage

**Summary**: Deryugina et al. group pollution monitors spatially and let wind-direction first stages vary by group (source: Deryugina_etal_2019_AER.pdf). This is meant to preserve regional transport variation while reducing monitor-specific local-source measurement error (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## Specification

The first stage interacts monitor-group indicators with wind-direction-bin indicators (source: Deryugina_etal_2019_AER.pdf). The preferred specification uses 100 spatial monitor groups based on $k$-means clustering of monitor locations, and the final PM2.5 sample includes 93 monitor groups with PM2.5 readings (source: Deryugina_etal_2019_AER.pdf).

$$
PM2.5_{cdmy}
= \sum_{g \in G} \sum_{b=0}^{2} \beta_b^g \mathbf{1}[G_c=g] \times WINDDIR_{cdmy}^{90b}
+ X'_{cdmy}\sigma + \alpha_c + \alpha_{sm} + \alpha_{my} + \epsilon_{cdmy}.
$$

The coefficient $\beta_b^g$ is allowed to vary across monitor groups, so the same wind-direction bin can imply different PM2.5 changes in different regions (source: Deryugina_etal_2019_AER.pdf). The authors use only four 90-degree wind bins in the preferred design because increasing the number of instruments is computationally burdensome (source: Deryugina_etal_2019_AER.pdf).

## Measurement-Error Logic

The authors argue that sparse monitor placement can make monitor readings an imperfect measure of county residents' average exposure (source: Deryugina_etal_2019_AER.pdf). By restricting the wind-direction effect to be the same for all monitors within a geographic group, the first stage downweights highly local pollution variation that might affect one monitor but not the broader county population (source: Deryugina_etal_2019_AER.pdf). They argue that nonlocal transported pollution is more likely than local-source emissions to move monitors in the same group in the same direction (source: Deryugina_etal_2019_AER.pdf).

## Robustness Checks

Table 9 changes the wind-angle bins from 90 degrees to 60 degrees, changes monitor groups from 100 to 50 or 200, and interacts instruments with season (source: Deryugina_etal_2019_AER.pdf). The mortality estimates remain similar across these changes, which the authors use as evidence that the first-stage aggregation decisions are not driving the result (source: Deryugina_etal_2019_AER.pdf).

| Specification | PM2.5 estimate | Wind bins | Monitor groups | Season interactions | F-statistic |
|---|---:|---:|---:|---|---:|
| Smaller wind bins | 0.690 | 60 degrees | 100 | No | 197 |
| Fewer monitor groups | 0.719 | 90 degrees | 50 | No | 554 |
| More monitor groups | 0.652 | 90 degrees | 200 | No | 161 |
| Season interactions | 0.603 | 90 degrees | 100 | Yes | NA |

Each estimate in the table is an IV estimate for the effect of a one-day PM2.5 increase on three-day elderly mortality per million beneficiaries (source: Deryugina_etal_2019_AER.pdf).

## First-Stage Strength by Wind Speed

Deryugina et al. argue that if the design captures nonlocal transport, the first stage should be weaker on low-wind-speed days and stronger on higher-wind-speed days (source: Deryugina_etal_2019_AER.pdf). Figure 7 reports first-stage $F$-statistics by wind-speed decile and shows the lowest $F$-statistic in the low-wind-speed subsample (source: Deryugina_etal_2019_AER.pdf).

**Figure 7:** Relationship between the Strength of the First Stage and Wind Speed (p. 35) (source: Deryugina_etal_2019_AER.pdf)  
![First-stage F-statistics by wind speed decile](figures/Deryugina_etal_2019_AER_fig7.png)
- Key visual finding: The first stage is strongest on higher-wind-speed days, which supports the transported-pollution interpretation (source: Deryugina_etal_2019_AER.pdf).
- **Figure notes:** Each bar comes from a first-stage regression using only observations in the corresponding wind-speed decile (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[wind-direction-instruments]]
- [[wind-iv-identification-assumptions]]
- [[wind-iv-late-monotonicity]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[deryugina-etal-2019-aer]]
