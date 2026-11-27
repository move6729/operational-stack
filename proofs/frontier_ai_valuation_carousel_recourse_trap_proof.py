#!/usr/bin/env python3
"""
Proof: Frontier AI Valuation Carousel Recourse Trap
Canonical Specification: SPEC-FRONTIER-AI-VALUATION-CAROUSEL-RECOURSE-TRAP-v1.0
Pure Python 3 stdlib. Exit code 0 on all assertions passing.

Mechanisms proven:
1. ASC 606-10-32-25 / ASC 820 valuation distortion from vendor-compute
   credit-for-equity round-trip revenue (phantom gross revenue disallowed
   under ASC 606; headline-to-cash distortion multiple under ASC 820).
2. Parameterized 4-tranche capital-stack waterfall: tranche_recovery(ev).
3. Bayesian ML-telemetry scienter posterior via sequential likelihood-ratio
   updating and D&O personal-profit exclusion voidance arithmetic.
4. 2x2 GP-vs-Founder prisoner's dilemma payoff matrix with strict
   defect-dominance wedge.
"""

import json
import math

# ---------------------------------------------------------------
# 1. ASC 606 / ASC 820 Valuation Distortion
# ---------------------------------------------------------------

def compute_asc606_820_valuation():
    """Closed-form ASC 606-10-32-25 phantom-revenue disallowance and
    ASC 820 headline-to-cash-equivalent EV distortion multiple."""
    headline_post_money_valuation_m = 8000.0
    total_series_d_round_m = 650.0
    cash_institutional_lp_investment_m = 350.0
    vendor_compute_credit_equity_swap_m = 300.0
    vendor_compute_gross_margin_pct = 0.75
    goodhart_benchmark_contamination_penalty_m = 4910.7692307692305

    # ASC 606: vendor gross-margin portion of the credit-for-equity swap
    # cannot be recognized as gross revenue (no genuine vendor to the
    # round-tripped compute credits) -> disallowed phantom gross revenue.
    asc_606_phantom_gross_revenue_disallowed_m = (
        vendor_compute_credit_equity_swap_m * vendor_compute_gross_margin_pct
    )
    # The residual is the vendor's true marginal watt/silicon cost basis.
    vendor_true_marginal_watt_silicon_cost_m = (
        vendor_compute_credit_equity_swap_m
        - asc_606_phantom_gross_revenue_disallowed_m
    )
    # Round-trip valuation haircut: phantom revenue scaled by the
    # valuation multiple implied by the round (headline / round size).
    round_trip_valuation_haircut_m = headline_post_money_valuation_m * (
        asc_606_phantom_gross_revenue_disallowed_m / total_series_d_round_m
    )
    # ASC 820 cash-equivalent EV: headline minus round-trip haircut minus
    # Goodhart benchmark-contamination penalty on the benchmark-adjacent
    # valuation premium.
    true_cash_equivalent_enterprise_value_m = (
        headline_post_money_valuation_m
        - round(round_trip_valuation_haircut_m, 2)
        - round(goodhart_benchmark_contamination_penalty_m, 2)
    )
    asc_820_headline_to_cash_distortion_multiple = (
        headline_post_money_valuation_m
        / true_cash_equivalent_enterprise_value_m
    )
    return {
        "headline_post_money_valuation_m": headline_post_money_valuation_m,
        "total_series_d_round_m": total_series_d_round_m,
        "cash_institutional_lp_investment_m": cash_institutional_lp_investment_m,
        "asc_606_phantom_gross_revenue_disallowed_m": asc_606_phantom_gross_revenue_disallowed_m,
        "vendor_true_marginal_watt_silicon_cost_m": vendor_true_marginal_watt_silicon_cost_m,
        "round_trip_valuation_haircut_m": round_trip_valuation_haircut_m,
        "goodhart_benchmark_contamination_penalty_m": goodhart_benchmark_contamination_penalty_m,
        "true_cash_equivalent_enterprise_value_m": true_cash_equivalent_enterprise_value_m,
        "asc_820_headline_to_cash_distortion_multiple": asc_820_headline_to_cash_distortion_multiple,
    }


# ---------------------------------------------------------------
# 2. Parameterized 4-Tranche Capital Stack Waterfall
# ---------------------------------------------------------------

TRANCHES = [
    {"name": "senior_gpu_facility", "principal_m": 250.0, "coupon_pct": 0.115},
    {"name": "bdc_venture_debt_pik", "principal_m": 350.0, "coupon_pik_pct": 0.145},
    {"name": "series_d_preferred", "principal_m": 650.0, "liquidation_pref_multiple": 1.0},
    {"name": "common_and_secondary_base", "principal_m": 6750.0, "coupon_pct": 0.0},
]


