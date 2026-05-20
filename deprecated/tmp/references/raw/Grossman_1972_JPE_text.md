## Bibliographic metadata
doi: null
authors: [Grossman, Michael]
title: On the Concept of Health Capital and the Demand for Health
year: 1972
venue: Journal of Political Economy
venue_type: journal

## Plain-English synthesis
Grossman builds the canonical economic model of health as a durable capital stock. People do not demand medical care for its own sake; they demand "good health," which produces healthy time and can be maintained or increased through investment. Health differs from other human capital because it changes the amount of time available for work and nonmarket activity, not just productivity during that time. The model treats medical care, own time, education, and other inputs as ways to produce gross health investment, while health depreciates with age. The key project use is conceptual: ozone norms and alerts can be understood as changing either the expected return to ex-ante health investment or the contemporaneous use of defensive inputs. Grossman supplies the health-production side of the project; Carleton et al. supply the ex-ante/ex-post adaptation timing structure.

## 1. Research question

Why do people demand medical care, and what determines how much health they produce? The paper argues that the right object of analysis is not the demand for medical services per se but the demand for the underlying commodity — "good health" — and constructs a formal economic model of that demand. Specific questions: How does the optimal stock of health capital vary over the life cycle with age (depreciation)? How do wage rates affect health and medical care demands? How does education (nonmarket efficiency) affect health and medical care?

## 2. Audience

Health economists and human capital theorists. The paper speaks directly to researchers studying medical care utilization, health differentials by age/education/income, and the household production paradigm pioneered by Becker (1965).

## 3. Method

Theoretical model in the Becker (1965) household production tradition. The key insight is that health is a *durable capital stock*, not a flow commodity — it produces "healthy time" (i.e., days free from illness) as output. The model is formally a life-cycle optimization problem, solved in both discrete and continuous time (calculus of variations / Euler equations).

Key structural elements:
- Intertemporal utility function over healthy time $h_i = \phi_i H_i$ and a composite commodity $Z_i$
- Health accumulation: $H_{i+1} - H_i = I_i - \delta_i H_i$, where $I_i$ is gross investment and $\delta_i$ is the (exogenous, age-varying) depreciation rate
- Gross investment production function: $I_i = I_i(M_i, TH_i; E_i)$, where $M_i$ is medical care, $TH_i$ is own time, and $E_i$ is human capital (education)
- Full-wealth constraint incorporating time lost to illness $TL_i = \Omega - h_i$
- Equilibrium: marginal efficiency of health capital (MEC) = user cost of capital $\pi_{i-1}(r - \tilde{\pi}_{i-1} + \delta_i)$

The paper develops both a pure investment model (health yields only time returns) and a consumption–investment model (health also directly enters utility). Most formal results use the pure investment case.

## 4. Data

None — purely theoretical paper. Empirical applications are deferred to Grossman (1970), his Columbia Ph.D. dissertation "The Demand for Health: A Theoretical and Empirical Investigation" (forthcoming NBER monograph).

## 5. Statistical methods

No empirical estimation. Formal results are derived analytically. Key comparative statics:
- Life cycle depreciation: $\tilde{H}_i = -s_i \varepsilon_i \tilde{\delta}_i$, where $s_i = \delta_i/(r + \delta_i)$ is depreciation's share of capital cost and $\varepsilon_i$ is the elasticity of the MEC schedule. Health falls with age at an accelerating rate.
- Gross investment (medical care) rises with age if and only if $\varepsilon < 1/s_i$ — sufficient condition is $\varepsilon < 1$.
- Wage elasticity of health: $e_{H,W} = (1-K)\varepsilon$, where $K$ = time's share in gross investment cost.
- Wage elasticity of medical care: $e_{M,W} = K\sigma_p + (1-K)\varepsilon > e_{H,W}$, because higher wages induce substitution of market goods for own time in production.
- Education effect on health: $\hat{H} = r_H \varepsilon$, where $r_H > 0$ if education raises gross investment productivity.
- Education effect on medical care: $\hat{M} = r_H(\varepsilon - 1)$ — if $\varepsilon < 1$, more educated people demand *more* health but *less* medical care.

## 6. Findings

1. **Life cycle**: If the depreciation rate rises with age (biological aging), the demand for health capital declines monotonically over the life cycle. The shadow price of health rises with age, not because the price of medical care rises, but because it costs more to maintain a deteriorating stock.

2. **Age and medical care**: A rising depreciation rate can simultaneously reduce desired health *and* increase medical care expenditure — as long as the MEC schedule is inelastic ($\varepsilon < 1$). The intuition: individuals partially offset higher depreciation via higher gross investment (medical care), even though they cannot fully compensate.

3. **Wage and health**: Higher wages raise the shadow value of healthy time (investment motive) and increase demand for both health and medical care. Medical care rises more than proportionally because high-wage individuals substitute medical care for their expensive own time.

4. **Education and health**: More educated people are more efficient producers of health (lower $\pi$). This shifts the MEC schedule rightward, raising optimal health. If $\varepsilon < 1$, they achieve better health with *less* medical care — a key prediction distinguishing the model from naive "income effect" stories.

5. **Death as an economic choice**: As depreciation cumulates with age, $H_i$ eventually falls to $H_{\min}$ and the individual "chooses" to die. Death is an optimal corner solution, not an exogenous event.

## 7. Contributions

- **First formal model of the demand for health as a durable capital stock.** Prior work (Mushkin 1962, Becker 1964, Fuchs 1966) had suggested health was a form of human capital but had not modeled it. Grossman shows health capital is *fundamentally different* from knowledge capital: knowledge raises productivity; health capital determines the total amount of time available (sick days vs. healthy days). This justifies a distinct model.

- **Shadow price framework for health.** The paper shows that the "price" of health depends on age (depreciation rate), wage (value of time), education (production efficiency), and input prices — not just the price of medical care. This reorients empirical research away from insurance/price effects toward supply-side determinants.

- **Reconciling positive age–medical care gradient and negative education–medical care gradient.** The model produces the observationally puzzling finding that older people use more medical care (high depreciation, $\varepsilon < 1$) while more educated people use less (lower $\pi$, better efficiency). Both patterns emerge from the same structural primitive — the elasticity of the MEC schedule.

- **Household production approach to health.** Extends Becker's (1965) time model to allow time loss due to illness, making sick time a genuine economic variable. Endogenizes length of life.

## 8. Replication feasibility

Purely theoretical — no data or code. The companion empirical work is Grossman (1970 dissertation / forthcoming NBER monograph), which uses survey data on individual health and medical care. The 1972 JPE paper is widely reprinted and the model is canonical in health economics.

---

*Extract saved from 33-page PDF (marker conversion, CPU mode, 2026-05-02). No figures with empirical content; 5 theoretical diagrams (MEC/supply curve intersections) omitted from this extraction.*
