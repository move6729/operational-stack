#!/usr/bin/env python3
"""Deterministic verification gate for the Defensive SAR Safe Harbor &
314(b) Debanking Cascade bundle
(SPEC-DEFENSIVE-SAR-SAFE-HARBOR-314B-DEBANKING-CASCADE-v1.0).

Verifies all 5 governing vectors against the exact locked v1.0 constants:

  Vector 1  Bank loss-to-fee asymmetry & critical audit-probability
            threshold p* = F / (L + F): JPMorgan (L = $290M class +
            $75M USVI = $365M TVPA loss, F = $3M/yr, R = 121.666667,
            p* = 0.00815217) and Deutsche Bank (L = $150M NYDFS +
            $75M class = $225M, F = $2M/yr, R = 112.5,
            p* = 0.00881057), with the p*-indifference identity
            p* L = (1 - p*) F and the p = 0.01 defection regime.
  Vector 2  Faithless-servant clawback (Staley: $10M/yr x 8 yr
            disloyalty = $80M) and relationship-manager total downside
            with contribution ($365M + $80M = $445M).
  Vector 3  FinCEN bounty / CCO salary defection ratio
            ($15M-$45M bounty vs. $450k salary -> 33.333333x-100x).
  Vector 4  314(b) five-hop correspondent debanking cascade
            (p_accept = 0.04, m = 5 -> survival 1.024e-07, debanking
            certainty 0.9999998976 >= 0.999999) + $50k/day contempt
            fine dominance over both relationship fee bases.
  Vector 5  UHNW liquidity cascade: shortfall on debanking
            ($125M Lombard + $100M unfunded LP - $25M buffer = $200M)
            and forced-liquidation wealth destruction
            (0.4 x $200M + 0.5 x $160M = $160M = 32% of $500M NAV).

Pure Python 3 standard library (json, sys). Prints a JSON receipt and
exits 0 iff every check reconciles within the stated tolerances.
"""

import json
import sys

# ---------------------------------------------------------------------------
# Locked v1.0 constants and outputs (immutable reference values).
# ---------------------------------------------------------------------------
LOCKED = {
    # JPMorgan TVPA exposure and retention economics.
    "jpm_class_settlement_usd": 290000000.0,
    "jpm_usvi_settlement_usd": 75000000.0,
    "jpm_total_tvpa_loss_usd": 365000000.0,
    "jpm_annual_relationship_fee_usd": 3000000.0,
    "jpm_loss_to_fee_ratio": 121.666667,
    "jpm_critical_audit_prob_threshold": 0.00815217,
    # Deutsche Bank NYDFS / class exposure and retention economics.
    "db_nydfs_penalty_usd": 150000000.0,
    "db_class_settlement_usd": 75000000.0,
    "db_total_loss_usd": 225000000.0,
    "db_annual_relationship_fee_usd": 2000000.0,
    "db_loss_to_fee_ratio": 112.5,
    "db_critical_audit_prob_threshold": 0.00881057,
    # Faithless-servant clawback (Staley) and RM downside.
    "staley_annual_comp_usd": 10000000.0,
    "staley_disloyalty_years": 8,
    "staley_faithless_servant_clawback_usd": 80000000.0,
    "rm_total_downside_with_contribution_usd": 445000000.0,
    # FinCEN bounty vs. CCO salary defection economics.
    "cco_salary_usd": 450000.0,
    "fincen_bounty_min_usd": 15000000.0,
    "fincen_bounty_max_usd": 45000000.0,
    "analyst_bounty_to_cco_salary_ratio_min": 33.333333,
    "analyst_bounty_to_cco_salary_ratio_max": 100.0,
    # 314(b) correspondent debanking cascade.
    "post_314b_bank_accept_prob": 0.04,
    "correspondent_bank_hops_m": 5,
    "five_hop_banking_survival_prob": 1.024e-07,
    "five_hop_debanking_certainty": 0.9999998976,
    "correspondent_contempt_daily_fine_usd": 50000.0,
    # UHNW liquidity cascade and forced liquidation.
    "uhnw_nav_baseline_usd": 500000000.0,
    "lombard_credit_line_usd": 125000000.0,
    "unfunded_lp_commitments_usd": 100000000.0,
    "liquid_cash_buffer_usd": 25000000.0,
    "liquidity_shortfall_on_debanking_usd": 200000000.0,
    "secondary_lp_fire_sale_haircut": 0.4,
    "defaulting_lp_forfeiture_rate": 0.5,
    "paid_in_lp_capital_at_risk_usd": 160000000.0,
    "forced_liquidation_wealth_destruction_usd": 160000000.0,
}

