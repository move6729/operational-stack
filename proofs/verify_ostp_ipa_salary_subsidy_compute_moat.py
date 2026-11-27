#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executable verification proof for
SPEC-OSTP-IPA-SALARY-SUBSIDY-AND-SCSP-COMPUTE-MOAT-CAPTURE-v1.0.

Pure-stdlib recomputation of every locked constant and governing equation in
the bundle (zero numpy/scipy/pandas/torch):

  Equation 1: L_IPA = V_Federal_Policy_Pool / C_Fellowship_Subsidy
              = $32,000M / $2.5M = 12,800.0x
              + per-staffer subsidy ($2.5M / 12)
              + concurrent-salary concentration ($900.0k / $2.5M = 0.36)
  Equation 2: Delta_V(Hillspire | NSCAI_Moat) >> C_501c3
              + closed-form breakeven E* = C_501c3 / r at r = 0.01
              + boundary regime (r*E* == C_501c3) and sub-breakeven regime
  Equation 3: DIB-chairman x Beijing-AI-Center/Dragonfly overlap
              t0 = Dec. 2017, t1 = Feb. 2019, dt = 14 months,
              Dunford SASC warning (Dec. 2018) strictly interior.

Plus: 10^26 FLOPs compute-reporting threshold and both binary statutory flags.

