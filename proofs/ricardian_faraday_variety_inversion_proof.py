#!/usr/bin/env python3
"""
Verification Engine: SPEC-RICARDIAN-FARADAY-VARIETY-INVERSION-v1.0
Pure Python 3 Standard Library — Zero Third-Party Dependencies
License: Unlicense (Public Domain)
"""

import json
import sys
from typing import Dict, List, Union


def compute_ashby_variety_inversion(
    n_nodes: int = 1000,
    rho_mono: float = 0.85,
    rho_bicam: float = 0.05,
) -> Dict[str, float]:
    """
    Computes effective sample size N_eff under intraclass correlation rho
    and the Ashby Requisite Variety amplification ratio (Gamma_Ashby).
    """
    n_eff_mono = n_nodes / (1.0 + (n_nodes - 1) * rho_mono)
    n_eff_bicam = n_nodes / (1.0 + (n_nodes - 1) * rho_bicam)
    gamma_ashby = n_eff_bicam / n_eff_mono

    assert abs(n_eff_mono - 1.1762630124095748) < 1e-6, f"n_eff_mono mismatch: {n_eff_mono}"
    assert abs(n_eff_bicam - 19.62708537782139) < 1e-6, f"n_eff_bicam mismatch: {n_eff_bicam}"
    assert abs(gamma_ashby - 16.685965978102908) < 1e-6, f"gamma_ashby mismatch: {gamma_ashby}"

    return {
        "n_nodes": float(n_nodes),
        "rho_mono": rho_mono,
        "rho_bicam": rho_bicam,
        "n_eff_mono": round(n_eff_mono, 6),
        "n_eff_bicam": round(n_eff_bicam, 6),
        "gamma_ashby": round(gamma_ashby, 6),
    }


def compute_ricardian_ooda_multiplier() -> Dict[str, float]:
    """
    Computes quadratic O(K^2) context re-billing under a 10-turn monolith chat loop
    versus a compartmentalized Ricardian OODA swarm cycle.
    """
    cum_in_tokens = sum(8000 + 25000 * k for k in range(1, 11))
    cum_out_tokens = 10 * 2000

    c_mono_std = (cum_in_tokens / 1e6) * 2.00 + (cum_out_tokens / 1e6) * 10.00
    c_mono_high = (cum_in_tokens / 1e6) * 4.00 + (cum_out_tokens / 1e6) * 20.00

    c_scout = (250000 / 1e6) * 0.022 + (3000 / 1e6) * 0.40
    c_gov = (8000 / 1e6) * 0.10 + (3000 / 1e6) * 2.00 + (600 / 1e6) * 10.00
    c_hands = (10000 / 1e6) * 0.0699 + (3000 / 1e6) * 1.40
    c_swarm_std = c_scout + c_gov + c_hands

    c_swarm_micro = (
        (100000 / 1e6) * 0.022
        + (1500 / 1e6) * 0.40
        + (8000 / 1e6) * 0.10
        + (10000 / 1e6) * 0.048
        + (1500 / 1e6) * 1.40
    )

    ooda_mult_std = c_mono_std / c_swarm_std
    ooda_mult_peak = c_mono_high / c_swarm_micro

    assert cum_in_tokens == 1455000, f"cum_in_tokens mismatch: {cum_in_tokens}"
    assert abs(c_mono_std - 3.110000) < 1e-6, f"c_mono_std mismatch: {c_mono_std}"
    assert abs(c_mono_high - 6.220000) < 1e-6, f"c_mono_high mismatch: {c_mono_high}"
    assert abs(c_scout - 0.006700) < 1e-6, f"c_scout mismatch: {c_scout}"
    assert abs(c_gov - 0.012800) < 1e-6, f"c_gov mismatch: {c_gov}"
    assert abs(c_hands - 0.004899) < 1e-6, f"c_hands mismatch: {c_hands}"
    assert abs(c_swarm_std - 0.024399) < 1e-6, f"c_swarm_std mismatch: {c_swarm_std}"
    assert abs(c_swarm_micro - 0.006180) < 1e-6, f"c_swarm_micro mismatch: {c_swarm_micro}"
    assert abs(ooda_mult_std - 127.46424033771876) < 1e-6, f"ooda_mult_std mismatch: {ooda_mult_std}"
    assert abs(ooda_mult_peak - 1006.4724919093851) < 1e-6, f"ooda_mult_peak mismatch: {ooda_mult_peak}"

    return {
        "cum_in_tokens": float(cum_in_tokens),
        "c_mono_std_usd": round(c_mono_std, 6),
        "c_mono_high_usd": round(c_mono_high, 6),
        "c_scout_usd": round(c_scout, 6),
        "c_gov_usd": round(c_gov, 6),
        "c_hands_usd": round(c_hands, 6),
        "c_swarm_std_usd": round(c_swarm_std, 6),
        "c_swarm_micro_usd": round(c_swarm_micro, 6),
        "ooda_mult_std": round(ooda_mult_std, 6),
        "ooda_mult_peak": round(ooda_mult_peak, 6),
    }


