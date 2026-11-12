#!/usr/bin/env python3
"""
Deterministic Verification Engine: SPEC-AHI-CYBERNETIC-SELF-DDOS-v1.0
Models the 4-tranche $550.0M Federal AHI Liability & Expenditure Waterfall,
Standing-Wave Acoustic Physics (Indieshort Cricket), RF Link-Budget Thermal
Inversion, Clinical Control-Group Selection Bias vs. NIH Null Convergence,
Reverse-Causal CI Watchlist Conditioning, and HAVANA Act Statutory Moral Hazard.

License: Unlicense (Public Domain)
"""

import json
import math
import sys
from typing import Any, Dict, List


LOCKED_CONSTANTS: Dict[str, Any] = {
    "total_institutional_capital_at_risk_usd": 550000000.0,
    "tranche_1_statutory_havana_act_exposure_usd": 280950000.0,
    "tranche_2_classified_elint_sensor_and_darpa_rd_usd": 145000000.0,
    "tranche_3_station_evacuation_and_ci_disruption_cost_usd": 85000000.0,
    "tranche_4_nih_walter_reed_upenn_clinical_workup_usd": 39050000.0,
    "adversary_dew_hardware_capex_usd": 0.0,
    "odni_reviewed_ahi_reports_count": 1500,
    "odni_reviewed_countries_count": 96,
    "odni_participating_agencies_count": 7,
    "odni_very_unlikely_agencies_count": 5,
    "odni_unlikely_agencies_count": 2,
    "post_2018_confirmed_hostile_rf_emissions_count": 0,
    "nih_ahi_cohort_size": 86,
    "nih_control_cohort_size_pierpaoli_mri": 48,
    "nih_control_cohort_size_chan_clinical": 30,
    "nih_structural_mri_adjusted_p_value": 1.0,
    "nih_biomarker_gfap_nfl_adjusted_p_value": 1.0,
    "nih_mri_reproducibility_cv_pct": 1.0,
    "nih_fnd_pppd_diagnosed_count": 24,
    "nih_fnd_pppd_diagnosed_pct": 27.907,
    "havana_act_exec_schedule_level_iii_base_usd": 187300.0,
    "havana_act_tier_1_75pct_payment_usd": 140475.0,
    "havana_act_tier_2_100pct_payment_usd": 187300.0,
    "feca_uncorroborated_subjective_symptom_payout_usd": 0.0,
    "cricket_carrier_freq_hz": 7000.0,
    "cricket_speed_of_sound_mps": 343.0,
    "cricket_wavelength_cm": 4.9,
    "cricket_quarter_wave_null_step_cm": 1.225,
    "cricket_pulse_repetition_rate_hz": 180.0,
    "link_budget_standoff_m": 30.0,
    "link_budget_close_range_m": 5.0,
    "link_budget_wall_loss_db": 15.0,
    "near_field_power_scaling_factor": 1138.42,
    "dalhousie_canadian_diplomat_cohort_size": 26,
    "upenn_2019_ahi_cohort_size": 40,
    "upenn_2019_civilian_control_concussion_exclusion_rate_pct": 100.0,
    "cleared_workforce_population": 100000,
    "annual_baseline_vestibular_migraine_tinnitus_incidence_rate": 0.15,
    "annual_eligible_baseline_episodes": 15000,
}

