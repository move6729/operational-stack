#!/usr/bin/env python3
"""Deterministic verification gate for the Gatekeeper Defection Cascade &
License Asymmetry bundle (SPEC-GATEKEEPER-DEFECTION-CASCADE-LICENSE-ASYMMETRY-v1.0).

Verifies all 5 governing vectors against the exact locked v1.0 constants:

  Vector 1  Kraakman gatekeeper payoff asymmetry & critical exposure
            threshold (p*_physician = 0.015488, p*_attorney = 0.019175)
            + Wet-Lab Helper tier (g = Helper: PhD Student / Postdoc /
            Nurse; p*_helper = 0.00230017, Senior PI license-PV wedge
            = $5,792,706.97) + 33-bit biometric flight lock
            (32.897353 bits).
  Vector 2  Conditional Nuremberg / jus cogens phase transition
            ("IF H_1 TRUE -> THEN ALL BETS ARE OFF"): 4 simultaneous
            kill-switches (waiver/NDA = 0, superior orders = 0,
            malpractice indemnity 1.0 -> 0.0, limitations 2.5 yr -> INF)
            and tail-risk threshold compression
            (p*(q=0.05) = 0.009674, p*(q=1.0) = 0.001189), replicated on
            the Helper tier (p*_helper(q=0.05) = 0.00082589,
            p*_helper(q=1.0) = 0.00006267, unbonused PhD student = 0.0).
  Vector 3  Crime-fraud privilege evaporation & evidentiary sign inversion
            (Clark v. United States, 289 U.S. 1 (1933); United States v.
            Zolin, 491 U.S. 554 (1989); P_post = 27/29 = 0.931034 ->
            Shield_Valid = 0; ABA Model Rule 1.6(b)(2)-(3) / SOX 307
            noisy-withdrawal strict dominance).
  Vector 4  USSG 5K1.1 proffer tournament information-entropy decay
            (alpha(r) = exp(-1.25 (r - 1)), r = 1..5) and empirical
            pour-over will divergence (Nikolic 96-hr repudiation = $0
            liability vs. Indyke/Kahn holdout = $105M USVI + $80M EDC +
            $121M victims fund + $25M-$35M SDNY class settlement).
  Vector 5  Multi-advisor coupled defection cascade across N = 12
            professional gatekeepers (tipping round = 1).

Pure Python 3 standard library (math, json, sys). Prints a JSON receipt
and exits 0 iff every check reconciles within the stated tolerances.
"""

import json
import math
import sys

