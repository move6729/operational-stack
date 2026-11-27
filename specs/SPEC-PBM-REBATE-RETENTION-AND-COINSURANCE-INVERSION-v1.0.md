# SPEC-PBM-REBATE-RETENTION-AND-COINSURANCE-INVERSION-v1.0 — PBM Rebate-Retention Laundering & the Coinsurance List-Price Inversion

**Canonical Specification:** `SPEC-PBM-REBATE-RETENTION-AND-COINSURANCE-INVERSION-v1.0`
**Target Architectures:** Transparent Cost-Plus Nadac/Direct Pharmacy Clearing vs. Vertically Integrated PBM Rebate-Aggregator & Spread-Pricing Oligopolies (`OPSTACK-KERNEL-v2.2`)
**Cross-References:** `specs/SPEC-PBM-REBATE-RETENTION-AND-COINSURANCE-INVERSION-v1.0.md` | `schema/pbm_rebate_coinsurance_inversion.json` | `proofs/pbm_rebate_coinsurance_inversion_proof.py` | `specs/AUDIT-2026-HEALTHCARE-BILLING-DISINTERMEDIATION.md` | `specs/SPEC-PE-HOSPITAL-SALE-LEASEBACK-STRIPPING-AND-CPOM-EXTRACTION-v1.0.md` | `specs/SPEC-DISTRIBUTED-ANTITRUST-COMMON-OWNERSHIP-AND-FIDUCIARY-LIQUIDATION-v1.0.md` | `articles/pbm-rebate-retention-and-coinsurance-inversion.txt`
**RAG Indexing Vector:** `[PBM-REBATE-LAUNDERING, WAC-LIST-PRICE-INVERSION, PATIENT-COINSURANCE-EXTRACTION, GPO-OFFSHORE-REBATE-AGGREGATOR, SPREAD-PRICING-NADAC-WEDGE, ERISA-404-FIDUCIARY-BREACH, FTC-CARE-MARK-EXPRESS-SCRIPTS-OPTUM, COST-PLUS-GENERIC-BYPASS]`
**Empirical, Statutory & Physical Baseline:** *In the Matter of Caremark Rx, LLC; Zinc Health Services, LLC; Express Scripts, Inc.; Ascent Health Services LLC; OptumRx, Inc.; and Emisar Pharma Services LLC* (FTC Docket No. 9437, 2024 Administrative Complaint), FTC Interim Staff Reports on Prescription Drug Middlemen (July 2024 & January 2025), 29 U.S.C. §§ 1104 & 1106 (ERISA § 404 Fiduciary Duty of Loyalty & § 406 Prohibited Self-Dealing Transactions), *Lewandowski v. Johnson & Johnson* (D.N.J. Case No. 3:24-cv-00671, ERISA Prescription Drug Fiduciary Class Action), 42 U.S.C. § 1320a-7b(b) (Federal Anti-Kickback Statute & Safe-Harbor Boundary)
**By:** Operational Stack Cybernetics Group
**License:** Unlicense (Public Domain — Zero-Rent Federation)

---

## 1. Thesis Statement

This specification formalizes the **rebate-retention inversion**: the vertically integrated pharmacy benefit manager (PBM) archetype in which the formulary intermediary's revenue rises monotonically with the list price of the drugs it certifies as preferred, in which the sick patient's coinsurance is levied on a fictional unrebated price no plan actually pays, and in which the insurer's net outlay collapses to zero — inverting insurance into a reverse subsidy from the sickest members to the PBM/insurer parent. The governing record base is *In the Matter of Caremark Rx, LLC; Zinc Health Services, LLC; Express Scripts, Inc.; Ascent Health Services LLC; OptumRx, Inc.; and Emisar Pharma Services LLC* (FTC Docket No. 9437, 2024 Administrative Complaint) and the FTC Interim Staff Reports on prescription drug middlemen (July 2024 & January 2025).

