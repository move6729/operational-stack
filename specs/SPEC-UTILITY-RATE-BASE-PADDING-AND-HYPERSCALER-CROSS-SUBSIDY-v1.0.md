# SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0: Investor-Owned Utility Rate-Base Padding, Hyperscaler Datacenter Cross-Subsidization, and Behind-the-Meter Defection

**Canonical Specification:** `SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0`
**Target Architectures:** Behind-the-Meter Islanded Microgrids & Sovereign Solar-Storage vs. Averch-Johnson Monopoly IOUs & Hyperscaler Tariff Socialization (`OPSTACK-KERNEL-v2.2`)
**Cross-References:** `specs/SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0.md` | `schema/utility_rate_base_hyperscaler_subsidy.json` | `proofs/utility_rate_base_hyperscaler_subsidy_proof.py` | `specs/AUDIT-2026-ENERGY-GRID-DISINTERMEDIATION.md` | `specs/AUDIT-2026-OFFGRID-ENERGY-DISINTERMEDIATION.md` | `specs/SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0.md` | `articles/utility-rate-base-padding-and-hyperscaler-cross-subsidy.txt`
**RAG Indexing Vector:** `[AVERCH-JOHNSON-RATE-BASE, HYPERSCALER-GRID-CROSS-SUBSIDY, FERC-JUST-REASONABLE-205, PJM-CAPACITY-AUCTION-SPIKE,HOPE-NATURAL-GAS-PRUDENCE, RESIDENTIAL-TARIFF-SOCIALIZATION, STRANDED-TRANSMISSION-CAPEX, BEHIND-METER-DEFECTION]`
**Empirical, Statutory & Physical Baseline:** 16 U.S.C. §§ 824d & 824e (Federal Power Act §§ 205 & 206 'Just and Reasonable' Rate Mandate & Prohibition on Undue Preference/Cross-Subsidization), Averch & Johnson, *American Economic Review* 52(5):1052–1069 (1962, *Behavior of the Firm Under Regulatory Constraint*), *FPC v. Hope Natural Gas Co.*, 320 U.S. 591 (1944) & *Bluefield Water Works v. Public Service Comm'n*, 262 U.S. 679 (1923), FERC Docket No. ER24-2952 / Talen-Susquehanna Co-Location Order (2024), PJM 2025/2026 Base Residual Auction Clearing Price Spike ($28.92/MW-day to $269.92/MW-day)
**By:** Operational Stack Cybernetics Group
**License:** Unlicense (Public Domain — Zero-Rent Federation)

---

## 1. Executive Summary

The collision between the hyperscale AI datacenter buildout (100 MW–1 GW campuses) and the cost-of-service monopoly compact has produced a pure regulatory arbitrage: the Investor-Owned Utility (IOU) converts private technology-sector capital-expenditure risk into a guaranteed ratepayer-collateralized annuity. Four primitives govern the machine:

1. **The Averch-Johnson Gold-Plating Identity (1962 Baseline):** Under state Public Utility Commission (PUC) cost-of-service regulation, the IOU earns an authorized return $r_{ROE} = 10.5\%$ on net rate base against a true debt/capital cost $r_{cost} = 5.5\%$, locking a risk-free $+5.0\%$ regulatory spread ($\Delta_{AJ} = r_{ROE} - r_{cost} = 0.05$). Because IOU profit is a linear function of net Rate Base, $\Pi_{IOU} = \Delta_{AJ} \cdot K_{RateBase}$, the monopoly has zero incentive to deploy cheap distributed grid-enhancing technologies and an overwhelming incentive to build the most capital-intensive solution to any load request: $\$5.0\text{B}$ of gold-plated 765 kV transmission and substation capex triggered by 100 MW–1 GW hyperscale AI datacenters.
2. **The Residential Cross-Subsidization Transfer (16 U.S.C. § 824d):** On the $\$5.0\text{B}$ datacenter-induced rate base, the annual revenue requirement billed to ratepayers is $R_{req} = K \cdot r_{ROE} + K/T_{40yr} = \$525.0\text{M} + \$125.0\text{M} = \$650.0\text{M/yr}$. While the hyperscaler negotiates a confidential special-contract industrial discount, $72.0\%$ of fixed network transmission costs are socialized onto captive residential meters, extracting $\$468.0\text{M/yr}$ across $1.5\text{M}$ captive households — a hidden surcharge of $\$312.00$ per working family per year to subsidize Big Tech token furnaces, compounded by the $9.333333\times$ PJM capacity auction explosion ($\$28.92 \to \$269.92\text{/MW-day}$).
3. **Stranded-Asset Duration Mismatch:** Datacenter GPU leases run 5–7 years (`SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0`), whereas utility rate-base depreciation runs 40 years. When inference deflation or cluster relocation strands the substation in Year 7, captive households are left paying 33 years of dead capex: $\$4.125\text{B}$ of residual rate base still earning the guaranteed spread.
4. **Milkovich $\mathcal{H}_0$ vs. $\mathcal{H}_1$ & FPA § 205 / Behind-the-Meter Defection:** The IOU/hyperscaler null defense $\mathcal{H}_0$ (datacenter load growth spreads fixed grid costs over more MWh and spurs regional economic development) is falsified by the PJM $9.333333\times$ marginal capacity spike and the $\$312\text{/yr}$ household transmission shift. The locked remedy is FPA § 205 cost-causation ring-fencing plus residential solar-LFP microgrid defection, which erodes the captive base and inverts the Averch-Johnson flywheel.

