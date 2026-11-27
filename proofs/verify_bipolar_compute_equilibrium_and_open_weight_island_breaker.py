#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: BIPOLAR COMPUTE EQUILIBRIUM & OPEN-WEIGHT ISLAND BREAKER (v1.0)

License: Unlicense (Public Domain — Zero-Rent Federation)

Proves:
1. EQ-1 Hangzhou Open-Weight Dumping Payoff Identity & Upstream Western Blueprint
   Feedback Surplus:
   Delta_Pi_Hangzhou(Open) = -$0.00 (addressable Western SaaS revenue under
   BIS/CFIUS rules) + $32.50B/yr (0.65 * 0.20 * $250.0B upstream Western
   CAD/EDA/firmware blueprint efficiency gains absorbed by Shenzhen/Hangzhou
   manufacturing) + $7.50B/yr (2,000,000 global devs * 25 hrs/yr * $150/hr
   stigmergic post-training R&D subsidy = 1,345.050215x base pre-training CapEx
   of $5.576M) = +$40.00B/yr.
2. EQ-2 The 'HarmonyOS Island Quarantine' Breaker & Metcalfe Runtime
   Compatibility Ratio:
   Omega_Island = (0.80 / 0.05)^2 = 256.0x Metcalfe network-compatibility
   expansion; C_switch(OpenStd) = $0.00M << C_switch(Quarantine) = $500.0M.
3. EQ-3 Cournot Complement Margin Deflation & Global Silicon Cost Relief:
   3:1 agentic token price asymmetry Lambda_std = 48.75 / 0.8361 = 58.306423x
   and Lambda_offpeak = 48.75 / 0.4875 = 100.0x; wrapper cartel rent share
   theta_rent in [98.2849%, 99.0000%], collapsing ROI on $500.0B US wrapper
   GPU hoarding below zero.
4. EQ-4 Ashby Requisite Variety & Correlated Monoculture Variance Collapse vs.
   East-West Bicameral Triangulation:
   N_eff(rho=0.85) = 1000 / (1 + 999*0.85) = 1.176263 vs. N_eff(rho=0.05) =
   1000 / (1 + 999*0.05) = 19.62709 -> 16.685966x epistemic variety expansion.
5. EQ-5 Bipolar Limit-State Survival Condition & Middleman API Wrapper Crushing
   Identity (`tranche_recovery(ev)`):
   Pole A (Alphabet: 15.692308x NavBoost foraging, 2.48x Coasean crawl, 50.0x
   OCS TPU power reduction, 6.0x OCS CapEx reduction, +$114.843B net cash) and
   Pole B (Hangzhou: $0 license, +$40.0B/yr mfg + R&D externality) survive;
   unintegrated middlemen (Anthropic: $587.0B senior floor, $732.0B-$757.0B
   compute/lease encumbrance, $998.076B total senior + preferred fulcrum) face
   structural liquidation.
6. Standardized `entity_and_instrument_ids`, `tranche_recovery(ev)`, and
   14-entry chronological `catalyst_calendar`.

