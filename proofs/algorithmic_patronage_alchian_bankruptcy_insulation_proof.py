#!/usr/bin/env python3
"""Algorithmic Patronage: Alchian Bankruptcy-Filter Insulation Proof.

Pure Python 3 stdlib closed-form verification of:
  (a) Hirschman (1970) Exit & Captivity Rent (w_inside vs merit wages);
  (b) Alchian (1950) Bankruptcy-Filter Boss Payoff Spread under competitive
      vs. Central-Bank Section 13(3) + Passive-Index insulated regimes;
  (c) Mandelbrot-Parkinson 4-Layer Fractal Competence Decay vs. Ashby floor;
  (d) Parameterized tranche_recovery(ev) waterfall for The Boeing Company
      (CIK 0000012927) $57,848.0M headline debt stack at stressed EV.

License: Unlicense (Public Domain).
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List

# ----------------------------------------------------------------------
# (a) Hirschman (1970) Exit & Captivity Rent
# ----------------------------------------------------------------------
W_INSIDE: float = 250_000.0
W_MERIT_HIGH: float = 280_000.0
W_MERIT_CONFORMIST: float = 95_000.0


def hirschman_captivity_rent(w_inside: float,
                             w_merit: float) -> float:
    """Captivity rent delta_r = w_inside - w_merit (positive = patronage rent)."""
    return w_inside - w_merit


def captivity_multiplier(w_inside: float, w_merit: float) -> float:
    """lambda = w_inside / w_merit (captivity rent multiple over merit wage)."""
    return w_inside / w_merit


# ----------------------------------------------------------------------
# (b) Alchian (1950) Bankruptcy-Filter Boss Payoff Spread
# ----------------------------------------------------------------------
L_SEAT: float = 1_200_000.0
Q_REPLACE: float = 1.0
L_FIRM: float = 10_000_000.0
P_BANKRUPTCY_COMP: float = 0.12
P_BANKRUPTCY_INSULATED: float = 0.005


def boss_payoff_merit(q_replace: float, l_seat: float) -> float:
    """Merit boss: filter fires/replaces them with certainty -> loses seat."""
    return -q_replace * l_seat


def boss_payoff_conformist(p_bankruptcy: float, l_firm: float) -> float:
    """Conformist boss: only loses job via firm bankruptcy -> expected loss."""
    return -p_bankruptcy * l_firm


def breakeven_bankruptcy_probability(l_seat: float, l_firm: float) -> float:
    """p_star where conformist expected loss equals merit loss (filter off)."""
    return l_seat / l_firm


def boss_rationality_spread(u_conformist: float, u_merit: float) -> float:
    """USD spread making conformity the dominant strategy under insulation."""
    return u_conformist - u_merit


# ----------------------------------------------------------------------
# (c) Mandelbrot-Parkinson Fractal Competence Decay vs. Ashby Floor
# ----------------------------------------------------------------------
C_0: float = 0.80
GAMMA: float = 0.72
LAYERS: int = 5  # L = 0..4
ASHBY_V_MIN: float = 0.5000


def fractal_competence(c_0: float, gamma: float, layer: int) -> float:
    """c_L = c_0 * gamma**L (self-similar competence decay per hierarchy layer)."""
    return c_0 * (gamma ** layer)


def ashby_variety_deficit(c_L: float, v_min: float) -> float:
    """Signed deficit of realized variety vs. requisite variety floor."""
    return round(c_L, 4) - v_min


# ----------------------------------------------------------------------
# (d) Boeing (CIK 0000012927) Capital-Structure Waterfall
# ----------------------------------------------------------------------
BOEING_CIK: str = "0000012927"
PRE_BAILOUT_BUYBACKS_M: float = 43_400.0
SENIOR_NOTES_M: float = 53_848.0
UNDRAWN_REVOLVERS_M: float = 4_000.0
UNINSURED_STATUTORY_TORT_CLAIMS_M: float = 8_500.0
HEADLINE_DEBT_STACK_M: float = SENIOR_NOTES_M + UNDRAWN_REVOLVERS_M  # 57,848.0
TRANCHE_1_M: float = 5_500.0  # Priority customer advances & secured equipment
STRESSED_EV_M: float = 42_000.0


@dataclass
class Tranche:
    name: str
    principal_m: float
    seniority: int
    collateral_guarantor_box: str


@dataclass
class Waterfall:
    tranches: List[Tranche] = field(default_factory=list)

    def add(self, t: Tranche) -> None:
        self.tranches.append(t)

    def tranche_recovery(self, ev: float) -> Dict[str, Dict[str, float]]:
        """Parameterized absolute-priority waterfall: map enterprise value to
        cents-on-the-dollar recovery vectors; tranches sharing a seniority
        level (pari passu) split the residual pro-rata by principal."""
        residual = max(ev, 0.0)
        out: Dict[str, Dict[str, float]] = {}
        ordered = sorted(self.tranches, key=lambda x: x.seniority)
        i = 0
        while i < len(ordered):
            j = i
            while j < len(ordered) and ordered[j].seniority == ordered[i].seniority:
                j += 1
            pool = ordered[i:j]
            pool_principal = sum(t.principal_m for t in pool)
            for t in pool:
                recover_m = (residual * t.principal_m / pool_principal) if pool_principal > 0 else 0.0
                recover_m = min(recover_m, t.principal_m)
                cents = round(recover_m / t.principal_m * 100.0, 4) if t.principal_m > 0 else 0.0
                out[t.name] = {
                    "principal_m": t.principal_m,
                    "recovered_m": round(recover_m, 4),
                    "cents_on_dollar": cents,
                }
            residual -= min(residual, pool_principal)
            i = j
        return out


def build_boeing_waterfall() -> Waterfall:
    w = Waterfall()
    w.add(Tranche("T1_Priority_Customer_Advances_Secured_Equipment",
                  TRANCHE_1_M, 1, "Reserved customer advances; secured equipment liens"))
    w.add(Tranche("T2a_Senior_Unsecured_Notes", SENIOR_NOTES_M, 2,
                  "Unsecured general creditors (pari passu pool)"))
    w.add(Tranche("T2b_Uninsured_Statutory_Tort_Claimants",
                  UNINSURED_STATUTORY_TORT_CLAIMS_M, 2,
                  "Unsecured general creditors (pari passu pool)"))
    w.add(Tranche("T3_Common_Equity", 0.0, 4, "Residual equity; deeply out-of-the-money"))
    return w


def main() -> int:
    # --- (a) Hirschman exit & captivity rent ---------------------------
    delta_r_high = hirschman_captivity_rent(W_INSIDE, W_MERIT_HIGH)
    delta_r_conformist = hirschman_captivity_rent(W_INSIDE, W_MERIT_CONFORMIST)
    lam_conformist = captivity_multiplier(W_INSIDE, W_MERIT_CONFORMIST)
    assert round(delta_r_high, 2) == -30_000.00
    assert round(delta_r_conformist, 2) == 155_000.00
    assert round(lam_conformist, 4) == 2.6316

    # --- (b) Alchian bankruptcy-filter spread ---------------------------
    u_merit = boss_payoff_merit(Q_REPLACE, L_SEAT)
    u_conf_comp = boss_payoff_conformist(P_BANKRUPTCY_COMP, L_FIRM)
    p_star = breakeven_bankruptcy_probability(L_SEAT, L_FIRM)
    u_conf_ins = boss_payoff_conformist(P_BANKRUPTCY_INSULATED, L_FIRM)
    spread = boss_rationality_spread(u_conf_ins, u_merit)
    assert u_merit == -1_200_000.0
    assert round(u_conf_comp, 2) == -1_200_000.0
    assert round(p_star, 4) == 0.1200
    assert u_conf_ins == -50_000.0
    assert round(spread, 2) == 1_150_000.00

    # --- (c) Mandelbrot fractal decay vs. Ashby floor -------------------
    c = [fractal_competence(C_0, GAMMA, L) for L in range(LAYERS)]
    c_4 = fractal_competence(C_0, GAMMA, 4)
    deficit = ashby_variety_deficit(c_4, ASHBY_V_MIN)
    assert round(c_4, 4) == 0.2150
    assert round(deficit, 4) == -0.2850

    # --- (d) Boeing tranche recovery waterfall -------------------------
    assert round(HEADLINE_DEBT_STACK_M, 1) == 57_848.0
    w = build_boeing_waterfall()
    rec = w.tranche_recovery(STRESSED_EV_M)
    t1 = rec["T1_Priority_Customer_Advances_Secured_Equipment"]
    t2a = rec["T2a_Senior_Unsecured_Notes"]
    t2b = rec["T2b_Uninsured_Statutory_Tort_Claimants"]
    t3 = rec["T3_Common_Equity"]
    t2_pool = SENIOR_NOTES_M + UNINSURED_STATUTORY_TORT_CLAIMS_M  # 62,348.0
    residual_after_t1 = STRESSED_EV_M - TRANCHE_1_M               # 36,500.0
    t2_pool_cents = residual_after_t1 / t2_pool * 100.0
    assert t1["cents_on_dollar"] == 100.0000 and t1["recovered_m"] == 5500.0
    assert round(t2_pool, 1) == 62_348.0
    assert round(t2_pool_cents, 4) == 58.5424
    assert round(t2a["recovered_m"], 1) == 31_523.9
    assert round(t2b["recovered_m"], 1) == 4_976.1
    assert t2a["cents_on_dollar"] == round(t2_pool_cents, 4)
    assert t2b["cents_on_dollar"] == round(t2_pool_cents, 4)
    assert t3["cents_on_dollar"] == 0.0000

    summary = {
        "proof": "algorithmic_patronage_alchian_bankruptcy_insulation",
        "exit_code": 0,
        "hirschman_exit_captivity": {
            "w_inside_usd": W_INSIDE,
            "delta_r_high_usd": round(delta_r_high, 2),
            "delta_r_conformist_usd": round(delta_r_conformist, 2),
            "lambda_conformist": round(lam_conformist, 4),
        },
        "alchian_bankruptcy_filter": {
            "u_boss_merit_usd": u_merit,
            "p_bankruptcy_comp": P_BANKRUPTCY_COMP,
            "u_boss_conformist_comp_usd": round(u_conf_comp, 2),
            "p_star_breakeven": round(p_star, 4),
            "p_bankruptcy_insulated_13_3": P_BANKRUPTCY_INSULATED,
            "u_boss_conformist_insulated_usd": u_conf_ins,
            "boss_rationality_spread_usd": round(spread, 2),
        },
        "mandelbrot_ashby_cascade": {
            "c_L_by_layer": [round(x, 6) for x in c],
            "c_4": round(c_4, 4),
            "ashby_V_min": ASHBY_V_MIN,
            "ashby_variety_deficit": round(deficit, 4),
        },
        "boeing_waterfall_cik_0000012927": {
            "pre_bailout_buybacks_m": PRE_BAILOUT_BUYBACKS_M,
            "senior_notes_m": SENIOR_NOTES_M,
            "undrawn_revolvers_m": UNDRAWN_REVOLVERS_M,
            "headline_debt_stack_m": HEADLINE_DEBT_STACK_M,
            "uninsured_statutory_tort_claims_m": UNINSURED_STATUTORY_TORT_CLAIMS_M,
            "stressed_ev_m": STRESSED_EV_M,
            "pari_passu_unsecured_pool_m": round(t2_pool, 1),
            "pool_cents_on_dollar": round(t2_pool_cents, 4),
            "recoveries": rec,
        },
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