# Tolerances: cent-level rounding on USD values; 6-decimal
# rounding/truncation on ratios and probabilities; 1e-9 on the
# near-certainty debanking complement.
TOL_MONEY = 5e-2
TOL_RATE = 1e-5
TOL_UNIT = 1e-6
TOL_CERTAINTY = 1e-9

# Regime probe: regulatory audit probability at which retention is tested.
P_AUDIT_REGIME = 0.01

REPORT = {"vectors": []}


def vector(idx, name):
    REPORT["vectors"].append(
        {"vector": idx, "name": name, "status": "PASS", "checks": []}
    )


def check(vec_idx, name, computed, expected, tol=None):
    if tol is None:
        ok = computed == expected
    else:
        ok = abs(computed - expected) <= tol
    REPORT["vectors"][vec_idx - 1]["checks"].append(
        {
            "name": name,
            "computed": computed,
            "expected": expected,
            "tolerance": tol if tol is not None else 0.0,
            "pass": bool(ok),
        }
    )
    return ok


def p_star(fee, loss):
    """Critical audit-probability threshold p* = F / (L + F).

    The bank is indifferent between retention and debanking when the
    expected audit loss p* L equals the retained fee (1 - p*) F.
    """
    return fee / (loss + fee)


def vector_1():
    """Bank loss-to-fee asymmetry & critical audit-probability thresholds."""
    vector(1, "bank_loss_to_fee_asymmetry_audit_thresholds")

    # JPMorgan: additive TVPA loss identity and retention economics.
    l_jpm = LOCKED["jpm_class_settlement_usd"] + LOCKED["jpm_usvi_settlement_usd"]
    check(1, "jpm_total_tvpa_loss_usd", l_jpm, LOCKED["jpm_total_tvpa_loss_usd"], TOL_MONEY)

    f_jpm = LOCKED["jpm_annual_relationship_fee_usd"]
    r_jpm = l_jpm / f_jpm
    check(1, "jpm_loss_to_fee_ratio", r_jpm, LOCKED["jpm_loss_to_fee_ratio"], TOL_RATE)

    ps_jpm = p_star(f_jpm, l_jpm)
    check(1, "jpm_critical_audit_prob_threshold", ps_jpm,
          LOCKED["jpm_critical_audit_prob_threshold"], TOL_RATE)

    # p*-indifference identity: p* L = (1 - p*) F = F L / (L + F).
    check(1, "jpm_p_star_indifference_identity_usd",
          ps_jpm * l_jpm, (1.0 - ps_jpm) * f_jpm, TOL_MONEY)

    # Deutsche Bank: additive NYDFS / class loss identity.
    l_db = LOCKED["db_nydfs_penalty_usd"] + LOCKED["db_class_settlement_usd"]
    check(1, "db_total_loss_usd", l_db, LOCKED["db_total_loss_usd"], TOL_MONEY)

    f_db = LOCKED["db_annual_relationship_fee_usd"]
    r_db = l_db / f_db
    check(1, "db_loss_to_fee_ratio", r_db, LOCKED["db_loss_to_fee_ratio"], TOL_RATE)

    ps_db = p_star(f_db, l_db)
    check(1, "db_critical_audit_prob_threshold", ps_db,
          LOCKED["db_critical_audit_prob_threshold"], TOL_RATE)

    check(1, "db_p_star_indifference_identity_usd",
          ps_db * l_db, (1.0 - ps_db) * f_db, TOL_MONEY)

    # Defection regime at p_audit = 0.01 > max(p*): expected audit loss
    # strictly dominates the retained fee for both banks.
    jpm_defect = 1.0 if P_AUDIT_REGIME * l_jpm > (1.0 - P_AUDIT_REGIME) * f_jpm else 0.0
    check(1, "jpm_defection_regime_at_p0.01", jpm_defect, 1.0)
    db_defect = 1.0 if P_AUDIT_REGIME * l_db > (1.0 - P_AUDIT_REGIME) * f_db else 0.0
    check(1, "db_defection_regime_at_p0.01", db_defect, 1.0)