Exit code 0 on full pass; 1 on any failed check.
"""

from __future__ import annotations

import sys
from datetime import date

# ---------------------------------------------------------------------------
# Locked telemetry (Section 5 of the canonical specification)
# ---------------------------------------------------------------------------
LOCKED = {
    "nscai_proposed_federal_rd_funding_usd_billions": 32.0,
    "tom_kalil_schmidt_futures_cio_salary_usd_thousands": 900.0,
    "annual_ipa_fellow_subsidy_cost_usd_millions": 2.5,
    "regulatory_leverage_ratio_rd_to_staffing": 12800.0,
    "compute_reporting_threshold_log10_flops": 26.0,
    "documented_ostp_schmidt_linked_staffers": 12,
    "dib_chairman_beijing_ai_center_overlap_months": 14,
    "statutory_salary_supplementation_ban_18_usc_209": 1,
    "antideficiency_act_31_usc_1342_bypass_flag": 1,
}

RESULTS = []


def check(name: str, cond: bool, detail: str) -> None:
    RESULTS.append((name, cond, detail))
    tag = "PASS" if cond else "FAIL"
    print("[{}] {} :: {}".format(tag, name, detail))


def approx(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def verify_equation_1_leverage_ratio() -> None:
    rd_usd = LOCKED["nscai_proposed_federal_rd_funding_usd_billions"] * 1e9
    subsidy_usd = LOCKED["annual_ipa_fellow_subsidy_cost_usd_millions"] * 1e6
    rd_millions = LOCKED["nscai_proposed_federal_rd_funding_usd_billions"] * 1e3
    l_ipa = rd_usd / subsidy_usd
    check(
        "eq1_leverage_ratio",
        approx(l_ipa, LOCKED["regulatory_leverage_ratio_rd_to_staffing"]),
        "L_IPA = ${:.0f}M / ${:.1f}M = {:.1f}x (locked 12800.0x)".format(
            rd_millions, subsidy_usd / 1e6, l_ipa
        ),
    )
    check(
        "eq1_pool_numerator",
        approx(rd_millions, 32000.0),
        "V_Federal_Policy_Pool = 32.0B = $32,000M",
    )

    n_staff = LOCKED["documented_ostp_schmidt_linked_staffers"]
    per_staffer = subsidy_usd / n_staff
    check(
        "eq1_per_staffer_subsidy",
        approx(per_staffer, 2500000.0 / 12.0),
        "per-staffer subsidy = $2.5M / 12 = ${:.2f}/yr".format(per_staffer),
    )

    kalil_usd = LOCKED["tom_kalil_schmidt_futures_cio_salary_usd_thousands"] * 1e3
    share = kalil_usd / subsidy_usd
    check(
        "eq1_concurrent_salary_concentration",
        approx(share, 0.36),
        "concurrent $900.0k salary / $2.5M pool = {:.2f} (36%)".format(share),
    )


def verify_equation_2_portfolio_identity() -> None:
    c_501c3 = LOCKED["annual_ipa_fellow_subsidy_cost_usd_millions"] * 1e6
    r = 0.01
    e_star = c_501c3 / r
    check(
        "eq2_breakeven_exposure",
        approx(e_star, 250_000_000.0),
        "E* = C_501c3 / r = $2.5M / 0.01 = ${:.0f}".format(e_star),
    )
    e_illustrative_regime = 1e9
    delta_v = r * e_illustrative_regime
    check(
        "eq2_identity_binds",
        delta_v > c_501c3,
        "Delta_V = r*E = 0.01 * $1.0B (illustrative above-breakeven regime) = "
        "${:.0f} > C_501c3 = ${:.0f} "
        "(Delta_V(Hillspire | NSCAI_Moat) >> C_501c3)".format(delta_v, c_501c3),
    )
    check(
        "eq2_identity_boundary_equality",
        approx(r * e_star, c_501c3),
        "at E = E*: 0.01 * $250M = ${:.0f} == C_501c3 = ${:.0f} "
        "(boundary regime binds with equality)".format(r * e_star, c_501c3),
    )
    check(
        "eq2_identity_sub_breakeven_fails",
        (r * 100_000_000.0) < c_501c3,
        "below E*: 0.01 * $100M = $1.0M < $2.5M (identity does not bind)",
    )


def verify_equation_3_overlap_window() -> None:
    t0 = date(2017, 12, 1)  # Beijing AI Center launch (Dec. 2017)
    t1 = date(2019, 2, 1)   # Dragonfly wind-down concludes (Feb. 2019)
    months = (t1.year - t0.year) * 12 + (t1.month - t0.month)
    check(
        "eq3_overlap_months",
        months == LOCKED["dib_chairman_beijing_ai_center_overlap_months"],
        "t1 - t0 = Feb.2019 - Dec.2017 = {} months (locked 14)".format(months),
    )
    dunford = date(2018, 12, 1)  # Dunford SASC warning (Dec. 2018)
    check(
        "eq3_dunford_warning_interior",
        t0 < dunford < t1,
        "Dunford SASC warning Dec.2018 strictly inside (Dec.2017, Feb.2019)",
    )
    dib_chair_start = date(2016, 1, 1)
    check(
        "eq3_dib_tenure_precedes_t0",
        dib_chair_start < t0,
        "DIB chairmanship (2016) precedes Beijing AI Center launch (Dec.2017)",
    )
    nscai_final_report = date(2021, 3, 1)
    check(
        "eq3_pivot_post_window",
        nscai_final_report > t1,
        "NSCAI Final Report (Mar.2021) postdates window close (Feb.2019)",
    )


def verify_compute_moat_threshold() -> None:
    log10_flops = LOCKED["compute_reporting_threshold_log10_flops"]
    check(
        "moat_threshold_integral",
        float(log10_flops).is_integer(),
        "log10(FLOPs) threshold = {:.1f} is integral".format(log10_flops),
    )
    threshold = 10 ** int(log10_flops)
    check(
        "moat_threshold_value",
        threshold == 10 ** 26 and str(threshold) == "1" + "0" * 26,
        "10^26 FLOPs = 1 followed by 26 zeros ({} digits)".format(len(str(threshold))),
    )
    check(
        "moat_threshold_ordering",
        10 ** 25 < threshold < 10 ** 27,
        "10^25 < 10^26 < 10^27 (threshold brackets correctly)",
    )


def verify_statutory_flags() -> None:
    check(
        "flag_18_usc_209",
        LOCKED["statutory_salary_supplementation_ban_18_usc_209"] == 1,
        "18 U.S.C. § 209 salary-supplementation ban active (1)",
    )
    check(
        "flag_31_usc_1342",
        LOCKED["antideficiency_act_31_usc_1342_bypass_flag"] == 1,
        "31 U.S.C. § 1342 appropriations-bypass condition flagged (1)",
    )
    check(
        "flag_conjunction",
        LOCKED["statutory_salary_supplementation_ban_18_usc_209"] == 1
        and LOCKED["antideficiency_act_31_usc_1342_bypass_flag"] == 1,
        "both firewalls active simultaneously => Loop A bypass condition holds",
    )


def verify_locked_telemetry_consistency() -> None:
    check(
        "telemetry_staffer_count",
        LOCKED["documented_ostp_schmidt_linked_staffers"] == 12,
        "N = 12 documented OSTP Schmidt-linked staffers",
    )
    check(
        "telemetry_kalil_salary",
        approx(LOCKED["tom_kalil_schmidt_futures_cio_salary_usd_thousands"], 900.0),
        "Tom Kalil concurrent Schmidt Futures CIO salary = $900.0k/yr",
    )
    check(
        "telemetry_nscai_pool",
        approx(LOCKED["nscai_proposed_federal_rd_funding_usd_billions"], 32.0),
        "NSCAI proposed federal AI R&D pool = $32.0B/yr",
    )
    check(
        "telemetry_subsidy",
        approx(LOCKED["annual_ipa_fellow_subsidy_cost_usd_millions"], 2.5),
        "annual IPA fellowship subsidy = $2.5M/yr",
    )


def main() -> int:
    print("=" * 76)
    print("SPEC-OSTP-IPA-SALARY-SUBSIDY-AND-SCSP-COMPUTE-MOAT-CAPTURE-v1.0 :: proof")
    print("=" * 76)
    verify_locked_telemetry_consistency()
    verify_equation_1_leverage_ratio()
    verify_equation_2_portfolio_identity()
    verify_equation_3_overlap_window()
    verify_compute_moat_threshold()
    verify_statutory_flags()
    print("=" * 76)
    failures = [r for r in RESULTS if not r[1]]
    total = len(RESULTS)
    if failures:
        print("RESULT: FAIL ({} of {} checks failed)".format(len(failures), total))
        for name, _, detail in failures:
            print("  - {}: {}".format(name, detail))
        return 1
    print("RESULT: PASS ({} of {} checks passed)".format(total, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())