def compute_pleistocene_dacc_extinction(
    gamma_dacc: float = 0.65,
    turns: int = 5,
) -> Dict[str, float]:
    """
    Computes survival probability of an out-of-distribution (OOD) hypothesis
    across multi-turn conversational RLHF accommodation vs. a Faraday JSON state box.
    """
    p_ood_chat = (1.0 - gamma_dacc) ** turns
    extinction_rate_chat = 1.0 - p_ood_chat
    p_ood_faraday = (1.0 - 0.0) ** turns

    assert abs(p_ood_chat - 0.0052521875) < 1e-6, f"p_ood_chat mismatch: {p_ood_chat}"
    assert abs(extinction_rate_chat - 0.9947478125) < 1e-6, f"extinction mismatch: {extinction_rate_chat}"
    assert abs(p_ood_faraday - 1.000000) < 1e-6, f"p_ood_faraday mismatch: {p_ood_faraday}"

    return {
        "gamma_dacc": gamma_dacc,
        "turns": float(turns),
        "p_ood_chat": round(p_ood_chat, 10),
        "p_ood_chat_pct": round(p_ood_chat * 100.0, 4),
        "extinction_rate_chat_pct": round(extinction_rate_chat * 100.0, 4),
        "p_ood_faraday": round(p_ood_faraday, 6),
    }


def compute_physical_and_ip_liquidation_ledger() -> Dict[str, float]:
    """
    Computes Sino-US physical manufacturing/grid ratios, Cournot open-weight cost
    compression externalities, shadow-library copyright settlement sinks, and
    ambient enterprise distillation share.
    """
    shipbuilding_multiple = 23250000.0 / 100000.0
    power_grid_multiple = 10100.0 / 4536.0

    cournot_mfg_externality_b = 250.0 * 0.20 * 0.65
    cournot_rd_externality_b = (2000000 * 25 * 150.0) / 1e9
    cournot_total_externality_b = cournot_mfg_externality_b + cournot_rd_externality_b
    stigmergic_pretrain_leverage = 7500.0 / 5.576

    shadow_library_liquidated_sink_m = 1500.00 + 19.50
    ambient_distill_share = 0.06 + (0.94 * 0.85)
    ambient_distill_rev_m = 33086.00 * ambient_distill_share
    snr_amplification = (0.99 / 0.01) / (0.20 / 0.80)

    assert abs(shipbuilding_multiple - 232.50) < 1e-6
    assert abs(power_grid_multiple - 2.22663139329806) < 1e-6
    assert abs(cournot_mfg_externality_b - 32.50) < 1e-6
    assert abs(cournot_rd_externality_b - 7.50) < 1e-6
    assert abs(cournot_total_externality_b - 40.00) < 1e-6
    assert abs(stigmergic_pretrain_leverage - 1345.0502152080344) < 1e-6
    assert abs(shadow_library_liquidated_sink_m - 1519.50) < 1e-6
    assert abs(ambient_distill_share - 0.8590) < 1e-6
    assert abs(ambient_distill_rev_m - 28420.874) < 1e-6
    assert abs(snr_amplification - 396.0) < 1e-6

    return {
        "shipbuilding_multiple": round(shipbuilding_multiple, 2),
        "power_grid_multiple": round(power_grid_multiple, 6),
        "cournot_mfg_externality_b": round(cournot_mfg_externality_b, 2),
        "cournot_rd_externality_b": round(cournot_rd_externality_b, 2),
        "cournot_total_externality_b": round(cournot_total_externality_b, 2),
        "stigmergic_pretrain_leverage": round(stigmergic_pretrain_leverage, 6),
        "shadow_library_liquidated_sink_m": round(shadow_library_liquidated_sink_m, 2),
        "ambient_distill_share": round(ambient_distill_share, 4),
        "ambient_distill_rev_m": round(ambient_distill_rev_m, 3),
        "snr_amplification": round(snr_amplification, 1),
    }