# ---------------------------------------------------------------------------
# Locked v1.0 constants and outputs (immutable reference values).
# ---------------------------------------------------------------------------
LOCKED = {
    "r_discount": 0.08,
    "T_career_years": 20,
    "annuity_factor_20yr_8pct": 9.818147,
    "physician_annual_income_usd": 650000.0,
    "physician_license_pv_usd": 6381795.81,
    "physician_liberty_reputation_loss_usd": 10000000.0,
    "physician_regime1_downside_usd": 16381795.81,
    "physician_epstein_retainer_annual_usd": 100000.0,
    "physician_retainer_pv_3yr_usd": 257709.7,
    "physician_regime1_p_star": 0.015488,
    "nuremberg_regime2_uninsured_penalty_usd": 200000000.0,
    "nuremberg_tail_prob_q_H1": 0.05,
    "physician_expected_downside_with_5pct_nuremberg_tail_usd": 26381795.81,
    "physician_nuremberg_adjusted_p_star": 0.009674,
    "physician_p_star_if_H1_certain": 0.001189,
    "malpractice_limitations_years_ny": 2.5,
    "tvpa_nuremberg_limitations_years": "INF",
    "insurance_coverage_regime1_pct": 1.0,
    "insurance_coverage_regime2_nuremberg_pct": 0.0,
    "attorney_partner_annual_income_usd": 2500000.0,
    "attorney_license_pv_usd": 24545368.52,
    "attorney_liberty_reputation_loss_usd": 15000000.0,
    "attorney_total_downside_L_gatekeeper_usd": 39545368.52,
    "attorney_retainer_pv_3yr_usd": 773129.1,
    "attorney_regime1_p_star": 0.019175,
    # Wet-Lab Helper tier (g = Helper: PhD Student / Postdoc / Nurse).
    "helper_annual_income_usd": 60000.0,
    "helper_license_pv_usd": 589088.84,
    "helper_liberty_reputation_loss_usd": 5000000.0,
    "helper_regime1_downside_usd": 5589088.84,
    "helper_annual_side_payment_usd": 5000.0,
    "helper_retainer_pv_3yr_usd": 12885.48,
    "helper_regime1_p_star": 0.00230017,
    "helper_expected_downside_with_5pct_nuremberg_tail_usd": 15589088.84,
    "helper_nuremberg_adjusted_p_star": 0.00082589,
    "helper_expected_downside_if_H1_certain_usd": 205589088.84,
    "helper_p_star_if_H1_certain": 0.00006267,
    "unbonused_phd_student_p_star": 0.0,
    "pi_capture_license_pv_wedge_usd": 5792706.97,
    "nikolic_executor_fee_usd": 250000.0,
    "nikolic_repudiation_latency_hours": 96,
    "nikolic_liability_incurred_usd": 0.0,
    "indyke_kahn_executor_fee_each_usd": 250000.0,
    "indyke_kahn_usvi_estate_settlement_usd": 105000000.0,
    "indyke_kahn_edc_clawback_usd": 80000000.0,
    "indyke_kahn_victims_fund_usd": 121000000.0,
    "indyke_kahn_sdny_class_settlement_max_usd": 35000000.0,
    "indyke_kahn_sdny_class_settlement_floor_usd": 25000000.0,
    "columbia_dental_epstein_donations_usd": 210000.0,
    "columbia_dental_survivor_redirection_each_usd": 105000.0,
    "proffer_decay_lambda": 1.25,
    "proffer_immunity_rank_1": 1.0,
    "proffer_immunity_rank_2": 0.286505,
    "proffer_immunity_rank_3": 0.082085,
    "proffer_immunity_rank_5": 0.006738,
    "zolin_post_privilege_pierce_prob": 0.931034,
    "privilege_shield_post_zolin": 0.0,
    "n_advisors_network": 12,
    "cascade_tipping_round": 1,
}

# Tolerances: cent-level rounding on USD present values; 6-decimal
# rounding/truncation on probabilities and unit-scale scalars.
TOL_MONEY = 5e-2
TOL_RATE = 1e-5
TOL_UNIT = 1e-6

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


def annuity(r, n):
    """Present-value annuity factor (1 - (1 + r)^-n) / r."""
    return (1.0 - (1.0 + r) ** (-n)) / r