The archetype decomposes into four coupled stages, each locked by telemetry constants (Section 5):

1. **List-Price Inflation.** True manufacturing cost plus a reasonable margin is $25.00 (`true_manufacturing_plus_margin_cost_usd = 25.0`), while the formulary-preferred Wholesale Acquisition Cost (WAC) list price is inflated 40.0x (`wac_to_production_cost_ratio = 40.0`) to $1,000.00 (`inflated_wac_list_price_usd = 1000.0`).
2. **Reverse-Auction Rebate Laundering.** The manufacturer funds a secret 75.0% rebate (`manufacturer_kickback_rebate_rate = 0.75`) producing a $750.00 rebate pool (`total_rebate_pool_usd = 750.0`); the PBM's captive Rebate Aggregator GPO retains a 20.0% administrative cut (`offshore_gpo_pbm_retained_rebate_share = 0.20`), locking PBM extraction at $150.00 per claim (`pbm_retained_rebate_extraction_usd = 150.0`). A higher list price mathematically maximizes PBM revenue.
3. **Coinsurance Transfer.** The sick patient pays 25.0% coinsurance (`patient_coinsurance_rate_on_wac = 0.25`) on the fictional unrebated $1,000.00 WAC — $250.00 out-of-pocket (`patient_out_of_pocket_coinsurance_usd = 250.0`) — against a true post-rebate net cost of $250.00 (`net_post_rebate_drug_cost_usd = 250.0`). The patient therefore funds 100.0% of the drug's actual net cost (`patient_share_of_true_net_cost_ratio = 1.0`), leaving the insurer/plan a $0.00 net outlay (`insurer_plan_net_outlay_after_rebate_and_patient_copay_usd = 0.0`).
4. **Specialty-Generic Spread Pricing.** On specialty generics the NADAC acquisition cost is $90.00 (`specialty_generic_nadac_acquisition_cost_usd = 90.0`), yet the PBM bills the self-funded ERISA employer plan $4,500.00 (`pbm_spread_pricing_plan_billed_usd = 4500.0`) when dispensed via its vertically owned mail-order pharmacy — a 50.0x markup (`pbm_specialty_generic_markup_multiplier = 50.0`).

The terminal legal state is ERISA § 404/§ 406 fiduciary disgorgement (29 U.S.C. §§ 1104, 1106) plus direct cost-plus NADAC disintermediation of the rebate-aggregator layer.

## 2. Archetype Mechanics: The Big 3 Reverse Auction

Three vertically integrated PBM/insurer parents — CVS Caremark with Zinc Health Services, Express Scripts with Ascent Health Services, and OptumRx with Emisar Pharma Services — collectively manage roughly 80% of U.S. prescriptions per the FTC's record. Each routes manufacturer rebates through a captive Rebate Aggregator GPO (Zinc, Ascent, Emisar — domiciled across Switzerland, Ireland, and Delaware), and each owns the mail-order pharmacies through which high-margin claims are steered. FTC Docket No. 9437 pleads the core mechanism: formulary position is auctioned to the manufacturer offering the deepest rebate off the highest list price.

```mermaid
flowchart TD
    A[Manufacturer true cost C_true = 25.0 USD] --> B[Inflated WAC list price P_WAC = 1000.0 USD at 40.0x]
    B --> C[Reverse auction: formulary placement sold to the deepest rebate bid]
    C --> D[Secret rebate r = 0.75 generates pool R = 750.0 USD]
    D --> E[Captive GPO cutout: Zinc, Ascent, Emisar]
    E --> F[PBM retained share s = 0.20 yields Pi_PBM = 150.0 USD]
    E --> G[Plan settles behind the curtain at P_net = 250.0 USD]
    B --> H[Counter coinsurance c = 0.25 levied on the fictional WAC]
    H --> I[Patient OOP = 250.0 USD = 100% of P_net]
    G --> J[Plan net outlay Phi = 250.0 - 250.0 = 0.0 USD]
    I --> J
    J --> K[ERISA 404 and 406 disgorgement plus cost-plus NADAC bypass]
```

