# Ex Ante Ex Post Adaptation

**Summary**: Ex-ante adaptation is durable preparation based on beliefs before shocks arrive; ex-post adaptation is contemporaneous response after shocks are realized (source: Carleton_etal_2024_HESECC.pdf). The project maps these channels onto ozone norms, daily shocks, and health-production inputs (source: Grossman_1972_JPE.pdf; source: Carleton_etal_2024_HESECC.pdf). Bento et al. (2023) provide direct causal evidence of this distinction: their adaptation measure $\hat{\beta}_W - \hat{\beta}_C = 0.514$ ppb/°C shows agents partially offset long-run temperature increases on ozone (source: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf).

**Sources**: Carleton_etal_2024_HESECC.pdf; Grossman_1972_JPE.pdf; Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf; Anderson_etal_2022_NBER.pdf

**Last updated**: 2026-05-19

---

## Definitions

Ex-post adaptation is reactive. It includes actions chosen after a weather or pollution shock is realized, such as staying indoors, changing activity timing, using medication, or seeking care (source: Carleton_etal_2024_HESECC.pdf).

Ex-ante adaptation is anticipatory. It includes durable investments or preparations chosen before shocks arrive, based on beliefs about future exposure: information acquisition, medical management, housing or filtration choices, and habits that reduce vulnerability (source: Carleton_etal_2024_HESECC.pdf; source: Grossman_1972_JPE.pdf).

## Project Mapping

The ozone norm $P_{im}$ is the part of exposure that can shape expectations. The daily shock $\epsilon_{it}$ is the part that arrives as a deviation from that expected environment. The health outcome depends on both exposure and defensive inputs:

$$
h_{it} = h(\rho_{it}, k(P_{im}), b_t(\epsilon_{it}, A_{it}), X_{it}).
$$

This expression is a conceptual map, not a literal estimating equation. It clarifies why the empirical model distinguishes expected exposure, unexpected exposure, alerts, and their interactions.

## Identification Concern

The cleanest interpretation requires $\epsilon_{it}$ to be less anticipated than $P_{im}$. Forecasts and alerts weaken that distinction if they let people anticipate the daily shock (source: Carleton_etal_2024_HESECC.pdf). That does not invalidate the design, but it changes the interpretation: the shock coefficient may include forecast-induced ex-ante or near-ex-ante behavior unless forecasts and alerts are modeled explicitly.

## Empirical evidence: Bento et al. (2023)

Bento et al. operationalize the ex-ante/ex-post distinction via the [[frisch-waugh-lovell-decomposition]]: the weather-shock coefficient ($\hat{\beta}_W = 1.678$ ppb/°C) is the short-run response before agents can adapt; the climate-norm coefficient ($\hat{\beta}_C = 1.164$ ppb/°C) is the long-run response after adaptation. The difference ($\hat{\beta}_W - \hat{\beta}_C = 0.514$ ppb/°C, SE 0.041) is statistically and economically significant, confirming that ex-ante adaptation is occurring. Ignoring it inflates the projected "climate penalty" by ~44% (source: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf).

## Alert programs and ex-ante adaptation (Anderson, Hyun, and Lee 2022)

AHL2022 identify the *contemporaneous* avoidance response $b$ to alerts (ex-post, triggered by the daily signal). Their RD design compares alert vs. no-alert days near the issuance threshold, holding actual PM roughly constant — so it isolates the information-provision effect on same-period behavior.

What AHL2022 do not test is whether the *introduction* of an alert program shifts agents' ex-ante defensive capital $k^*$ — i.e., whether the existence of the AQAS changes long-run investment in health capital or pollution protection. The JMP's norm × alert interaction ($\hat{\beta}_A^N$) is designed to test precisely this, examining whether norm-level exposure effects differ between counties or periods with vs. without alerts active. See [[anderson-hyun-lee-2022-nber]] and [[air-quality-alerts-and-avoidance-behavior]].

## Related pages

- [[health-production-and-adaptation]]
- [[forecasts-alerts-and-identification]]
- [[carleton-etal-2024-hesecc]]
- [[grossman-1972-jpe]]
- [[bento-miller-mookerjee-severnini-2023-jeem]]
- [[climate-norm-weather-shock-decomposition]]
- [[anderson-hyun-lee-2022-nber]]
- [[air-quality-alerts-and-avoidance-behavior]]
- [[welfare-bounds-alert-programs]]