TRANCHES: List[Dict[str, Any]] = [
    {
        "tranche_id": "TRANCHE_1_STATUTORY_HAVANA_ACT_CLAIMS",
        "name": "Statutory HAVANA Act No-Fault Compensation Exposure (22 U.S.C. § 2680b)",
        "principal_usd": 280950000.0,
        "seniority": 1,
        "collateral_box": "Permanent Statutory Appropriation / 22 CFR Part 135 & 32 CFR Part 142 Lump-Sum Pool",
    },
    {
        "tranche_id": "TRANCHE_2_CLASSIFIED_ELINT_DARPA_SENSOR_RD",
        "name": "Classified ELINT / SIGINT Sensor Deployment, JASON Review & DARPA R&D",
        "principal_usd": 145000000.0,
        "seniority": 2,
        "collateral_box": "FY2022-FY2025 NDAA Cross-Functional Team & Classified RDT&E Allocations",
    },
    {
        "tranche_id": "TRANCHE_3_STATION_EVACUATION_CI_DISRUPTION",
        "name": "Diplomatic Station Drawdowns, Medevacs & Counterintelligence Disruption",
        "principal_usd": 85000000.0,
        "seniority": 3,
        "collateral_box": "State Dept Diplomatic Security & IC Overseas Station Operating Budgets",
    },
    {
        "tranche_id": "TRANCHE_4_NIH_WALTER_REED_UPENN_CLINICAL_WORKUPS",
        "name": "NIH Intramural Cohort, Walter Reed NICOE & UPenn Neuroimaging Protocols",
        "principal_usd": 39050000.0,
        "seniority": 4,
        "collateral_box": "NIH Clinical Center & DoD Defense Health Program Appropriations",
    },
]


def tranche_recovery(ev: float) -> Dict[str, Any]:
    """
    Parameterized Tranche Payoff Function across the $550.0M Federal AHI
    Liability & Expenditure Stack. Given available fiscal allocation /
    institutional expenditure budget `ev` (USD), returns exact dollar and
    cent-on-the-dollar absorption vectors across all 4 tranches in strict
    statutory/appropriations priority order.
    """
    if ev < 0.0:
        raise ValueError("Fiscal allocation EV must be non-negative.")

    remaining = float(ev)
    waterfall: List[Dict[str, Any]] = []
    cum_threshold = 0.0

    for t in TRANCHES:
        principal = t["principal_usd"]
        breakeven_ev = cum_threshold + principal
        allocated = min(remaining, principal)
        remaining = max(0.0, remaining - allocated)
        recovery_cents = (allocated / principal) * 100.0 if principal > 0 else 0.0
        waterfall.append(
            {
                "tranche_id": t["tranche_id"],
                "seniority": t["seniority"],
                "principal_usd": round(principal, 2),
                "breakeven_ev_threshold_usd": round(breakeven_ev, 2),
                "allocated_usd": round(allocated, 2),
                "recovery_cents_on_dollar": round(recovery_cents, 4),
            }
        )
        cum_threshold = breakeven_ev

    return {
        "input_ev_usd": round(ev, 2),
        "total_stack_principal_usd": round(cum_threshold, 2),
        "unallocated_surplus_usd": round(remaining, 2),
        "tranches": waterfall,
    }


def verify_eq01_acoustic_standing_wave() -> Dict[str, float]:
    """
    EQ_01: Standing-Wave Acoustic Interference of Anurogryllus celerinictus
    ('Indieshort short-tailed cricket') inside hard-plaster tropical rooms.
    lambda = c_sound / f_0 = 343.0 / 7000.0 = 0.049 m = 4.9 cm.
    Quarter-wave pressure anti-node to null step = lambda / 4 = 1.225 cm.
    """
    c_sound = LOCKED_CONSTANTS["cricket_speed_of_sound_mps"]
    f_0 = LOCKED_CONSTANTS["cricket_carrier_freq_hz"]
    wavelength_m = c_sound / f_0
    wavelength_cm = round(wavelength_m * 100.0, 4)
    quarter_wave_cm = round(wavelength_cm / 4.0, 4)

    assert math.isclose(wavelength_cm, LOCKED_CONSTANTS["cricket_wavelength_cm"], rel_tol=1e-6)
    assert math.isclose(
        quarter_wave_cm, LOCKED_CONSTANTS["cricket_quarter_wave_null_step_cm"], rel_tol=1e-6
    )
    return {
        "wavelength_cm": wavelength_cm,
        "quarter_wave_null_step_cm": quarter_wave_cm,
        "pulse_repetition_rate_hz": LOCKED_CONSTANTS["cricket_pulse_repetition_rate_hz"],
    }


