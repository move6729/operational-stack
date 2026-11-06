#!/usr/bin/env python3
"""Closed-form proof bundle for the distributed antitrust, ERISA fiduciary,
and cloud-subpoena liquidation specification.

Canonical Specification:
    SPEC-DISTRIBUTED-ANTITRUST-COMMON-OWNERSHIP-AND-FIDUCIARY-LIQUIDATION-v1.0

Governing equations verified below (pure stdlib, deterministic):

    S1  HHI_Base      = 10000 / N
        Delta_HHI_CO  = lambda_CO * 10000 * (N - 1) / N
        MHHI          = HHI_Base + Delta_HHI_CO
        Multiple      = Delta_HHI_CO / DOJ_Delta_HHI_Threshold
    S2  L_plan        = A * Delta_r * T
        D_fee         = A * phi * T
        L_single      = L_plan + D_fee
        L_systemic    = L_single * N_plans
    S3  O_house       = U * R * delta_rent
        L_house       = 3 * T_SOL * O_house          (Clayton Act Sec. 4)
    S4  O_wage        = N_w * W * delta_wage
        L_wage        = 3 * T_SOL * O_wage           (RICO Sec. 1964(c))
    S5  Omega = 0  ==>  P_adverse(FRCP 37(e)(2)) = 1
    S6  P_survival    = p_capture ** K
        P_cascade     = 1 - P_survival
    S7  L_combined    = L_systemic + L_house + L_wage

Exit status 0 if and only if every locked constant is reproduced exactly.
"""

import sys

LOCKED = {
    "N_Competitors_Coal": 5,
    "HHI_Base_Pts": 2000.0,
    "beta_Big3_Combined_Share": 0.2200,
    "lambda_CO_Internalization": 0.3500,
    "Delta_HHI_CO_Pts": 2800.0,
    "MHHI_Total_Pts": 4800.0,
    "DOJ_HHI_Threshold_Pts": 1800.0,
    "DOJ_Delta_HHI_Threshold_Pts": 100.0,
    "Multiple_Above_DOJ_Delta_Limit": 28.0,
    "A_Plan_BlackRock_USD": 10000000000.0,
    "D_Corp_BlackRock_Debt_USD": 400000000.0,
    "Rank_Equity_BlackRock": 4,
    "Delta_r_ESG_Drag": 0.0125,
    "phi_Management_Fee": 0.0015,
    "T_ERISA_Window_Yrs": 4,
    "L_ERISA_Plan_Loss_USD": 500000000.0,
    "D_ERISA_Fee_Disgorgement_Exact_USD": 60000000.0,
    "L_ERISA_Total_Single_Plan_USD": 560000000.0,
    "N_S_and_P_Plans_Exposed": 100,
    "L_ERISA_Systemic_100Plans_USD": 56000000000.0,
    "U_Cartel_Housing_Units": 1300000,
    "N_States_Housing_Cartel": 44,
    "R_Unit_Annual_Base_USD": 20000.0,
    "delta_Rent_Markup": 0.0500,
    "T_Antitrust_SOL_Yrs": 4,
    "O_Housing_Annual_Overcharge_USD": 1300000000.0,
    "O_Housing_4yr_Overcharge_USD": 5200000000.0,
    "L_Housing_Treble_Damages_USD": 15600000000.0,
    "N_Workers_Wage_Class": 250000,
    "W_Annual_Base_Wage_USD": 50000.0,
    "delta_Wage_Suppression_Arbitrage": 0.0800,
    "O_Wage_Annual_Suppression_USD": 1000000000.0,
    "O_Wage_4yr_Suppression_USD": 4000000000.0,
    "L_RICO_Clayton_Wage_Treble_USD": 12000000000.0,
    "Omega_Cloud_Metadata": 0.0000,
    "P_Adverse_Inference_Rule37e2": 1.0000,
    "p_Capture_Single_Regulator": 0.8500,
    "K_Distributed_Enforcer_Nodes": 20,
    "P_Cartel_Survival_Distributed": 0.038760,
    "P_Collateral_Estoppel_Cascade": 0.961240,
    "L_Combined_Cartel_Liquidation_USD": 83600000000.0,
}

RESULTS = []


def close(a, b, rel=1e-9):
    """Relative-equality test with a unit floor for zero-safe scaling."""
    return abs(a - b) <= rel * max(abs(a), abs(b), 1.0)


