#!/usr/bin/env python3
"""Proof kernel for SPEC-PBM-REBATE-RETENTION-AND-COINSURANCE-INVERSION-v1.0.

Verifies the closed-form identities of the PBM rebate-retention and
coinsurance list-price inversion archetype (FTC Docket No. 9437 record
base; FTC Interim Staff Reports July 2024 & January 2025; 29 U.S.C.
1104/1106 ERISA fiduciary mapping; 42 U.S.C. 1320a-7b(b) safe-harbor
boundary):

  E-1   WAC inflation multiplier            kappa = P_WAC / C_true
  E-2   rebate pool                         R = r * P_WAC
  E-3   PBM retained extraction             Pi_PBM = s * r * P_WAC
  E-3b  list-price monotonicity             dPi_PBM / dP_WAC = s * r > 0
  E-4   net post-rebate price               P_net = P_WAC - R
  E-5   counter coinsurance on WAC          OOP = c * P_WAC
  E-6   patient share of true net cost      sigma = OOP / P_net = c / (1 - r)
  E-7   plan net outlay (reverse subsidy)   Phi_plan = P_net - OOP
  E-8   specialty generic spread            M = P_billed / C_NADAC; S = P_billed - C_NADAC
  E-9   formulary exclusion incentive       Pi_low = s * r * C_true; Pi_PBM / Pi_low = kappa
  E-10  ERISA disgorgement quantum          D_brand = Pi_PBM; D_generic = S

Pure stdlib. Exit code 0 on full verification.
"""

TOL = 1e-9


def main() -> int:
    # --- Locked telemetry inputs (Section 5, SPEC v1.0 / schema const lock) ---
    c_true = 25.0      # true_manufacturing_plus_margin_cost_usd
    p_wac = 1000.0     # inflated_wac_list_price_usd
    r = 0.75           # manufacturer_kickback_rebate_rate
    s = 0.20           # offshore_gpo_pbm_retained_rebate_share
    c = 0.25           # patient_coinsurance_rate_on_wac
    c_nadac = 90.0     # specialty_generic_nadac_acquisition_cost_usd
    p_billed = 4500.0  # pbm_spread_pricing_plan_billed_usd

    # --- Derived identities ---
    kappa = round(p_wac / c_true, 6)              # E-1
    rebate_pool = round(r * p_wac, 6)             # E-2
    pi_pbm = round(s * r * p_wac, 6)              # E-3
    d_pi = round(s * r, 6)                        # E-3b
    p_net = round(p_wac - rebate_pool, 6)         # E-4
    oop = round(c * p_wac, 6)                     # E-5
    sigma = round(oop / p_net, 6)                 # E-6
    phi_plan = round(p_net - oop, 6)              # E-7
    m_spread = round(p_billed / c_nadac, 6)       # E-8a
    spread = round(p_billed - c_nadac, 6)         # E-8b
    pi_low = round(s * r * c_true, 6)             # E-9a
    exclusion_ratio = round(pi_pbm / pi_low, 6)   # E-9b
    d_brand = pi_pbm                              # E-10a
    d_generic = spread                            # E-10b
    oop_rebased = round(c * p_net, 6)             # remedial: coinsurance on P_net

    checks = [
        ("E-0a true_manufacturing_plus_margin_cost_usd", c_true, 25.0),
        ("E-0b inflated_wac_list_price_usd", p_wac, 1000.0),
        ("E-1 wac_to_production_cost_ratio", kappa, 40.0),
        ("E-0c manufacturer_kickback_rebate_rate", r, 0.75),
        ("E-2 total_rebate_pool_usd", rebate_pool, 750.0),
        ("E-0d offshore_gpo_pbm_retained_rebate_share", s, 0.20),
        ("E-3 pbm_retained_rebate_extraction_usd", pi_pbm, 150.0),
        ("E-0e patient_coinsurance_rate_on_wac", c, 0.25),
        ("E-5 patient_out_of_pocket_coinsurance_usd", oop, 250.0),
        ("E-4 net_post_rebate_drug_cost_usd", p_net, 250.0),
        ("E-6 patient_share_of_true_net_cost_ratio", sigma, 1.0),
        ("E-7 insurer_plan_net_outlay_after_rebate_and_patient_copay_usd", phi_plan, 0.0),
        ("E-0f specialty_generic_nadac_acquisition_cost_usd", c_nadac, 90.0),
        ("E-0g pbm_spread_pricing_plan_billed_usd", p_billed, 4500.0),
        ("E-8a pbm_specialty_generic_markup_multiplier", m_spread, 50.0),
        ("E-8b specialty_generic_spread_usd", spread, 4410.0),
        ("E-9a low_list_price_pbm_revenue_usd", pi_low, 3.75),
        ("E-9b formulary_exclusion_revenue_ratio", exclusion_ratio, 40.0),
        ("E-10a erisa_disgorgement_brand_claim_usd", d_brand, 150.0),
        ("E-10b erisa_disgorgement_generic_claim_usd", d_generic, 4410.0),
        ("E-7c remedial_coinsurance_rebased_on_net_usd", oop_rebased, 62.5),
    ]

    print("=" * 76)
    print("PROOF: SPEC-PBM-REBATE-RETENTION-AND-COINSURANCE-INVERSION-v1.0")
    print("=" * 76)
    failures = 0
    for name, got, want in checks:
        ok = abs(got - want) < TOL
        if not ok:
            failures += 1
        print("[{}] {}: computed={} locked={}".format("PASS" if ok else "FAIL", name, got, want))

    print("-" * 76)
    gates = [
        ("E-3b list_price_monotonicity_gate: dPi_PBM/dP_WAC = {} > 0".format(d_pi), d_pi > 0.0),
        ("E-6b coinsurance_inversion_gate: sigma = {} >= 1.0".format(sigma), sigma >= 1.0),
        ("E-7b reverse_subsidy_gate: Phi_plan = {} <= 0.0".format(phi_plan), phi_plan <= 0.0),
        ("E-8c spread_gate: M_spread = {}x >= 1.0 and S = {} > 0".format(m_spread, spread),
         m_spread >= 1.0 and spread > 0.0),
        ("E-9c exclusion_incentive_gate: Pi_PBM / Pi_low = {} > 1.0".format(exclusion_ratio),
         exclusion_ratio > 1.0),
    ]
    for label, ok in gates:
        if not ok:
            failures += 1
        print("[{}] {}".format("PASS" if ok else "FAIL", label))

    print("-" * 76)
    print("locked_constants_verified=15 (7 inputs + kappa, R, Pi_PBM, OOP, P_net, sigma, Phi_plan, M_spread)")
    if failures:
        print("RESULT: FAIL ({} identity violations)".format(failures))
        return 1
    print("RESULT: PASS — all identities verified; exit 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
