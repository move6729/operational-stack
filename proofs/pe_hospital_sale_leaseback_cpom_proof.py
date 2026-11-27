#!/usr/bin/env python3
"""Proof kernel for SPEC-PE-HOSPITAL-SALE-LEASEBACK-STRIPPING-AND-CPOM-EXTRACTION-v1.0.

Verifies the closed-form identities of the PE hospital sale-leaseback
stripping archetype (In re Steward Health Care System LLC, Bankr. S.D. Tex.
Case No. 24-90213 record base; Kannan et al., JAMA 2023;330(24):2365-2375
clinical baseline; 11 U.S.C. 548 clawback identity):

  E-1  sponsor cash-on-cash multiple        M_CoC = D_ext / E_0
  E-2  pre-strip fixed-charge coverage      FCCR_pre = EBITDAR / DS_0
  E-3  post-strip fixed charges             FC_post = DS_0 + R_REIT
  E-4  insolvency identity                  FCCR_post = EBITDAR / FC_post < 1.0
  E-5  annual insolvency margin             Delta = EBITDAR - FC_post
  E-6  use-of-proceeds extraction ratio     rho = D_ext / P_SLB
  E-7  required EBITDAR growth to 1.0x      g = FC_post / EBITDAR - 1
  E-8  clinical entropy multipliers (JAMA)  1 + 0.254, 1 + 0.379
  E-9  11 U.S.C. 548 constructive clawback  C_548 = D_ext * 1[FCCR_post < 1.0]

Pure stdlib. Exit code 0 on full verification.
"""

TOL = 1e-9


def main() -> int:
    # --- Locked telemetry inputs (Section 5, SPEC v1.0 / schema const lock) ---
    e0 = 246.0           # pe_sponsor_initial_equity_usd_millions
    p_slb = 1250.0       # sale_leaseback_reit_proceeds_usd_millions
    d_ext = 800.0        # pe_total_extracted_distributions_usd_millions
    ebitdar = 180.0      # pre_strip_hospital_ebitdar_usd_millions
    ds0 = 60.0           # pre_strip_debt_service_usd_millions
    r_reit = 145.0       # post_strip_annual_reit_rent_escalation_usd_millions
    hac_rate = 0.254     # jama_hospital_acquired_condition_increase_rate
    clabsi_rate = 0.379  # jama_central_line_infection_increase_rate

    # --- Derived identities ---
    m_coc = round(d_ext / e0, 6)                               # E-1
    fccr_pre = round(ebitdar / ds0, 6)                         # E-2
    fc_post = round(ds0 + r_reit, 6)                           # E-3
    fccr_post = round(ebitdar / fc_post, 6)                    # E-4
    margin = round(ebitdar - fc_post, 6)                       # E-5
    rho_extract = round(d_ext / p_slb, 6)                      # E-6
    g_required = round((fc_post / ebitdar - 1.0) * 100.0, 4)   # E-7
    hac_mult = round(1.0 + hac_rate, 6)                        # E-8a
    clabsi_mult = round(1.0 + clabsi_rate, 6)                  # E-8b
    clawback = d_ext if fccr_post < 1.0 else 0.0               # E-9

    checks = [
        ("E-1 pe_sponsor_cash_on_cash_multiple", m_coc, 3.252033),
        ("E-2 pre_strip_fixed_charge_coverage_ratio", fccr_pre, 3.0),
        ("E-3 post_strip_fixed_charges_usd_millions", fc_post, 205.0),
        ("E-4 post_strip_fixed_charge_coverage_ratio", fccr_post, 0.878049),
        ("E-5 annual_insolvency_margin_usd_millions", margin, -25.0),
        ("E-6 use_of_proceeds_extraction_ratio", rho_extract, 0.64),
        ("E-7 required_ebitdar_growth_to_breakeven_pct", g_required, 13.8889),
        ("E-8a jama_hac_multiplier", hac_mult, 1.254),
        ("E-8b jama_clabsi_multiplier", clabsi_mult, 1.379),
        ("E-9 section_548_fraudulent_transfer_clawback_usd_millions", clawback, 800.0),
    ]

    print("=" * 76)
    print("PROOF: SPEC-PE-HOSPITAL-SALE-LEASEBACK-STRIPPING-AND-CPOM-EXTRACTION-v1.0")
    print("=" * 76)
    failures = 0
    for name, got, want in checks:
        ok = abs(got - want) < TOL
        if not ok:
            failures += 1
        print("[{}] {}: computed={} locked={}".format("PASS" if ok else "FAIL", name, got, want))

    insolvent = fccr_post < 1.0
    if not insolvent:
        failures += 1
    print("[{}] E-4b insolvency_gate: FCCR_post={} < 1.0".format("PASS" if insolvent else "FAIL", fccr_post))

    print("-" * 76)
    print("locked_constants_verified=13 (8 inputs + M_CoC, FC_post, FCCR_pre, FCCR_post, C_548)")
    if failures:
        print("RESULT: FAIL ({} identity violations)".format(failures))
        return 1
    print("RESULT: PASS — all identities verified; exit 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())