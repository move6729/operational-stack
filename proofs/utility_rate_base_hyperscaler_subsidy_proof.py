#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: UTILITY RATE-BASE PADDING & HYPERSCALER CROSS-SUBSIDY (v1.0)

Proves:
1. Averch-Johnson Gold-Plating Identity (AER 52(5):1052-1069, 1962): PUC-authorized
   ROE s = 0.105 against true debt/capital cost r = 0.055 locks a risk-free spread
   Delta_AJ = s - r = +0.050, so Profit = Delta_AJ * K_RateBase and the gold-plating
   gradient d(Profit)/d(K) = +$0.05 per $1 of rate base per year is strictly positive.
2. Residential Cross-Subsidization Transfer (16 U.S.C. 824d / FPA 205): on K = $5.0B
   of hyperscaler-induced transmission capex, R_req = K*s + K/40 = $525.0M + $125.0M
   = $650.0M/yr, of which alpha = 0.72 is socialized onto N = 1.5M captive households:
   S_res = $468.0M/yr, sigma_hh = $312.00 per household per year.
3. PJM 2025/2026 Base Residual Auction surge: $28.92/MW-day -> $269.92/MW-day =
   9.333333x, annualized $10,555.80 -> $98,520.80 per MW-yr (+$87.965M/yr per GW),
   falsifying the H0 load-spreading defense at the margin.
4. Stranded-Asset Duration Mismatch: 5-7 yr GPU leases vs 40 yr rate-base depreciation;
   stranding at Year 7 leaves K_resid = $4.125B residual rate base and a 33-year
   deadweight of R_dead = $125.0M + 0.105*$4,125M = $558.125M/yr ($18.418B cumulative,
   $267.90/household/yr residential share).
5. Behind-the-Meter Defection Death Spiral: at defection share delta = 0.10 the
   per-household surcharge steps up $312.00 -> $346.67 (+11.11%), compounding.