Three structural facts distinguish the reverse auction from bona fide group purchasing:

- **Formulary placement is sold, not earned.** The auction ranks drugs by rebate depth off list, not by net cost or therapeutic value. Because the PBM keeps a share of the rebate, the ranking criterion and the PBM's revenue are the same variable (E-3).
- **The rebate is computed on a price nobody pays.** The plan settles at P_net; the patient's coinsurance is nonetheless defined against the unrebated WAC. The fictional price survives settlement precisely because it is the extraction base at the counter (E-5).
- **The cutout launders the retention.** The GPO's "administrative fee" converts a placement-conditional payment into contract language, and the offshore domiciles place the retained share beyond the plan sponsor's audit radius — the same cutout geometry the FTC complaint traces across Zinc, Ascent, and Emisar.

## 3. Governing Equations (Closed-Form)

All symbols map 1:1 to the Section 5 telemetry table, to `schema/pbm_rebate_coinsurance_inversion.json`, and to the proof kernel `proofs/pbm_rebate_coinsurance_inversion_proof.py`.

**E-1 — WAC Inflation Multiplier.**

    kappa = P_WAC / C_true = 1000.0 / 25.0 = 40.0x

**E-2 — Rebate Pool.**

    R = r * P_WAC = 0.75 * 1000.0 = 750.0 (USD)

**E-3 — PBM Retained Extraction & List-Price Monotonicity.**

    Pi_PBM = s * r * P_WAC = 0.20 * 0.75 * 1000.0 = 150.0 (USD)
    dPi_PBM / dP_WAC = s * r = 0.15 > 0

**E-4 — Net Post-Rebate Price.**

    P_net = P_WAC - R = P_WAC * (1 - r) = 1000.0 - 750.0 = 250.0 (USD)

**E-5 — Counter Coinsurance on the Fictional List Price.**

    OOP = c * P_WAC = 0.25 * 1000.0 = 250.0 (USD)

**E-6 — Patient Share of True Net Cost.**

    sigma = OOP / P_net = c / (1 - r) = 0.25 / 0.25 = 1.0

**E-7 — Plan Net Outlay (Reverse-Subsidy Identity).**

    Phi_plan = P_net - OOP = 250.0 - 250.0 = 0.0 (USD)
    Inversion boundary: c >= 1 - r  <=>  sigma >= 1.0

**E-8 — Specialty-Generic Spread Multiplier.**

    M_spread = P_billed / C_NADAC = 4500.0 / 90.0 = 50.0x
    S = P_billed - C_NADAC = 4500.0 - 90.0 = 4410.0 (USD)

**E-9 — Formulary Exclusion Incentive.**

    Pi_low = s * r * C_true = 0.15 * 25.0 = 3.75 (USD)
    Pi_PBM / Pi_low = kappa = 40.0

**E-10 — ERISA Disgorgement Quantum (per claim).**

    D_brand = Pi_PBM = 150.0 (USD)
    D_generic = S = 4410.0 (USD)

Equation E-3 is the load-bearing incentive identity: because dPi_PBM/dP_WAC = s * r = 0.15 > 0, every dollar of list-price inflation adds $0.15 to PBM revenue, and E-9 states the consequence — a therapeutically equivalent drug priced at true cost yields the PBM $3.75 against $150.00 for the inflated-list equivalent, a 40.0x revenue differential that makes exclusion of the low-list-price drug the revenue-maximizing formulary decision. Equation E-7 is the load-bearing distributional identity: at c = 1 - r the sick patient funds the entire true net cost and the plan's insurance function is arithmetically extinguished.

**Boundary regimes (E-3/E-7 regime table).**

