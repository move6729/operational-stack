#!/usr/bin/env python3
"""Deterministic proof for SPEC-PRIVATE-CREDIT-PIK-OUROBOROS-AND-BERMUDA-REINSURANCE-ARBITRAGE-v1.0.

Verifies, in pure Python 3 standard-library arithmetic, all six governing
equations (EQ-1 through EQ-6) and every constant of the locked empirical
payload embedded below.

Governing equations (closed form, per spec Sections 2.2 through 6.1):

  EQ-1  Bad-PIK compounding debt trajectory & true vs. optical DSCR:
          r_0 = r_base + s_cash;  I_0 = P_0 * r_0
          DSCR_True,0 = FCF / I_0 < 1
          r_total = r_0 + dr_step = r_cash + r_PIK
          P_t = P_0 * (1 + r_PIK)^t
          DSCR_Optical,1 = FCF / (P_0 * r_cash) > 1
        Empirical baseline identities (Lincoln Q1 2025 / Fitch BDC index):
          M_bad = s_bad(2025) / s_bad(2021)
          phi_bad = s_bad(2025) / s_PIK(2025)
          dLTV = LTV(2025) - LTV(0)
          Cov_Cash = Cov_GAAP * (1 - alpha_PIK,Fitch)

  EQ-2  Synthetic PIK revolver / DDTL round-trip identity:
          I_Cash,Reported = FCF_net + dD_Rev = P_0 * r_cash (unchanged 11%)
          dD_Net = P_0 * r_cash - FCF_net > 0
          alpha_PIK,Reported = 0;  DSCR_Econ = FCF / I_0

  EQ-3  BDC / RIC cash-fee-on-phantom-PIK liquidity drain (26 U.S.C. 852(a)):
          NII_Pre = R * (1 - c_ops - f_mgmt)
          Fee_PartI = tau_inc * NII_Pre
          NII_GAAP = (1 - tau_inc) * NII_Pre
          Div(rho) = rho * NII_GAAP
          CF_Net = R * [(1 - a) - c_ops - f_mgmt - tau_inc*(1 - c_ops - f_mgmt)
                        - rho*(1 - tau_inc)*(1 - c_ops - f_mgmt)]
          alpha* = (1 - rho) * (1 - tau_inc) * (1 - c_ops - f_mgmt)

  EQ-4  No-clawback Part I NII incentive siphon asymmetry:
          Pi_GP,PartI = tau_inc * sum(PIK_t) > 0;  Clawback_PartI = 0
          dW_LP,T = -[(1 - R_rec) * P_T + tau_inc * sum(PIK_t)]
          Principal loss vs. original par = R_rec * P_T - P_0

  EQ-5  GP-led continuation vehicle rational self-dealing inequality:
          dU_GP = (1 - theta_roll) * c_1 * max(0, V_L3 - H_1)
                  + PV(f_2) * V_L3 - c_1 * max(0, V_mkt - H_1) > 0

  EQ-6  Part A - RNF / CFO risk-based capital compression:
          RBC_Debt = (w_s*C1_s + w_m*C1_m) / (w_s + w_m)
          RBC_All  = w_s*C1_s + w_m*C1_m + w_eq*C1_Equity
          K_Debt = C1_Equity / RBC_Debt;  K_All = C1_Equity / RBC_All
        Part B - 4-layer look-through leverage & cascading wipeout:
          Slice_full = (1 - LTV_OpCo)*(1 - LTV_NAV)*Attach_RNF*0.10 = 0.0210
          L_Full = 1 / Slice_full
          d_1 = 1 - LTV_OpCo
          d_2 = d_1 * (1 + w_eq_RNF)
          d_3 = d_1 / Attach_RNF
          d_4 = d_2 + (1 - LTV_OpCo) * Buf_Bermuda

Exit code 0 iff every locked constant and structural identity holds within
1e-6 absolute tolerance (the locked payload is pinned to six decimals).
"""

from __future__ import annotations

import sys

TOL = 1e-6

# Spec-pinned auxiliary constants (Sections 2.3 and 6.1 of the canonical spec):
# working-capital / maintenance-CapEx cash drain inside the EQ-2 round-trip,
# and the fourth factor of the EQ-6 Part B compound equity slice
# (0.35 * 0.75 * 0.80 * 0.10 = 0.0210).
WC_CAPEX_DRAIN_M = 3.75
BERMUDA_EXPOSED_SLICE_FRACTION = 0.10

