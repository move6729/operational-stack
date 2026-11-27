#!/usr/bin/env python3
"""Verification engine: distressed infrastructure absorption and BTM power consolidation.

Deterministic, pure-stdlib checks of the double-marginalization / TPU economics,
GAAP-vs-economic GPU depreciation distortion, distressed absorption & fortress
liquidity coverage, and the fulcrum tranche recovery waterfall for the
$50,000.00M Distressed Merchant Neocloud & BTM Power Complex.

Exit code 0 on full verification (all assertions pass to 1e-6 precision).
"""

import json
import sys

TOL = 1e-6


def approx(a: float, b: float) -> bool:
    return abs(a - b) <= TOL


def compute_double_marginalization_and_spv_spread() -> dict:
    atc_tpu = 0.68
    atc_neocloud = 2.18
    srmc_electricity = 0.18
    atc_advantage_multiple = atc_neocloud / atc_tpu
    unit_cost_reduction_pct = (1.0 - atc_tpu / atc_neocloud) * 100.0

    spv_principal_b = 35.0
    spv_yield = 0.0710
    neocloud_yield = 0.0930
    annual_financing_savings_m = spv_principal_b * (neocloud_yield - spv_yield) * 1000.0
    six_year_financing_savings_b = (annual_financing_savings_m * 6.0) / 1000.0

    assert approx(atc_advantage_multiple, 3.2058823529411766)
    assert approx(unit_cost_reduction_pct, 68.80733944954129)
    assert approx(annual_financing_savings_m, 770.00)
    assert approx(six_year_financing_savings_b, 4.620)
    assert srmc_electricity < atc_tpu < atc_neocloud

    return {
        "atc_tpu_per_watt": atc_tpu,
        "atc_neocloud_per_watt": atc_neocloud,
        "srmc_electricity_per_watt": srmc_electricity,
        "atc_advantage_multiple": round(atc_advantage_multiple, 6),
        "unit_cost_reduction_pct": round(unit_cost_reduction_pct, 4),
        "spv_principal_b": spv_principal_b,
        "spv_yield": spv_yield,
        "neocloud_yield": neocloud_yield,
        "annual_financing_savings_m": round(annual_financing_savings_m, 2),
        "six_year_financing_savings_b": round(six_year_financing_savings_b, 3),
    }


def compute_depreciation_distortion_and_permanence() -> dict:
    active_gpu_ppe_m = 33823.0
    cip_ppe_m = 11918.0
    total_tech_cip_m = 45741.0
    tau_gaap = 6.0
    tau_econ = 2.0
    tau_power_shell = 40.0

    d_gaap_m = active_gpu_ppe_m / tau_gaap
    d_econ_m = active_gpu_ppe_m / tau_econ
    unbooked_obsolescence_deficit_m = d_econ_m - d_gaap_m
    shell_to_silicon_lifespan_ratio = tau_power_shell / tau_econ

    assert approx(cip_ppe_m + active_gpu_ppe_m, total_tech_cip_m)
    assert approx(d_gaap_m, 5637.166666666667)
    assert approx(d_econ_m, 16911.50)
    assert approx(unbooked_obsolescence_deficit_m, 11274.333333333334)
    assert approx(shell_to_silicon_lifespan_ratio, 20.0)

    return {
        "active_gpu_ppe_m": active_gpu_ppe_m,
        "cip_ppe_m": cip_ppe_m,
        "total_tech_cip_m": total_tech_cip_m,
        "tau_gaap_years": tau_gaap,
        "tau_econ_years": tau_econ,
        "tau_power_shell_years": tau_power_shell,
        "d_gaap_m_per_yr": round(d_gaap_m, 6),
        "d_econ_m_per_yr": round(d_econ_m, 6),
        "unbooked_obsolescence_deficit_m_per_yr": round(unbooked_obsolescence_deficit_m, 6),
        "shell_to_silicon_lifespan_ratio": shell_to_silicon_lifespan_ratio,
    }