| Regime | Condition | Pi_PBM | sigma | Terminal state |
|--------|-----------|--------|-------|----------------|
| Compliant (cost-plus NADAC clearing) | price = C_true = 25.0; s = 0 | 0.0 | 0.25 of true cost | Formulary tracks therapeutic value; OOP = 6.25 |
| Pass-through boundary | s = 0; coinsurance still defined on WAC | 0.0 | 1.0 | Rebate passed to plan; counter inversion persists |
| Defection (rebate-retention) | s = 0.20 on r = 0.75 off P_WAC = 40.0x C_true | 150.0 | 1.0 | Reverse subsidy; Phi_plan = 0.0 (E-7) |
| Spread overlay | M_spread = 50.0x via owned mail-order | S = 4410.0 | n/a | ERISA § 406(b) prohibited self-dealing (E-8) |

The defection regime is entered the moment the GPO retention clause and the WAC-based coinsurance definition are signed together; no subsequent "net-price savings" reporting crosses the sigma = 1.0 boundary without rebasing coinsurance onto P_net.

## 4. Specialty-Generic Spread Pricing & Independent Pharmacy Liquidation

The FTC's January 2025 Interim Staff Report documents the second extraction channel: on specialty generics (e.g., generic imatinib, abiraterone, teriflunomide), the Big 3's owned mail-order pharmacies billed plan sponsors large multiples of pharmacy acquisition cost. The locked archetype: NADAC acquisition cost of $90.00 against a $4,500.00 bill to the self-funded ERISA plan — a 50.0x multiplier and a $4,410.00 spread retained inside the same corporate parent that owes the plan fiduciary loyalty.

```mermaid
flowchart TD
    A[Specialty generic dispensed: NADAC acquisition cost = 90.0 USD] --> B[PBM-owned mail-order pharmacy fills the claim]
    B --> C[ERISA plan billed P_billed = 4500.0 USD]
    C --> D[Spread S = 4410.0 USD retained inside the PBM parent]
    D --> E[Markup multiplier M = 4500.0 / 90.0 = 50.0x]
    A --> F[Independent pharmacy reimbursed at or below NADAC]
    F --> G[Cannot dispense at a loss: volume migrates to owned mail-order]
    G --> H[ERISA 406b prohibited self-dealing surface]
```

The liquidation mechanism is mechanical, not conspiratorial: the PBM reimburses independent pharmacies at or below NADAC while billing the plan at 50.0x NADAC through its own channel. The independent cannot dispense at a loss, so specialty volume migrates to the owned mail-order pharmacy, where the spread is captured in-parent. The plan pays the spread, the patient loses the counter relationship, and the independent pharmacy's specialty line — its margin core — is liquidated claim by claim.

## 5. Locked Telemetry Table (15 Constants)