def tranche_recovery(ev_millions: float) -> List[Dict[str, Union[str, float]]]:
    """
    Parameterized priority waterfall recovery across the $75,000.00M
    Standalone Frontier AI Lab / SaaS Wrapper Capital Stack.
    """
    tranches = [
        {
            "tranche_id": "T1",
            "name": "Senior Secured Cloud/GPU Lease & Credit Facilities",
            "principal_m": 35000.00,
        },
        {
            "tranche_id": "T2",
            "name": "Class-Action Copyright Settlement & Statutory Judgment Reserves",
            "principal_m": 1519.50,
        },
        {
            "tranche_id": "T3",
            "name": "Unsecured Cloud Commitments & Convertible Notes",
            "principal_m": 8480.50,
        },
        {
            "tranche_id": "T4",
            "name": "Series D-F Preferred & Crossover Growth Equity",
            "principal_m": 30000.00,
        },
    ]

    remaining_ev = max(0.0, float(ev_millions))
    results: List[Dict[str, Union[str, float]]] = []
    cum_prior = 0.0

    for t in tranches:
        principal = t["principal_m"]
        rec_m = min(principal, remaining_ev)
        remaining_ev = max(0.0, remaining_ev - rec_m)
        cents = (rec_m / principal) * 100.0 if principal > 0 else 0.0
        cum_prior += principal
        results.append(
            {
                "tranche_id": t["tranche_id"],
                "name": t["name"],
                "principal_m": round(principal, 2),
                "breakeven_ev_m": round(cum_prior, 2),
                "recovery_m": round(rec_m, 2),
                "recovery_cents": round(cents, 6),
            }
        )

    return results


def main() -> int:
    ashby = compute_ashby_variety_inversion()
    ooda = compute_ricardian_ooda_multiplier()
    pleistocene = compute_pleistocene_dacc_extinction()
    ledger = compute_physical_and_ip_liquidation_ledger()
    waterfall_22500 = tranche_recovery(22500.00)

    assert abs(float(waterfall_22500[0]["recovery_m"]) - 22500.00) < 1e-6
    assert abs(float(waterfall_22500[0]["recovery_cents"]) - 64.285714) < 1e-6
    assert abs(float(waterfall_22500[1]["recovery_m"]) - 0.00) < 1e-6
    assert abs(float(waterfall_22500[2]["recovery_m"]) - 0.00) < 1e-6
    assert abs(float(waterfall_22500[3]["recovery_m"]) - 0.00) < 1e-6

    summary = {
        "specification": "SPEC-RICARDIAN-FARADAY-VARIETY-INVERSION-v1.0",
        "status": "VERIFIED_DETERMINISTIC_ZERO_DRIFT",
        "ashby_variety_inversion": ashby,
        "ricardian_ooda_economics": ooda,
        "pleistocene_dacc_operant_conditioning": pleistocene,
        "sino_us_physical_and_ip_liquidation_ledger": ledger,
        "stressed_waterfall_ev_22500m": waterfall_22500,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