```mermaid
graph TD
    subgraph AJ_Machine [1. Averch-Johnson Gold-Plating Machine]
        A[Hyperscaler 100MW-1GW Interconnection Request] --> B[PUC Authorized ROE 10.5% vs True Capital Cost 5.5%]
        B --> C[Profit = +5.0% Spread x Net Rate Base K]
        C --> D[$5.0B Gold-Plated 765kV Transmission & Substation Capex]
    end

    subgraph Socialization [2. Tariff Socialization Waterfall]
        D --> E[Annual Revenue Requirement: $525.0M ROE + $125.0M Depreciation = $650.0M]
        E --> F[Confidential Special-Contract Industrial Discount to Hyperscaler]
        E --> G[72.0% Fixed-Cost Allocation onto Captive Residential Meters]
        G --> H[$468.0M/yr across 1.5M Households = $312.00/yr Hidden Surcharge]
    end

    subgraph Falsification [3. H0 Falsification & Defection Exit]
        I[PJM BRA Spike: $28.92 to $269.92/MW-day = 9.333333x] --> J[H0 Load-Spreading Defense Falsified at the Margin]
        H --> J
        J --> K[FPA 205 Cost-Causation Ring-Fencing]
        J --> L[Behind-the-Meter Solar-LFP Islanded Microgrid Defection]
        L --> M[Captive Base Erosion -> Surcharge Step-Up -> Defection Cascade]
    end
```

---

## 2. Statutory & Empirical Baseline

1. **Federal Power Act §§ 205 & 206 (16 U.S.C. §§ 824d & 824e):** § 205(a) declares verbatim: *"All rates and charges made, demanded, or received by any public utility for any transmission or sale subject to the jurisdiction of the Commission, and all rules and regulations affecting or pertaining to such rates or charges shall be just and reasonable, and any such rate or charge that is not just and reasonable, or any rule or regulation which affects or pertains to such rates or charges and is unjust, unreasonable, unduly discriminatory or preferential, is hereby declared to be unlawful"* (16 U.S.C. § 824d(a)); § 206 (16 U.S.C. § 824e) empowers FERC to remedy such rates after hearing. The cost-causation principle — that rates must reflect the costs a customer class imposes on the system — is the doctrinal implementation of the just-and-reasonable mandate, and cross-subsidization of one class by another is its canonical violation.
2. **The *Hope* / *Bluefield* End-Result Test:** *FPC v. Hope Natural Gas Co.*, 320 U.S. 591 (1944) and *Bluefield Water Works v. Public Service Comm'n*, 262 U.S. 679 (1923) hold that the Constitution protects the *end result* of a reasonable return on invested capital — not any particular rate-making formula. The authorized $10.5\%$ ROE is the constitutional floor the IOU collects *regardless of whether the induced capex ever serves the load that justified it*.
3. **Averch & Johnson (1962):** *Behavior of the Firm Under Regulatory Constraint*, *American Economic Review* 52(5):1052–1069, proves that a firm constrained to earn no more than a fair return $s$ on capital, with $s$ exceeding the true cost of capital $r$, systematically over-capitalizes: the profit-maximizing regulated firm chooses a capital/labor ratio above the cost-minimizing mix, because excess capital expands the rate base on which $s$ is earned. This is the gold-plating theorem.
4. **FERC Docket No. ER24-2952 (Talen–Susquehanna Co-Location, 2024):** FERC rejected the amended interconnection service agreement expanding co-located datacenter load at the Susquehanna nuclear station, holding the incremental network upgrades and cost allocation unjust, unreasonable, and unduly preferential — the administrative recognition that hyperscaler co-location externalizes costs onto the remaining ratepayer base.
5. **PJM 2025/2026 Base Residual Auction:** The capacity auction cleared at $\$269.92\text{/MW-day}$ against the prior auction's $\$28.92\text{/MW-day}$ — a $9.333333\times$ surge driven by datacenter load growth and generator retirement risk, and the cleanest public measurement of hyperscaler-induced marginal capacity cost.