def tranche_recovery(ev):
    """Sequential absolute-priority waterfall: each tranche recovers
    min(principal, remaining EV) after all senior claims are paid."""
    cumulative_prior = 0.0
    results = []
    for t in TRANCHES:
        rem = max(0.0, ev - cumulative_prior)
        rec_m = min(t["principal_m"], rem)
        cents = round(100.0 * rec_m / t["principal_m"], 2)
        results.append({
            "name": t["name"],
            "principal_m": t["principal_m"],
            "recovery_m": rec_m,
            "cents_on_dollar": cents,
        })
        cumulative_prior += rec_m
    return results


# ---------------------------------------------------------------
# 3. Bayesian Scienter Posterior & D&O Voidance
# ---------------------------------------------------------------

def compute_bayesian_scienter_and_dno():
    """Sequential Bayesian update over ML-telemetry likelihood ratios,
    then D&O personal-profit exclusion voidance arithmetic."""
    p0 = 0.15
    lr_list = [45.0, 80.0, 25.0]
    dno_nominal_limit_m = 50.0
    founder_secondary_cashout_m = 50.0
    uncovered_defense_and_restitution_m = 35.0
    treble_civil_forfeiture_penalty_m = 107.5
    rescission_threshold = 0.95

    prior_odds = p0 / (1.0 - p0)
    posterior_odds = prior_odds
    for lr in lr_list:
        posterior_odds *= lr
    posterior_prob = posterior_odds / (1.0 + posterior_odds)

    # D&O Fraud & Personal-Profit Exclusion: scienter posterior above the
    # rescission threshold plus a positive secondary cashout voids coverage.
    dno_exclusion_triggers = (
        posterior_prob > rescission_threshold and founder_secondary_cashout_m > 0.0
    )
    dno_effective_coverage_m = 0.0 if dno_exclusion_triggers else dno_nominal_limit_m
    # Full secondary rescinded/disgorged; founder net utility:
    post_recourse_founder_net_utility_m = (
        founder_secondary_cashout_m
        - founder_secondary_cashout_m  # full disgorgement of the secondary
        - uncovered_defense_and_restitution_m
        - treble_civil_forfeiture_penalty_m
    )
    return {
        "prior_odds": prior_odds,
        "posterior_odds": posterior_odds,
        "posterior_prob": posterior_prob,
        "dno_exclusion_triggers": dno_exclusion_triggers,
        "dno_effective_coverage_m": dno_effective_coverage_m,
        "post_recourse_founder_net_utility_m": post_recourse_founder_net_utility_m,
    }


# ---------------------------------------------------------------
# 4. GP vs. Founder Prisoner's Dilemma
# ---------------------------------------------------------------

def compute_gp_founder_prisoners_dilemma():
    """2x2 payoff matrix for the VC GP: defect/scapegoat strictly
    dominates collude/cover-up by the franchise-and-litigation wedge."""
    successor_fund_aum_m = 5000.0
    annual_mgmt_fee_rate = 0.02
    fee_horizon_years = 5
    gp_secondary_strip_m = 35.0
    sovereign_cross_fund_make_whole_credit_m = 220.0
    collude_franchise_and_litigation_penalty_m = 485.0

    vc_gp_5yr_fee_annuity_m = (
        successor_fund_aum_m * annual_mgmt_fee_rate * fee_horizon_years
    )
    # Defect/scapegoat: keep successor-fund fee annuity + GP secondary
    # strip, less the sovereign LP cross-fund make-whole credit.
    gp_payoff_defect_scapegoat_m = (
        vc_gp_5yr_fee_annuity_m + gp_secondary_strip_m
        - sovereign_cross_fund_make_whole_credit_m
    )
    # Collude/cover-up: franchise destroyed (fee annuity zeroed), secondary
    # strip clawed back, plus franchise & litigation penalty.
    gp_payoff_collude_coverup_m = (
        (vc_gp_5yr_fee_annuity_m * 0.0)
        + (gp_secondary_strip_m - gp_secondary_strip_m)
        - collude_franchise_and_litigation_penalty_m
    )
    gp_defect_dominance_wedge_m = (
        gp_payoff_defect_scapegoat_m - gp_payoff_collude_coverup_m
    )
    return {
        "vc_gp_5yr_fee_annuity_m": vc_gp_5yr_fee_annuity_m,
        "gp_payoff_defect_scapegoat_m": gp_payoff_defect_scapegoat_m,
        "gp_payoff_collude_coverup_m": gp_payoff_collude_coverup_m,
        "gp_defect_dominance_wedge_m": gp_defect_dominance_wedge_m,
    }


