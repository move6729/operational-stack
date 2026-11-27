#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPSTACK Proof: Collateral Floor & Regulatory Cartel — Deterministic Tranche
Recovery Waterfall, Mag-7 Collateral Shock, Ashby Bypass, Landauer Rent.
Pure Python 3 stdlib. Exit code 0 on success.

Bundle: SPEC-COLLATERAL-FLOOR-REGULATORY-CARTEL-v1.0
License: Unlicense (Public Domain)
"""

import json
import math
import sys

# ----------------------------------------------------------------------
# Locked constants
# ----------------------------------------------------------------------
K_B = 1.380649e-23          # Boltzmann constant, J/K
T_AMBIENT = 300.0           # ambient temperature, K
LN2 = math.log(2.0)         # Landauer bit-erasure factor
MAG7_TOTAL_CAP = 17.264e12  # Mag-7 aggregate market cap, USD
POOL_TOTAL = 1000.0         # stylized clearing pool, $B
FED_BACKSTOP_PIVOT = 950.0  # Schelling sovereign backstop pivot, $B

TRANCHES = [
    ("T1_Secured_Repo_UCC_8_511bc", 300.0),
    ("T2_Swap_QFC_11USC560", 150.0),
    ("T3_Household_Entitlements_UCC_8_503", 500.0),
    ("T4_Equity_SubDebt", 50.0),
]


def tranche_recovery(ev: float) -> dict:
    """Deterministic waterfall over the $1,000B stylized clearing pool.

    Absolute priority: T1 -> T2 -> T3 -> T4. Returns exact dollar
    recovery, cent-on-the-dollar recovery, T3 statutory haircut %,
    and the Schelling sovereign backstop B_Fed(ev) = max(0, 950 - ev).
    """
    remaining = ev
    rows = []
    for name, face in TRANCHES:
        pay = min(remaining, face)
        remaining -= pay
        rows.append({
            "tranche": name,
            "face_usd_b": face,
            "recovery_usd_b": round(pay, 6),
            "cents_on_dollar": round(pay / face, 6),
        })
    t3 = rows[2]
    haircut_pct = (1.0 - t3["cents_on_dollar"]) * 100.0
    return {
        "ev_usd_b": ev,
        "waterfall": rows,
        "t3_haircut_pct": round(haircut_pct, 4),
        "fed_backstop_usd_b": b_fed(ev),
        "residual_to_t4_usd_b": round(remaining, 6),
    }


def b_fed(ev: float) -> float:
    """Schelling sovereign backstop: B_Fed(ev) = max(0, 950 - ev)."""
    return max(0.0, FED_BACKSTOP_PIVOT - ev)


def collateral_drawdown(delta: float, w_inc: float = 0.332,
                        v_sp500: float = 52.0) -> dict:
    """Mag-7 collateral drawdown: USD shock, household incidence,
    S&P 500 implied decline."""
    shock = MAG7_TOTAL_CAP * delta
    return {
        "delta_pct": delta * 100.0,
        "drawdown_usd": shock,
        "household_incidence_usd": shock * w_inc,
        "sp500_decline_pct": v_sp500 * delta,
        "w_inc": w_inc,
        "v_sp500": v_sp500,
    }


def ashby_bypass_probability(v_filter: float, v_prompt: float,
                             attempts: int) -> float:
    """Ashby requisite-variety bypass: cumulative probability that at
    least one prompt-side variety vector evades the filter.
    P_bypass = 1 - (v_filter / v_prompt)^attempts  (v_filter < v_prompt).
    """
    if v_prompt <= 0:
        raise ValueError("v_prompt must be positive")
    ratio = min(1.0, v_filter / v_prompt)
    return 1.0 - ratio ** attempts


def landauer_rent_compression(p_api: float, c_elec: float) -> float:
    """Ratio of API price per 1M tokens to the Landauer thermodynamic
    floor cost of the same computation (c_elec in $/kWh; 4096 bits/token).
    """
    c_joule = c_elec / 3.6e6  # $/kWh -> $/J
    bits_per_token = 4096.0
    energy_per_token = K_B * T_AMBIENT * LN2 * bits_per_token  # J
    floor_per_million = 1e6 * energy_per_token * c_joule       # $
    return p_api / floor_per_million


CATALYST_CALENDAR = [
    ("1662-05-19", "Maryland colonial land-charter entitlement precedent"),
    ("1791-02-25", "First Bank of the United States charter (sovereign collateral doctrine)"),
    ("1913-12-23", "Federal Reserve Act enacted (lender-of-last-resort pivot)"),
    ("1933-06-16", "Glass-Steagall Act (banking/securities cartel separation)"),
    ("1971-08-15", "Nixon gold-window closure (fiat collateral pivot)"),
    ("2000-12-21", "Commodity Futures Modernization Act (QFC carve-out)"),
    ("2008-09-15", "Lehman Brothers Ch.11 filing (QFC close-out stress)"),
    ("2014-11-24", "FDIC/QFC stay-rule resolution framework"),
    ("2020-03-23", "Fed unlimited QE / corporate bond backstop"),
    ("2027-01-15", "Projected tri-party repo collateral wall"),
]


def main() -> int:
    failures = []

    def check(label: str, cond: bool) -> None:
        if not cond:
            failures.append(label)

    # (1) Tranche waterfall checkpoints
    r600 = tranche_recovery(600.0)
    r800 = tranche_recovery(800.0)
    r1000 = tranche_recovery(1000.0)

    check("EV600 T3 recovery $150B", abs(r600["waterfall"][2]["recovery_usd_b"] - 150.0) < 1e-9)
    check("EV600 T3 haircut 70%", abs(r600["t3_haircut_pct"] - 70.0) < 1e-6)
    check("EV600 Fed backstop $350B", abs(r600["fed_backstop_usd_b"] - 350.0) < 1e-9)
    check("EV800 T3 recovery $350B", abs(r800["waterfall"][2]["recovery_usd_b"] - 350.0) < 1e-9)
    check("EV800 T3 haircut 30%", abs(r800["t3_haircut_pct"] - 30.0) < 1e-6)
    check("EV800 Fed backstop $150B", abs(r800["fed_backstop_usd_b"] - 150.0) < 1e-9)
    check("EV1000 T4 par", r1000["waterfall"][3]["cents_on_dollar"] == 1.0)
    check("EV1000 zero backstop", r1000["fed_backstop_usd_b"] == 0.0)
    check("Waterfall conservation", abs(sum(r["recovery_usd_b"] for r in r1000["waterfall"]) - POOL_TOTAL) < 1e-9)

    # (2) Mag-7 collateral shocks
    d40 = collateral_drawdown(0.40)
    d50 = collateral_drawdown(0.50)
    d60 = collateral_drawdown(0.60)
    check("40% shock $6.9056T", abs(d40["drawdown_usd"] - 6.9056e12) < 1e6)
    check("50% shock $8.632T", abs(d50["drawdown_usd"] - 8.632e12) < 1e6)
    check("60% shock $10.3584T", abs(d60["drawdown_usd"] - 10.3584e12) < 1e6)

    # (3) Ashby bypass -> 1.0 within <12 hours
    v_filter, v_prompt = 12.0, 4096.0
    attempts_12h = 720  # 1 attempt/minute for 12 hours
    p12 = ashby_bypass_probability(v_filter, v_prompt, attempts_12h)
    check("Ashby bypass -> 1.0", p12 > 0.999999)
    # solve hours to reach 0.999999
    per_attempt = v_filter / v_prompt
    n_needed = math.log(1e-6, per_attempt)
    hours = n_needed / 60.0
    check("Bypass within 12h", hours < 12.0)

    # (4) Landauer rent compression
    compression = landauer_rent_compression(p_api=15.0, c_elec=0.10)
    check("Landauer compression > 1e6", compression > 1e6)

    # (5) Catalyst calendar integrity
    check("Calendar has 10 entries", len(CATALYST_CALENDAR) == 10)
    check("Calendar endpoints", CATALYST_CALENDAR[0][0] == "1662-05-19"
          and CATALYST_CALENDAR[-1][0] == "2027-01-15")
    for iso, _ in CATALYST_CALENDAR:
        y, m, d = (int(x) for x in iso.split("-"))
        check("ISO date valid " + iso, 1 <= m <= 12 and 1 <= d <= 31 and 1600 <= y <= 2100)

    summary = {
        "bundle": "collateral_floor_regulatory_cartel",
        "ev600": {"t3_recovery_usd_b": r600["waterfall"][2]["recovery_usd_b"],
                  "t3_haircut_pct": r600["t3_haircut_pct"],
                  "fed_backstop_usd_b": r600["fed_backstop_usd_b"]},
        "ev800": {"t3_recovery_usd_b": r800["waterfall"][2]["recovery_usd_b"],
                  "t3_haircut_pct": r800["t3_haircut_pct"],
                  "fed_backstop_usd_b": r800["fed_backstop_usd_b"]},
        "mag7_shocks_usd": {"40pct": d40["drawdown_usd"], "50pct": d50["drawdown_usd"],
                            "60pct": d60["drawdown_usd"]},
        "ashby": {"v_filter": v_filter, "v_prompt": v_prompt,
                  "p_bypass_12h": p12, "hours_to_p999999": round(hours, 3)},
        "landauer_rent_compression": compression,
        "catalyst_calendar": CATALYST_CALENDAR,
        "assertions_failed": failures,
        "status": "PASS" if not failures else "FAIL",
    }
    print(json.dumps(summary, indent=2))
    if failures:
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
