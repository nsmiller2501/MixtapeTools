# Welfare Bounds for Alert Programs

**Summary**: Anderson, Hyun, and Lee (2022) develop a welfare-bounds framework that lets researchers estimate a conservative lower bound on the social welfare gain from an information-provision alert program without measuring private utility directly. The key insight: since more accurate information weakly helps private agents, any reduction in publicly reimbursed health costs is a lower bound on total social welfare gain.

**Sources**: Anderson_etal_2022_NBER.pdf

**Last updated**: 2026-05-19

---

## The Decomposition

Welfare for agent $i$ decomposes into private utility and the fiscal externality:

$$
W_i = U_i(a_i, pm) + E_i
$$

where $U_i$ is private utility net of avoidance costs and $E_i$ is health expenditures borne by the government (publicly reimbursed costs). The change from receiving an alert is:

$$
\Delta W_i = \Delta U_i + \Delta E_i
$$

**Lower-bound argument**: Receiving an accurate alert about high PM (when PM actually is elevated) improves the agent's information set. More accurate information about a health-relevant variable weakly improves private decision-making, so:

$$
\Delta U_i \geq 0 \implies \Delta E_i \leq \Delta W_i
$$

Therefore the estimated reduction in *government-borne* health expenditures $\Delta E_i$ is a lower bound on total welfare gain, even though the alert also triggers avoidance actions that are individually costly.

## Why $\Delta U_i \geq 0$

Private utility is:

$$
U_i(a_i, pm) = b_i(a_i) - s_i^{\text{pvt}} \cdot p_s(a_i, pm)
$$

where $b_i(a_i)$ is the net benefit of avoidance action minus its cost, $s_i^{\text{pvt}}$ is the private cost-sharing rate, and $p_s(a_i, pm)$ is the probability of an adverse health event. An alert shifts agents' beliefs about PM from $pm^{\text{avg}}$ to $pm^{\text{hi}}$, inducing stronger avoidance actions. Agents who voluntarily take those actions must expect them to increase private utility (revealed preference); the alert just enables them to act on information they did not previously have.

The private utility gain from the alert:

$$
\Delta U_i = \left[b_i(a_i(pm^{\text{hi}})) - b_i(a_i(pm^{\text{avg}}))\right] - s_i^{\text{pvt}}\left[p_s(a_i(pm^{\text{hi}}), c) - p_s(a_i(pm^{\text{avg}}), c)\right]
$$

This can be positive even though avoidance is costly, because health risk reduction dominates.

## Empirical identification of $\Delta E$

AHL2022 identify $\Delta E$ via the fiscal externality mechanism:

- Government-reimbursed health expenditures ($\approx 70\%$ of total in South Korea) fall when alerts are issued.
- The RD-estimated coefficient on the alert indicator (using the above-threshold PM running variable as the instrument) identifies the LATE of alert receipt on per-capita government health spending.
- **Result**: Alert system reduced government-borne health costs by $28.6M over 2016–2017 (contemporaneous), $36.7M including dynamic effects.
- System maintenance cost ≈$4M. **Minimum BCR: 7.1:1** (contemporaneous) or **9.2:1** (dynamic).

## JMP application

The JMP adopts this framework directly. In the JMP estimating equation:

$$
h_{it} = \cdots + \beta_A A_{it} + \cdots
$$

when $h_{it}$ is the **government-share** component of Medicare inpatient costs, $\hat{\beta}_A$ identifies $\Delta E$ — the fiscal externality from alert-induced avoidance behavior. This provides a welfare lower bound $\Delta E \leq \Delta W$ and, combined with OOP cost estimates (an upper bound on WTP), brackets the social welfare gain from the alert program.

The JMP extends AHL2022's single lower-bound calculation in two ways:

1. **Two-sided bounding**: Out-of-pocket spending reduction bounds WTP from above, giving $\Delta E \leq \Delta W \leq \Delta \text{WTP}$.
2. **Shock × alert interactions**: Testing $\beta_A^S$ and $\beta_A^N$ (alert interactions with the shock and norm) probes whether alert introduction shifts ex-ante defensive capital $k^*$, which AHL2022 does not test.

## Generalizability

The bounds approach applies to any information-provision intervention where:
1. The externality (fiscal cost, publicly reimbursed expenditure) is separately observable.
2. More accurate information weakly improves private utility.

AHL2022 note this framework applies to restaurant hygiene report cards, electricity usage information programs, hospital quality report cards, and similar public-information interventions.

## Related pages

- [[anderson-hyun-lee-2022-nber]]
- [[air-quality-alerts-and-avoidance-behavior]]
- [[ex-ante-ex-post-adaptation]]
- [[health-production-and-adaptation]]
- [[forecasts-alerts-and-identification]]