def check(label, cond):
    RESULTS.append((label, bool(cond)))


def main():
    k = LOCKED

    # ------------------------------------------------------------------
    # S1. Common-ownership MHHI internalization gate
    # ------------------------------------------------------------------
    n = k["N_Competitors_Coal"]
    check("S1.1 equal-share baseline: HHI_Base == 10000/N",
          close(k["HHI_Base_Pts"], 10000.0 / n))
    delta_co = k["lambda_CO_Internalization"] * 10000.0 * (n - 1) / n
    check("S1.2 Delta_HHI_CO == lambda_CO * 10000 * (N-1)/N",
          close(delta_co, k["Delta_HHI_CO_Pts"]))
    mhi = k["HHI_Base_Pts"] + delta_co
    check("S1.3 MHHI_Total == HHI_Base + Delta_HHI_CO",
          close(mhi, k["MHHI_Total_Pts"]))
    multiple = k["Delta_HHI_CO_Pts"] / k["DOJ_Delta_HHI_Threshold_Pts"]
    check("S1.4 Multiple == Delta_HHI_CO / DOJ_Delta_HHI_Threshold",
          close(multiple, k["Multiple_Above_DOJ_Delta_Limit"]))
    check("S1.5 DOJ structural presumption triggered (MHHI>1800, Delta>100)",
          k["MHHI_Total_Pts"] > k["DOJ_HHI_Threshold_Pts"]
          and k["Delta_HHI_CO_Pts"] > k["DOJ_Delta_HHI_Threshold_Pts"])
    check("S1.6 internalization coupling bounded (lambda_CO*beta < 1)",
          k["lambda_CO_Internalization"] * k["beta_Big3_Combined_Share"] < 1.0)

    # ------------------------------------------------------------------
    # S2. ERISA fiduciary loss and exact fee disgorgement
    # ------------------------------------------------------------------
    a_plan = k["A_Plan_BlackRock_USD"]
    t_erisa = k["T_ERISA_Window_Yrs"]
    plan_loss = a_plan * k["Delta_r_ESG_Drag"] * t_erisa
    check("S2.1 single-plan loss == A * Delta_r * T",
          close(plan_loss, k["L_ERISA_Plan_Loss_USD"]))
    fee_disgorged = a_plan * k["phi_Management_Fee"] * t_erisa
    check("S2.2 fee disgorgement == A * phi * T",
          close(fee_disgorged, k["D_ERISA_Fee_Disgorgement_Exact_USD"]))
    single_total = plan_loss + fee_disgorged
    check("S2.3 single-plan total == loss + disgorgement",
          close(single_total, k["L_ERISA_Total_Single_Plan_USD"]))
    systemic = single_total * k["N_S_and_P_Plans_Exposed"]
    check("S2.4 systemic exposure == single-plan total * N_plans",
          close(systemic, k["L_ERISA_Systemic_100Plans_USD"]))
    check("S2.5 creditor/equity conflict predicate (rank<=5, debt>0)",
          k["Rank_Equity_BlackRock"] <= 5
          and k["D_Corp_BlackRock_Debt_USD"] > 0.0)
    check("S2.6 conflict exposure ratio strictly positive",
          k["D_Corp_BlackRock_Debt_USD"] / a_plan > 0.0)

    # ------------------------------------------------------------------
    # S3. Housing-cartel overcharge and Clayton Act treble damages
    # ------------------------------------------------------------------
    o_house_ann = (k["U_Cartel_Housing_Units"]
                   * k["R_Unit_Annual_Base_USD"]
                   * k["delta_Rent_Markup"])
    check("S3.1 annual housing overcharge == U * R * delta_rent",
          close(o_house_ann, k["O_Housing_Annual_Overcharge_USD"]))
    o_house_4yr = o_house_ann * k["T_Antitrust_SOL_Yrs"]
    check("S3.2 4-year housing overcharge == annual * T_SOL",
          close(o_house_4yr, k["O_Housing_4yr_Overcharge_USD"]))
    house_treble = 3.0 * o_house_4yr
    check("S3.3 Clayton Sec. 4 treble == 3 * 4-year overcharge",
          close(house_treble, k["L_Housing_Treble_Damages_USD"]))
    check("S3.4 cartel footprint well-formed (0 < states <= 50, units > 0)",
          0 < k["N_States_Housing_Cartel"] <= 50
          and k["U_Cartel_Housing_Units"] > 0)

    # ------------------------------------------------------------------
    # S4. Wage-suppression overcharge and RICO/Clayton treble damages
    # ------------------------------------------------------------------
    o_wage_ann = (k["N_Workers_Wage_Class"]
                  * k["W_Annual_Base_Wage_USD"]
                  * k["delta_Wage_Suppression_Arbitrage"])
    check("S4.1 annual wage suppression == N_w * W * delta_wage",
          close(o_wage_ann, k["O_Wage_Annual_Suppression_USD"]))
    o_wage_4yr = o_wage_ann * k["T_Antitrust_SOL_Yrs"]
    check("S4.2 4-year wage suppression == annual * T_SOL",
          close(o_wage_4yr, k["O_Wage_4yr_Suppression_USD"]))
    wage_treble = 3.0 * o_wage_4yr
    check("S4.3 RICO Sec. 1964(c) treble == 3 * 4-year suppression",
          close(wage_treble, k["L_RICO_Clayton_Wage_Treble_USD"]))

    # ------------------------------------------------------------------
    # S5. Cloud-subpoena spoliation and FRCP 37(e)(2) inference
    # ------------------------------------------------------------------
    check("S5.1 total cloud-metadata spoliation (Omega == 0)",
          k["Omega_Cloud_Metadata"] == 0.0)
    check("S5.2 Rule 37(e)(2) adverse inference certain (P == 1)",
          k["P_Adverse_Inference_Rule37e2"] == 1.0)
    check("S5.3 spoliation-inference coupling (Omega==0) == (P==1)",
          (k["Omega_Cloud_Metadata"] == 0.0)
          == (k["P_Adverse_Inference_Rule37e2"] == 1.0))

    # ------------------------------------------------------------------
    # S6. Distributed enforcement: joint capture and estoppel cascade
    # ------------------------------------------------------------------
    p_cap = k["p_Capture_Single_Regulator"]
    nodes = k["K_Distributed_Enforcer_Nodes"]
    p_surv = round(p_cap ** nodes, 6)
    check("S6.1 joint-capture survival == p_capture^K (6 d.p.)",
          p_surv == k["P_Cartel_Survival_Distributed"])
    p_cascade = round(1.0 - p_surv, 6)
    check("S6.2 estoppel cascade == 1 - survival (6 d.p.)",
          p_cascade == k["P_Collateral_Estoppel_Cascade"])
    check("S6.3 distributed enforcement dominates single regulator",
          p_surv < p_cap)
    check("S6.4 survival probability strictly interior",
          0.0 < k["P_Cartel_Survival_Distributed"] < 1.0)

    # ------------------------------------------------------------------
    # S7. Combined cartel-liquidation identity
    # ------------------------------------------------------------------
    combined = (k["L_ERISA_Systemic_100Plans_USD"]
                + k["L_Housing_Treble_Damages_USD"]
                + k["L_RICO_Clayton_Wage_Treble_USD"])
    check("S7.1 L_combined == ERISA_sys + housing + wage treble",
          close(combined, k["L_Combined_Cartel_Liquidation_USD"]))
    check("S7.2 all liability components strictly positive",
          min(k["L_ERISA_Systemic_100Plans_USD"],
              k["L_Housing_Treble_Damages_USD"],
              k["L_RICO_Clayton_Wage_Treble_USD"]) > 0.0)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    for label, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", label))
    print("MHHI_Total_Pts=%.1f  Delta_HHI_CO_Pts=%.1f  Multiple=%.1f"
          % (mhi, delta_co, multiple))
    print("L_ERISA_Systemic_USD=%.1f  L_Housing_Treble_USD=%.1f  "
          "L_Wage_Treble_USD=%.1f" % (systemic, house_treble, wage_treble))
    print("P_Survival=%.6f  P_Cascade=%.6f  L_Combined_USD=%.1f"
          % (p_surv, p_cascade, combined))
    failed = [label for label, ok in RESULTS if not ok]
    if failed:
        print("RESULT: FAIL (%d/%d checks)" % (len(failed), len(RESULTS)))
        return 1
    print("RESULT: PASS (%d/%d checks)" % (len(RESULTS), len(RESULTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