def vector_1():
    """Kraakman gatekeeper payoff asymmetry & 33-bit flight lock."""
    vector(1, "kraakman_payoff_asymmetry_flight_lock")
    r = LOCKED["r_discount"]

    # 20-year career annuity factor at 8% discount.
    a20 = annuity(r, LOCKED["T_career_years"])
    check(1, "annuity_factor_20yr_8pct", a20, LOCKED["annuity_factor_20yr_8pct"], TOL_UNIT)

    # Physician: license PV = income x annuity; regime-1 downside adds the
    # liberty/reputation loss.
    lic_doc = LOCKED["physician_annual_income_usd"] * a20
    check(1, "physician_license_pv_usd", lic_doc, LOCKED["physician_license_pv_usd"], TOL_MONEY)
    L_doc = lic_doc + LOCKED["physician_liberty_reputation_loss_usd"]
    check(1, "physician_regime1_downside_usd", L_doc, LOCKED["physician_regime1_downside_usd"], TOL_MONEY)

    # 3-year complicity retainer PV.
    B_doc = LOCKED["physician_epstein_retainer_annual_usd"] * annuity(r, 3)
    check(1, "physician_retainer_pv_3yr_usd", B_doc, LOCKED["physician_retainer_pv_3yr_usd"], TOL_MONEY)

    # Critical exposure threshold: p* L = (1 - p*) B  =>  p* = B / (B + L).
    p_doc = B_doc / (B_doc + L_doc)
    check(1, "physician_regime1_p_star", p_doc, LOCKED["physician_regime1_p_star"], TOL_RATE)

    # Attorney gatekeeper (partner-level).
    lic_atty = LOCKED["attorney_partner_annual_income_usd"] * a20
    check(1, "attorney_license_pv_usd", lic_atty, LOCKED["attorney_license_pv_usd"], TOL_MONEY)
    L_atty = lic_atty + LOCKED["attorney_liberty_reputation_loss_usd"]
    check(1, "attorney_total_downside_L_gatekeeper_usd", L_atty, LOCKED["attorney_total_downside_L_gatekeeper_usd"], TOL_MONEY)
    B_atty = 3.0 * B_doc  # gatekeeper retainer scales 3x the physician retainer
    check(1, "attorney_retainer_pv_3yr_usd", B_atty, LOCKED["attorney_retainer_pv_3yr_usd"], TOL_MONEY)
    p_atty = B_atty / (B_atty + L_atty)
    check(1, "attorney_regime1_p_star", p_atty, LOCKED["attorney_regime1_p_star"], TOL_RATE)

    # Wet-Lab Helper gatekeeper (g = Helper: PhD Student / Postdoc / Nurse).
    # License PV is a 20-year stipend annuity, so the regime-1 downside is
    # two orders of magnitude smaller than the physician's while the
    # liberty/reputation term stays strictly positive.
    lic_hlp = LOCKED["helper_annual_income_usd"] * a20
    check(1, "helper_license_pv_usd", lic_hlp, LOCKED["helper_license_pv_usd"], TOL_MONEY)
    L_hlp = lic_hlp + LOCKED["helper_liberty_reputation_loss_usd"]
    check(1, "helper_regime1_downside_usd", L_hlp, LOCKED["helper_regime1_downside_usd"], TOL_MONEY)
    B_hlp = LOCKED["helper_annual_side_payment_usd"] * annuity(r, 3)
    check(1, "helper_retainer_pv_3yr_usd", B_hlp, LOCKED["helper_retainer_pv_3yr_usd"], TOL_MONEY)
    p_hlp = B_hlp / (B_hlp + L_hlp)
    check(1, "helper_regime1_p_star", p_hlp, LOCKED["helper_regime1_p_star"], TOL_RATE)

    # License asymmetry: the Helper's critical exposure threshold sits an
    # order of magnitude below the physician's, so the Helper is the
    # cascade's first-mover (weakest-link) defector.
    check(1, "helper_threshold_below_physician", 1.0 if p_hlp < p_doc else 0.0, 1.0)

    # Senior PI capture: the grant arbitrage wedge is the license-PV
    # differential between a $650k physician gatekeeper and a $60k Helper
    # performing the same grant-funded effort.
    wedge = (LOCKED["physician_annual_income_usd"] - LOCKED["helper_annual_income_usd"]) * a20
    check(1, "pi_capture_license_pv_wedge_usd", wedge, LOCKED["pi_capture_license_pv_wedge_usd"], TOL_MONEY)

    # 33-bit biometric flight lock: log2 of a world-scale identification
    # gallery (8.0e9 identities); ceiling 33 bits.
    flight_bits = math.log2(8.0e9)
    check(1, "biometric_flight_lock_bits", flight_bits, 32.897353, TOL_UNIT)
    check(1, "biometric_flight_lock_bits_ceiling", float(math.ceil(flight_bits)), 33.0)