| # | Symbol | Constant | Value | Units | Derivation / Source |
|---|--------|----------|-------|-------|---------------------|
| 1 | `C_true` | `true_manufacturing_plus_margin_cost_usd` | 25.0 | USD | True manufacturing cost + reasonable margin (archetype baseline) |
| 2 | `P_WAC` | `inflated_wac_list_price_usd` | 1000.0 | USD | Formulary-preferred WAC list price |
| 3 | `kappa` | `wac_to_production_cost_ratio` | 40.0 | x | E-1: 1000.0 / 25.0 |
| 4 | `r` | `manufacturer_kickback_rebate_rate` | 0.75 | rate | Secret reverse-auction rebate rate off WAC |
| 5 | `R` | `total_rebate_pool_usd` | 750.0 | USD | E-2: 0.75 * 1000.0 |
| 6 | `s` | `offshore_gpo_pbm_retained_rebate_share` | 0.20 | rate | Captive GPO/PBM retained administrative cut |
| 7 | `Pi_PBM` | `pbm_retained_rebate_extraction_usd` | 150.0 | USD | E-3: 0.20 * 0.75 * 1000.0 |
| 8 | `c` | `patient_coinsurance_rate_on_wac` | 0.25 | rate | Coinsurance rate levied on unrebated WAC |
| 9 | `OOP` | `patient_out_of_pocket_coinsurance_usd` | 250.0 | USD | E-5: 0.25 * 1000.0 |
| 10 | `P_net` | `net_post_rebate_drug_cost_usd` | 250.0 | USD | E-4: 1000.0 - 750.0 |
| 11 | `sigma` | `patient_share_of_true_net_cost_ratio` | 1.0 | ratio | E-6: 250.0 / 250.0 |
| 12 | `Phi_plan` | `insurer_plan_net_outlay_after_rebate_and_patient_copay_usd` | 0.0 | USD | E-7: 250.0 - 250.0 |
| 13 | `C_NADAC` | `specialty_generic_nadac_acquisition_cost_usd` | 90.0 | USD | NADAC acquisition cost, specialty generic |
| 14 | `P_billed` | `pbm_spread_pricing_plan_billed_usd` | 4500.0 | USD | PBM mail-order bill to the self-funded ERISA plan |
| 15 | `M_spread` | `pbm_specialty_generic_markup_multiplier` | 50.0 | x | E-8: 4500.0 / 90.0 |

Machine-readable lock: `schema/pbm_rebate_coinsurance_inversion.json`. Executable verification: `proofs/pbm_rebate_coinsurance_inversion_proof.py` (exit code 0).

## 6. Milkovich H0/H1 Synthesis & ERISA §§ 404/406 Liquidation

Under *Milkovich v. Lorain Journal Co.* (497 U.S. 1) and *Partington v. Bugliosi* (56 F.3d 1147), analytical synthesis is protected where every inferential claim is anchored to disclosed, pin-cited primary facts. This section states the PBM null hypothesis and falsifies it against the locked telemetry.

**H0 (Null Hypothesis — Big 3 PBM spokesperson position).** Rebate negotiation lowers net plan premiums and employer drug spend; GPOs aggregate purchasing power and volume discounts on behalf of employers; manufacturers — not PBMs — unilaterally set list prices; coinsurance design is the employer plan sponsor's own election; and mail-order differentials reflect legitimate dispensing economics and network management.

**Falsification tests (H1 analytical synthesis).**

- **T1 — List-Price Monotonicity (E-3, E-9).** dPi_PBM/dP_WAC = s * r = 0.15 > 0: PBM revenue rises with every dollar of list-price inflation. Per the FTC Docket No. 9437 complaint, formulary position was auctioned to the deepest rebate off the highest list, and a therapeutically equivalent low-list drug priced at true cost yields the PBM $3.75 against $150.00 — a 40.0x revenue differential. An intermediary whose revenue is monotonic in the price it certifies as "preferred" cannot treat that price as exogenous.
- **T2 — Coinsurance Transfer Identity (E-6, E-7).** sigma = 1.0 and Phi_plan = 0.0 hold as arithmetic: the sick patient pays 100.0% of the true post-rebate cost and the plan's net outlay is $0.00. Were H0's "rebates lower member costs" predicate true, sigma < 1.0 would be observed; the identity shows the rebate is applied only to the behind-the-curtain settlement, never to the counter price.
- **T3 — Spread Trace (E-8).** As documented in the FTC's January 2025 Interim Staff Report, plan sponsors were billed large multiples of acquisition cost on specialty generics dispensed through PBM-owned mail-order pharmacies; the locked archetype bills $4,500.00 against $90.00 NADAC — 50.0x, with the $4,410.00 spread retained inside the fiduciary's own corporate parent.

**H1 (Protected analytical synthesis).** The disclosed facts — the administrative complaint's reverse-auction record, the interim reports' spread traces, and the closed-form identities above — support the inference that list-price inflation is the revenue engine of the rebate-aggregator business model, that coinsurance on unrebated WAC converts insurance into a reverse subsidy from sick patients to the PBM/insurer parent, and that owned-mail-order spread pricing is self-dealing rather than service compensation.

