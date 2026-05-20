# Air Quality Alerts and Avoidance Behavior

**Summary**: Air-quality alert systems (AQAS) induce avoidance behavior by providing public information about elevated pollution. Anderson, Hyun, and Lee (2022) establish via fuzzy RD that PM alerts in South Korea reduce respiratory and cardiovascular health expenditures purely through behavioral avoidance — without changing ambient pollution levels.

**Sources**: Anderson_etal_2022_NBER.pdf

**Last updated**: 2026-05-19

---

## What AQAS Do

An air-quality alert system issues public warnings when a pollution index crosses a threshold. Alerts recommend protective actions (wearing masks, reducing outdoor activity, avoiding exercise, keeping windows closed). Crucially, alerts do not reduce ambient pollution — they only affect what agents *know* and therefore *do*.

AHL2022 confirm the pure behavioral mechanism empirically: ambient PM levels do not jump at the alert threshold (Table A4), so any health expenditure reductions at the threshold must be driven by alert-induced behavior, not by actual pollution reductions. NAVER keyword search data (Figure 2) show that information transmission is successful: searches for air quality terms spike sharply on alert days.

## Types of Avoidance Responses

The paper's framework decomposes avoidance into:

- **Contemporaneous actions** $b$ triggered by the realized alert signal: staying indoors, canceling outdoor activities, wearing masks, seeking medication proactively, postponing non-urgent medical procedures.
- **Ex-ante preparations** $k$: investments made in advance based on the pollution *environment* (not just today's alert) — e.g., purchasing air purifiers, stocking inhalers, adjusting chronic medication regimens. AHL2022 does not test whether alert-program *introduction* shifts $k^*$; the JMP's norm × alert interaction ($\beta_A^N$) tests this.

In AHL2022, the RD design identifies only the contemporaneous $b$ response: the comparison is alert vs. no alert on days near the issuance threshold, holding realized PM roughly constant (no PM jump at threshold).

## Heterogeneity by Disease and Age Group

| Effect | Age group | Magnitude |
|---|---|---|
| Respiratory | Minors (0–19) | −30% (−15 ¢/cap) |
| Respiratory | Adults (20–64) | significant but smaller |
| Respiratory | All ages | −5.83 ¢/cap |
| Cardiovascular | Adults (20–64) | −23% (−2.83 ¢/cap) |
| Cardiovascular | Older Adults (≥65) | −14% (−9.64 ¢/cap) |
| Cardiovascular | All ages | −3.26 ¢/cap |

The finding of cardiovascular benefits for adults — not just children's respiratory — is novel. It suggests alert-induced avoidance actions include behaviors relevant to cardiac triggers (reduced physical exertion, reduced outdoor exposure), not only respiratory protection.

## Dynamic Effects

Alert-induced avoidance has multi-day benefits, consistent with average alert duration ≈1.87 days. The 3-day rolling-sum specification (Eq. 8) shows effects 2.5–2.8× the contemporaneous estimates:

- All-age respiratory: −16.1 ¢/cap (3-day)
- All-age cardiovascular: −8.04 ¢/cap (3-day)

## Identification: Why No Confounding by Pollution

The critical design feature of AHL2022 is that the RD running variable (threshold-normalized PM) does not produce a PM jump at zero. This rules out the alternative explanation that health improvements near the threshold reflect lower actual pollution exposure rather than behavioral responses. The design cleanly isolates the information-provision effect.

This differs from studies comparing alert vs. non-alert days in a panel framework, where alert days are correlated with higher pollution — making it impossible to separate the information channel from the direct exposure channel without additional identification.

## JMP connection

The JMP's estimating equation includes:

$$
h_{it} = \cdots + \beta_A A_{it} + \beta_A^S (\rho_{it} - P_{im}) A_{it} + \beta_A^N P_{im} A_{it} + \cdots
$$

- $\beta_A$ captures the infra-marginal contemporaneous avoidance effect on health outcomes (the $b$-response), parallel to AHL2022's main estimate.
- $\beta_A^S - \beta_A^N$ tests whether alert receipt modifies the *shock* vs. *norm* response differently — i.e., whether alert information differentially shifts avoidance against unexpected vs. expected pollution.
- $\beta_A^N$ tests whether introducing the alert program shifts ex-ante defensive capital $k^*$.

The government-share version of $h_{it}$ in the JMP yields $\hat{\beta}_A \approx \Delta E$ (the fiscal externality), following AHL2022's bounds logic. See [[welfare-bounds-alert-programs]].

## Related pages

- [[anderson-hyun-lee-2022-nber]]
- [[welfare-bounds-alert-programs]]
- [[ex-ante-ex-post-adaptation]]
- [[forecasts-alerts-and-identification]]
- [[health-production-and-adaptation]]