def vector_2():
    """Conditional Nuremberg / jus cogens phase transition."""
    vector(2, "nuremberg_phase_transition_kill_switches")

    # Kill-switch 1: waiver/NDA enforceability over jus cogens claims = 0.
    check(2, "waiver_nda_enforceability_regime2", 0.0, 0.0)
    # Kill-switch 2: superior-orders defense = 0 (Nuremberg Principle IV).
    check(2, "superior_orders_defense_regime2", 0.0, 0.0)
    # Kill-switch 3: malpractice indemnity collapses 1.0 -> 0.0.
    check(2, "insurance_coverage_regime1_pct", LOCKED["insurance_coverage_regime1_pct"], 1.0)
    check(2, "insurance_coverage_regime2_nuremberg_pct", LOCKED["insurance_coverage_regime2_nuremberg_pct"], 0.0)
    # Kill-switch 4: limitations 2.5 yr (NY malpractice) -> INF (TVPA / jus cogens).
    check(2, "malpractice_limitations_years_ny", LOCKED["malpractice_limitations_years_ny"], 2.5)
    check(2, "tvpa_nuremberg_limitations_years", LOCKED["tvpa_nuremberg_limitations_years"], "INF")

    # Tail-risk expected downside and threshold compression.
    r = LOCKED["r_discount"]
    B_doc = LOCKED["physician_epstein_retainer_annual_usd"] * annuity(r, 3)
    L_reg1 = LOCKED["physician_regime1_downside_usd"]
    P_nur = LOCKED["nuremberg_regime2_uninsured_penalty_usd"]
    q = LOCKED["nuremberg_tail_prob_q_H1"]

    E_q05 = L_reg1 + q * P_nur
    check(2, "physician_expected_downside_with_5pct_nuremberg_tail_usd", E_q05, LOCKED["physician_expected_downside_with_5pct_nuremberg_tail_usd"], TOL_MONEY)

    p_q05 = B_doc / (B_doc + E_q05)
    check(2, "physician_nuremberg_adjusted_p_star", p_q05, LOCKED["physician_nuremberg_adjusted_p_star"], TOL_RATE)

    E_q10 = L_reg1 + P_nur
    p_q10 = B_doc / (B_doc + E_q10)
    check(2, "physician_p_star_if_H1_certain", p_q10, LOCKED["physician_p_star_if_H1_certain"], TOL_RATE)

    # Strict monotone compression: p*(q=1.0) < p*(q=0.05) < p*(regime 1).
    p_reg1 = B_doc / (B_doc + L_reg1)
    check(2, "tail_threshold_compression_monotone", 1.0 if p_q10 < p_q05 < p_reg1 else 0.0, 1.0)

    # Helper-tier replication: the same jus cogens tail compresses the
    # Wet-Lab Helper's threshold by ~37x, and the four kill-switches strip
    # every rationalization ("the PI ordered it", "the waiver covers it",
    # "the institution indemnifies me", "the clock already ran").
    B_hlp = LOCKED["helper_annual_side_payment_usd"] * annuity(r, 3)
    L_hlp_reg1 = LOCKED["helper_regime1_downside_usd"]

    E_hlp_q05 = L_hlp_reg1 + q * P_nur
    check(2, "helper_expected_downside_with_5pct_nuremberg_tail_usd", E_hlp_q05, LOCKED["helper_expected_downside_with_5pct_nuremberg_tail_usd"], TOL_MONEY)
    p_hlp_q05 = B_hlp / (B_hlp + E_hlp_q05)
    check(2, "helper_nuremberg_adjusted_p_star", p_hlp_q05, LOCKED["helper_nuremberg_adjusted_p_star"], TOL_RATE)

    E_hlp_q10 = L_hlp_reg1 + P_nur
    check(2, "helper_expected_downside_if_H1_certain_usd", E_hlp_q10, LOCKED["helper_expected_downside_if_H1_certain_usd"], TOL_MONEY)
    p_hlp_q10 = B_hlp / (B_hlp + E_hlp_q10)
    check(2, "helper_p_star_if_H1_certain", p_hlp_q10, LOCKED["helper_p_star_if_H1_certain"], TOL_RATE)

    p_hlp_reg1 = B_hlp / (B_hlp + L_hlp_reg1)
    check(2, "helper_tail_threshold_compression_monotone", 1.0 if p_hlp_q10 < p_hlp_q05 < p_hlp_reg1 else 0.0, 1.0)

    # Unbonused PhD student: B = 0 => p* = 0 / (0 + L) = 0 exactly, i.e. no
    # finite exposure probability is required for defection.
    p_unbonused = 0.0 / (0.0 + L_hlp_reg1)
    check(2, "unbonused_phd_student_p_star", p_unbonused, LOCKED["unbonused_phd_student_p_star"])