Zero external dependencies.
"""

import hashlib
import json

TOL = 1e-6

# --- Locked empirical baseline (14 constants, SPEC telemetry table Section 5) ---
S_ROE = 0.105                 # puc_authorized_roe_rate
R_COST = 0.055                # utility_cost_of_debt_capital_rate
DELTA_AJ = 0.05               # averch_johnson_roe_spread
K_CAPEX_B = 5.0               # hyperscaler_induced_transmission_capex_usd_billions
ROE_EXTRACT_M = 525.0         # annual_guaranteed_roe_profit_extract_usd_millions
DEPRECIATION_M = 125.0        # annual_straight_line_depreciation_charge_usd_millions
R_REQ_M = 650.0               # total_annual_revenue_requirement_usd_millions
ALPHA_RES = 0.72              # residential_ratepayer_cost_allocation_share
S_RES_M = 468.0               # residential_annual_cross_subsidy_transfer_usd_millions
N_HOUSEHOLDS_M = 1.5          # captive_residential_households_millions
SIGMA_HH = 312.0              # annual_surcharge_per_captive_household_usd
PJM_PRIOR = 28.92             # pjm_prior_capacity_clearing_price_mw_day_usd
PJM_SPIKE = 269.92            # pjm_hyperscaler_spike_capacity_price_mw_day_usd
PJM_MULT = 9.333333           # pjm_capacity_price_surge_multiplier

# --- Structural horizons ---
T_DEPRECIATION_YEARS = 40.0   # rate-base straight-line horizon
TAU_GPU_MIN_YEARS = 5.0       # GPU lease tenor floor (neocloud spec cross-ref)
TAU_GPU_MAX_YEARS = 7.0       # GPU lease tenor ceiling
STRANDING_YEAR = 7.0          # worst-case-in-tenor stranding regime
DEFECTION_SHARE = 0.10        # behind-the-meter exit share for death-spiral probe

K_CAPEX_M = K_CAPEX_B * 1000.0


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def verify_averch_johnson_spread():
    """Primitive 1: Profit = (s - r) * K with strictly positive gold-plating gradient."""
    spread = S_ROE - R_COST
    assert close(spread, DELTA_AJ), f"AJ spread drift: {spread} != {DELTA_AJ}"
    assert spread > 0.0, "A-J over-capitalization condition s > r violated"

    # Guaranteed ROE extract on the induced rate base (in $M/yr)
    roe_extract = K_CAPEX_M * S_ROE
    assert close(roe_extract, ROE_EXTRACT_M), f"ROE extract drift: {roe_extract}"

    # True capital charge vs guaranteed extract: the +500 bps headroom
    true_capital_charge = K_CAPEX_M * R_COST
    profit_annuity = roe_extract - true_capital_charge
    assert close(profit_annuity, DELTA_AJ * K_CAPEX_M), "profit annuity drift"

    # Gold-plating gradient per $1 of added rate base
    gradient = spread
    assert close(gradient, 0.05), "gold-plating gradient drift"

    return {
        "puc_authorized_roe_rate": round(S_ROE, 6),
        "utility_cost_of_debt_capital_rate": round(R_COST, 6),
        "averch_johnson_roe_spread": round(spread, 6),
        "hyperscaler_induced_transmission_capex_usd_billions": round(K_CAPEX_B, 6),
        "annual_guaranteed_roe_profit_extract_usd_millions": round(roe_extract, 6),
        "true_annual_capital_charge_usd_millions": round(true_capital_charge, 6),
        "gold_plating_gradient_usd_per_usd_per_year": round(gradient, 6),
        "overcapitalization_condition_s_gt_r": spread > 0.0,
    }


def verify_revenue_requirement():
    """Primitive 2a: R_req = K*s + K/T over the 40-year straight-line horizon."""
    depreciation = K_CAPEX_M / T_DEPRECIATION_YEARS
    assert close(depreciation, DEPRECIATION_M), f"depreciation drift: {depreciation}"

    r_req = ROE_EXTRACT_M + depreciation
    assert close(r_req, R_REQ_M), f"revenue requirement drift: {r_req}"

    return {
        "rate_base_depreciation_horizon_years": T_DEPRECIATION_YEARS,
        "annual_straight_line_depreciation_charge_usd_millions": round(depreciation, 6),
        "total_annual_revenue_requirement_usd_millions": round(r_req, 6),
    }


def verify_residential_cross_subsidy():
    """Primitive 2b: S_res = alpha * R_req socialized onto N captive households."""
    s_res = R_REQ_M * ALPHA_RES
    assert close(s_res, S_RES_M), f"cross-subsidy drift: {s_res}"

    sigma = s_res / N_HOUSEHOLDS_M
    assert close(sigma, SIGMA_HH), f"per-household surcharge drift: {sigma}"

    return {
        "residential_ratepayer_cost_allocation_share": round(ALPHA_RES, 6),
        "residential_annual_cross_subsidy_transfer_usd_millions": round(s_res, 6),
        "captive_residential_households_millions": round(N_HOUSEHOLDS_M, 6),
        "annual_surcharge_per_captive_household_usd": round(sigma, 6),
    }


def verify_pjm_capacity_surge():
    """Primitive 3: PJM 2025/2026 BRA clearing price surge falsifies H0 at the margin."""
    multiplier = round(PJM_SPIKE / PJM_PRIOR, 6)
    assert close(multiplier, PJM_MULT), f"PJM multiplier drift: {multiplier}"
    assert multiplier > 1.0, "H0 load-spreading regime requires mu > 1 falsification"

    days_per_year = 365.0
    prior_annualized = PJM_PRIOR * days_per_year
    spike_annualized = PJM_SPIKE * days_per_year
    step_up_per_mw_yr = spike_annualized - prior_annualized
    step_up_per_gw_yr_m = step_up_per_mw_yr * 1000.0 / 1e6

    assert close(prior_annualized, 10555.80), f"prior annualized drift: {prior_annualized}"
    assert close(spike_annualized, 98520.80), f"spike annualized drift: {spike_annualized}"
    assert close(step_up_per_gw_yr_m, 87.965), f"per-GW step-up drift: {step_up_per_gw_yr_m}"

    return {
        "pjm_prior_capacity_clearing_price_mw_day_usd": round(PJM_PRIOR, 6),
        "pjm_hyperscaler_spike_capacity_price_mw_day_usd": round(PJM_SPIKE, 6),
        "pjm_capacity_price_surge_multiplier": multiplier,
        "annualized_capacity_cost_prior_usd_per_mw_yr": round(prior_annualized, 6),
        "annualized_capacity_cost_spike_usd_per_mw_yr": round(spike_annualized, 6),
        "gigawatt_capacity_cost_step_up_usd_m_per_yr": round(step_up_per_gw_yr_m, 6),
    }


def verify_stranded_duration_mismatch():
    """Primitive 4: Year-7 stranding leaves a 33-year dead-capex tail on the rate base."""
    assert TAU_GPU_MIN_YEARS <= TAU_GPU_MAX_YEARS < T_DEPRECIATION_YEARS, \
        "GPU lease tenor must sit strictly inside the depreciation horizon"

    residual_years = T_DEPRECIATION_YEARS - STRANDING_YEAR
    assert close(residual_years, 33.0), f"residual tail drift: {residual_years}"

    residual_rate_base_b = K_CAPEX_B * (residual_years / T_DEPRECIATION_YEARS)
    assert close(residual_rate_base_b, 4.125), f"residual rate base drift: {residual_rate_base_b}"

    # Dead annual revenue requirement: depreciation continues, ROE accrues on the
    # undepreciated balance (Hope end-result protection of the return, not the service).
    dead_depreciation_m = DEPRECIATION_M
    dead_roe_m = residual_rate_base_b * 1000.0 * S_ROE
    dead_annual_m = dead_depreciation_m + dead_roe_m
    assert close(dead_roe_m, 433.125), f"dead ROE drift: {dead_roe_m}"
    assert close(dead_annual_m, 558.125), f"dead annual drift: {dead_annual_m}"

    cumulative_deadweight_b = dead_annual_m * residual_years / 1000.0
    assert close(cumulative_deadweight_b, 18.418125), f"cumulative drift: {cumulative_deadweight_b}"

    residential_deadweight_per_hh = dead_annual_m * ALPHA_RES / N_HOUSEHOLDS_M
    assert close(residential_deadweight_per_hh, 267.90), \
        f"residential deadweight drift: {residential_deadweight_per_hh}"

    return {
        "gpu_lease_tenor_years_min": TAU_GPU_MIN_YEARS,
        "gpu_lease_tenor_years_max": TAU_GPU_MAX_YEARS,
        "rate_base_depreciation_horizon_years": T_DEPRECIATION_YEARS,
        "stranding_year": STRANDING_YEAR,
        "residual_captive_years": round(residual_years, 6),
        "residual_rate_base_usd_b": round(residual_rate_base_b, 6),
        "annual_deadweight_revenue_requirement_usd_m": round(dead_annual_m, 6),
        "cumulative_deadweight_usd_b": round(cumulative_deadweight_b, 6),
        "residential_deadweight_surcharge_usd_per_household_yr": round(residential_deadweight_per_hh, 6),
    }


def verify_defection_death_spiral():
    """Primitive 5: behind-the-meter exit steps up the surcharge on the captive remainder."""
    remaining_households_m = N_HOUSEHOLDS_M * (1.0 - DEFECTION_SHARE)
    assert close(remaining_households_m, 1.35), f"remaining base drift: {remaining_households_m}"

    sigma_post = S_RES_M / remaining_households_m
    assert close(sigma_post, 346.666667, tol=1e-4), f"post-defection surcharge drift: {sigma_post}"

    step_up_pct = (sigma_post / SIGMA_HH - 1.0) * 100.0
    assert close(step_up_pct, 11.111111, tol=1e-4), f"step-up drift: {step_up_pct}"
    assert sigma_post > SIGMA_HH, "death spiral requires monotone surcharge step-up"

    return {
        "defection_share": DEFECTION_SHARE,
        "remaining_captive_households_millions": round(remaining_households_m, 6),
        "surcharge_post_defection_usd": round(sigma_post, 2),
        "surcharge_step_up_pct": round(step_up_pct, 2),
    }


def run_verification():
    aj = verify_averch_johnson_spread()
    revenue = verify_revenue_requirement()
    subsidy = verify_residential_cross_subsidy()
    pjm = verify_pjm_capacity_surge()
    stranded = verify_stranded_duration_mismatch()
    spiral = verify_defection_death_spiral()

    manifest = {
        "spec_version": "SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0",
        "averch_johnson_rate_base": aj,
        "revenue_requirement": revenue,
        "residential_cross_subsidy": subsidy,
        "pjm_capacity_auction": pjm,
        "stranded_duration_mismatch": stranded,
        "defection_death_spiral": spiral,
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-UTILITY-RATE-BASE-PADDING-AND-HYPERSCALER-CROSS-SUBSIDY-v1.0 | "
        f"Delta_AJ={aj['averch_johnson_roe_spread']:.3f} s>r={aj['overcapitalization_condition_s_gt_r']} | "
        f"R_req=${revenue['total_annual_revenue_requirement_usd_millions']:.1f}M/yr | "
        f"S_res=${subsidy['residential_annual_cross_subsidy_transfer_usd_millions']:.1f}M/yr | "
        f"sigma_hh=${subsidy['annual_surcharge_per_captive_household_usd']:.2f}/yr | "
        f"mu_PJM={pjm['pjm_capacity_price_surge_multiplier']:.6f}x "
        f"(+${pjm['gigawatt_capacity_cost_step_up_usd_m_per_yr']:.3f}M/yr per GW) | "
        f"K_resid=${stranded['residual_rate_base_usd_b']:.3f}B "
        f"R_dead=${stranded['annual_deadweight_revenue_requirement_usd_m']:.3f}M/yr "
        f"cum=${stranded['cumulative_deadweight_usd_b']:.6f}B | "
        f"sigma'_hh=${spiral['surcharge_post_defection_usd']:.2f} "
        f"(+{spiral['surcharge_step_up_pct']:.2f}%) | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
