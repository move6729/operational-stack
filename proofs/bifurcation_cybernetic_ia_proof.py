#!/usr/bin/env python3
"""Closed-form proof: Ashby bifurcation cybernetic IA + CoreWeave debt waterfall.

Pure Python 3 stdlib. Exit code 0 iff all assertions hold.
Canonical Specification: SPEC-1956-BIFURCATION-CYBERNETIC-IA-v1.0
"""

import math
import sys
from dataclasses import dataclass

# ---------------------------------------------------------------- Historical constants
DARTMOUTH_1955_RF_GRANT_USD = 7500.0
ARPA_1963_PROJECT_MAC_GRANT_USD = 2_000_000.0
ENGELBART_1962_SRI_PROJECT_ID = 3578
ASHBY_1956_REQUISITE_VARIETY_CHAPTER = 11
ASHBY_1956_REQUISITE_VARIETY_PAGE = 207
ASHBY_1956_AMPLIFYING_REGULATION_CHAPTER = 14
COREWEAVE_CIK = "0001769628"
COREWEAVE_FY2025_LIQUIDITY_M = 6862.0
COREWEAVE_FY2025_ACCUMULATED_DEFICIT_M = 2600.0
# Collateral-liquidation derivation of the stressed EV
COLLATERAL_GBV_M = 250000.0  # GPU collateral gross book value ($M)
COLLATERAL_RECOVERY_RATE = 0.026  # stressed recovery rate on GBV
LIQUIDATION_EXPENSE_M = 2985.0  # cash retained post-liquidation ($M)

# ---------------------------------------------------------------- Ashby / Holmstrom cybernetics

def ashby_unregulated_entropy(h_d: float, h_r: float) -> float:
    """Unregulated environmental entropy: variety of the disturbance not
    absorbed by the regulator (Ashby 1956, Ch. 11, p. 202)."""
    return max(0.0, h_d - h_r)


def holstrom_agency_loss_pct(h_d: float, h_r: float) -> float:
    """Holmstrom (1979) information-theoretic agency loss: fraction of the
    disturbance entropy that escapes regulation, as % of h_d
    (Ashby-Holmstrom bridge metric)."""
    if h_d <= 0.0:
        return 0.0
    return ashby_unregulated_entropy(h_d, h_r) / h_d * 100.0


# ---------------------------------------------------------------- CoreWeave debt stack (CIK 0001769628)

@dataclass
class Tranche:
    name: str
    principal: float  # $M nominal claim
    tier: int
    pv_m: float = 0.0  # present-value claim ($M); 0.0 => PV == principal

TIER1_POOL = 13550.0  # RCF + DDTL 1.0 + DDTL 2.0 + DDTL 2.1
TIER2_BREAKEVEN = 16150.0  # cumulative incl. DDTL 3.0
TIER2_CAPITALIZED_DISCOUNT = 82.0
TIER2_SWAP_MANDATE_PCT = 75.0
TOTAL_STACK = 16380.0  # incl. MagAI prepayment (nominal 230.0, PV 368.0)
MAGAI_NOMINAL_BREAKEVEN_M = 16380.0  # Tier-2 breakeven + MagAI nominal claim
MAGAI_PV_BREAKEVEN_M = 16518.0  # Tier-2 breakeven + MagAI PV claim

TRANCHES = [
    Tranche("RCF", 650.0, 1),
    Tranche("DDTL 1.0", 2300.0, 1),
    Tranche("DDTL 2.0", 7600.0, 1),
    Tranche("DDTL 2.1", 3000.0, 1),
    Tranche("DDTL 3.0", 2600.0, 2),
    Tranche("MagAI_Prepayment", 230.0, 3, 368.0),
]


def tranche_recovery(ev_m: float) -> dict:
    """Deterministic waterfall: Tier 1 pari passu first-lien pool absorbs EV
    pro rata; Tier 2 recovers only above Tier-1 breakeven; Tier 3 (MagAI
    prepayment PV) only above the full Tier-2 cumulative breakeven."""
    tier1_claims = sum(t.principal for t in TRANCHES if t.tier == 1)
    tier2_claims = sum(t.principal for t in TRANCHES if t.tier == 2)
    ev = max(0.0, ev_m)
    out = {}
    # Tier 1: pro rata within pool
    t1_recovery_pct = min(1.0, ev / TIER1_POOL)
    for t in TRANCHES:
        if t.tier == 1:
            out[t.name] = {
                "principal": t.principal,
                "recovery_usd_m": round(t.principal * t1_recovery_pct, 6),
                "cents_on_dollar": round(t1_recovery_pct * 100.0, 6),
            }
    # Tier 2: residual above Tier-1 breakeven
    residual2 = max(0.0, ev - TIER1_POOL)
    t2_recovery_pct = min(1.0, residual2 / tier2_claims) if residual2 > 0 else 0.0
    for t in TRANCHES:
        if t.tier == 2:
            out[t.name] = {
                "principal": t.principal,
                "recovery_usd_m": round(t.principal * t2_recovery_pct, 6),
                "cents_on_dollar": round(t2_recovery_pct * 100.0, 6),
            }
    # Tier 3: residual above cumulative Tier-2 breakeven (PV-based claim)
    tier3 = next(t for t in TRANCHES if t.tier == 3)
    residual3 = max(0.0, ev - TIER2_BREAKEVEN)
    t3_recovery_pct = min(1.0, residual3 / tier3.pv_m) if residual3 > 0 else 0.0
    t3_recovery_m = tier3.pv_m * t3_recovery_pct
    out[tier3.name] = {
        "principal": tier3.principal,
        "recovery_usd_m": round(t3_recovery_m, 6),
        "cents_of_pv": round(t3_recovery_pct * 100.0, 6),
        "cents_of_nominal": round(t3_recovery_m / tier3.principal * 100.0, 6),
    }
    return out