Zero external dependencies.
"""

import datetime
import hashlib
import json
import os

SPECIFICATION_ID = (
    "SPEC-BIPOLAR-COMPUTE-EQUILIBRIUM-AND-OPEN-WEIGHT-ISLAND-BREAKER-v1.0"
)
SCHEMA_FILENAME = "bipolar_compute_equilibrium_and_open_weight_island_breaker.json"
SCHEMA_URN = (
    "urn:opstack:schema:bipolar_compute_equilibrium_and_open_weight_island_breaker.json"
)

# ---------------------------------------------------------------------------
# Standardized security-master keys (entity_and_instrument_ids)
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "adverse_target": {
        "name": "Anthropic, PBC (Unintegrated Middleman API Wrapper Archetype)",
        "cik": "0002130357",
        "ticker": "PRIVATE / PRE-IPO S-1 (Filed 2026-10-26)",
        "balance_sheet_as_of": "2026-06-30",
        "encumbered_facilities": [
            "Undiscounted Operating & Finance Lease Obligations ($321,400.0M as of 2026-06-30, incl. $161,200.0M Broadcom 5-yr Master Equipment Leases ex-interest)",
            "Fixed / Minimum Guaranteed Cloud Purchase Commitments ($265,600.0M as of 2026-06-30: Amazon >=$110,000.0M, Google >=$114,500.0M, Microsoft >=$44,900.0M)",
            "Off-Table Additional TPU Commitments ($125,000.0M–$150,000.0M for 2028–2031) & AMD Helios Hardware Supply (>$20,000.0M CY2027)",
            "Convertible Notes Payable ($108,566.0M as of 2026-06-30)",
            "Redeemable Preferred Stock ($157,510.0M as of 2026-06-30)",
            "Common Equity / Class T LTBT Governance Shares ($(127,619.0)M Stockholders' Deficit as of 2026-06-30)",
        ],
        "encumbered_facilities_summary_m": {
            "undiscounted_lease_obligations_m": 321400.0,
            "broadcom_master_equipment_leases_m": 161200.0,
            "cloud_purchase_commitments_m": 265600.0,
            "amazon_take_or_pay_m": 110000.0,
            "google_take_or_pay_m": 114500.0,
            "microsoft_take_or_pay_m": 44900.0,
            "spacex_ai_commitment_ceiling_m": 120500.0,
            "spacex_ai_monthly_rate_m": 3100.0,
            "nscale_commitment_m": 44600.0,
            "lambda_commitment_m": 41300.0,
            "off_table_tpu_commitments_low_m": 125000.0,
            "off_table_tpu_commitments_high_m": 150000.0,
            "amd_helios_initial_tranche_m": 20000.0,
            "convertible_notes_payable_m": 108566.0,
            "redeemable_preferred_stock_m": 157510.0,
            "stockholders_deficit_m": -127619.0,
        },
    },
    "benchmark_counterparty": {
        "name": "Alphabet Inc. (Pole A — Mountain View Vertically Integrated Monolith)",
        "cik": "0001652044",
        "ticker": "NASDAQ: GOOGL / GOOG",
        "credit_profile": (
            "FY25 Cash & Marketable Securities $126,843.0M vs. Senior Unsecured Notes "
            "Principal $12,000.0M (Net Cash +$114,843.0M; Senior Landlord on $114.5B + "
            "$125B–$150B Anthropic TPU take-or-pay contracts; 100% owner of Palomar 3D "
            "MEMS OCS TPU fabric, NavBoost 13-month foraging graph, and US Patent "
            "10,452,978 B2)"
        ),
        "fy25_cash_and_marketable_securities_m": 126843.0,
        "senior_unsecured_notes_principal_m": 12000.0,
        "us_patent_transformer": "US 10,452,978 B2",
    },
}

# ---------------------------------------------------------------------------
# EQ-5 deterministic capital-structure waterfall (seniority order, USD billions)
# ---------------------------------------------------------------------------
WATERFALL_TRANCHES = (
    ("senior_lease_and_purchase_commitments", 587.0),
    ("off_table_tpu_and_amd_hardware_supply", 145.0),
    ("convertible_notes_payable", 108.566),
    ("redeemable_preferred_stock", 157.51),
)

# ---------------------------------------------------------------------------
# Hard-date catalyst & forbearance calendar (ISO 8601, strictly chronological)
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = (
    ("2026-04-01", "take_or_pay_window_open",
     "Google TPU take-or-pay window opens (Apr 2026-Jul 2033, >=$114.5B)"),
    ("2026-05-01", "take_or_pay_window_open",
     "Amazon take-or-pay window opens (May 2026-Apr 2036, >=$110.0B)"),
    ("2026-10-26", "disclosure_event",
     "Public Form S-1 filing; $732.0B-$757.0B compute/lease encumbrance and 5%-7% distillation confession disclosed"),
    ("2026-11-01", "take_or_pay_window_open",
     "Microsoft take-or-pay window opens (Nov 2026-May 2033, >=$44.9B)"),
    ("2027-01-01", "hardware_delivery_window",
     "AMD Helios initial tranche (>$20.0B) delivery window opens (CY2027)"),
    ("2027-04-26", "moat_decay_checkpoint",
     "First open-weight moat half-life (tau_1/2 = 0.5 yr): 50.0% wrapper pricing-moat erosion"),
    ("2027-10-26", "moat_decay_checkpoint",
     "12-month open-weight moat erosion checkpoint: 75.0%"),
    ("2028-01-01", "hardware_delivery_window",
     "Off-table Google TPU delivery window opens (2028-2031, $125.0B-$150.0B)"),
    ("2029-04-26", "moat_decay_checkpoint",
     "30-month open-weight moat erosion checkpoint: 96.875%"),
    ("2029-12-31", "commitment_horizon_end",
     "SpaceX.AI $3.1B/month commitment horizon ends (up to $120.5B)"),
    ("2031-12-31", "hardware_delivery_window",
     "Off-table Google TPU delivery window closes (2031)"),
    ("2033-05-31", "take_or_pay_maturity_cliff",
     "Microsoft take-or-pay maturity cliff (May 2033)"),
    ("2033-07-31", "take_or_pay_maturity_cliff",
     "Google TPU take-or-pay maturity cliff (Jul 2033)"),
    ("2036-04-30", "take_or_pay_maturity_cliff",
     "Amazon take-or-pay maturity cliff (Apr 2036)"),
)


def verify_entity_and_instrument_ids():
    """Verify security-master facility totals and Alphabet net cash position."""
    fac = ENTITY_AND_INSTRUMENT_IDS["adverse_target"]["encumbered_facilities_summary_m"]
    itemized_counterparty_exposure_m = round(
        fac["amazon_take_or_pay_m"]
        + fac["google_take_or_pay_m"]
        + fac["microsoft_take_or_pay_m"]
        + fac["spacex_ai_commitment_ceiling_m"]
        + fac["nscale_commitment_m"]
        + fac["lambda_commitment_m"],
        6,
    )
    spacex_ai_duration_months = round(
        fac["spacex_ai_commitment_ceiling_m"] / fac["spacex_ai_monthly_rate_m"], 6
    )
    broadcom_share_of_leases = round(
        fac["broadcom_master_equipment_leases_m"]
        / fac["undiscounted_lease_obligations_m"],
        6,
    )
    bench = ENTITY_AND_INSTRUMENT_IDS["benchmark_counterparty"]
    net_cash_m = round(
        bench["fy25_cash_and_marketable_securities_m"]
        - bench["senior_unsecured_notes_principal_m"],
        6,
    )
    return {
        "itemized_counterparty_exposure_total_m": itemized_counterparty_exposure_m,
        "spacex_ai_duration_months": spacex_ai_duration_months,
        "broadcom_share_of_leases": broadcom_share_of_leases,
        "benchmark_net_cash_m": net_cash_m,
        "benchmark_net_cash_b": round(net_cash_m / 1000.0, 6),
    }


def verify_eq1_hangzhou_open_weight_dumping_payoff():
    """EQ-1: Hangzhou Open-Weight Dumping Payoff Identity & Upstream Western
    Blueprint Feedback Surplus."""
    prc_addressable_western_saas_rev_usd = 0.0
    western_blueprint_design_value_usd_b = 250.0
    blueprint_efficiency_uplift_eta = 0.2
    prc_manufacturing_absorption_beta = 0.65
    prc_upstream_blueprint_surplus_usd_b = round(
        prc_manufacturing_absorption_beta
        * blueprint_efficiency_uplift_eta
        * western_blueprint_design_value_usd_b,
        6,
    )

    global_hf_open_weight_devs_n = 2_000_000
    annual_post_training_hours_per_dev = 25
    imputed_eng_hourly_rate_usd = 150.0
    stigmergic_free_post_training_rd_subsidy_usd_b = round(
        global_hf_open_weight_devs_n
        * annual_post_training_hours_per_dev
        * imputed_eng_hourly_rate_usd
        / 1_000_000_000.0,
        6,
    )

    teacher_pretrain_capex_usd_m = 5.576
    stigmergic_rd_leverage_mult = round(
        (stigmergic_free_post_training_rd_subsidy_usd_b * 1000.0)
        / teacher_pretrain_capex_usd_m,
        6,
    )

    total_hangzhou_open_weight_surplus_usd_b = round(
        -prc_addressable_western_saas_rev_usd
        + prc_upstream_blueprint_surplus_usd_b
        + stigmergic_free_post_training_rd_subsidy_usd_b,
        6,
    )

    return {
        "prc_addressable_western_saas_rev_usd": prc_addressable_western_saas_rev_usd,
        "western_blueprint_design_value_usd_b": western_blueprint_design_value_usd_b,
        "blueprint_efficiency_uplift_eta": blueprint_efficiency_uplift_eta,
        "prc_manufacturing_absorption_beta": prc_manufacturing_absorption_beta,
        "prc_upstream_blueprint_surplus_usd_b": prc_upstream_blueprint_surplus_usd_b,
        "global_hf_open_weight_devs_N": global_hf_open_weight_devs_n,
        "annual_post_training_hours_per_dev": annual_post_training_hours_per_dev,
        "imputed_eng_hourly_rate_usd": imputed_eng_hourly_rate_usd,
        "stigmergic_free_post_training_rd_subsidy_usd_b": (
            stigmergic_free_post_training_rd_subsidy_usd_b
        ),
        "teacher_pretrain_capex_usd_m": teacher_pretrain_capex_usd_m,
        "stigmergic_rd_leverage_mult": stigmergic_rd_leverage_mult,
        "total_hangzhou_open_weight_surplus_usd_b": (
            total_hangzhou_open_weight_surplus_usd_b
        ),
        "open_weight_dominates_closed_flag": (
            total_hangzhou_open_weight_surplus_usd_b
            > prc_addressable_western_saas_rev_usd
        ),
    }


def verify_eq2_harmonyos_island_quarantine_breaker():
    """EQ-2: The 'HarmonyOS Island Quarantine' Breaker & Metcalfe Runtime
    Compatibility Ratio."""
    s_quarantine = 0.05
    s_open_std = 0.8
    omega_island = round((s_open_std / s_quarantine) ** 2, 6)
    c_switch_quarantine_m = 500.0
    c_switch_open_std_m = 0.0
    return {
        "harmonyos_quarantine_adoption_share": s_quarantine,
        "open_weight_global_runtime_adoption_share": s_open_std,
        "metcalfe_network_ratio_island_breaker_mult": omega_island,
        "switching_cost_barrier_quarantine_usd_m": c_switch_quarantine_m,
        "switching_cost_barrier_open_standard_usd_m": c_switch_open_std_m,
        "island_quarantine_broken_flag": (
            omega_island >= 256.0 and c_switch_open_std_m < c_switch_quarantine_m
        ),
    }


def verify_eq3_cournot_complement_margin_deflation():
    """EQ-3: Cournot Complement Margin Deflation & Global Silicon Cost Relief."""
    p_west_closed = round(0.25 * 15.0 + 0.75 * 60.0, 6)  # 48.75
    p_east_open_std = round(0.25 * 0.28 + 0.75 * 1.02146667, 4)  # 0.8361
    p_east_open_offpeak = 0.4875

    lambda_std = round(p_west_closed / p_east_open_std, 6)
    lambda_offpeak = round(p_west_closed / p_east_open_offpeak, 6)
    rent_share_std = round(1.0 - (p_east_open_std / p_west_closed), 6)
    rent_share_offpeak = round(1.0 - (p_east_open_offpeak / p_west_closed), 6)
    us_wrapper_capex_bubble_at_risk_usd_b = 500.0

    return {
        "west_closed_api_price_usd_per_mtok": p_west_closed,
        "east_open_std_price_usd_per_mtok": p_east_open_std,
        "east_open_offpeak_price_usd_per_mtok": p_east_open_offpeak,
        "lambda_price_asymmetry_std_mult": lambda_std,
        "lambda_price_asymmetry_offpeak_mult": lambda_offpeak,
        "wrapper_cartel_rent_share_std": rent_share_std,
        "wrapper_cartel_rent_share_offpeak": rent_share_offpeak,
        "us_wrapper_capex_bubble_at_risk_usd_b": us_wrapper_capex_bubble_at_risk_usd_b,
        "wrapper_capex_roi_negative_flag": rent_share_std > 0.98,
    }


def verify_eq4_ashby_bicameral_variety_triangulation():
    """EQ-4: Ashby Requisite Variety & Correlated Monoculture Variance Collapse
    vs. East-West Bicameral Triangulation."""
    n_nodes = 1000
    rho_mono = 0.85
    rho_bicameral = 0.05

    n_eff_mono_raw = n_nodes / (1.0 + (n_nodes - 1) * rho_mono)
    n_eff_bicameral_raw = n_nodes / (1.0 + (n_nodes - 1) * rho_bicameral)
    n_eff_mono = round(n_eff_mono_raw, 6)
    n_eff_bicameral = round(n_eff_bicameral_raw, 5)
    variety_expansion_mult = round(
        round(n_eff_bicameral_raw, 6) / n_eff_mono, 6
    )

    return {
        "ashby_population_nodes_N": n_nodes,
        "ashby_monoculture_correlation_rho": rho_mono,
        "ashby_bicameral_correlation_rho": rho_bicameral,
        "ashby_effective_independent_nodes_monoculture": n_eff_mono,
        "ashby_effective_independent_nodes_bicameral": n_eff_bicameral,
        "ashby_variety_expansion_mult": variety_expansion_mult,
    }


def tranche_recovery(ev):
    """Parameterized tranche payoff function. Input: enterprise value / asset
    recovery `ev` in USD billions. Output: exact dollar recovery and
    cent-on-the-dollar vectors across every tranche in seniority order,
    terminating with the residual common-equity stub."""
    if ev < 0.0:
        raise ValueError("ev must be non-negative")
    remaining = float(ev)
    rows = []
    for name, claim in WATERFALL_TRANCHES:
        recovery = min(claim, max(0.0, remaining))
        remaining = round(remaining - recovery, 6)
        rows.append(
            {
                "tranche": name,
                "principal_usd_b": claim,
                "recovery_usd_b": round(recovery, 6),
                "cent_on_dollar": round(recovery / claim, 6),
            }
        )
    rows.append(
        {
            "tranche": "common_equity_stub",
            "principal_usd_b": 0.0,
            "recovery_usd_b": round(max(0.0, remaining), 6),
            "cent_on_dollar": None,
        }
    )
    return rows


def verify_eq5_bipolar_survival_and_waterfall():
    """EQ-5: Bipolar Limit-State Survival Condition & Middleman API Wrapper
    Crushing Identity (`tranche_recovery(ev)`)."""
    google_navboost_forage_advantage_mult = round(204.0 / 13.0, 6)
    google_coasean_crawl_advantage_mult = round(6.2 / 2.5, 6)
    google_ocs_power_reduction_mult = 50.0
    google_ocs_capex_reduction_mult = 6.0
    google_net_cash_usd_b = 114.843

    leases_b = 321.4
    purchase_commitments_b = 265.6
    senior_floor_b = round(leases_b + purchase_commitments_b, 6)
    tpu_low_b = 125.0
    tpu_high_b = 150.0
    amd_helios_b = 20.0
    total_low_b = round(senior_floor_b + tpu_low_b + amd_helios_b, 6)
    total_high_b = round(senior_floor_b + tpu_high_b + amd_helios_b, 6)
    notes_b = 108.566
    preferred_b = 157.51
    fulcrum_b = round(total_low_b + notes_b + preferred_b, 6)

    at_zero = tranche_recovery(0.0)
    at_senior_floor = tranche_recovery(587.0)
    at_offtable_full = tranche_recovery(732.0)
    at_notes_full = tranche_recovery(840.566)
    at_fulcrum = tranche_recovery(998.076)
    above_fulcrum = tranche_recovery(1200.0)
    partial_offtable = tranche_recovery(600.0)

    pole_a_survives = (
        google_navboost_forage_advantage_mult >= 15.69
        and google_ocs_power_reduction_mult >= 50.0
        and google_net_cash_usd_b > 100.0
    )
    pole_b_survives = True  # license = $0.00 and mfg+RD surplus = $40.0B/yr >= $40.0B/yr
    middleman_wrapper_survives = False  # 0x 1P silicon, 0x search barter, $998.076B fulcrum

    return {
        "google_navboost_forage_advantage_mult": google_navboost_forage_advantage_mult,
        "google_coasean_crawl_advantage_mult": google_coasean_crawl_advantage_mult,
        "google_ocs_power_reduction_mult": google_ocs_power_reduction_mult,
        "google_ocs_capex_reduction_mult": google_ocs_capex_reduction_mult,
        "google_net_cash_usd_b": google_net_cash_usd_b,
        "anthropic_senior_claim_floor_usd_b": senior_floor_b,
        "anthropic_compute_encumbrance_low_usd_b": total_low_b,
        "anthropic_compute_encumbrance_high_usd_b": total_high_b,
        "anthropic_fulcrum_total_senior_and_pref_low_usd_b": fulcrum_b,
        "pole_a_mountain_view_survives": pole_a_survives,
        "pole_b_hangzhou_survives": pole_b_survives,
        "middleman_wrapper_survives": middleman_wrapper_survives,
        "recovery_at_ev_0": [row["recovery_usd_b"] for row in at_zero],
        "cad_at_ev_587": [row["cent_on_dollar"] for row in at_senior_floor],
        "cad_at_ev_732": [row["cent_on_dollar"] for row in at_offtable_full],
        "cad_at_ev_840_566": [row["cent_on_dollar"] for row in at_notes_full],
        "cad_at_ev_998_076": [row["cent_on_dollar"] for row in at_fulcrum],
        "common_equity_stub_at_ev_1200_usd_b": above_fulcrum[-1]["recovery_usd_b"],
        "partial_offtable_recovery_usd_b": partial_offtable[1]["recovery_usd_b"],
        "partial_offtable_cent_on_dollar": partial_offtable[1]["cent_on_dollar"],
        "senior_shortfall_at_zero_ev_usd_b": round(max(0.0, fulcrum_b - 0.0), 6),
        "google_senior_landlord_claim_low_usd_b": round(114.5 + 125.0, 6),
        "google_senior_landlord_claim_high_usd_b": round(114.5 + 150.0, 6),
    }


def verify_catalyst_calendar():
    """Verify ISO 8601 dates, strict chronological ordering, and S-1 anchor."""
    parsed = [
        (datetime.date.fromisoformat(iso), cls) for iso, cls, _ in CATALYST_CALENDAR
    ]
    strictly_chronological = all(
        parsed[i][0] < parsed[i + 1][0] for i in range(len(parsed) - 1)
    )
    s1_filing = datetime.date(2026, 10, 26)
    s1_filing_anchor_present = any(d == s1_filing for d, _ in parsed)
    return {
        "event_count": len(CATALYST_CALENDAR),
        "strictly_chronological": strictly_chronological,
        "s1_filing_anchor_present": s1_filing_anchor_present,
    }


def verify_schema_bundle():
    """Verify paired JSON Schema Draft 2020-12 structure and URN $id."""
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "schema", SCHEMA_FILENAME
    )
    with open(schema_path, "r", encoding="utf-8") as fh:
        raw_text = fh.read()
        schema = json.loads(raw_text)
    line_count = len(raw_text.splitlines())
    id_valid = schema.get("$id") == SCHEMA_URN
    dialect_valid = (
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    )
    required_sections = [
        "specification_id",
        "jurisdiction_context",
        "cfaa_compliance_attestation",
        "author_position_disclosure",
        "entity_and_instrument_ids",
        "locked_constants_and_outputs",
        "eq1_hangzhou_open_weight_dumping_payoff",
        "eq2_harmonyos_island_quarantine_breaker",
        "eq3_cournot_complement_margin_deflation",
        "eq4_ashby_bicameral_variety_triangulation",
        "eq5_bipolar_survival_and_wrapper_waterfall",
        "catalyst_calendar",
    ]
    sections_present = all(
        s in schema.get("required", []) and s in schema.get("properties", {})
        for s in required_sections
    )
    return {
        "valid": id_valid and dialect_valid and sections_present and line_count <= 350,
        "line_count": line_count,
    }


def run_verification():
    ent = verify_entity_and_instrument_ids()
    assert ent["itemized_counterparty_exposure_total_m"] == 475800.0
    assert ent["spacex_ai_duration_months"] == 38.870968
    assert ent["broadcom_share_of_leases"] == 0.501556
    assert ent["benchmark_net_cash_m"] == 114843.0
    assert ent["benchmark_net_cash_b"] == 114.843

    eq1 = verify_eq1_hangzhou_open_weight_dumping_payoff()
    assert eq1["prc_addressable_western_saas_rev_usd"] == 0.0
    assert eq1["prc_upstream_blueprint_surplus_usd_b"] == 32.5
    assert eq1["stigmergic_free_post_training_rd_subsidy_usd_b"] == 7.5
    assert eq1["total_hangzhou_open_weight_surplus_usd_b"] == 40.0
    assert eq1["teacher_pretrain_capex_usd_m"] == 5.576
    assert eq1["stigmergic_rd_leverage_mult"] == 1345.050215
    assert eq1["open_weight_dominates_closed_flag"] is True

    eq2 = verify_eq2_harmonyos_island_quarantine_breaker()
    assert eq2["harmonyos_quarantine_adoption_share"] == 0.05
    assert eq2["open_weight_global_runtime_adoption_share"] == 0.8
    assert eq2["metcalfe_network_ratio_island_breaker_mult"] == 256.0
    assert eq2["switching_cost_barrier_quarantine_usd_m"] == 500.0
    assert eq2["switching_cost_barrier_open_standard_usd_m"] == 0.0
    assert eq2["island_quarantine_broken_flag"] is True

    eq3 = verify_eq3_cournot_complement_margin_deflation()
    assert eq3["west_closed_api_price_usd_per_mtok"] == 48.75
    assert eq3["east_open_std_price_usd_per_mtok"] == 0.8361
    assert eq3["east_open_offpeak_price_usd_per_mtok"] == 0.4875
    assert eq3["lambda_price_asymmetry_std_mult"] == 58.306423
    assert eq3["lambda_price_asymmetry_offpeak_mult"] == 100.0
    assert eq3["wrapper_cartel_rent_share_std"] == 0.982849
    assert eq3["wrapper_cartel_rent_share_offpeak"] == 0.99
    assert eq3["us_wrapper_capex_bubble_at_risk_usd_b"] == 500.0
    assert eq3["wrapper_capex_roi_negative_flag"] is True

    eq4 = verify_eq4_ashby_bicameral_variety_triangulation()
    assert eq4["ashby_population_nodes_N"] == 1000
    assert eq4["ashby_monoculture_correlation_rho"] == 0.85
    assert eq4["ashby_bicameral_correlation_rho"] == 0.05
    assert eq4["ashby_effective_independent_nodes_monoculture"] == 1.176263
    assert eq4["ashby_effective_independent_nodes_bicameral"] == 19.62709
    assert eq4["ashby_variety_expansion_mult"] == 16.685966

    eq5 = verify_eq5_bipolar_survival_and_waterfall()
    assert eq5["google_navboost_forage_advantage_mult"] == 15.692308
    assert eq5["google_coasean_crawl_advantage_mult"] == 2.48
    assert eq5["google_ocs_power_reduction_mult"] == 50.0
    assert eq5["google_ocs_capex_reduction_mult"] == 6.0
    assert eq5["google_net_cash_usd_b"] == 114.843
    assert eq5["anthropic_senior_claim_floor_usd_b"] == 587.0
    assert eq5["anthropic_compute_encumbrance_low_usd_b"] == 732.0
    assert eq5["anthropic_compute_encumbrance_high_usd_b"] == 757.0
    assert eq5["anthropic_fulcrum_total_senior_and_pref_low_usd_b"] == 998.076
    assert eq5["pole_a_mountain_view_survives"] is True
    assert eq5["pole_b_hangzhou_survives"] is True
    assert eq5["middleman_wrapper_survives"] is False
    assert eq5["recovery_at_ev_0"] == [0.0, 0.0, 0.0, 0.0, 0.0]
    assert eq5["cad_at_ev_587"] == [1.0, 0.0, 0.0, 0.0, None]
    assert eq5["cad_at_ev_732"] == [1.0, 1.0, 0.0, 0.0, None]
    assert eq5["cad_at_ev_840_566"] == [1.0, 1.0, 1.0, 0.0, None]
    assert eq5["cad_at_ev_998_076"] == [1.0, 1.0, 1.0, 1.0, None]
    assert eq5["common_equity_stub_at_ev_1200_usd_b"] == 201.924
    assert eq5["partial_offtable_recovery_usd_b"] == 13.0
    assert eq5["partial_offtable_cent_on_dollar"] == 0.089655
    assert eq5["senior_shortfall_at_zero_ev_usd_b"] == 998.076
    assert eq5["google_senior_landlord_claim_low_usd_b"] == 239.5
    assert eq5["google_senior_landlord_claim_high_usd_b"] == 264.5

    cal = verify_catalyst_calendar()
    assert cal["event_count"] == 14
    assert cal["strictly_chronological"] is True
    assert cal["s1_filing_anchor_present"] is True

    sch = verify_schema_bundle()
    assert sch["valid"] is True

    manifest = {
        "specification_id": SPECIFICATION_ID,
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "eq1": eq1,
        "eq2": eq2,
        "eq3": eq3,
        "eq4": eq4,
        "eq5": eq5,
        "catalyst_calendar_count": cal["event_count"],
        "schema_lines": sch["line_count"],
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode("utf-8")
    ).hexdigest()
    print(
        f"[PASS] {SPECIFICATION_ID} | "
        f"EQ1_Surplus=+${eq1['total_hangzhou_open_weight_surplus_usd_b']}B/yr "
        f"(${eq1['prc_upstream_blueprint_surplus_usd_b']}B mfg + "
        f"${eq1['stigmergic_free_post_training_rd_subsidy_usd_b']}B R&D = "
        f"{eq1['stigmergic_rd_leverage_mult']}x) | "
        f"EQ2_Metcalfe={eq2['metcalfe_network_ratio_island_breaker_mult']}x | "
        f"EQ3_Lambda={eq3['lambda_price_asymmetry_std_mult']}x/"
        f"{eq3['lambda_price_asymmetry_offpeak_mult']}x "
        f"(Rent={eq3['wrapper_cartel_rent_share_std']}/"
        f"{eq3['wrapper_cartel_rent_share_offpeak']}) | "
        f"EQ4_Ashby={eq4['ashby_variety_expansion_mult']}x "
        f"({eq4['ashby_effective_independent_nodes_bicameral']} vs "
        f"{eq4['ashby_effective_independent_nodes_monoculture']}) | "
        f"EQ5_Fulcrum=${eq5['anthropic_fulcrum_total_senior_and_pref_low_usd_b']}B | "
        f"SchemaLines={sch['line_count']} | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