def vector_2():
    """Faithless-servant clawback & relationship-manager downside."""
    vector(2, "faithless_servant_clawback_rm_downside")

    clawback = LOCKED["staley_annual_comp_usd"] * LOCKED["staley_disloyalty_years"]
    check(2, "staley_faithless_servant_clawback_usd", clawback,
          LOCKED["staley_faithless_servant_clawback_usd"], TOL_MONEY)

    rm_downside = LOCKED["jpm_total_tvpa_loss_usd"] + clawback
    check(2, "rm_total_downside_with_contribution_usd", rm_downside,
          LOCKED["rm_total_downside_with_contribution_usd"], TOL_MONEY)

    # Clawback strictly increases the RM downside beyond the bank loss alone.
    strict = 1.0 if rm_downside > LOCKED["jpm_total_tvpa_loss_usd"] else 0.0
    check(2, "rm_downside_strictly_exceeds_bank_loss", strict, 1.0)


def vector_3():
    """FinCEN bounty / CCO salary defection ratio."""
    vector(3, "fincen_bounty_cco_salary_defection_ratio")

    salary = LOCKED["cco_salary_usd"]
    ratio_min = LOCKED["fincen_bounty_min_usd"] / salary
    check(3, "analyst_bounty_to_cco_salary_ratio_min", ratio_min,
          LOCKED["analyst_bounty_to_cco_salary_ratio_min"], TOL_RATE)

    ratio_max = LOCKED["fincen_bounty_max_usd"] / salary
    check(3, "analyst_bounty_to_cco_salary_ratio_max", ratio_max,
          LOCKED["analyst_bounty_to_cco_salary_ratio_max"], TOL_RATE)

    # Minimum bounty strictly dominates the CCO annual salary.
    dom = 1.0 if LOCKED["fincen_bounty_min_usd"] > salary else 0.0
    check(3, "bounty_min_dominates_cco_salary", dom, 1.0)

    # Bounty band spans exactly 3x (max / min = 3.0).
    check(3, "bounty_band_span_ratio", ratio_max / ratio_min, 3.0, TOL_UNIT)


def vector_4():
    """314(b) five-hop correspondent debanking cascade & contempt fine."""
    vector(4, "s314b_five_hop_debanking_cascade")

    p_accept = LOCKED["post_314b_bank_accept_prob"]
    m = LOCKED["correspondent_bank_hops_m"]

    survival = p_accept ** m
    check(4, "five_hop_banking_survival_prob", survival,
          LOCKED["five_hop_banking_survival_prob"], 1e-12)

    certainty = 1.0 - survival
    check(4, "five_hop_debanking_certainty", certainty,
          LOCKED["five_hop_debanking_certainty"], TOL_CERTAINTY)

    # Debanking is a near-certainty: 1 - p^m >= 0.999999.
    near_certain = 1.0 if certainty >= 0.999999 else 0.0
    check(4, "debanking_certainty_ge_0.999999", near_certain, 1.0)

    # Annualized contempt fine dominates both relationship fee bases.
    fine_annual = LOCKED["correspondent_contempt_daily_fine_usd"] * 365.0
    check(4, "contempt_fine_annualized_usd", fine_annual, 18250000.0, TOL_MONEY)

    dom_jpm = 1.0 if fine_annual > LOCKED["jpm_annual_relationship_fee_usd"] else 0.0
    check(4, "contempt_fine_dominates_jpm_fee", dom_jpm, 1.0)
    dom_db = 1.0 if fine_annual > LOCKED["db_annual_relationship_fee_usd"] else 0.0
    check(4, "contempt_fine_dominates_db_fee", dom_db, 1.0)