def compute_absorption_and_fortress_liquidity() -> dict:
    global_crossing_capex_b = 15.0
    global_crossing_recovery_b = 2.25
    dark_fiber_cents = 15.0

    wulf_hawesville_mw = 401.0
    wulf_lake_mariner_mw = 360.0
    cifr_colorado_city_mw = 168.0
    total_step_in_shell_mw = wulf_hawesville_mw + wulf_lake_mariner_mw + cifr_colorado_city_mw

    queue_bypass_months = 48.0
    novation_window_days = 30.0
    equip_trigger_mw = wulf_hawesville_mw * 0.50

    alphabet_intersect_acq_b = 4.75
    intersect_btm_pipeline_b = 20.0

    gpu_capex_m = 32000.0
    btm_shell_capex_m = 18000.0
    complex_gross_capex_m = gpu_capex_m + btm_shell_capex_m
    gpu_salvage_m = gpu_capex_m * 0.15
    btm_shell_clearing_m = 12700.0
    btm_shell_clearing_pct = (btm_shell_clearing_m / btm_shell_capex_m) * 100.0
    ev_stressed_m = gpu_salvage_m + btm_shell_clearing_m
    ev_stressed_cents_blended = (ev_stressed_m / complex_gross_capex_m) * 100.0

    googl_net_cash_m = 114843.0
    brk_cash_tbills_m = 377400.0
    combined_fortress_cash_m = googl_net_cash_m + brk_cash_tbills_m
    fortress_liquidity_coverage_multiple = combined_fortress_cash_m / ev_stressed_m

    pjm_surge_mult = 269.92 / 28.92
    averch_johnson_household_surcharge_usd = (5000.0 * 0.13 * 0.72) / 1.5
    aj_aggregate_transfer_m = 5000.0 * 0.13 * 0.72

    assert approx(global_crossing_recovery_b / global_crossing_capex_b, 0.15)
    assert approx(dark_fiber_cents, 15.0)
    assert approx(total_step_in_shell_mw, 929.0)
    assert approx(equip_trigger_mw, 200.5)
    assert approx(complex_gross_capex_m, 50000.0)
    assert approx(gpu_salvage_m, 4800.0)
    assert approx(btm_shell_clearing_pct, 70.55555555555556)
    assert approx(ev_stressed_m, 17500.0)
    assert approx(ev_stressed_cents_blended, 35.00)
    assert approx(combined_fortress_cash_m, 492243.0)
    assert approx(fortress_liquidity_coverage_multiple, 28.128171428571428)
    assert approx(pjm_surge_mult, 9.333333333333334)
    assert approx(averch_johnson_household_surcharge_usd, 312.00)
    assert approx(aj_aggregate_transfer_m, 468.0)

    return {
        "global_crossing_capex_b": global_crossing_capex_b,
        "global_crossing_recovery_b": global_crossing_recovery_b,
        "dark_fiber_cents_on_dollar": dark_fiber_cents,
        "wulf_hawesville_mw": wulf_hawesville_mw,
        "wulf_lake_mariner_mw": wulf_lake_mariner_mw,
        "cifr_colorado_city_mw": cifr_colorado_city_mw,
        "total_step_in_shell_mw": total_step_in_shell_mw,
        "queue_bypass_months": queue_bypass_months,
        "novation_window_days": novation_window_days,
        "equip_trigger_mw": round(equip_trigger_mw, 1),
        "alphabet_intersect_acq_b": alphabet_intersect_acq_b,
        "intersect_btm_pipeline_b": intersect_btm_pipeline_b,
        "complex_gross_capex_m": complex_gross_capex_m,
        "gpu_capex_m": gpu_capex_m,
        "btm_shell_capex_m": btm_shell_capex_m,
        "gpu_salvage_m": round(gpu_salvage_m, 2),
        "btm_shell_clearing_m": btm_shell_clearing_m,
        "btm_shell_clearing_pct_of_replacement": round(btm_shell_clearing_pct, 6),
        "ev_stressed_m": round(ev_stressed_m, 2),
        "ev_stressed_blended_cents": round(ev_stressed_cents_blended, 4),
        "googl_net_cash_m": googl_net_cash_m,
        "brk_cash_tbills_m": brk_cash_tbills_m,
        "combined_fortress_cash_m": combined_fortress_cash_m,
        "fortress_liquidity_coverage_multiple": round(fortress_liquidity_coverage_multiple, 6),
        "pjm_surge_multiple": round(pjm_surge_mult, 6),
        "averch_johnson_household_surcharge_usd_per_yr": round(averch_johnson_household_surcharge_usd, 2),
        "averch_johnson_aggregate_transfer_m_per_yr": round(aj_aggregate_transfer_m, 1),
    }


TRANCHES = [
    ("T1", 14000.00),
    ("T2", 16000.00),
    ("T3", 10000.00),
    ("T4", 10000.00),
]


def tranche_recovery(ev_millions: float) -> list:
    """Absolute priority waterfall: map enterprise value to per-tranche
    dollar recovery, cents-on-the-dollar, and write-down percentage."""
    remaining = ev_millions
    out = []
    for name, principal in TRANCHES:
        recovered = min(remaining, principal)
        remaining = max(remaining - principal, 0.0)
        cents = (recovered / principal) * 100.0
        write_down_pct = ((principal - recovered) / principal) * 100.0
        out.append(
            {
                "tranche": name,
                "principal_m": principal,
                "recovered_m": round(recovered, 2),
                "cents_on_dollar": round(cents, 4),
                "write_down_pct": round(write_down_pct, 4),
            }
        )
    return out


def verify_waterfall() -> dict:
    total_principal = sum(p for _, p in TRANCHES)
    assert approx(total_principal, 50000.0)

    rows = tranche_recovery(17500.0)
    assert approx(rows[0]["recovered_m"], 14000.00)
    assert approx(rows[0]["cents_on_dollar"], 100.0000)
    assert approx(rows[1]["recovered_m"], 3500.00)
    assert approx(rows[1]["cents_on_dollar"], 21.8750)
    assert approx(rows[1]["write_down_pct"], 78.1250)
    assert approx(rows[2]["recovered_m"], 0.00)
    assert approx(rows[2]["cents_on_dollar"], 0.0000)
    assert approx(rows[3]["recovered_m"], 0.00)
    assert approx(rows[3]["cents_on_dollar"], 0.0000)

    # Full-par and zero-EV boundary checks
    full = tranche_recovery(50000.0)
    assert all(approx(r["cents_on_dollar"], 100.0) for r in full)
    zero = tranche_recovery(0.0)
    assert all(approx(r["cents_on_dollar"], 0.0) for r in zero)

    return {
        "complex_gross_capex_m": total_principal,
        "stressed_ev_m": 17500.0,
        "waterfall_at_stressed_ev": rows,
    }


def main() -> int:
    summary = {
        "verification": "distressed_infrastructure_absorption_and_btm_power_consolidation",
        "tolerance": TOL,
        "double_marginalization_and_spv_spread": compute_double_marginalization_and_spv_spread(),
        "depreciation_distortion_and_permanence": compute_depreciation_distortion_and_permanence(),
        "absorption_and_fortress_liquidity": compute_absorption_and_fortress_liquidity(),
        "debt_stack_and_fulcrum_waterfall": verify_waterfall(),
        "exit_code": 0,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