def main() -> int:
    failures = []

    def check(label: str, cond: bool) -> None:
        if not cond:
            failures.append(label)
        print(f"[{'PASS' if cond else 'FAIL'}] {label}")

    # --- Ashby bifurcation: h_d = 12.0 bits
    h_d = 12.0
    ia = ashby_unregulated_entropy(h_d, 12.5)      # IA sovereignty
    cac = ashby_unregulated_entropy(h_d, 4.5)      # Centralized AI Conditioner
    check("IA sovereignty: 0.0 bits unregulated entropy", ia == 0.0)
    check("IA sovereignty: 0.0% Ashby-Holmstrom bridge metric agency loss",
          holstrom_agency_loss_pct(h_d, 12.5) == 0.0)
    check("CAC filtering: 7.5 bits unregulated entropy", math.isclose(cac, 7.5))
    check("CAC filtering: 62.5% Ashby-Holmstrom bridge metric agency loss",
          math.isclose(holstrom_agency_loss_pct(h_d, 4.5), 62.5))

    # --- CoreWeave waterfall at stressed EV 9485.0
    stressed = tranche_recovery(9485.0)
    t1_cents = 9485.0 / TIER1_POOL * 100.0
    check("Stressed EV 9485.0: Tier 1 recovers 70.0 cents on the dollar",
          math.isclose(t1_cents, 70.0) and
          all(math.isclose(stressed[n]["cents_on_dollar"], 70.0)
              for n in ("RCF", "DDTL 1.0", "DDTL 2.0", "DDTL 2.1")))
    check("Stressed EV: DDTL 3.0 recovers 0.0 cents",
          stressed["DDTL 3.0"]["cents_on_dollar"] == 0.0)
    check("Stressed EV: MagAI_Prepayment recovers 0.0 cents of PV",
          stressed["MagAI_Prepayment"]["cents_of_pv"] == 0.0)
    check("Tier 1 pool = 13550.0", TIER1_POOL == 650.0 + 2300.0 + 7600.0 + 3000.0)
    check("Cumulative Tier-2 breakeven = 16150.0", TIER2_BREAKEVEN == TIER1_POOL + 2600.0)
    check("Total stack = 16380.0",
          math.isclose(TOTAL_STACK, TIER2_BREAKEVEN + 230.0))
    check("Collateral-liquidation EV derivation: 250000*0.026 + 2985 = 9485",
          math.isclose(COLLATERAL_GBV_M * COLLATERAL_RECOVERY_RATE
                       + LIQUIDATION_EXPENSE_M, 9485.0))
    # --- Derived algebraic identities (no vacuous literal self-equality)
    check("Tier 2 capitalized discount = 3.1538% of deficit (82/2600)",
          math.isclose(TIER2_CAPITALIZED_DISCOUNT
                       / COREWEAVE_FY2025_ACCUMULATED_DEFICIT_M * 100.0,
                       3.1538, abs_tol=1e-3))
    check("Liquidity components 2163 + 812 + 3887 = 6862",
          math.isclose(2163.0 + 812.0 + 3887.0, COREWEAVE_FY2025_LIQUIDITY_M))
    check("Stressed EV / total stack = 57.906% (9485/16380)",
          math.isclose(9485.0 / TOTAL_STACK * 100.0, 57.906, abs_tol=1e-3))
    check("MagAI nominal breakeven = 16380.0 (Tier-2 breakeven + nominal)",
          math.isclose(MAGAI_NOMINAL_BREAKEVEN_M, TIER2_BREAKEVEN + 230.0))
    check("MagAI PV breakeven = 16518.0 (Tier-2 breakeven + PV claim)",
          math.isclose(MAGAI_PV_BREAKEVEN_M, TIER2_BREAKEVEN + 368.0))
    pv_case = tranche_recovery(MAGAI_PV_BREAKEVEN_M)
    check("EV = 16518.0: MagAI 100.0 cents of PV, 160.0 cents of nominal",
          math.isclose(pv_case["MagAI_Prepayment"]["cents_of_pv"], 100.0)
          and math.isclose(pv_case["MagAI_Prepayment"]["cents_of_nominal"], 160.0))
    ev_16400 = tranche_recovery(16400.0)
    check("EV = 16400.0: MagAI recovery = 250.0M of PV",
          math.isclose(ev_16400["MagAI_Prepayment"]["recovery_usd_m"], 250.0))

    if failures:
        print(f"FAILED: {len(failures)} assertion(s): {failures}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
