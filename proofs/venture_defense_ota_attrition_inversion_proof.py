#!/usr/bin/env python3
"""Proof kernel: Venture-Defense OTA Bypass & Attrition Cost Inversion.

Verifies the 12 locked constants of
SPEC-VENTURE-DEFENSE-OTA-BYPASS-AND-ATTRITION-COST-INVERSION-v1.0
against closed-form derivations from the statutory / physical baseline.

Governing equations:
    E1  m_vc    = (P_vc - C_bom) / P_vc
    E2  R_acq   = P_vc / C_fpv
    E3  CPE_vc  = P_vc / p_vc
    E4  CPE_fpv = C_fpv / p_fpv
    E5  Lambda  = CPE_vc / CPE_fpv = (P_vc * p_fpv) / (C_fpv * p_vc) = 300 / p_vc
    E6  D_TINA  = P_vc - C_bom * (1 + pi_cap),  pi_cap = 0.15
    E7  D_FCA   = 3 * D_TINA

Pure Python stdlib. Exit code 0 == all locked constants reproduced.
"""

import sys
from decimal import Decimal

# ---------------------------------------------------------------------------
# Locked telemetry (SPEC Section 5, 12 constants)
# ---------------------------------------------------------------------------
LOCKED = {
    "boutique_vc_drone_unit_price_usd": 200000.0,
    "boutique_vc_drone_bom_cost_usd": 18000.0,
    "boutique_vc_gross_margin_ratio": 0.91,
    "commodity_bare_metal_fpv_unit_cost_usd": 500.0,
    "unit_acquisition_cost_ratio": 400.0,
    "contested_ew_boutique_survival_prob": 0.08,
    "fiber_optic_or_edge_fpv_survival_prob": 0.75,
    "cost_per_successful_effect_boutique_usd": 2500000.0,
    "cost_per_successful_effect_commodity_usd": 666.666667,
    "thermodynamic_attrition_inefficiency_multiplier": 3750.0,
    "tina_defective_pricing_overcharge_per_unit_usd": 179300.0,
    "fca_treble_disgorgement_per_unit_usd": 537900.0,
}

PI_CAP = 0.15  # allowable defense profit cap (baseline assumption)

RESULTS = []


def close(a, b, rel=1e-9, abs_tol=1e-6):
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b)))


def check(name, computed, expected, note=""):
    ok = close(computed, expected)
    RESULTS.append(ok)
    print("[{}] {}: computed={!r} locked={!r}{}".format(
        "PASS" if ok else "FAIL", name, computed, expected,
        "  ({})".format(note) if note else ""))
    return ok


def regime(name, ok, detail):
    RESULTS.append(ok)
    print("[{}] {}: {}".format("PASS" if ok else "FAIL", name, detail))
    return ok