LOCKED = {
    "lincoln_q1_2025_pik_metrics": {
        "pik_loan_share_q4_2021": 0.07,
        "pik_loan_share_q1_2025": 0.11,
        "bad_pik_share_of_total_loans_q4_2021": 0.02,
        "bad_pik_share_of_total_loans_q1_2025": 0.06,
        "bad_pik_tripling_multiple": 3.0,
        "bad_pik_share_of_pik_loans_q1_2025": 0.545455,
        "bad_pik_ltv_at_origination": 0.49,
        "bad_pik_ltv_q1_2025": 0.86,
        "bad_pik_ltv_delta_pct_points": 0.37,
        "fitch_bdc_avg_pik_income_share_2025": 0.081,
        "fitch_bdc_unadjusted_dividend_coverage": 1.013,
        "fitch_bdc_cash_adjusted_dividend_coverage": 0.930947,
    },
    "gear_1_borrower_pik_toggle_and_synthetic_revolver_model": {
        "initial_loan_principal_m": 100.0,
        "sofr_base_rate": 0.0525,
        "initial_cash_spread": 0.0575,
        "initial_all_in_cash_rate": 0.11,
        "initial_annual_cash_interest_m": 11.0,
        "stressed_borrower_fcf_pre_interest_m": 8.25,
        "true_pre_toggle_cash_dscr": 0.75,
        "pik_toggle_step_up_bps": 0.015,
        "post_toggle_total_coupon": 0.125,
        "post_toggle_cash_coupon": 0.045,
        "post_toggle_pik_coupon": 0.08,
        "post_toggle_annual_cash_interest_m": 4.5,
        "post_toggle_optical_cash_dscr": 1.833333,
        "year_3_compounded_principal_m": 125.9712,
        "year_3_cumulative_pik_accrued_m": 25.9712,
        "synthetic_pik_revolver_draw_m": 6.5,
        "synthetic_pik_reported_pik_pct": 0.0,
        "synthetic_pik_economic_dscr": 0.75,
    },
    "gear_1b_bdc_ric_cash_drain_and_no_clawback_siphon": {
        "bdc_gross_investment_income_m": 100.0,
        "bdc_debt_interest_and_opex_fraction_c_ops": 0.35,
        "bdc_management_fee_fraction_f_mgmt": 0.12,
        "bdc_pre_incentive_nii_fraction": 0.53,
        "bdc_part_1_incentive_fee_rate_tau_inc": 0.20,
        "bdc_part_1_cash_incentive_fee_fraction": 0.106,
        "bdc_reported_gaap_nii_fraction": 0.424,
        "ric_statutory_distribution_min_rho_ric": 0.90,
        "mandatory_cash_dividend_90pct_nii_m": 38.16,
        "mandatory_cash_dividend_100pct_nii_m": 42.40,
        "total_mandatory_cash_outflow_90pct_m": 95.76,
        "total_mandatory_cash_outflow_100pct_m": 100.0,
        "critical_pik_share_threshold_alpha_crit_90pct": 0.0424,
        "critical_pik_share_threshold_alpha_crit_100pct": 0.0,
        "stressed_bdc_pik_share_alpha_pik": 0.15,
        "bdc_actual_cash_revenue_at_15pct_pik_m": 85.0,
        "bdc_annual_net_cash_burn_at_90pct_div_m": -10.76,
        "bdc_annual_net_cash_burn_at_100pct_div_m": -15.0,
        "no_clawback_3yr_gp_cash_siphon_on_25_97m_pik_m": 5.19424,
        "terminal_loan_recovery_rate": 0.40,
        "terminal_lp_principal_loss_on_100m_loan_m": -49.61152,
        "gp_clawback_on_part_1_nii_fees_m": 0.0,
    },
    "gear_2_continuation_vehicle_and_cross_fund_collusion": {
        "cv_market_volume_2024_b": 72.0,
        "cv_market_volume_2025_b": 107.0,
        "cv_yoy_growth_pct": 0.486111,
        "fund_1_invested_cost_basis_m": 200.0,
        "fund_1_hurdle_value_m": 250.0,
        "true_third_party_market_clearing_value_v_mkt_m": 220.0,
        "gp_self_marked_asc820_level3_cv_value_v_l3_m": 340.0,
        "valuation_overstatement_pct": 0.545455,
        "carry_rate_c_1": 0.20,
        "gp_carry_at_true_market_exit_m": 0.0,
        "gp_phantom_carry_crystallized_via_cv_m": 18.0,
        "gp_rollover_reinvestment_fraction": 0.50,
        "new_cv_present_value_fee_rate_pv_f2": 0.08,
        "gp_new_cv_management_fee_pv_m": 27.2,
        "gp_net_payoff_advantage_cv_over_honest_exit_m": 36.2,
    },
    "gear_3_and_4_rnf_cfo_rbc_arbitrage_and_bermuda_cascade": {
        "bermuda_ceded_us_life_annuity_reserves_b": 900.0,
        "bermuda_2025_new_cessions_b": 73.0,
        "naic_direct_equity_c1_rbc_factor": 0.30,
        "rnf_senior_note_tranche_share": 0.60,
        "rnf_senior_c1_factor_naic_1": 0.0068,
        "rnf_mezz_note_tranche_share": 0.20,
        "rnf_mezz_c1_factor_naic_2": 0.015,
        "rnf_equity_tranche_share": 0.20,
        "rnf_blended_c1_rbc_factor_affiliated_equity": 0.06708,
        "rnf_debt_tranches_only_blended_c1_factor": 0.00885,
        "rbc_arbitrage_compression_ratio_all_tranches": 4.472272,
        "rbc_arbitrage_compression_ratio_debt_slices": 33.898305,
        "cascade_stack_operating_co_debt_share": 0.65,
        "cascade_stack_pe_fund_nav_loan_ltv": 0.25,
        "cascade_stack_rnf_debt_tranche_attachment": 0.80,
        "cascade_stack_bermuda_reinsurer_capital_buffer": 0.08,
        "look_through_effective_leverage_multiple": 47.619048,
        "ebitda_drop_to_wipe_opco_equity_pct": 0.35,
        "ebitda_drop_to_wipe_pe_fund_nav_equity_pct": 0.4375,
        "ebitda_drop_to_impair_rnf_rated_notes_pct": 0.42,
        "ebitda_drop_to_breach_bermuda_reinsurer_solvency_pct": 0.448,
    },
}