def vector_5():
    """UHNW liquidity cascade & forced-liquidation wealth destruction."""
    vector(5, "uhnw_liquidity_forced_liquidation_destruction")

    # Shortfall on debanking: frozen Lombard line + unfunded LP
    # commitments net of the liquid cash buffer.
    shortfall = (LOCKED["lombard_credit_line_usd"]
                 + LOCKED["unfunded_lp_commitments_usd"]
                 - LOCKED["liquid_cash_buffer_usd"])
    check(5, "liquidity_shortfall_on_debanking_usd", shortfall,
          LOCKED["liquidity_shortfall_on_debanking_usd"], TOL_MONEY)

    # Forced-liquidation wealth destruction: fire-sale haircut on the
    # secondary LP-stake sale covering the shortfall plus forfeiture of
    # paid-in capital from defaulting LPs.
    destruction = (LOCKED["secondary_lp_fire_sale_haircut"] * shortfall
                   + LOCKED["defaulting_lp_forfeiture_rate"]
                   * LOCKED["paid_in_lp_capital_at_risk_usd"])
    check(5, "forced_liquidation_wealth_destruction_usd", destruction,
          LOCKED["forced_liquidation_wealth_destruction_usd"], TOL_MONEY)

    # Shortfall strictly exceeds the liquid buffer -> forced sale regime.
    forced = 1.0 if shortfall > LOCKED["liquid_cash_buffer_usd"] else 0.0
    check(5, "shortfall_exceeds_liquid_buffer", forced, 1.0)

    # Destruction as a fraction of baseline NAV (= 0.32).
    check(5, "wealth_destruction_pct_of_nav",
          destruction / LOCKED["uhnw_nav_baseline_usd"], 0.32, TOL_UNIT)

    # Destruction is bounded above by baseline NAV.
    bounded = 1.0 if destruction <= LOCKED["uhnw_nav_baseline_usd"] else 0.0
    check(5, "wealth_destruction_bounded_by_nav", bounded, 1.0)


def debanking_cascade_outputs():
    """Derived structural outputs emitted alongside the vector receipt."""
    l_jpm = LOCKED["jpm_total_tvpa_loss_usd"]
    f_jpm = LOCKED["jpm_annual_relationship_fee_usd"]
    l_db = LOCKED["db_total_loss_usd"]
    f_db = LOCKED["db_annual_relationship_fee_usd"]
    return {
        "jpm_p_star_indifference_usd": round(f_jpm * l_jpm / (l_jpm + f_jpm), 2),
        "db_p_star_indifference_usd": round(f_db * l_db / (l_db + f_db), 2),
        "contempt_fine_annualized_usd":
            LOCKED["correspondent_contempt_daily_fine_usd"] * 365.0,
        "wealth_destruction_pct_of_nav":
            LOCKED["forced_liquidation_wealth_destruction_usd"]
            / LOCKED["uhnw_nav_baseline_usd"],
        "regime_defection_audit_prob": P_AUDIT_REGIME,
    }


def main():
    vector_1()
    vector_2()
    vector_3()
    vector_4()
    vector_5()

    for v in REPORT["vectors"]:
        if any(not c["pass"] for c in v["checks"]):
            v["status"] = "FAIL"

    all_pass = len(REPORT["vectors"]) == 5 and all(
        v["status"] == "PASS" for v in REPORT["vectors"]
    )
    receipt = {
        "spec_id": "SPEC-DEFENSIVE-SAR-SAFE-HARBOR-314B-DEBANKING-CASCADE-v1.0",
        "proof_file": "proofs/verify_defensive_sar_safe_harbor_314b_debanking_cascade.py",
        "locked_constants_and_outputs": LOCKED,
        "vectors": REPORT["vectors"],
        "debanking_cascade_outputs": debanking_cascade_outputs(),
        "all_vectors_pass": all_pass,
    }
    print(json.dumps(receipt, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())