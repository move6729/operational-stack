#!/usr/bin/env python3
"""
Canonical Proof: SPEC-ALGORITHMIC-SURVEILLANCE-PRICING-AND-SECTION-1981-UNRUH-LIQUIDATION-v1.0
Models:
1. AAA Mass Arbitration Fee Blow-Up & Cal. Civ. Proc. Code § 1281.97 Default Dynamics
2. Pro Se Edge-Compute OpEx vs. Corporate Defense OpEx Asymmetry
3. California Unruh Civil Rights Act (Cal. Civ. Code §§ 51, 52(a)) Statutory Liquidation
4. Principal-Agent Executive Horizon Distortion (Jensen-Meckling / Holmström)
5. Parameterized Tranche Recovery Waterfall under $10.0B Unruh Class Judgment Stress
"""

import json
import sys
from typing import Dict, Any


def tranche_recovery(ev_usd_m: float, unruh_judgment_usd_m: float) -> Dict[str, Any]:
    """
    Maps post-judgment Enterprise Value (ev_usd_m) and Unruh judgment liability
    (unruh_judgment_usd_m) across Uber's debt stack tranches (in $M).
    """
    secured_aurora_notes_m = 1125.0
    unsecured_notes_and_converts_m = 9475.0
    undrawn_revolver_commitment_m = 5000.0
    total_note_principal_m = secured_aurora_notes_m + unsecured_notes_and_converts_m
    total_debt_and_facility_m = total_note_principal_m + undrawn_revolver_commitment_m

    # Tier 1: Senior Secured Exchangeable Notes (Aurora Innovation Class A pledge)
    secured_recovery_m = min(ev_usd_m, secured_aurora_notes_m)
    secured_cents = round((secured_recovery_m / secured_aurora_notes_m) * 100.0, 4)
    residual_ev_after_secured_m = max(0.0, ev_usd_m - secured_aurora_notes_m)

    # Tier 2: Senior Unsecured Notes + 2028 Converts + Pari Passu Unruh Judgment Claim
    unsecured_pool_claims_m = unsecured_notes_and_converts_m + unruh_judgment_usd_m
    unsecured_pool_recovery_m = min(residual_ev_after_secured_m, unsecured_pool_claims_m)
    unsecured_cents = round((unsecured_pool_recovery_m / unsecured_pool_claims_m) * 100.0, 4)

    # Tier 3: Common Equity Residual
    residual_equity_m = max(0.0, residual_ev_after_secured_m - unsecured_pool_claims_m)

    return {
        "uber_total_note_principal_usd_m": total_note_principal_m,
        "uber_revolver_commitment_usd_m": undrawn_revolver_commitment_m,
        "uber_total_debt_and_facility_stack_usd_m": total_debt_and_facility_m,
        "uber_secured_aurora_pledge_notes_usd_m": secured_aurora_notes_m,
        "uber_unsecured_notes_and_converts_usd_m": unsecured_notes_and_converts_m,
        "stress_ev_post_judgment_usd_m": ev_usd_m,
        "unsecured_pool_total_claims_usd_m": unsecured_pool_claims_m,
        "secured_recovery_usd_m": secured_recovery_m,
        "secured_recovery_cents_on_dollar": secured_cents,
        "unsecured_pool_recovery_usd_m": unsecured_pool_recovery_m,
        "unsecured_recovery_cents_on_dollar": unsecured_cents,
        "residual_equity_recovery_usd_m": residual_equity_m,
    }