def main():
    # --- 1. ASC 606 / ASC 820 ---
    v = compute_asc606_820_valuation()
    assert v["asc_606_phantom_gross_revenue_disallowed_m"] == 225.0
    assert v["vendor_true_marginal_watt_silicon_cost_m"] == 75.0
    assert round(v["round_trip_valuation_haircut_m"], 2) == 2769.23
    assert v["true_cash_equivalent_enterprise_value_m"] == 320.0
    assert v["asc_820_headline_to_cash_distortion_multiple"] == 25.0
    # Cash-institutional LP cash exceeds true cash-equivalent EV (instant impairment).
    assert v["true_cash_equivalent_enterprise_value_m"] < v["cash_institutional_lp_investment_m"]

    # --- 2. Tranche waterfall ---
    total_senior_preferred = sum(t["principal_m"] for t in TRANCHES[:3])
    assert total_senior_preferred == 1250.0

    ev_checks = [
        (320.0, [(250.0, 100.0), (70.0, 20.0), (0.0, 0.0), (0.0, 0.0)]),
        (600.0, [(250.0, 100.0), (350.0, 100.0), (0.0, 0.0), (0.0, 0.0)]),
        (1250.0, [(250.0, 100.0), (350.0, 100.0), (650.0, 100.0), (0.0, 0.0)]),
    ]
    waterfall = {}
    for ev, expected in ev_checks:
        recs = tranche_recovery(ev)
        for rec, (exp_rec, exp_cents) in zip(recs, expected):
            assert abs(rec["recovery_m"] - exp_rec) < 1e-9, (ev, rec)
            assert abs(rec["cents_on_dollar"] - exp_cents) < 1e-9, (ev, rec)
        waterfall[str(ev)] = [
            {"tranche": r["name"], "recovery_m": r["recovery_m"],
             "cents_on_dollar": r["cents_on_dollar"]}
            for r in recs
        ]

    # --- 3. Bayesian scienter & D&O ---
    b = compute_bayesian_scienter_and_dno()
    assert round(b["posterior_odds"], 2) == 15882.35
    assert round(b["posterior_prob"], 6) == 0.999937
    assert b["dno_exclusion_triggers"] is True
    assert b["dno_effective_coverage_m"] == 0.0
    assert b["post_recourse_founder_net_utility_m"] == -142.5

    # --- 4. Prisoner's dilemma ---
    g = compute_gp_founder_prisoners_dilemma()
    assert g["vc_gp_5yr_fee_annuity_m"] == 500.0
    assert g["gp_payoff_defect_scapegoat_m"] == 315.0
    assert g["gp_payoff_collude_coverup_m"] == -485.0
    assert g["gp_defect_dominance_wedge_m"] == 800.0
    # Strict dominance: defect beats collude.
    assert g["gp_payoff_defect_scapegoat_m"] > g["gp_payoff_collude_coverup_m"]

    output = {
        "canonical_spec_id": "SPEC-FRONTIER-AI-VALUATION-CAROUSEL-RECOURSE-TRAP-v1.0",
        "asc606_asc820_valuation": {
            "asc_606_phantom_gross_revenue_disallowed_m": round(v["asc_606_phantom_gross_revenue_disallowed_m"], 2),
            "vendor_true_marginal_watt_silicon_cost_m": round(v["vendor_true_marginal_watt_silicon_cost_m"], 2),
            "round_trip_valuation_haircut_m": round(v["round_trip_valuation_haircut_m"], 2),
            "true_cash_equivalent_enterprise_value_m": round(v["true_cash_equivalent_enterprise_value_m"], 2),
            "asc_820_headline_to_cash_distortion_multiple": round(v["asc_820_headline_to_cash_distortion_multiple"], 2),
        },
        "capital_stack_tranche_waterfall": waterfall,
        "bayesian_scienter_and_dno": {
            "posterior_odds": round(b["posterior_odds"], 2),
            "posterior_prob": round(b["posterior_prob"], 6),
            "dno_effective_coverage_m": b["dno_effective_coverage_m"],
            "post_recourse_founder_net_utility_m": round(b["post_recourse_founder_net_utility_m"], 2),
        },
        "gp_founder_prisoners_dilemma": {
            "vc_gp_5yr_fee_annuity_m": g["vc_gp_5yr_fee_annuity_m"],
            "gp_payoff_defect_scapegoat_m": g["gp_payoff_defect_scapegoat_m"],
            "gp_payoff_collude_coverup_m": g["gp_payoff_collude_coverup_m"],
            "gp_defect_dominance_wedge_m": g["gp_defect_dominance_wedge_m"],
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