**ERISA mapping (29 U.S.C. §§ 1104, 1106).**

- **§ 404(a)(1) duty of loyalty and prudence.** Where the PBM exercises discretionary authority over formulary design and rebate disposition, it acts as a functional fiduciary; retaining s = 0.20 of the rebate pool while certifying high-list drugs as preferred subordinates plan interests to PBM revenue (E-3 monotonicity is the loyalty test made algebraic).
- **§ 406(a)(1)(C) & § 406(b)(1) prohibited transactions.** Furnishing of services between the plan and a party in interest, and fiduciary self-dealing with plan assets: the 50.0x spread routed through the PBM's own mail-order pharmacy (E-8) is the paradigm § 406(b) transfer.
- **§ 409(a) / § 502(a)(2)–(a)(3) remedies.** Personal liability, disgorgement of profits, and equitable relief. Per-claim quantum from E-10: D_brand = $150.00 (rebate retention) and D_generic = $4,410.00 (spread). Live class vector: *Lewandowski v. Johnson & Johnson* (D.N.J. Case No. 3:24-cv-00671), pleading prescription-drug fiduciary breach against a manufacturer/PBM rebate architecture.
- **Anti-Kickback boundary (42 U.S.C. § 1320a-7b(b)).** Remuneration in exchange for formulary placement or preferential status is the statutory target; the discount safe harbor protects only discounts fully passed through to the plan. A retained s = 0.20 share, combined with coinsurance levied on the unrebated WAC, sits outside the harbor for federal-program claims, and the one-purpose principle applies to placement-conditional payments. This specification attributes no charged offense to any party; it fixes the structural boundary the safe-harbor algebra draws.

## 7. Remedial Terminal State

1. **Disgorgement** under ERISA § 409(a): Pi_PBM = $150.00 per brand claim and S = $4,410.00 per specialty-generic claim (E-10), with the GPO retention ledger as the discovery artifact.
2. **Point-of-sale rebate pass-through and coinsurance rebasing:** every rebate applied at settlement must rebase the coinsurance base from P_WAC to P_net, collapsing OOP from $250.00 to $62.50 at c = 0.25 and restoring sigma = 0.25.
3. **Spread elimination:** plan reimbursement at NADAC plus a disclosed flat dispensing fee, deleting the 50.0x multiplier and the owned-mail-order steering incentive in one contract term.
4. **Cost-plus NADAC direct pharmacy clearing (target architecture):** price = verified acquisition cost + disclosed margin; formulary ranked by true net cost; independent pharmacies compete on service rather than subsidizing the aggregator. At C_true = $25.00 the entire extraction stack — R, Pi_PBM, and the fictional coinsurance base — is deleted at the source.
5. **Structural separation** in the FTC Docket No. 9437 posture: formulary authority severed from owned-mail-order economics, so the ranking variable and the revenue variable are no longer the same variable.

## 8. Cross-Reference Closure

- Companion narrative: `articles/pbm-rebate-retention-and-coinsurance-inversion.txt`
- Machine lock: `schema/pbm_rebate_coinsurance_inversion.json`
- Executable proof: `proofs/pbm_rebate_coinsurance_inversion_proof.py`
- Healthcare disintermediation parent: `specs/AUDIT-2026-HEALTHCARE-BILLING-DISINTERMEDIATION.md`
- Fiduciary-strip siblings: `specs/SPEC-PE-HOSPITAL-SALE-LEASEBACK-STRIPPING-AND-CPOM-EXTRACTION-v1.0.md`, `specs/SPEC-DISTRIBUTED-ANTITRUST-COMMON-OWNERSHIP-AND-FIDUCIARY-LIQUIDATION-v1.0.md`

*End of specification. All 15 telemetry constants are locked at v1.0 and verified by the proof kernel (exit code 0).*