def run_verification() -> Dict[str, Any]:
    # 1. Promotional Fee Waiver & Considine AAA Mass Arbitration Cohort
    delta_f_fee_waiver_usd = 3.99
    n_aaa_claimants = 31500
    g_cohort_promo_shift_usd = round(n_aaa_claimants * delta_f_fee_waiver_usd, 2)

    f_aaa_filing_usd = 500.0
    f_aaa_mgmt_usd = 1400.0
    f_aaa_arbitrator_usd = 1500.0
    f_aaa_total_per_claim_usd = f_aaa_filing_usd + f_aaa_mgmt_usd + f_aaa_arbitrator_usd

    l_aaa_gross_schedule_usd = round(n_aaa_claimants * f_aaa_total_per_claim_usd, 2)
    l_aaa_net_committed_usd = 91600000.0

    n_ca_batch_claimants = 7771
    l_ca_batch_invoice_usd = round(n_ca_batch_claimants * f_aaa_mgmt_usd, 2)

    m_aaa_fee_to_promo_blowup = round(l_aaa_net_committed_usd / g_cohort_promo_shift_usd, 4)
    ccp_1281_97_default_window_days = 30

    # 2. Pro Se Edge Compute vs. Corporate Defense Asymmetry
    c_edge_pro_se_opex_usd = 0.05
    c_corp_defense_opex_usd = 16250.0
    m_pro_se_opex_asymmetry = round(c_corp_defense_opex_usd / c_edge_pro_se_opex_usd, 4)

    # 3. California Unruh Act (Cal. Civ. Code § 52(a)) Statutory Liquidation
    d_stat_unruh_usd = 4000.0
    l_unruh_31500_cohort_usd = round(n_aaa_claimants * d_stat_unruh_usd, 2)

    n_tx_affected = 2500000
    g_promo_shift_usd = round(n_tx_affected * delta_f_fee_waiver_usd, 2)
    l_gross_unruh_usd = round(n_tx_affected * d_stat_unruh_usd, 2)
    m_statutory_blowup_ratio = round(l_gross_unruh_usd / g_promo_shift_usd, 4)

    p_cert_settled = 0.15
    l_expected_settlement_usd = round(p_cert_settled * l_gross_unruh_usd, 2)
    net_ev_destruction_usd = round(g_promo_shift_usd - l_expected_settlement_usd, 2)

    # 4. Executive Agency Horizon Distortion (Jensen-Meckling / Holmström)
    t_exec_tenure_years = 2.5
    tau_litigation_lag_years = 4.0
    annual_rsu_bonus_usd = 168000.0
    indicator_clawback_within_tenure = 1.0 if tau_litigation_lag_years <= t_exec_tenure_years else 0.0
    u_exec_net_payoff_usd = round(
        t_exec_tenure_years * annual_rsu_bonus_usd - indicator_clawback_within_tenure * l_expected_settlement_usd,
        2,
    )

    # 5. Capital Structure & Tranche Recovery Waterfall ($12,000M Stress EV, $10,000M Unruh Claim)
    waterfall = tranche_recovery(ev_usd_m=12000.0, unruh_judgment_usd_m=10000.0)

    results = {
        "delta_f_fee_waiver_usd": delta_f_fee_waiver_usd,
        "n_aaa_claimants": n_aaa_claimants,
        "g_cohort_promo_shift_usd": g_cohort_promo_shift_usd,
        "f_aaa_filing_usd": f_aaa_filing_usd,
        "f_aaa_mgmt_usd": f_aaa_mgmt_usd,
        "f_aaa_arbitrator_usd": f_aaa_arbitrator_usd,
        "f_aaa_total_per_claim_usd": f_aaa_total_per_claim_usd,
        "l_aaa_gross_schedule_usd": l_aaa_gross_schedule_usd,
        "l_aaa_net_committed_usd": l_aaa_net_committed_usd,
        "n_ca_batch_claimants": n_ca_batch_claimants,
        "l_ca_batch_invoice_usd": l_ca_batch_invoice_usd,
        "m_aaa_fee_to_promo_blowup": m_aaa_fee_to_promo_blowup,
        "ccp_1281_97_default_window_days": ccp_1281_97_default_window_days,
        "c_edge_pro_se_opex_usd": c_edge_pro_se_opex_usd,
        "c_corp_defense_opex_usd": c_corp_defense_opex_usd,
        "m_pro_se_opex_asymmetry": m_pro_se_opex_asymmetry,
        "d_stat_unruh_usd": d_stat_unruh_usd,
        "l_unruh_31500_cohort_usd": l_unruh_31500_cohort_usd,
        "n_tx_affected": n_tx_affected,
        "g_promo_shift_usd": g_promo_shift_usd,
        "l_gross_unruh_usd": l_gross_unruh_usd,
        "m_statutory_blowup_ratio": m_statutory_blowup_ratio,
        "p_cert_settled": p_cert_settled,
        "l_expected_settlement_usd": l_expected_settlement_usd,
        "net_ev_destruction_usd": net_ev_destruction_usd,
        "t_exec_tenure_years": t_exec_tenure_years,
        "tau_litigation_lag_years": tau_litigation_lag_years,
        "u_exec_net_payoff_usd": u_exec_net_payoff_usd,
        "uber_total_note_principal_usd_m": waterfall["uber_total_note_principal_usd_m"],
        "uber_revolver_commitment_usd_m": waterfall["uber_revolver_commitment_usd_m"],
        "uber_total_debt_and_facility_stack_usd_m": waterfall["uber_total_debt_and_facility_stack_usd_m"],
        "uber_secured_aurora_pledge_notes_usd_m": waterfall["uber_secured_aurora_pledge_notes_usd_m"],
        "uber_unsecured_notes_and_converts_usd_m": waterfall["uber_unsecured_notes_and_converts_usd_m"],
        "stress_ev_post_judgment_usd_m": waterfall["stress_ev_post_judgment_usd_m"],
        "unsecured_pool_total_claims_usd_m": waterfall["unsecured_pool_total_claims_usd_m"],
        "unsecured_recovery_cents_on_dollar": waterfall["unsecured_recovery_cents_on_dollar"],
    }

    # Exact Deterministic Assertions across all 34 locked constants
    assert results["delta_f_fee_waiver_usd"] == 3.99
    assert results["n_aaa_claimants"] == 31500
    assert results["g_cohort_promo_shift_usd"] == 125685.0
    assert results["f_aaa_filing_usd"] == 500.0
    assert results["f_aaa_mgmt_usd"] == 1400.0
    assert results["f_aaa_arbitrator_usd"] == 1500.0
    assert results["f_aaa_total_per_claim_usd"] == 3400.0
    assert results["l_aaa_gross_schedule_usd"] == 107100000.0
    assert results["l_aaa_net_committed_usd"] == 91600000.0
    assert results["n_ca_batch_claimants"] == 7771
    assert results["l_ca_batch_invoice_usd"] == 10879400.0
    assert results["m_aaa_fee_to_promo_blowup"] == 728.8061
    assert results["ccp_1281_97_default_window_days"] == 30
    assert results["c_edge_pro_se_opex_usd"] == 0.05
    assert results["c_corp_defense_opex_usd"] == 16250.0
    assert results["m_pro_se_opex_asymmetry"] == 325000.0
    assert results["d_stat_unruh_usd"] == 4000.0
    assert results["l_unruh_31500_cohort_usd"] == 126000000.0
    assert results["n_tx_affected"] == 2500000
    assert results["g_promo_shift_usd"] == 9975000.0
    assert results["l_gross_unruh_usd"] == 10000000000.0
    assert results["m_statutory_blowup_ratio"] == 1002.5063
    assert results["p_cert_settled"] == 0.15
    assert results["l_expected_settlement_usd"] == 1500000000.0
    assert results["net_ev_destruction_usd"] == -1490025000.0
    assert results["t_exec_tenure_years"] == 2.5
    assert results["tau_litigation_lag_years"] == 4.0
    assert results["u_exec_net_payoff_usd"] == 420000.0
    assert results["uber_total_note_principal_usd_m"] == 10600.0
    assert results["uber_revolver_commitment_usd_m"] == 5000.0
    assert results["uber_total_debt_and_facility_stack_usd_m"] == 15600.0
    assert results["uber_secured_aurora_pledge_notes_usd_m"] == 1125.0
    assert results["uber_unsecured_notes_and_converts_usd_m"] == 9475.0
    assert results["stress_ev_post_judgment_usd_m"] == 12000.0
    assert results["unsecured_pool_total_claims_usd_m"] == 19475.0
    assert results["unsecured_recovery_cents_on_dollar"] == 55.8408

    return results


if __name__ == "__main__":
    output = run_verification()
    print(json.dumps(output, indent=2))
    sys.exit(0)