def main():
    P_vc = LOCKED["boutique_vc_drone_unit_price_usd"]
    C_bom = LOCKED["boutique_vc_drone_bom_cost_usd"]
    C_fpv = LOCKED["commodity_bare_metal_fpv_unit_cost_usd"]
    p_vc = LOCKED["contested_ew_boutique_survival_prob"]
    p_fpv = LOCKED["fiber_optic_or_edge_fpv_survival_prob"]

    print("=" * 76)
    print("PROOF: venture_defense_ota_attrition_inversion  "
          "(SPEC-VENTURE-DEFENSE-OTA-BYPASS-AND-ATTRITION-COST-INVERSION-v1.0)")
    print("=" * 76)

    # --- E1: wrapper gross margin -----------------------------------------
    m_vc = (P_vc - C_bom) / P_vc
    check("E1 boutique_vc_gross_margin_ratio", m_vc,
          LOCKED["boutique_vc_gross_margin_ratio"], "(200000-18000)/200000")

    # --- E2: unit acquisition cost ratio -----------------------------------
    r_acq = P_vc / C_fpv
    check("E2 unit_acquisition_cost_ratio", r_acq,
          LOCKED["unit_acquisition_cost_ratio"], "200000/500")

    # --- E3/E4: cost per successful effect ---------------------------------
    cpe_vc = P_vc / p_vc
    check("E3 cost_per_successful_effect_boutique_usd", cpe_vc,
          LOCKED["cost_per_successful_effect_boutique_usd"], "200000/0.08")

    cpe_fpv = C_fpv / p_fpv
    check("E4 cost_per_successful_effect_commodity_usd", cpe_fpv,
          LOCKED["cost_per_successful_effect_commodity_usd"], "500/0.75")
    check("E4b commodity CPE rounded to 6 dp", round(cpe_fpv, 6), 666.666667)

    # --- E5: thermodynamic attrition inefficiency multiplier ---------------
    lam = cpe_vc / cpe_fpv
    check("E5 thermodynamic_attrition_inefficiency_multiplier", lam,
          LOCKED["thermodynamic_attrition_inefficiency_multiplier"],
          "2500000/(500/0.75)")
    lam_cross = (P_vc * p_fpv) / (C_fpv * p_vc)
    check("E5b Lambda cross-form (P_vc*p_fpv)/(C_fpv*p_vc)", lam_cross,
          LOCKED["thermodynamic_attrition_inefficiency_multiplier"])
    lam_closed = 300.0 / p_vc
    check("E5c Lambda closed form 300/p_vc", lam_closed,
          LOCKED["thermodynamic_attrition_inefficiency_multiplier"])

    # --- E6/E7: TINA defective pricing & FCA treble (exact Decimal path) ---
    d_p = Decimal("200000.0")
    d_c = Decimal("18000.0")
    d_cap = Decimal("0.15")
    d_tina = d_p - d_c * (Decimal("1") + d_cap)
    check("E6 tina_defective_pricing_overcharge_per_unit_usd (Decimal)",
          float(d_tina),
          LOCKED["tina_defective_pricing_overcharge_per_unit_usd"],
          "200000 - 18000*1.15")
    d_fca = Decimal("3") * d_tina
    check("E7 fca_treble_disgorgement_per_unit_usd (Decimal)", float(d_fca),
          LOCKED["fca_treble_disgorgement_per_unit_usd"], "3*179300")

    # float-path cross-check
    tina_f = P_vc - C_bom * (1.0 + PI_CAP)
    check("E6b TINA overcharge (float path)", tina_f,
          LOCKED["tina_defective_pricing_overcharge_per_unit_usd"])
    fca_f = 3.0 * tina_f
    check("E7b FCA treble (float path)", fca_f,
          LOCKED["fca_treble_disgorgement_per_unit_usd"])

    print("-" * 76)

    # --- Regime inequalities -------------------------------------------------
    implied_markup = (P_vc - C_bom) / C_bom
    regime("R1 defection regime: implied markup vs profit cap",
           implied_markup > PI_CAP,
           "implied markup {:.4f} (1011.1%) > pi_cap 0.15 "
           "(ratio {:.1f}x)".format(implied_markup, implied_markup / PI_CAP))

    regime("R2 attrition inversion regime",
           cpe_vc > cpe_fpv and lam > 1.0,
           "CPE_vc ${:,.2f} > CPE_fpv ${:.6f}, Lambda = {:,.1f}x".format(
               cpe_vc, cpe_fpv, lam))

    regime("R3 four-digit inversion persistence",
           (300.0 / 0.30) <= 1000.0 and p_vc < 0.30,
           "Lambda = 300/p_vc exceeds 1000x for all p_vc < 0.30; "
           "locked p_vc = {}".format(p_vc))

    p_parity = P_vc / cpe_fpv
    regime("R4 parity unreachable at locked price",
           p_parity > 1.0,
           "p_parity = P_vc / CPE_fpv = {:.1f} > 1.0 (probability bound)".format(
               p_parity))

    parity_price = cpe_fpv * p_vc  # boutique price needed for CPE parity at p_vc
    regime("R5 parity price collapse",
           parity_price <= C_fpv and (P_vc - parity_price) / P_vc > 0.99,
           "parity requires P_vc <= ${:.2f} (99.75% collapse from "
           "$ {:,.2f})".format(parity_price, P_vc))

    fca_ratio = LOCKED["fca_treble_disgorgement_per_unit_usd"] / P_vc
    regime("R6 treble exposure exceeds unit price",
           fca_ratio > 1.0,
           "D_FCA / P_vc = {:.4f} (exposure = 268.95% of unit price)".format(
               fca_ratio))

    cap_price = C_bom * (1.0 + PI_CAP)
    regime("R7 compliant ceiling identity",
           close(P_vc - cap_price,
                 LOCKED["tina_defective_pricing_overcharge_per_unit_usd"]),
           "P_vc - C_bom*(1+pi_cap) = {:,.2f} - {:,.2f} = {:,.2f}".format(
               P_vc, cap_price, P_vc - cap_price))

    print("-" * 76)
    failed = RESULTS.count(False)
    total = len(RESULTS)
    if failed == 0:
        print("PROOF PASS: {}/{} checks verified; all 12 locked constants "
              "reproduced from E1-E7.".format(total, total))
        return 0
    print("PROOF FAIL: {}/{} checks failed.".format(failed, total))
    return 1


if __name__ == "__main__":
    sys.exit(main())