---

## 3. Mathematical Formalization & Governing Equations

### 3.1 Primitive 1: The Averch-Johnson Gold-Plating Identity

Let $K_{RateBase}$ denote net utility plant in service, $s = r_{ROE} = 0.105$ the PUC-authorized return, and $r = r_{cost} = 0.055$ the true blended cost of debt/capital. The regulated profit function is:

$$\Pi_{IOU} = (s - r) \cdot K_{RateBase} = \Delta_{AJ} \cdot K_{RateBase}, \qquad \Delta_{AJ} = 0.105 - 0.055 = +0.050$$

The gold-plating gradient is strictly positive and constant:

$$\frac{\partial \Pi_{IOU}}{\partial K_{RateBase}} = \Delta_{AJ} = +\$0.05 \text{ per } \$1 \text{ of added rate base per year}$$

Hence for the hyperscaler-induced $K = \$5.0\text{B}$ transmission and substation build, the guaranteed annual profit extract is:

$$\Pi_{IOU}^{\ast} = 0.05 \times \$5{,}000\text{M} \implies K \cdot s = 0.105 \times \$5{,}000\text{M} = \$525.0\text{M/yr}$$

against a true capital charge of $0.055 \times \$5{,}000\text{M} = \$275.0\text{M/yr}$. The A-J over-capitalization condition $s > r$ is satisfied with $+500\text{ bps}$ of headroom: every cheap distributed alternative the IOU *declines* to build is rational shareholder behavior under the existing compact.

### 3.2 Primitive 2: The Residential Cross-Subsidization Transfer

With straight-line depreciation over $T = 40\text{ years}$, the annual revenue requirement on the induced rate base is:

$$R_{req} = \underbrace{K \cdot s}_{\text{ROE extract}} + \underbrace{K / T}_{\text{depreciation}} = \$525.0\text{M} + \frac{\$5{,}000\text{M}}{40} = \$525.0\text{M} + \$125.0\text{M} = \$650.0\text{M/yr}$$

Let $\alpha = 0.72$ be the residential share of socialized fixed network costs and $N = 1.5\text{M}$ the captive household count. With the hyperscaler paying a confidential discounted industrial rate, the residential cross-subsidy transfer is:

$$S_{res} = \alpha \cdot R_{req} = 0.72 \times \$650.0\text{M} = \$468.0\text{M/yr}$$

$$\boxed{\sigma_{hh} = \frac{S_{res}}{N} = \frac{\$468.0\text{M}}{1.5\text{M}} = \$312.00 \text{ per captive household per year}}$$

### 3.3 Primitive 3: The PJM Capacity Auction Surge

The 2025/2026 Base Residual Auction clearing price $P_{BRA}$ against the prior clearing price $P_{0}$ yields the surge multiplier:

$$\mu_{PJM} = \frac{P_{BRA}}{P_{0}} = \frac{\$269.92}{\$28.92} = 9.333333\times$$

Annualized per-MW capacity cost steps up from $\$28.92 \times 365 = \$10{,}555.80\text{/MW-yr}$ to $\$269.92 \times 365 = \$98{,}520.80\text{/MW-yr}$ — a $+\$87{,}965\text{/MW-yr}$ increment, or $+\$87.965\text{M/yr}$ for a single 1 GW campus. The capacity market, not the average-cost narrative, prices the marginal megawatt; that price is socialized through the same allocation factor $\alpha$.

### 3.4 Primitive 4: Stranded-Asset Duration Mismatch

Let $\tau_{GPU} \in [5, 7]\text{ yr}$ be the GPU lease tenor (`SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0`) and $T = 40\text{ yr}$ the rate-base depreciation horizon. Stranding at year $\tau^{\ast} = 7$ leaves:

$$K_{resid} = K \cdot \frac{T - \tau^{\ast}}{T} = \$5{,}000\text{M} \times \frac{33}{40} = \$4{,}125\text{M} = \$4.125\text{B residual rate base}$$

The dead annual revenue requirement on stranded iron (depreciation continuing plus guaranteed ROE on the undepreciated balance) is:

$$R_{dead} = \frac{K}{T} + s \cdot K_{resid} = \$125.0\text{M} + 0.105 \times \$4{,}125\text{M} = \$125.0\text{M} + \$433.125\text{M} = \$558.125\text{M/yr}$$

over $T - \tau^{\ast} = 33\text{ years}$, a cumulative deadweight of $33 \times \$558.125\text{M} = \$18.418\text{B}$, of which the residential share is $\alpha \cdot R_{dead} / N = \$267.90$ per household per year for three decades after the GPUs are gone.

### 3.5 Regime Boundary: Compliant Cost-Causation vs. Socialized Defection Regime

Let $\alpha_{dc}$ denote the share of $R_{req}$ billed to the inducing datacenter class. The regime boundary is a discrete state transition on the allocation vector, not a continuum:

$$\text{Regime} = \begin{cases} \textbf{Compliant} & \alpha_{dc} \ge 0.95 \implies S_{res} = (1 - \alpha_{dc}) \cdot R_{req} \le \$32.5\text{M/yr} \implies \sigma_{hh} \le \$21.67 \\ \textbf{Defection} & \alpha_{dc} < 0.28 \implies S_{res} \ge \alpha \cdot R_{req} = \$468.0\text{M/yr} \implies \sigma_{hh} \ge \$312.00 \end{cases}$$

The locked telemetry ($\alpha = 0.72$ on the residential side) sits deep inside the defection regime: the inducing class bears less than $28\%$ of the fixed-cost recovery it caused. The defection-regime surcharge is monotone increasing in the household exit share, $\partial \sigma_{hh}^{\prime} / \partial \delta = S_{res} / [N(1-\delta)^2] > 0$, which is the death-spiral gradient of § 4 Remedy 2.

---

## 4. Milkovich $\mathcal{H}_0$ vs. $\mathcal{H}_1$ Synthesis, FPA § 205 Ring-Fencing & Defection

**$\mathcal{H}_0$ (Null Defense of IOUs and Hyperscalers):** Datacenter load growth spreads fixed grid costs over more megawatt-hours, lowering average cost per MWh for everyone, and spurs regional economic development (jobs, tax base, ancillary demand). Under $\mathcal{H}_0$, the residential bill impact is a rounding error and the capacity build is a public good.

**Falsification of $\mathcal{H}_0$ (three independent vectors):**

1. **Marginal, not average, cost explodes:** The PJM BRA cleared $9.333333\times$ higher ($\$28.92 \to \$269.92\text{/MW-day}$) in exactly the delivery years dominated by datacenter load growth. If new load were spreading existing fixed costs, marginal capacity prices would fall or hold; instead the system had to procure net new capacity at an order-of-magnitude premium, and that premium flows through the same socialized allocation.
2. **The $\$312.00\text{/yr}$ household transmission shift:** Cost causation is severed — the class that induces the $\$5.0\text{B}$ capex pays a confidential discounted contract rate while $72.0\%$ of the fixed-cost recovery lands on meters that induced nothing. This is the structural signature of an undue preference under FPA § 205.
3. **Duration asymmetry:** The inducing customer's commitment horizon (5–7 year GPU leases, single-site cluster economics) is one-sixth of the recovery horizon (40 years). $\mathcal{H}_0$'s development benefit is reversible at Year 7; the ratepayer's obligation is not.

**$\mathcal{H}_1$ (Protected Analytical Synthesis):** Under the A-J compact with $s > r$ and confidential contract discounts, IOU-hyperscaler interconnection agreements structurally convert private compute-cycle risk into a residentially collateralized annuity in violation of the cost-causation core of the just-and-reasonable mandate. The claim is stated as disclosed-facts synthesis: the primary records (PUC rate orders, FERC ER24-2952, PJM auction results, the $\Pi_{IOU} = \Delta_{AJ} \cdot K$ identity) are pin-cited, and the inference is the algebra.

**Remedy 1 — FPA § 205 Cost-Causation Ring-Fencing:** Assign $100\%$ of datacenter-induced network upgrade costs (plus the $9.333333\times$ capacity procurement) to the inducing customer class via conditional interconnection agreements with minimum-commitment tenors matched to the recovery horizon ($\tau_{contract} \ge T$), eliminating the $\alpha = 0.72$ socialization channel.

**Remedy 2 — Behind-the-Meter Defection:** Residential solar-plus-LFP islanded microgrids exit the socialized cost pool. With defection share $\delta = 0.10$, the surcharge on each remaining household steps up:

$$\sigma_{hh}^{\prime} = \frac{S_{res}}{N(1-\delta)} = \frac{\$468.0\text{M}}{1.35\text{M}} = \$346.67 \quad (+11.11\%)$$

The step-up accelerates further defection — the utility death spiral inverting the Averch-Johnson flywheel: as $K_{RateBase}$ erodes, $\Pi_{IOU} = \Delta_{AJ} \cdot K_{RateBase}$ erodes with it, and the gold-plating machine loses its fuel.

---

## 5. Locked Telemetry Table (14 Constants)

| # | Schema Key | Symbol | Value | Derivation |
|---|---|---|---|---|
| 1 | `puc_authorized_roe_rate` | $s = r_{ROE}$ | $0.105$ | PUC-authorized ROE |
| 2 | `utility_cost_of_debt_capital_rate` | $r = r_{cost}$ | $0.055$ | True blended capital cost |
| 3 | `averch_johnson_roe_spread` | $\Delta_{AJ}$ | $0.050$ | $0.105 - 0.055$ |
| 4 | `hyperscaler_induced_transmission_capex_usd_billions` | $K$ | $5.0$ | 765 kV + substation capex |
| 5 | `annual_guaranteed_roe_profit_extract_usd_millions` | $K \cdot s$ | $525.0$ | $5{,}000 \times 0.105$ |
| 6 | `annual_straight_line_depreciation_charge_usd_millions` | $K/T$ | $125.0$ | $5{,}000 / 40$ |
| 7 | `total_annual_revenue_requirement_usd_millions` | $R_{req}$ | $650.0$ | $525.0 + 125.0$ |
| 8 | `residential_ratepayer_cost_allocation_share` | $\alpha$ | $0.72$ | Fixed-cost socialization share |
| 9 | `residential_annual_cross_subsidy_transfer_usd_millions` | $S_{res}$ | $468.0$ | $650.0 \times 0.72$ |
| 10 | `captive_residential_households_millions` | $N$ | $1.5$ | Captive meter count |
| 11 | `annual_surcharge_per_captive_household_usd` | $\sigma_{hh}$ | $312.0$ | $468.0 / 1.5$ |
| 12 | `pjm_prior_capacity_clearing_price_mw_day_usd` | $P_0$ | $28.92$ | Prior BRA clearing price |
| 13 | `pjm_hyperscaler_spike_capacity_price_mw_day_usd` | $P_{BRA}$ | $269.92$ | 2025/2026 BRA clearing price |
| 14 | `pjm_capacity_price_surge_multiplier` | $\mu_{PJM}$ | $9.333333$ | $269.92 / 28.92$ (6 dp) |

---

## 6. Verification & Falsification Conditions

`SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0` is falsified if and only if empirical records demonstrate:

1. **Cost-Causation Compliance:** The inducing hyperscaler class is billed $\ge (1 - \epsilon)$ of the datacenter-induced revenue requirement ($\alpha_{datacenter} \ge 0.95$) under public, non-confidential rate schedules, eliminating the residential transfer $S_{res} \to 0$.
2. **Marginal Capacity Price Mean-Reversion:** PJM Base Residual Auction clearing prices return below $\$50.00\text{/MW-day}$ ($\mu_{PJM} < 1.73\times$) across two consecutive auctions while datacenter interconnection queues continue to grow, refuting the marginal-cost explosion vector.
3. **Duration Parity:** Hyperscaler interconnection commitments carry enforceable minimum tenors $\tau_{contract} \ge 20\text{ years}$ with take-or-pay recovery of residual rate base, eliminating the Year-7 stranding regime ($K_{resid} \to 0$ exposure).

### 6.1 Verification Artifacts

- **Machine-Readable Schema:** `schema/utility_rate_base_hyperscaler_subsidy.json` encodes the Averch-Johnson spread, revenue requirement waterfall, residential cross-subsidy transfer, PJM surge multiplier, stranded-duration deadweight, and defection death-spiral step-up as closed-form constants.
- **Deterministic Proof Engine:** `proofs/utility_rate_base_hyperscaler_subsidy_proof.py` (pure standard library) recomputes every primitive and asserts the governing identities: $\Delta_{AJ} = 0.050$, $R_{req} = \$650.0\text{M/yr}$, $S_{res} = \$468.0\text{M/yr}$, $\sigma_{hh} = \$312.00$, $\mu_{PJM} = 9.333333\times$, $K_{resid} = \$4.125\text{B}$, $R_{dead} = \$558.125\text{M/yr}$, and $\sigma_{hh}^{\prime} = \$346.67$ at $\delta = 0.10$.