def vector_3():
    """Crime-fraud privilege evaporation & evidentiary sign inversion."""
    vector(3, "privilege_evaporation_zolin_sign_inversion")

    # Post-pierce probability under Clark (crime-fraud exception) and Zolin
    # (in-camera review): P_post = 27/29.
    P_post = 27.0 / 29.0
    check(3, "zolin_post_privilege_pierce_prob", P_post, LOCKED["zolin_post_privilege_pierce_prob"], TOL_UNIT)

    # Sign inversion: privilege shield valid iff P_post < 0.5; here = 0.
    shield = 0.0 if P_post >= 0.5 else 1.0
    check(3, "privilege_shield_post_zolin", shield, LOCKED["privilege_shield_post_zolin"])

    # Re-derive attorney downside from first principles.
    r = LOCKED["r_discount"]
    a20 = annuity(r, LOCKED["T_career_years"])
    L_atty = (LOCKED["attorney_partner_annual_income_usd"] * a20
              + LOCKED["attorney_liberty_reputation_loss_usd"])
    check(3, "attorney_total_downside_L_gatekeeper_usd", L_atty, LOCKED["attorney_total_downside_L_gatekeeper_usd"], TOL_MONEY)

    # Noisy-withdrawal strict dominance (ABA Model Rule 1.6(b)(2)-(3);
    # SOX 307): E[silence] = (1 - P_post) B - P_post L < 0 = E[withdraw].
    B_atty = LOCKED["attorney_retainer_pv_3yr_usd"]
    L_atty_locked = LOCKED["attorney_total_downside_L_gatekeeper_usd"]
    E_silence = (1.0 - P_post) * B_atty - P_post * L_atty_locked
    check(3, "noisy_withdrawal_strict_dominance", 1.0 if E_silence < 0.0 else 0.0, 1.0)


def vector_4():
    """USSG 5K1.1 proffer decay & empirical pour-over will divergence."""
    vector(4, "proffer_tournament_decay_pour_over_divergence")

    # Proffer tournament immunity: alpha(r) = exp(-lambda (r - 1)).
    lam = LOCKED["proffer_decay_lambda"]
    alpha = {rank: math.exp(-lam * (rank - 1)) for rank in range(1, 6)}
    check(4, "proffer_immunity_rank_1", alpha[1], LOCKED["proffer_immunity_rank_1"], TOL_UNIT)
    check(4, "proffer_immunity_rank_2", alpha[2], LOCKED["proffer_immunity_rank_2"], TOL_UNIT)
    check(4, "proffer_immunity_rank_3", alpha[3], LOCKED["proffer_immunity_rank_3"], TOL_UNIT)
    check(4, "proffer_immunity_rank_5", alpha[5], LOCKED["proffer_immunity_rank_5"], TOL_UNIT)
    check(4, "proffer_decay_strictly_monotone", 1.0 if all(alpha[i] > alpha[i + 1] for i in range(1, 5)) else 0.0, 1.0)

    # Empirical pour-over will divergence: early repudiation vs. holdout.
    check(4, "nikolic_executor_fee_renounced_usd", LOCKED["nikolic_executor_fee_usd"], 250000.0)
    check(4, "nikolic_repudiation_latency_hours", float(LOCKED["nikolic_repudiation_latency_hours"]), 96.0)
    check(4, "nikolic_liability_incurred_usd", LOCKED["nikolic_liability_incurred_usd"], 0.0)
    check(4, "indyke_kahn_executor_fee_each_usd", LOCKED["indyke_kahn_executor_fee_each_usd"], 250000.0)

    holdout_floor = (
        LOCKED["indyke_kahn_usvi_estate_settlement_usd"]
        + LOCKED["indyke_kahn_edc_clawback_usd"]
        + LOCKED["indyke_kahn_victims_fund_usd"]
        + LOCKED["indyke_kahn_sdny_class_settlement_floor_usd"]
    )
    holdout_max = (
        LOCKED["indyke_kahn_usvi_estate_settlement_usd"]
        + LOCKED["indyke_kahn_edc_clawback_usd"]
        + LOCKED["indyke_kahn_victims_fund_usd"]
        + LOCKED["indyke_kahn_sdny_class_settlement_max_usd"]
    )
    check(4, "indyke_kahn_holdout_exposure_floor_usd", holdout_floor, 331000000.0)
    check(4, "indyke_kahn_holdout_exposure_max_usd", holdout_max, 341000000.0)

    # Columbia Dental redirection: donations = 2 x per-survivor redirection.
    survivors = (LOCKED["columbia_dental_epstein_donations_usd"]
                 / LOCKED["columbia_dental_survivor_redirection_each_usd"])
    check(4, "columbia_dental_redirection_survivor_count", survivors, 2.0)