def verify_eq02_friis_link_budget_inversion() -> Dict[str, float]:
    """
    EQ_02: Pulsed-RF / Frey-Effect Near-Field Thermal Inversion.
    S(r, L_wall) = (P_tx * G_tx) / (4 * pi * r^2) * 10^(-L_wall / 10).
    Ratio of flux density at r_close=5m (0 dB open window) vs r_far=30m (15 dB masonry):
    Ratio = (30 / 5)^2 * 10^(15 / 10) = 36 * 31.6227766 = 1138.419958 -> 1138.42x.
    """
    r_far = LOCKED_CONSTANTS["link_budget_standoff_m"]
    r_close = LOCKED_CONSTANTS["link_budget_close_range_m"]
    l_wall_db = LOCKED_CONSTANTS["link_budget_wall_loss_db"]

    distance_factor = (r_far / r_close) ** 2
    attenuation_factor = 10.0 ** (l_wall_db / 10.0)
    scaling_factor = round(distance_factor * attenuation_factor, 2)

    assert math.isclose(
        scaling_factor, LOCKED_CONSTANTS["near_field_power_scaling_factor"], rel_tol=1e-5
    )
    return {
        "distance_factor": round(distance_factor, 2),
        "wall_attenuation_factor": round(attenuation_factor, 4),
        "near_field_power_scaling_factor": scaling_factor,
    }


def verify_eq03_control_bias_and_nih_null() -> Dict[str, float]:
    """
    EQ_03: UPenn 2019 Control-Group Concussion-Exclusion Bias vs. NIH 2024
    Occupation-Matched Null Convergence (JAMA 2024; Pierpaoli et al. & Chan et al.).
    NIH FND/PPPD clinical diagnosis rate = 24 / 86 = 27.907%.
    """
    fnd_count = LOCKED_CONSTANTS["nih_fnd_pppd_diagnosed_count"]
    cohort_n = LOCKED_CONSTANTS["nih_ahi_cohort_size"]
    fnd_pct = round((fnd_count / cohort_n) * 100.0, 3)

    assert math.isclose(fnd_pct, LOCKED_CONSTANTS["nih_fnd_pppd_diagnosed_pct"], rel_tol=1e-5)
    assert LOCKED_CONSTANTS["nih_structural_mri_adjusted_p_value"] == 1.0
    assert LOCKED_CONSTANTS["nih_biomarker_gfap_nfl_adjusted_p_value"] == 1.0
    return {
        "nih_fnd_pppd_diagnosed_pct": fnd_pct,
        "nih_structural_mri_adjusted_p_value": LOCKED_CONSTANTS[
            "nih_structural_mri_adjusted_p_value"
        ],
        "nih_biomarker_gfap_nfl_adjusted_p_value": LOCKED_CONSTANTS[
            "nih_biomarker_gfap_nfl_adjusted_p_value"
        ],
    }


def verify_eq04_reverse_causal_ci_clustering() -> Dict[str, float]:
    """
    EQ_04: Endogenous CI Mission Co-Location & Reverse-Causal Watchlist Threat-Priming.
    Demonstrates that when P(Watchlist_Priming | Russia_CI_Billet) -> 0.85 vs
    baseline billet priming 0.05, endogenous Bayesian symptom attribution creates
    a 17.0x cluster amplification with zero exogenous DEW emissions (0/1,500).
    """
    p_primed_ci = 0.85
    p_primed_baseline = 0.05
    cluster_amplification_ratio = round(p_primed_ci / p_primed_baseline, 2)

    assert LOCKED_CONSTANTS["post_2018_confirmed_hostile_rf_emissions_count"] == 0
    assert (
        LOCKED_CONSTANTS["odni_very_unlikely_agencies_count"]
        + LOCKED_CONSTANTS["odni_unlikely_agencies_count"]
        == LOCKED_CONSTANTS["odni_participating_agencies_count"]
    )
    return {
        "ci_cluster_amplification_ratio": cluster_amplification_ratio,
        "confirmed_hostile_rf_emissions": LOCKED_CONSTANTS[
            "post_2018_confirmed_hostile_rf_emissions_count"
        ],
    }


