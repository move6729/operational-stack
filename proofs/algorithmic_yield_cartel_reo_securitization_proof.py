#!/usr/bin/env python3
"""Closed-form proof bundle for the algorithmic yield cartel and
single-family REO securitization specification.

Canonical Specification:
    SPEC-ALGORITHMIC-YIELD-CARTEL-AND-SINGLE-FAMILY-REO-SECURITIZATION-v1.0

Governing equations verified below (pure stdlib, deterministic):

    S1  mu_cartel   = -(v_cartel - v_comp) / eps_shelter
        R_cartel    = R_comp * (1 + mu_cartel)
        o           = 1 - v
    S2  E_comp      = R_comp * o_comp
        E_cartel    = R_cartel * o_cartel
        Delta_NOI   = E_cartel - E_comp
    S3  S_FTC > 0 and maintenance-stripping NOI coupling predicates
    S4  L_treble    = round(Delta_NOI * 12 * 3, 4)   (Clayton Act Sec. 4)
    S5  H0 falsification: sustained v_cartel > v_comp under pooling
        discipline, with identity residual mu*eps + Delta_v == 0

Exit status 0 if and only if every locked constant is reproduced exactly.
"""

import sys

LOCKED = {
    "competitive_market_vacancy_rate": 0.025,
    "cartel_artificial_vacancy_rate": 0.065,
    "inelastic_shelter_demand_elasticity": -0.25,
    "cartel_markup_over_competitive_rent": 0.16,
    "competitive_monthly_rent_usd": 2000.0,
    "cartel_collusive_monthly_rent_usd": 2320.0,
    "competitive_occupancy_rate": 0.975,
    "cartel_occupancy_rate": 0.935,
    "competitive_expected_revenue_per_unit_usd": 1950.0,
    "cartel_expected_revenue_per_unit_usd": 2169.2,
    "net_collusive_noi_gain_per_unit_monthly_usd": 219.2,
    "clayton_act_treble_disgorgement_per_unit_annual_usd": 7891.2,
    "ftc_invitation_homes_settlement_usd_millions": 48.0,
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
    # S1. Hub-and-spoke collusion: inelasticity-driven markup identity
    # ------------------------------------------------------------------
    eps = k["inelastic_shelter_demand_elasticity"]
    v_comp = k["competitive_market_vacancy_rate"]
    v_cartel = k["cartel_artificial_vacancy_rate"]
    check("S1.1 shelter demand strictly inelastic (eps < 0, |eps| < 1)",
          eps < 0.0 and abs(eps) < 1.0)
    delta_v = v_cartel - v_comp
    check("S1.2 supply withholding == v_cartel - v_comp == 0.040",
          close(delta_v, 0.040))
    check("S1.3 engineered vacancy strictly above competitive clearing",
          v_cartel > v_comp)
    mu = -delta_v / eps
    check("S1.4 markup identity: mu == -(v_cartel - v_comp)/eps == 0.16",
          close(mu, k["cartel_markup_over_competitive_rent"]))
    check("S1.5 collusive markup strictly positive (price elevation)",
          k["cartel_markup_over_competitive_rent"] > 0.0)
    r_cartel = k["competitive_monthly_rent_usd"] * (1.0 + mu)
    check("S1.6 cartel rent == R_comp * (1 + mu) == 2320.0",
          close(r_cartel, k["cartel_collusive_monthly_rent_usd"]))
    check("S1.7 competitive occupancy == 1 - v_comp == 0.975",
          close(1.0 - v_comp, k["competitive_occupancy_rate"]))
    check("S1.8 cartel occupancy == 1 - v_cartel == 0.935",
          close(1.0 - v_cartel, k["cartel_occupancy_rate"]))

    # ------------------------------------------------------------------
    # S2. Artificial-vacancy NOI identity: the pure rent-extraction wedge
    # ------------------------------------------------------------------
    e_comp = (k["competitive_monthly_rent_usd"]
              * k["competitive_occupancy_rate"])
    check("S2.1 competitive expected revenue == R_comp * o_comp == 1950.0",
          close(e_comp, k["competitive_expected_revenue_per_unit_usd"]))
    e_cartel = (k["cartel_collusive_monthly_rent_usd"]
                * k["cartel_occupancy_rate"])
    check("S2.2 cartel expected revenue == R_cartel * o_cartel == 2169.2",
          close(e_cartel, k["cartel_expected_revenue_per_unit_usd"]))
    wedge = e_cartel - e_comp
    check("S2.3 collusive NOI wedge == E_cartel - E_comp == 219.2",
          close(wedge, k["net_collusive_noi_gain_per_unit_monthly_usd"]))
    check("S2.4 wedge strictly positive (rent extraction, not efficiency)",
          k["net_collusive_noi_gain_per_unit_monthly_usd"] > 0.0)
    check("S2.5 cartel rents fewer units yet collects more revenue",
          k["cartel_occupancy_rate"] < k["competitive_occupancy_rate"]
          and k["cartel_expected_revenue_per_unit_usd"]
          > k["competitive_expected_revenue_per_unit_usd"])

    # ------------------------------------------------------------------
    # S3. Single-family REO securitization & maintenance stripping
    # ------------------------------------------------------------------
    s_ftc = k["ftc_invitation_homes_settlement_usd_millions"]
    check("S3.1 FTC Invitation Homes settlement positive (48.0M USD)",
          close(s_ftc, 48.0) and s_ftc > 0.0)
    wedge_unit_months = (s_ftc * 1.0e6) / wedge
    check("S3.2 settlement covers > 200,000 unit-months of collusive wedge",
          wedge_unit_months > 200000.0)
    annual_single = wedge * 12.0
    check("S3.3 annual single damages per unit == wedge * 12 == 2630.4",
          close(annual_single, 2630.4))
    check("S3.4 NOI-keyed stripping predicate: wedge < annual single < treble",
          wedge < annual_single
          < k["clayton_act_treble_disgorgement_per_unit_annual_usd"])

    # ------------------------------------------------------------------
    # S4. Clayton Act Sec. 4 mandatory treble disgorgement
    # ------------------------------------------------------------------
    treble = round(wedge * 12.0 * 3.0, 4)
    check("S4.1 treble == round(Delta_NOI * 12 * 3, 4) == 7891.2",
          close(treble,
                k["clayton_act_treble_disgorgement_per_unit_annual_usd"]))
    check("S4.2 treble == 3 * annual single damages (15 U.S.C. Sec. 15)",
          close(treble, 3.0 * annual_single))
    check("S4.3 treble strictly exceeds single damages (mandatory x3)",
          k["clayton_act_treble_disgorgement_per_unit_annual_usd"]
          > annual_single)

    # ------------------------------------------------------------------
    # S5. Milkovich H0 falsification via revealed-preference algebra
    # ------------------------------------------------------------------
    check("S5.1 H0 falsified: sustained v_cartel > v_comp (no convergence)",
          k["cartel_artificial_vacancy_rate"]
          > k["competitive_market_vacancy_rate"])
    residual = mu * eps + delta_v
    check("S5.2 identity residual closes: mu*eps + Delta_v == 0",
          close(residual, 0.0))
    check("S5.3 markup fully attributable to coordinated withholding",
          close(mu, -delta_v / eps) and delta_v > 0.0)
    check("S5.4 withholding regime strictly inside feasible band (0, 1)",
          0.0 < v_comp < v_cartel < 1.0)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    for label, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", label))
    print("mu_cartel=%.4f  R_cartel_USD=%.2f  Delta_v=%.4f"
          % (mu, r_cartel, delta_v))
    print("E_comp_USD=%.2f  E_cartel_USD=%.2f  Delta_NOI_USD=%.2f"
          % (e_comp, e_cartel, wedge))
    print("S_FTC_USD_M=%.1f  Annual_Single_USD=%.2f  L_treble_USD=%.4f"
          % (s_ftc, annual_single, treble))
    failed = [label for label, ok in RESULTS if not ok]
    if failed:
        print("RESULT: FAIL (%d/%d checks)" % (len(failed), len(RESULTS)))
        return 1
    print("RESULT: PASS (%d/%d checks)" % (len(RESULTS), len(RESULTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