_RESULTS: list = []


def check(label: str, computed: float, locked: float) -> None:
    """Record an equality assertion |computed - locked| <= TOL."""
    computed = float(computed)
    locked = float(locked)
    _RESULTS.append((label, computed, locked, abs(computed - locked) <= TOL))


def require(label: str, condition: bool) -> None:
    """Record a strict inequality / ordering assertion."""
    _RESULTS.append((label, 1.0 if condition else 0.0, 1.0, bool(condition)))


def verify_group(group: str, inputs: dict, outputs: dict) -> int:
    """Assert full key coverage of a locked group, then match every leaf."""
    locked = LOCKED[group]
    merged = dict(inputs)
    merged.update(outputs)
    uncovered = sorted(set(locked) - set(merged))
    unexpected = sorted(set(merged) - set(locked))
    if uncovered:
        raise AssertionError(f"{group}: locked keys not covered by proof: {uncovered}")
    if unexpected:
        raise AssertionError(f"{group}: proof keys absent from locked payload: {unexpected}")
    for key in sorted(locked):
        check(f"{group}.{key}", merged[key], locked[key])
    return len(locked)


def eq1_empirical_baseline() -> int:
    """EQ-1 empirical identities: Lincoln Q1 2025 bad-PIK drift & Fitch coverage."""
    inp = {
        "pik_loan_share_q4_2021": 0.07,
        "pik_loan_share_q1_2025": 0.11,
        "bad_pik_share_of_total_loans_q4_2021": 0.02,
        "bad_pik_share_of_total_loans_q1_2025": 0.06,
        "bad_pik_ltv_at_origination": 0.49,
        "bad_pik_ltv_q1_2025": 0.86,
        "fitch_bdc_avg_pik_income_share_2025": 0.081,
        "fitch_bdc_unadjusted_dividend_coverage": 1.013,
    }
    out = {
        "bad_pik_tripling_multiple": (
            inp["bad_pik_share_of_total_loans_q1_2025"]
            / inp["bad_pik_share_of_total_loans_q4_2021"]
        ),
        "bad_pik_share_of_pik_loans_q1_2025": (
            inp["bad_pik_share_of_total_loans_q1_2025"] / inp["pik_loan_share_q1_2025"]
        ),
        "bad_pik_ltv_delta_pct_points": (
            inp["bad_pik_ltv_q1_2025"] - inp["bad_pik_ltv_at_origination"]
        ),
        "fitch_bdc_cash_adjusted_dividend_coverage": (
            inp["fitch_bdc_unadjusted_dividend_coverage"]
            * (1.0 - inp["fitch_bdc_avg_pik_income_share_2025"])
        ),
    }
    require(
        "EQ-1.cash_adjusted_coverage_below_unity",
        out["fitch_bdc_cash_adjusted_dividend_coverage"] < 1.0
        < inp["fitch_bdc_unadjusted_dividend_coverage"],
    )
    return verify_group("lincoln_q1_2025_pik_metrics", inp, out)