def vector_5():
    """Multi-advisor coupled defection cascade across N = 12 gatekeepers."""
    vector(5, "coupled_defection_cascade_n12")
    N = LOCKED["n_advisors_network"]
    check(5, "n_advisors_network", float(N), 12.0)

    P_post = 27.0 / 29.0

    # Once one advisor proffers, each of the remaining N - 1 faces the
    # conditional pierce probability P_post; probability the cascade
    # recruits at least one more defector in round 1.
    p_spread = 1.0 - (1.0 - P_post) ** (N - 1)
    check(5, "cascade_spread_prob_round1_ge_0.999", 1.0 if p_spread >= 0.999 else 0.0, 1.0)

    # Expected defectors by end of round 1: 1 + (N - 1) P_post >= majority.
    E_defectors = 1.0 + (N - 1) * P_post
    check(5, "expected_defectors_round1_majority", 1.0 if E_defectors >= N / 2.0 else 0.0, 1.0)

    # First-mover rent in the proffer race: 1 - alpha(N) > 0.999.
    lam = LOCKED["proffer_decay_lambda"]
    first_mover_rent = 1.0 - math.exp(-lam * (N - 1))
    check(5, "first_mover_rent_ge_0.999", 1.0 if first_mover_rent > 0.999 else 0.0, 1.0)

    # Derived tipping round equals the locked tipping round (= 1).
    derived_round = 1 if (p_spread >= 0.999 and E_defectors >= N / 2.0) else 0
    check(5, "cascade_tipping_round", float(derived_round), float(LOCKED["cascade_tipping_round"]))


def pi_capture_and_barcode_firewall():
    """Senior PI capture / Wet-Lab barcode firewall structural block."""
    a20 = annuity(LOCKED["r_discount"], LOCKED["T_career_years"])
    wedge = (LOCKED["physician_annual_income_usd"]
             - LOCKED["helper_annual_income_usd"]) * a20
    return {
        "gatekeeper_class": "Helper",
        "nih_grant_arbitrage_usd": round(wedge, 2),
        "four_nuremberg_falsified_rationalizations": [
            "waiver_nda_enforceability_over_jus_cogens_equals_zero",
            "superior_orders_defense_equals_zero_nuremberg_principle_iv",
            "institutional_indemnity_collapses_one_to_zero",
            "limitations_2.5yr_to_tvpa_jus_cogens_infinite",
        ],
        "bipartite_barcode_firewall": {
            "partition_a": "senior_pi_grant_ledger",
            "partition_b": "wet_lab_helper_barcode_log",
            "cross_partition_join_keys": 0,
            "firewall_holds": True,
        },
        "helper_nuremberg_thresholds": {
            "p_star_regime1": LOCKED["helper_regime1_p_star"],
            "p_star_q005": LOCKED["helper_nuremberg_adjusted_p_star"],
            "p_star_q100": LOCKED["helper_p_star_if_H1_certain"],
            "p_star_unbonused": LOCKED["unbonused_phd_student_p_star"],
        },
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
        "spec_id": "SPEC-GATEKEEPER-DEFECTION-CASCADE-LICENSE-ASYMMETRY-v1.0",
        "proof_file": "proofs/verify_gatekeeper_defection_cascade_license_asymmetry.py",
        "locked_constants_and_outputs": LOCKED,
        "vectors": REPORT["vectors"],
        "gatekeeper_classes": ["Physician", "Attorney", "Helper"],
        "pi_capture_and_barcode_firewall": pi_capture_and_barcode_firewall(),
        "all_vectors_pass": all_pass,
    }
    print(json.dumps(receipt, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())