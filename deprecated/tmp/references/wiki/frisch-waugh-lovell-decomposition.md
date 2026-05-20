# Frisch–Waugh–Lovell Decomposition

**Summary**: The Frisch–Waugh–Lovell (FWL) theorem states that in a partitioned OLS regression, the coefficients on one subset of regressors equal those from regressing the residualized outcome on residualized versions of that subset. In climate-economy applications, it enables a single regression to simultaneously identify both short-run (weather-shock) and long-run (climate-norm) effects without bias from the de-seasonalization typically required by panel FE models.

**Sources**: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf

**Last updated**: 2026-05-19

---

## The theorem

Let the regression model be partitioned as:

$$
y = X_1\beta_1 + X_2\beta_2 + \varepsilon
$$

The FWL theorem (Frisch and Waugh 1933; Lovell 1963) states that $\hat{\beta}_2$ from this joint regression equals $\hat{\beta}_2$ from:

$$
M_1 y = (M_1 X_2)\beta_2 + e
$$

where $M_1 = I - X_1(X_1'X_1)^{-1}X_1'$ is the residual-maker on $X_1$. That is: partial out $X_1$ from both $y$ and $X_2$, then regress.

**Key implication for de-seasonalization**: If $X_2$ (the regressors of interest) are already orthogonal to $X_1$ (the fixed effects), then $M_1 X_2 \approx X_2$, and the outcome $y$ need not be de-seasonalized to recover consistent $\hat{\beta}_2$. This is what Bento et al. (2023) exploit: by constructing both weather shocks and climate norms as deviations from or averages of the same moving-average base, the regressors are approximately de-seasonalized, so the outcome (ozone) can enter the regression in levels.

## Application to climate impacts (Bento et al. 2023)

Bento et al. decompose observed temperature $x_{it}$ into:
- **Climate norm** $\bar{x}_{i\bar{p}}$: 30-year monthly moving average, lagged 1 year
- **Weather shock** $(x_{it} - \bar{x}_{i\bar{p}})$: contemporaneous deviation from the norm

Their unifying estimating equation (Eq. 6):

$$
y_{it} = \alpha + \beta_W(x_{it} - \bar{x}_{i\bar{p}}) + \beta_C \bar{x}_{i\bar{p}} + \mu_i + \lambda_s + \nu_{it}
$$

FWL guarantees:
- **$\hat{\beta}_W \approx \hat{\beta}_{FE}$** from the standard panel FE regression — weather shocks identify the short-run effect, no adaptation absorbed
- **$\hat{\beta}_C \approx \hat{\beta}_{CS}$** from the pure cross-section — climate norms identify the long-run effect, inclusive of all adaptation
- The adaptation measure $\hat{\beta}_W - \hat{\beta}_C$ is directly testable from the covariance matrix of a single regression, without SUR or bootstrap

Verified empirically: shock estimate 1.678 ≈ panel FE estimate 1.659; norm estimate 1.164 ≈ cross-section estimate 1.166 (source: Bento_Miller_Mookerjee_Severnini_2023_JEEM.pdf).

## Why this matters for the JMP project

The JMP project adopts the same FWL decomposition to separately identify responses to expected long-run ozone norms $P_{im}$ vs. unexpected daily shocks $\epsilon_{it}$. The norm–shock gap $\beta^S - \beta^N$ recovers the effectiveness of agents' intrinsic ex-ante defensive actions. The FWL theorem is the technical guarantee that both coefficients can be recovered from one equation without de-meaning the health outcome, and that the norm and shock estimates are interpretable as long-run and short-run limits respectively.

See [[bento-miller-mookerjee-severnini-2023-jeem]] for full empirical details and [[climate-norm-weather-shock-decomposition]] for the implementation of the norm construction.

## Relationship to other identification approaches

The FWL decomposition is agnostic about whether agents are rational, myopic, or inattentive — it does not require a structural model of expectations. It only requires that the 30-year MA is a good proxy for the climate norm agents actually experience. This is distinct from the [[ex-ante-ex-post-adaptation]] framework (Carleton et al. 2024), which requires a timing assumption about when agents learn about shocks.

The FWL approach also differs from the [[wind-direction-instruments]] IV strategy: FWL identifies the causal decomposition through the norm/shock orthogonality structure; IV additionally addresses endogeneity of realized ozone.

## Related pages

- [[bento-miller-mookerjee-severnini-2023-jeem]]
- [[climate-norm-weather-shock-decomposition]]
- [[ex-ante-ex-post-adaptation]]
- [[carleton-etal-2024-hesecc]]