def eq1_eq2_gear1_toggle_and_synthetic_revolver(sink: dict) -> int:
    """EQ-1 compounding trajectory & DSCR optics; EQ-2 synthetic revolver round-trip."""
    inp = {
        "initial_loan_principal_m": 100.0,
        "sofr_base_rate": 0.0525,
        "initial_cash_spread": 0.0575,
        "stressed_borrower_fcf_pre_interest_m": 8.25,
        "pik_toggle_step_up_bps": 0.015,
        "post_toggle_cash_coupon": 0.045,
        "post_toggle_pik_coupon": 0.08,
    }
    p0 = inp["initial_loan_principal_m"]
    fcf = inp["stressed_borrower_fcf_pre_interest_m"]
    r0 = inp["sofr_base_rate"] + inp["initial_cash_spread"]
    i0 = p0 * r0
    r_cash = inp["post_toggle_cash_coupon"]
    r_pik = inp["post_toggle_pik_coupon"]
    r_total = r0 + inp["pik_toggle_step_up_bps"]
    i_cash_post = p0 * r_cash
    p1 = p0 * (1.0 + r_pik)
    p2 = p0 * (1.0 + r_pik) ** 2
    p3 = p0 * (1.0 + r_pik) ** 3
    pik_3 = p3 - p0
    fcf_net = fcf - WC_CAPEX_DRAIN_M
    draw = i0 - fcf_net
    out = {
        "initial_all_in_cash_rate": r0,
        "initial_annual_cash_interest_m": i0,
        "true_pre_toggle_cash_dscr": fcf / i0,
        "post_toggle_total_coupon": r_total,
        "post_toggle_annual_cash_interest_m": i_cash_post,
        "post_toggle_optical_cash_dscr": fcf / i_cash_post,
        "year_3_compounded_principal_m": p3,
        "year_3_cumulative_pik_accrued_m": pik_3,
        "synthetic_pik_revolver_draw_m": draw,
        "synthetic_pik_reported_pik_pct": 0.0,
        "synthetic_pik_economic_dscr": fcf / i0,
    }
    # EQ-1 structural identities (spec Section 2.2).
    check("EQ-1.coupon_decomposition", r_cash + r_pik, r_total)
    check("EQ-1.P1_trajectory", p1, 108.0)
    check("EQ-1.P2_trajectory", p2, 116.64)
    check("EQ-1.true_post_toggle_dscr", fcf / (p0 * (r_cash + r_pik)), 0.66)
    require("EQ-1.true_dscr_below_unity", fcf / i0 < 1.0)
    require("EQ-1.optical_dscr_above_unity", out["post_toggle_optical_cash_dscr"] > 1.0)
    # EQ-2 round-trip identity (spec Section 2.3): reported cash interest is
    # funded by net organic FCF plus a same-syndicate revolver/DDTL draw.
    check("EQ-2.round_trip_cash_interest_identity", fcf_net + draw, i0)
    require("EQ-2.synthetic_draw_strictly_positive", draw > 0.0)
    require("EQ-2.economic_dscr_equals_true_dscr", out["synthetic_pik_economic_dscr"] == fcf / i0)
    sink.update(p0=p0, p3=p3, pik_3=pik_3)
    return verify_group("gear_1_borrower_pik_toggle_and_synthetic_revolver_model", inp, out)


