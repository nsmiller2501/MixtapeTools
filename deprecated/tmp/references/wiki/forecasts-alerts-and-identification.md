# Forecasts Alerts And Identification

**Summary**: Forecasts and alerts can make realized pollution shocks partly anticipated, which changes the interpretation of panel weather or pollution estimates (source: Carleton_etal_2024_HESECC.pdf). For the project, AQAD alerts are both policy treatments and information variables that may affect defensive behavior (source: Carleton_etal_2024_HESECC.pdf).

**Sources**: Carleton_etal_2024_HESECC.pdf; Deryugina_etal_2019_AER.pdf; Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf; Anderson_etal_2022_NBER.pdf

**Last updated**: 2026-05-19

---

## Forecasts As An Identification Problem

Carleton et al. emphasize that panel fixed-effects weather regressions often rely on short-run weather variation being plausibly as-good-as-random (source: Carleton_etal_2024_HESECC.pdf). Forecasts complicate this logic. If people observe forecasts and adjust behavior before the realized shock, then realized weather is not purely unexpected from the behavioral point of view (source: Carleton_etal_2024_HESECC.pdf).

The implication is that a coefficient on realized weather or pollution can mix direct exposure effects with forecast-induced adaptation. Forecast controls are one way to separate expected from unexpected realized variation (source: Carleton_etal_2024_HESECC.pdf).

## Application To Ozone Alerts

AQAD alerts are public forecasts or warnings about air quality. In the project, they can affect health through at least three paths:

- They may induce contemporaneous avoidance or medical behavior on alert days.
- They may reveal information about expected pollution risk, changing beliefs about $P_{im}$.
- They may be correlated with forecasted ozone shocks, which affects the interpretation of $\epsilon_{it}$.

This means alerts should be treated as part of the information environment, not only as a binary policy control (source: Carleton_etal_2024_HESECC.pdf).

## Interaction With Wind IV

Deryugina et al. use wind direction as an instrument for acute pollution exposure and assume wind affects health only through pollution after controls (source: Deryugina_etal_2019_AER.pdf). In an ozone-alert setting, wind may also predict forecasted ozone and alert issuance. That creates a project-specific exclusion issue: the wind instrument must be defended against both physical exposure channels and information/behavior channels (source: Deryugina_etal_2019_AER.pdf; source: Carleton_etal_2024_HESECC.pdf).

## Design Implications

The project should separately track realized ozone, ozone norms, alerts, visibility, and weather conditions. If feasible, forecast variables should be added or proxied so the analysis can distinguish unexpected shocks from forecasted shocks. Robustness should ask whether the estimated shock effect changes when alert days, visibility, or forecastable high-ozone conditions are controlled more aggressively.

## Ozone Action Day null result (Bento et al. 2023)

Bento et al. (2023) test directly whether OAD alerts induce short-run adaptive responses to temperature shocks. Adding the interaction $\text{Shock} \times \mathbf{1}[\text{Action Day}]$ to their main estimating equation on the 2004–2013 OAD sample yields:

$$
\hat{\beta}_{\text{Shock} \times \text{Action Day}} = 0.068, \quad \text{SE} = 0.188 \quad (\text{statistically insignificant})
$$

No meaningful short-run adaptive response detected nationally. This baseline — absent for ozone concentration outcomes — motivates asking whether health outcome responses to alerts are detectable in the JMP setting, where alerts may induce behavioral changes (avoidance, medication) without necessarily reducing ambient ozone (source: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf).

## Causal evidence that alerts induce avoidance (Anderson, Hyun, and Lee 2022)

AHL2022 provide the cleanest empirical evidence that PM alerts actually change behavior. Using a fuzzy RD on South Korea's PM alert threshold, they show:

1. Alerts raise the probability of behavioral avoidance (proxied by NAVER keyword searches).
2. Alerts reduce government-borne health expenditures by ≈30% for youth respiratory and ≈14–23% for adult cardiovascular.
3. Ambient PM does *not* jump at the alert threshold — effects are purely behavioral (avoidance), not due to pollution reduction.

This validates the treatment of AQAD alerts in the JMP as information-provision events that shift avoidance behavior $b$ without confounding via actual exposure changes. The corresponding fiscal externality $\Delta E$ (government health cost reduction) enters the JMP's benefit-cost accounting as a lower bound on $\Delta W$. See [[anderson-hyun-lee-2022-nber]] and [[welfare-bounds-alert-programs]].

## Related pages

- [[ex-ante-ex-post-adaptation]]
- [[health-production-and-adaptation]]
- [[wind-iv-identification-assumptions]]
- [[adapting-wind-iv-to-ozone-shocks]]
- [[bento-miller-mookerjee-severnini-2023-jeem]]
- [[anderson-hyun-lee-2022-nber]]
- [[air-quality-alerts-and-avoidance-behavior]]
- [[welfare-bounds-alert-programs]]
