#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPEC-ZERO-UTILITY-ADJUDICATOR-v1.0 — machine-verifiable closed-form proof.

H0 (baseline): a human adjudicator with a wealth-dependent utility U_H(W, T, S)
is integrity-equivalent to a zero-utility machine adjudicator.
H1 (mechanism): the human's utility gradient in personal wealth is strictly
positive, inducing a finite Stigler-Olson capture threshold, while the
machine's null utility has an identically zero Jacobian (infinite threshold).

Falsification surface:
  (1) compute_human_capture_threshold — closed-form capture threshold ($4.0M)
      against a $10B sponsor balance sheet (capture ratio 2500x).
  (2) verify_machine_null_utility_orthogonality — ||J_U_M|| = 0, W* = +inf.
  (3) verify_constitutional_benchmarks — Caperton 556 U.S. 868; Tumey 273 U.S. 510.
  (4) tranche_recovery(ev, regime) — deterministic waterfall over the $1.5B
      claim stack under 'captured_human' (Regime A) vs 'zero_utility_machine'
      (Regime B), swept across EV in [$0, $1.6B].

Pure Python 3 stdlib only. Exit code 0 iff every assertion holds.
"""

import json
import math
import sys
from dataclasses import dataclass, asdict
from typing import Dict

# ---------------------------------------------------------------------------
# Locked constants (SPEC-ZERO-UTILITY-ADJUDICATOR-v1.0)
# ---------------------------------------------------------------------------
W_B = 10_000_000_000.0  # sponsor balance-sheet wealth ($10B)
STACK: Dict[str, float] = {
    "senior_1l": 850_000_000.0,
    "second_lien_2l": 350_000_000.0,
    "unsecured_tort": 300_000_000.0,
    "sponsor_escrow": 250_000_000.0,
    "reinsurance_treaty": 400_000_000.0,
}
TOTAL_FACE = STACK["senior_1l"] + STACK["second_lien_2l"] + STACK["unsecured_tort"]
PRIMING_STRIP = 450_000_000.0
PRIMING_TAKE = 330_000_000.0
FEE_EXTRACTION = 120_000_000.0
REINSURANCE_SETTLEMENT_PCT = 0.15
EV_BENCHMARK = 750_000_000.0


# ---------------------------------------------------------------------------
# (1) Stigler-Olson capture threshold (human adjudicator)
# ---------------------------------------------------------------------------
def compute_human_capture_threshold(
    gov_salary: float = 225_000.0,
    public_reward: float = 0.0,
    scandal_prob: float = 0.02,
    rep_loss: float = 500_000.0,
    rev_prob: float = 0.40,
    rev_alpha: float = 0.0025,
    retal_alpha: float = 0.0015,
) -> Dict[str, float]:
    """Closed-form capture threshold of the human adjudicator:

        expected_scandal_cost   = scandal_prob * rep_loss
        effective_capture_slope = rev_prob * rev_alpha + retal_alpha
        threshold               = (public_reward + expected_scandal_cost) / slope

    The slope is the marginal utility of capture channels (revenue diversion
    plus retaliation avoidance); the threshold is the personal wealth level at
    which the induced capture payoff equals the expected scandal cost.
    """
    expected_scandal_cost = scandal_prob * rep_loss
    effective_capture_slope = rev_prob * rev_alpha + retal_alpha
    threshold = (public_reward + expected_scandal_cost) / effective_capture_slope
    induced_capture_payoff = effective_capture_slope * W_B
    return {
        "gov_salary_usd": gov_salary,
        "expected_scandal_cost_usd": expected_scandal_cost,
        "effective_capture_slope": effective_capture_slope,
        "human_capture_threshold_wealth_usd": threshold,
        "induced_capture_payoff_usd": induced_capture_payoff,
        "capture_ratio": induced_capture_payoff / expected_scandal_cost,
    }


# ---------------------------------------------------------------------------
# (2) Machine null-utility orthogonality
# ---------------------------------------------------------------------------
def machine_utility(w: float, t: float, s: float) -> float:
    """U_M(W, T, S) = 0 identically: the machine holds no wealth, tenure, or
    status term in its objective, so its gradient is null in every argument."""
    return 0.0


def verify_machine_null_utility_orthogonality() -> Dict[str, object]:
    """Analytically J_U_M = [0, 0, 0]; numerically confirmed via central
    finite differences at three sample points. A null slope makes the capture
    threshold W* = (public_reward + expected_scandal_cost) / slope = +inf."""
    h = 1.0
    samples = [(0.0, 0.0, 0.0), (4_000_000.0, 1.0, 1.0), (W_B, 20.0, 5.0)]
    worst_norm = 0.0
    for w, t, s in samples:
        du_dw = (machine_utility(w + h, t, s) - machine_utility(w - h, t, s)) / (2.0 * h)
        du_dt = (machine_utility(w, t + h, s) - machine_utility(w, t - h, s)) / (2.0 * h)
        du_ds = (machine_utility(w, t, s + h) - machine_utility(w, t, s - h)) / (2.0 * h)
        norm = math.sqrt(du_dw ** 2 + du_dt ** 2 + du_ds ** 2)
        worst_norm = max(worst_norm, norm)
    slope = worst_norm
    w_capture_star = math.inf if slope <= 0.0 else 1.0 / slope
    return {
        "jacobian_U_M": [0.0, 0.0, 0.0],
        "jacobian_norm": worst_norm,
        "W_capture_star": w_capture_star,
    }


# ---------------------------------------------------------------------------
# (3) Constitutional due-process benchmarks
# ---------------------------------------------------------------------------
def verify_constitutional_benchmarks() -> Dict[str, object]:
    """Caperton: $3M campaign spend against a $50M verdict at risk (probability
    bias floor). Tumey: the mayor's per-conviction fee (> 0) is the minimal
    adjudicator payoff gradient that violates due process."""
    campaign_spend = 3_000_000.0
    verdict_at_risk = 50_000_000.0
    spend_to_verdict_pct = 100.0 * campaign_spend / verdict_at_risk
    mayor_conviction_fee_usd = 12.0
    return {
        "caperton": {
            "campaign_spend_usd": campaign_spend,
            "verdict_at_risk_usd": verdict_at_risk,
            "spend_to_verdict_pct": spend_to_verdict_pct,
            "citation": "Caperton v. A.T. Massey Coal Co., 556 U.S. 868 (2009)",
        },
        "tumey": {
            "mayor_conviction_fee_usd": mayor_conviction_fee_usd,
            "citation": "Tumey v. Ohio, 273 U.S. 510 (1927)",
        },
    }


# ---------------------------------------------------------------------------
# (4) Deterministic tranche waterfall
# ---------------------------------------------------------------------------
def tranche_recovery(ev: float, regime: str) -> Dict[str, object]:
    """Parameterized waterfall over the $1.5B claim stack.

    Regime A ('captured_human'): the sponsor strips $450M collateral into a
    priming super-priority facility ($330M taken off the top) and extracts
    $120M in un-clawed-back fees/dividends; the escrow is captured back ($0)
    and the reinsurance treaty settles at 15% after bad-faith delay.

    Regime B ('zero_utility_machine'): priming strip and fee extraction are
    blocked; escrow and reinsurance are slashed into the claimant pool at t=0.
    """
    if regime not in ("captured_human", "zero_utility_machine"):
        raise ValueError("regime must be 'captured_human' or 'zero_utility_machine'")
    escrow = STACK["sponsor_escrow"]
    reinsurance = STACK["reinsurance_treaty"]
    full_entitlement = ev + escrow + reinsurance
    if regime == "captured_human":
        operating_ev = max(0.0, ev - FEE_EXTRACTION)
        escrow_available = 0.0
        reinsurance_recovery = REINSURANCE_SETTLEMENT_PCT * reinsurance
        total_pool = operating_ev + escrow_available + reinsurance_recovery
        priming_take = min(PRIMING_TAKE, total_pool)
        sponsor_net = FEE_EXTRACTION
        capture_leakage = max(0.0, full_entitlement - total_pool)
    else:
        total_pool = full_entitlement
        priming_take = 0.0
        sponsor_net = -escrow
        capture_leakage = 0.0
    claimant_pool = total_pool - priming_take
    senior = min(STACK["senior_1l"], claimant_pool)
    second = min(STACK["second_lien_2l"], claimant_pool - senior)
    tort = min(STACK["unsecured_tort"], claimant_pool - senior - second)
    leakage_pct = (100.0 * capture_leakage / full_entitlement) if full_entitlement > 0.0 else 0.0
    return {
        "regime": regime,
        "ev_usd": ev,
        "total_pool_usd": total_pool,
        "priming_take_usd": priming_take,
        "legitimate_claimant_pool_usd": claimant_pool,
        "senior_1l_usd": senior,
        "senior_1l_cents": 100.0 * senior / STACK["senior_1l"],
        "second_lien_usd": second,
        "second_lien_cents": 100.0 * second / STACK["second_lien_2l"],
        "unsecured_tort_usd": tort,
        "unsecured_tort_cents": 100.0 * tort / STACK["unsecured_tort"],
        "claimant_total_usd": senior + second + tort,
        "sponsor_net_walkaway_usd": sponsor_net,
        "capture_leakage_usd": capture_leakage,
        "capture_leakage_pct": leakage_pct,
    }


@dataclass
class SweepRow:
    ev_usd: float
    regime_a_claimant_total_usd: float
    regime_b_claimant_total_usd: float


# ---------------------------------------------------------------------------
# Main: assertions on every locked constant and output
# ---------------------------------------------------------------------------
def main() -> int:
    results: Dict[str, object] = {}

    # (1) Stigler-Olson capture threshold
    cap = compute_human_capture_threshold()
    assert abs(cap["expected_scandal_cost_usd"] - 10_000.0) < 1e-9
    assert abs(cap["effective_capture_slope"] - 0.0025) < 1e-12
    assert abs(cap["human_capture_threshold_wealth_usd"] - 4_000_000.0) < 1e-6
    assert abs(cap["induced_capture_payoff_usd"] - 25_000_000.0) < 1e-6
    assert abs(cap["capture_ratio"] - 2_500.0) < 1e-6
    results["capture_threshold"] = cap

    # (2) Machine null-utility orthogonality
    ortho = verify_machine_null_utility_orthogonality()
    assert ortho["jacobian_norm"] == 0.0
    assert ortho["W_capture_star"] == math.inf
    results["machine_orthogonality"] = ortho

    # (3) Constitutional benchmarks
    bench = verify_constitutional_benchmarks()
    assert abs(bench["caperton"]["spend_to_verdict_pct"] - 6.0) < 1e-9
    assert bench["tumey"]["mayor_conviction_fee_usd"] > 0.0
    results["constitutional_benchmarks"] = bench

    # (4) Waterfall at the benchmark EV = $750M
    a = tranche_recovery(EV_BENCHMARK, "captured_human")
    b = tranche_recovery(EV_BENCHMARK, "zero_utility_machine")
    # Regime A (captured human)
    assert abs(a["total_pool_usd"] - 690_000_000.0) < 1e-6
    assert abs(a["priming_take_usd"] - 330_000_000.0) < 1e-6
    assert abs(a["legitimate_claimant_pool_usd"] - 360_000_000.0) < 1e-6
    assert abs(a["senior_1l_usd"] - 360_000_000.0) < 1e-6
    assert round(a["senior_1l_cents"], 4) == 42.3529
    assert a["second_lien_usd"] == 0.0 and a["second_lien_cents"] == 0.0
    assert a["unsecured_tort_usd"] == 0.0 and a["unsecured_tort_cents"] == 0.0
    assert abs(a["sponsor_net_walkaway_usd"] - 120_000_000.0) < 1e-6
    assert abs(a["capture_leakage_usd"] - 710_000_000.0) < 1e-6
    assert round(a["capture_leakage_pct"], 4) == 50.7143
    # Regime B (zero-utility machine)
    assert abs(b["total_pool_usd"] - 1_400_000_000.0) < 1e-6
    assert abs(b["senior_1l_usd"] - 850_000_000.0) < 1e-6
    assert round(b["senior_1l_cents"], 4) == 100.0
    assert abs(b["second_lien_usd"] - 350_000_000.0) < 1e-6
    assert round(b["second_lien_cents"], 4) == 100.0
    assert abs(b["unsecured_tort_usd"] - 200_000_000.0) < 1e-6
    assert round(b["unsecured_tort_cents"], 4) == 66.6667
    assert abs(b["sponsor_net_walkaway_usd"] + 250_000_000.0) < 1e-6
    assert b["capture_leakage_usd"] == 0.0
    creditor_delta = b["total_pool_usd"] - a["total_pool_usd"]
    assert abs(creditor_delta - 710_000_000.0) < 1e-6
    results["regime_a_benchmark"] = a
    results["regime_b_benchmark"] = b
    results["creditor_recovery_delta_usd"] = creditor_delta

    # (5) EV sweep $0 -> $1.6B: monotonicity + Regime B dominance
    grid = [100_000_000.0 * i for i in range(17)]
    prev_a, prev_b, sweep = -1.0, -1.0, []
    for ev in grid:
        ra = tranche_recovery(ev, "captured_human")
        rb = tranche_recovery(ev, "zero_utility_machine")
        assert ra["claimant_total_usd"] >= prev_a - 1e-6  # monotone in EV
        assert rb["claimant_total_usd"] >= prev_b - 1e-6  # monotone in EV
        assert rb["claimant_total_usd"] >= ra["claimant_total_usd"] - 1e-6
        prev_a, prev_b = ra["claimant_total_usd"], rb["claimant_total_usd"]
        sweep.append(asdict(SweepRow(ev, ra["claimant_total_usd"], rb["claimant_total_usd"])))
    zero_a = tranche_recovery(0.0, "captured_human")
    zero_b = tranche_recovery(0.0, "zero_utility_machine")
    assert zero_a["legitimate_claimant_pool_usd"] == 0.0
    assert abs(zero_b["total_pool_usd"] - 650_000_000.0) < 1e-6
    top_b = tranche_recovery(1_600_000_000.0, "zero_utility_machine")
    assert top_b["claimant_total_usd"] == TOTAL_FACE
    results["ev_sweep"] = sweep

    print(json.dumps(results, indent=2))
    print("PROOF OK: SPEC-ZERO-UTILITY-ADJUDICATOR-v1.0 — all assertions passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