def eq3_eq4_gear1b_ric_drain_and_siphon(sink: dict) -> int:
    """EQ-3 RIC liquidity drain & critical PIK threshold; EQ-4 no-clawback siphon."""
    inp = {
        "bdc_gross_investment_income_m": 100.0,
        "bdc_debt_interest_and_opex_fraction_c_ops": 0.35,
        "bdc_management_fee_fraction_f_mgmt": 0.12,
        "bdc_part_1_incentive_fee_rate_tau_inc": 0.20,
        "ric_statutory_distribution_min_rho_ric": 0.90,
        "stressed_bdc_pik_share_alpha_pik": 0.15,
        "terminal_loan_recovery_rate": 0.40,
    }
    rev = inp["bdc_gross_investment_income_m"]
    c_ops = inp["bdc_debt_interest_and_opex_fraction_c_ops"]
    f_mgmt = inp["bdc_management_fee_fraction_f_mgmt"]
    tau = inp["bdc_part_1_incentive_fee_rate_tau_inc"]
    rho = inp["ric_statutory_distribution_min_rho_ric"]
    alpha = inp["stressed_bdc_pik_share_alpha_pik"]
    r_rec = inp["terminal_loan_recovery_rate"]
    nii_pre_frac = 1.0 - c_ops - f_mgmt
    fee_frac = tau * nii_pre_frac
    nii_frac = (1.0 - tau) * nii_pre_frac
    fixed_cash = (c_ops + f_mgmt + fee_frac) * rev
    div_90 = rho * nii_frac * rev
    div_100 = 1.0 * nii_frac * rev
    out_90 = fixed_cash + div_90
    out_100 = fixed_cash + div_100
    cash_rev = rev * (1.0 - alpha)
    alpha_crit_90 = (1.0 - rho) * (1.0 - tau) * nii_pre_frac
    alpha_crit_100 = (1.0 - 1.0) * (1.0 - tau) * nii_pre_frac
    p0 = sink["p0"]
    p3 = sink["p3"]
    pik_3 = sink["pik_3"]
    siphon = tau * pik_3
    out = {
        "bdc_pre_incentive_nii_fraction": nii_pre_frac,
        "bdc_part_1_cash_incentive_fee_fraction": fee_frac,
        "bdc_reported_gaap_nii_fraction": nii_frac,
        "mandatory_cash_dividend_90pct_nii_m": div_90,
        "mandatory_cash_dividend_100pct_nii_m": div_100,
        "total_mandatory_cash_outflow_90pct_m": out_90,
        "total_mandatory_cash_outflow_100pct_m": out_100,
        "critical_pik_share_threshold_alpha_crit_90pct": alpha_crit_90,
        "critical_pik_share_threshold_alpha_crit_100pct": alpha_crit_100,
        "bdc_actual_cash_revenue_at_15pct_pik_m": cash_rev,
        "bdc_annual_net_cash_burn_at_90pct_div_m": cash_rev - out_90,
        "bdc_annual_net_cash_burn_at_100pct_div_m": cash_rev - out_100,
        "no_clawback_3yr_gp_cash_siphon_on_25_97m_pik_m": siphon,
        "terminal_lp_principal_loss_on_100m_loan_m": r_rec * p3 - p0,
        "gp_clawback_on_part_1_nii_fees_m": 0.0,
    }
    # EQ-3 structural identities (spec Section 3.2): the closed-form threshold
    # equals the outflow-form threshold, and the CF_Net bracket form equals
    # cash revenue minus total mandatory cash outflows.
    check("EQ-3.alpha_crit_90_outflow_form", 1.0 - out_90 / rev, alpha_crit_90)
    check(
        "EQ-3.cf_net_closed_form_90",
        rev * ((1.0 - alpha) - c_ops - f_mgmt - tau * nii_pre_frac
               - rho * (1.0 - tau) * nii_pre_frac),
        cash_rev - out_90,
    )
    check("EQ-3.ric_100pct_cash_closure", out_100, rev)
    require("EQ-3.cash_burn_negative_at_15pct_pik", cash_rev - out_90 < 0.0 and cash_rev - out_100 < 0.0)
    require("EQ-3.fitch_avg_pik_exceeds_alpha_crit_90", 0.081 > alpha_crit_90)
    # EQ-4 structural identities (spec Section 3.3): terminal LP wealth
    # transfer and carrying-value write-off on the compounded claim.
    check("EQ-4.lp_total_wealth_transfer", -((1.0 - r_rec) * p3 + siphon), -80.77696)
    check("EQ-4.carrying_value_writeoff", -(1.0 - r_rec) * p3, -75.58272)
    require("EQ-4.siphon_strictly_positive_zero_clawback", siphon > 0.0)
    return verify_group("gear_1b_bdc_ric_cash_drain_and_no_clawback_siphon", inp, out)


