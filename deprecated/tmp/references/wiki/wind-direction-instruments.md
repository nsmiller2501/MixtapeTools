# Wind Direction Instruments

**Summary**: Wind direction instruments use day-to-day shifts in where air arrives from to generate quasi-experimental pollution variation (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. implement this with monitor-group-by-wind-bin instruments for daily PM2.5 (source: Deryugina_etal_2019_AER.pdf).

**Sources**: Deryugina_etal_2019_AER.pdf

**Last updated**: 2026-05-03

---

## Core Idea

Deryugina et al. instrument daily county PM2.5 with daily wind direction because wind transports pollution from upwind locations into a county (source: Deryugina_etal_2019_AER.pdf). The design uses changes in wind direction rather than prevailing wind direction because predictable prevailing winds may influence monitor placement or residential sorting (source: Deryugina_etal_2019_AER.pdf). The authors state that this makes the method better suited to acute exposure than chronic exposure (source: Deryugina_etal_2019_AER.pdf).

## Construction

The wind instrument is based on daily county wind direction, with wind direction defined as the direction the wind is blowing from (source: Deryugina_etal_2019_AER.pdf). In the preferred first stage, wind direction is grouped into 90-degree bins and interacted with spatial monitor-group indicators (source: Deryugina_etal_2019_AER.pdf). The omitted wind-direction category is $[270,360)$, so the included bins are $[0,90)$, $[90,180)$, and $[180,270)$ (source: Deryugina_etal_2019_AER.pdf).

$$
Z_{cdmy}^{gb}
= \mathbf{1}[G_c=g] \times WINDDIR_{cdmy}^{90b}.
$$

## Why Geography-Specific Instruments Matter

The effect of a wind direction on pollution differs across places because upwind emissions sources, terrain, coastlines, and regional transport patterns differ across places (source: Deryugina_etal_2019_AER.pdf). The Bay Area example shows higher PM2.5 when wind comes from the southeast and lower PM2.5 when wind comes from the west or north (source: Deryugina_etal_2019_AER.pdf). The Boston example shows higher PM2.5 when wind comes from the southwest and lower PM2.5 when wind comes from ocean or less populated directions (source: Deryugina_etal_2019_AER.pdf).

**Figure 2:** Bay Area wind direction and PM2.5 (p. 6) (source: Deryugina_etal_2019_AER.pdf)  
![Bay Area wind direction and PM2.5 first stage](figures/Deryugina_etal_2019_AER_fig2.png)
- Key visual finding: The first-stage pattern varies sharply by wind direction in the Bay Area (source: Deryugina_etal_2019_AER.pdf).
- **Figure notes:** The plotted regression uses 10-degree wind-direction bins, fixed effects, flexible weather controls, and robust standard errors (source: Deryugina_etal_2019_AER.pdf).

**Figure 3:** Boston wind direction and PM2.5 (p. 7) (source: Deryugina_etal_2019_AER.pdf)  
![Boston wind direction and PM2.5 first stage](figures/Deryugina_etal_2019_AER_fig3.png)
- Key visual finding: The Boston first-stage pattern differs from the Bay Area pattern, which motivates allowing wind effects to vary by geography (source: Deryugina_etal_2019_AER.pdf).
- **Figure notes:** The figure uses the same structure as Figure 2 for a different region (source: Deryugina_etal_2019_AER.pdf).

## Diagnostic Value

Wind-direction instruments should have a strong first stage for the pollutant or shock they are meant to move (source: Deryugina_etal_2019_AER.pdf). Deryugina et al. report large first-stage $F$-statistics in their main tables and state that weak-instrument bias is not a concern in their setting (source: Deryugina_etal_2019_AER.pdf). They also use placebo wind instruments and LIML as robustness checks against spurious or weak first-stage concerns (source: Deryugina_etal_2019_AER.pdf).

## Related pages

- [[monitor-group-first-stage]]
- [[wind-iv-identification-assumptions]]
- [[wind-iv-late-monotonicity]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[deryugina-etal-2019-aer]]