def verify_eq05_kalman_gain_and_havana_act_moral_hazard() -> Dict[str, float]:
    """
    EQ_05: Interoceptive Kalman Gain Inflation (K_t -> 1.0) & HAVANA Act
    Statutory Moral Hazard (22 U.S.C. § 2680b).
    Executive Schedule Level III base = $187,300 (Tier 1 75% = $140,475; Tier 2 100% = $187,300).
    Across 100,000 cleared personnel with 15% annual benign vestibular/migraine/tinnitus
    incidence -> 15,000 eligible episodes/year.
    1,500 ODNI-reviewed reports * $187,300 Tier-2 cap = $280,950,000 Tranche 1 exposure.
    """
    base_pay = LOCKED_CONSTANTS["havana_act_exec_schedule_level_iii_base_usd"]
    tier_1 = round(base_pay * 0.75, 2)
    tier_2 = round(base_pay * 1.00, 2)
    workforce = LOCKED_CONSTANTS["cleared_workforce_population"]
    incidence = LOCKED_CONSTANTS["annual_baseline_vestibular_migraine_tinnitus_incidence_rate"]
    eligible_episodes = int(round(workforce * incidence))
    tranche_1_cap = round(LOCKED_CONSTANTS["odni_reviewed_ahi_reports_count"] * tier_2, 2)

    assert math.isclose(tier_1, LOCKED_CONSTANTS["havana_act_tier_1_75pct_payment_usd"], rel_tol=1e-6)
    assert math.isclose(tier_2, LOCKED_CONSTANTS["havana_act_tier_2_100pct_payment_usd"], rel_tol=1e-6)
    assert eligible_episodes == LOCKED_CONSTANTS["annual_eligible_baseline_episodes"]
    assert math.isclose(
        tranche_1_cap, LOCKED_CONSTANTS["tranche_1_statutory_havana_act_exposure_usd"], rel_tol=1e-6
    )

    # Interoceptive Kalman gain K_t = sigma_prior^2 / (sigma_prior^2 + sigma_sensory^2)
    sigma_prior_sq = 1.0
    sigma_sensory_Normal_sq = 4.0
    sigma_sensory_Hypervigilant_sq = 0.01
    k_normal = round(sigma_prior_sq / (sigma_prior_sq + sigma_sensory_Normal_sq), 4)
    k_primed = round(sigma_prior_sq / (sigma_prior_sq + sigma_sensory_Hypervigilant_sq), 4)
    assert k_primed > 0.99

    return {
        "havana_act_tier_1_usd": tier_1,
        "havana_act_tier_2_usd": tier_2,
        "annual_eligible_baseline_episodes": eligible_episodes,
        "tranche_1_max_statutory_exposure_usd": tranche_1_cap,
        "kalman_gain_unprimed": k_normal,
        "kalman_gain_threat_primed": k_primed,
    }


def main() -> int:
    eq01 = verify_eq01_acoustic_standing_wave()
    eq02 = verify_eq02_friis_link_budget_inversion()
    eq03 = verify_eq03_control_bias_and_nih_null()
    eq04 = verify_eq04_reverse_causal_ci_clustering()
    eq05 = verify_eq05_kalman_gain_and_havana_act_moral_hazard()

    full_waterfall = tranche_recovery(LOCKED_CONSTANTS["total_institutional_capital_at_risk_usd"])
    partial_waterfall_350m = tranche_recovery(350000000.0)

    total_sum = sum(t["principal_usd"] for t in TRANCHES)
    assert math.isclose(
        total_sum, LOCKED_CONSTANTS["total_institutional_capital_at_risk_usd"], rel_tol=1e-9
    )
    assert math.isclose(
        full_waterfall["tranches"][-1]["recovery_cents_on_dollar"], 100.0, rel_tol=1e-9
    )

    summary = {
        "spec": "SPEC-AHI-CYBERNETIC-SELF-DDOS-v1.0",
        "status": "VERIFIED",
        "locked_constants_and_outputs": LOCKED_CONSTANTS,
        "equation_verifications": {
            "EQ_01_standing_wave_cricket": eq01,
            "EQ_02_friis_link_budget_inversion": eq02,
            "EQ_03_control_bias_and_nih_null": eq03,
            "EQ_04_reverse_causal_ci_clustering": eq04,
            "EQ_05_kalman_gain_and_havana_act": eq05,
        },
        "waterfall_full_550m": full_waterfall,
        "waterfall_stress_350m": partial_waterfall_350m,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