def eq5_gear2_continuation_vehicle() -> int:
    """EQ-5 GP-led continuation vehicle rational self-dealing inequality."""
    inp = {
        "cv_market_volume_2024_b": 72.0,
        "cv_market_volume_2025_b": 107.0,
        "fund_1_invested_cost_basis_m": 200.0,
        "fund_1_hurdle_value_m": 250.0,
        "true_third_party_market_clearing_value_v_mkt_m": 220.0,
        "gp_self_marked_asc820_level3_cv_value_v_l3_m": 340.0,
        "carry_rate_c_1": 0.20,
        "gp_rollover_reinvestment_fraction": 0.50,
        "new_cv_present_value_fee_rate_pv_f2": 0.08,
    }
    v24 = inp["cv_market_volume_2024_b"]
    v25 = inp["cv_market_volume_2025_b"]
    h1 = inp["fund_1_hurdle_value_m"]
    v_mkt = inp["true_third_party_market_clearing_value_v_mkt_m"]
    v_l3 = inp["gp_self_marked_asc820_level3_cv_value_v_l3_m"]
    c1 = inp["carry_rate_c_1"]
    theta = inp["gp_rollover_reinvestment_fraction"]
    f2 = inp["new_cv_present_value_fee_rate_pv_f2"]
    carry_mkt = c1 * max(0.0, v_mkt - h1)
    carry_cv = c1 * max(0.0, v_l3 - h1)
    fee_pv = f2 * v_l3
    du_gp = (1.0 - theta) * carry_cv + fee_pv - carry_mkt
    out = {
        "cv_yoy_growth_pct": (v25 - v24) / v24,
        "valuation_overstatement_pct": (v_l3 - v_mkt) / v_mkt,
        "gp_carry_at_true_market_exit_m": carry_mkt,
        "gp_phantom_carry_crystallized_via_cv_m": carry_cv,
        "gp_new_cv_management_fee_pv_m": fee_pv,
        "gp_net_payoff_advantage_cv_over_honest_exit_m": du_gp,
    }
    check("EQ-5.hard_cash_carry_after_rollover", (1.0 - theta) * carry_cv, 9.0)
    require("EQ-5.market_exit_below_hurdle_zero_carry", v_mkt < h1 and carry_mkt == 0.0)
    require("EQ-5.self_dealing_inequality_strictly_positive", du_gp > 0.0)
    return verify_group("gear_2_continuation_vehicle_and_cross_fund_collusion", inp, out)


def eq6_gear34_rbc_compression_and_bermuda_cascade() -> int:
    """EQ-6 Part A RBC compression; Part B look-through leverage & cascade."""
    inp = {
        "bermuda_ceded_us_life_annuity_reserves_b": 900.0,
        "bermuda_2025_new_cessions_b": 73.0,
        "naic_direct_equity_c1_rbc_factor": 0.30,
        "rnf_senior_note_tranche_share": 0.60,
        "rnf_senior_c1_factor_naic_1": 0.0068,
        "rnf_mezz_note_tranche_share": 0.20,
        "rnf_mezz_c1_factor_naic_2": 0.015,
        "rnf_equity_tranche_share": 0.20,
        "cascade_stack_operating_co_debt_share": 0.65,
        "cascade_stack_pe_fund_nav_loan_ltv": 0.25,
        "cascade_stack_rnf_debt_tranche_attachment": 0.80,
        "cascade_stack_bermuda_reinsurer_capital_buffer": 0.08,
    }
    c1_eq = inp["naic_direct_equity_c1_rbc_factor"]
    w_s = inp["rnf_senior_note_tranche_share"]
    f_s = inp["rnf_senior_c1_factor_naic_1"]
    w_m = inp["rnf_mezz_note_tranche_share"]
    f_m = inp["rnf_mezz_c1_factor_naic_2"]
    w_e = inp["rnf_equity_tranche_share"]
    ltv_opco = inp["cascade_stack_operating_co_debt_share"]
    ltv_nav = inp["cascade_stack_pe_fund_nav_loan_ltv"]
    attach = inp["cascade_stack_rnf_debt_tranche_attachment"]
    buf = inp["cascade_stack_bermuda_reinsurer_capital_buffer"]
    # EQ-6 Part A (spec Section 5.2).
    rbc_debt = (w_s * f_s + w_m * f_m) / (w_s + w_m)
    rbc_all = w_s * f_s + w_m * f_m + w_e * c1_eq
    k_debt = c1_eq / rbc_debt
    k_all = c1_eq / rbc_all
    # EQ-6 Part B (spec Section 6.1).
    e_opco = 1.0 - ltv_opco
    e_nav = 1.0 - ltv_nav
    slice_full = e_opco * e_nav * attach * BERMUDA_EXPOSED_SLICE_FRACTION
    l_full = 1.0 / slice_full
    l_layer3 = 1.0 / (e_opco * e_nav * (1.0 - attach))
    d1 = e_opco
    d2 = d1 * (1.0 + w_e)
    d3 = d1 / attach
    d4 = d2 + e_opco * buf
    out = {
        "rnf_blended_c1_rbc_factor_affiliated_equity": rbc_all,
        "rnf_debt_tranches_only_blended_c1_factor": rbc_debt,
        "rbc_arbitrage_compression_ratio_all_tranches": k_all,
        "rbc_arbitrage_compression_ratio_debt_slices": k_debt,
        "look_through_effective_leverage_multiple": l_full,
        "ebitda_drop_to_wipe_opco_equity_pct": d1,
        "ebitda_drop_to_impair_rnf_rated_notes_pct": d2,
        "ebitda_drop_to_wipe_pe_fund_nav_equity_pct": d3,
        "ebitda_drop_to_breach_bermuda_reinsurer_solvency_pct": d4,
    }
    # EQ-6 Part A structural identities.
    check("EQ-6A.tranche_partition", w_s + w_m + w_e, 1.0)
    check("EQ-6A.debt_attachment_partition", w_s + w_m, attach)
    require("EQ-6A.debt_compression_dominates_all_tranche", k_debt > k_all > 1.0)
    # EQ-6 Part B structural identities.
    check("EQ-6B.layer3_look_through_leverage", l_layer3, 19.047619)
    check("EQ-6B.composite_slice_buffer_equivalence", slice_full, e_opco * e_nav * buf)
    check("EQ-6B.nav_wipeout_band_form", d2 + d1 * w_e * ltv_nav, d3)
    require("EQ-6B.cascade_thresholds_strictly_ordered", d1 < d2 < d3 < d4)
    return verify_group("gear_3_and_4_rnf_cfo_rbc_arbitrage_and_bermuda_cascade", inp, out)


def main() -> int:
    sink: dict = {}
    stages = [
        ("EQ-1   empirical PIK baseline identities (Lincoln / Fitch)", eq1_empirical_baseline()),
        ("EQ-1/2 Gear 1 bad-PIK toggle & synthetic revolver round-trip", eq1_eq2_gear1_toggle_and_synthetic_revolver(sink)),
        ("EQ-3/4 Gear 1b BDC/RIC cash drain & no-clawback siphon", eq3_eq4_gear1b_ric_drain_and_siphon(sink)),
        ("EQ-5   Gear 2 continuation vehicle self-dealing inequality", eq5_gear2_continuation_vehicle()),
        ("EQ-6   Gear 3/4 RBC compression & Bermuda cascade leverage", eq6_gear34_rbc_compression_and_bermuda_cascade()),
    ]
    for label, count in stages:
        print(f"OK  {label}: {count} locked constants reproduced")
    failed = [row for row in _RESULTS if not row[3]]
    total = len(_RESULTS)
    print(f"checks: {total}  passed: {total - len(failed)}  failed: {len(failed)}")
    if failed:
        for label, computed, locked, _ in failed:
            print(f"FAIL {label}: computed={computed!r} locked={locked!r}")
        return 1
    print("PROOF PASS: EQ-1..EQ-6 reproduce the full locked payload within 1e-6.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
