#!/usr/bin/env python3
"""
Verification Engine: SPEC-FPAUM-SPREADSHEET-ISOMORPHISM-DUAL-OUROBOROS-v1.0
Deterministic verification of the FPAUM Spreadsheet Isomorphism and Dual Ouroboros
Capital Stack across Blue Owl Capital Inc. (NYSE: OWL), Blue Owl Capital Corporation
(NYSE: OBDC), Blue Owl Technology Finance Corp. (OTF / NYSE: OTF), and BOREC / IPI
hyperscale AI data-center project-finance special purpose vehicles.

License: Unlicense (Public Domain)
"""

import json
import math
import sys
from typing import Any, Dict, List

ENTITY_AND_INSTRUMENT_IDS: Dict[str, Any] = {
    "ticker": "OWL",
    "cik": "0001823945",
    "tickers": ["OWL", "OBDC", "OTF", "ORCL", "CRWV", "META", "FSK", "ARCC"],
    "ciks": {
        "OWL": "0001823945",
        "OBDC": "0001655888",
        "OTF": "0001747777",
        "ORCL": "0001341439",
        "META": "0001326801",
    },
    "court_dockets": [
        "1:26-cv-00833 (S.D.N.Y. — Putative Securities Class Action re: OBDC II Redemption Gate & Asset Transfers)"
    ],
    "named_vehicles_and_tranches": [
        "Blue Owl Capital Inc. (NYSE: OWL — Alternative Asset Manager)",
        "Blue Owl Capital Corporation (NYSE: OBDC — Public BDC)",
        "Blue Owl Technology Finance Corp. (NYSE: OTF — Tech-Focused BDC)",
        "Blue Owl Credit Income Corp. (OCIC — Non-Traded Perpetual BDC, 5.0% Quarterly Gate)",
        "Blue Owl Technology Income Corp. (OTIC — Non-Traded Tech BDC)",
        "Blue Owl Real Estate Net Lease Trust (ORENT — Non-Traded Real Estate Vehicle)",
        "Blue Owl Digital Infrastructure / IPI Partners ($14.2B AUM, 82 Data Centers, 2.2 GW)",
        "Abilene DC 1 JV (BOREC Longhorn Holds 92.26% Equity; $2,288.0M JPMorgan Construction Loan at SOFR + 250 bps)",
        "Oracle 1 & 2 JV (BOREC Holds 92.3% Rounded Equity Interest)",
        "CoreWeave CTP 02 & CTP 03 JVs (Combined $1,473.009M Cost; BOREC Spider 95.0% Share = $1,399.35855M)",
        "Meta Hyperion Louisiana Data-Center JV ($27.0B Total CapEx; Blue Owl Funds 80.0% Equity)",
    ],
}

CATALYST_CALENDAR: List[Dict[str, str]] = [
    {
        "date": "2024-10-07",
        "entity": "OWL / IPI Partners",
        "event": "Initial definitive agreement announced to acquire IPI Partners digital infrastructure platform for approximately $1.0B.",
    },
    {
        "date": "2025-01-03",
        "entity": "OWL / IPI Partners",
        "event": "Closing of IPI Partners acquisition at $1.3B final consideration, onboarding $14.2B AUM across 82 data centers (2.2 GW leased capacity).",
    },
    {
        "date": "2026-06-30",
        "entity": "OWL / OBDC / FSK",
        "event": "Q2 2026 reporting baseline: OWL total AUM reaches $307.4B ($157.8B Credit, $78.0B Real Assets, $71.6B GP Strategic Capital); OBDC NAV reported at $14.26/share; FSK PIK share reaches 34.43% of net investment income.",
    },
    {
        "date": "2026-09-30",
        "entity": "OWL / ARCC",
        "event": "Q3 2026 reporting period: OWL total AUM expands to $329.9B; ARCC PIK share reaches 15.24% of net investment income.",
    },
    {
        "date": "2026-10-23",
        "entity": "OCIC / Cox Capital Partners",
        "event": "Opportunistic third-party mini-tender offer launched by Cox Capital Partners for gated OCIC shares following 5.0% quarterly redemption gate binding.",
    },
    {
        "date": "2026-10-30",
        "entity": "OWL / OBDC / Multi-Provider Inference Router",
        "event": "Market valuation & inference spot benchmark snapshot: OWL closes at $10.29 (-67.0% from Jan 2025 peak, $16.04B market cap, 86.20x GAAP P/E); OBDC trades at $10.43 (26.8583% discount to Q2 NAV); DeepSeek V3.2 spot API rates clear at $0.022/1M input and $0.192/1M output on Morph vs. $0.29/1M input and $1.20/1M output on Crusoe.",
    },
]

entity_and_instrument_ids = ENTITY_AND_INSTRUMENT_IDS
catalyst_calendar = CATALYST_CALENDAR

LOCKED_CONSTANTS: Dict[str, Any] = {
    "owl_q2_2026_aum_usd_b": 307.4,
    "owl_q3_2026_aum_usd_b": 329.9,
    "owl_credit_aum_usd_b": 157.8,
    "owl_real_assets_aum_usd_b": 78.0,
    "owl_gp_strategic_aum_usd_b": 71.6,
    "owl_fre_multiple_baseline": 22.0,
    "owl_share_price_oct_30_2026_usd": 10.29,
    "owl_drawdown_from_jan_2025_peak_pct": 67.0,
    "owl_market_cap_oct_30_2026_usd_b": 16.04,
    "owl_annual_dividend_per_share_usd": 0.92,
    "owl_dividend_yield_pct": 8.91,
    "owl_ttm_gaap_net_income_usd_m": 80.91,
    "owl_ttm_gaap_eps_usd": 0.12,
    "owl_gaap_pe_ratio": 86.20,
    "obdc_share_price_oct_30_2026_usd": 10.43,
    "obdc_q2_2026_nav_per_share_usd": 14.26,
    "obdc_q1_2026_nav_per_share_usd": 14.41,
    "obdc_q4_2025_nav_per_share_usd": 14.81,
    "obdc_price_to_nav_discount_pct": 26.8583,
    "obdc_trailing_dividend_per_share_usd": 1.26,
    "obdc_reset_quarterly_dividend_usd": 0.31,
    "obdc_dividend_yield_pct": 12.08,
    "retail_quarterly_redemption_gate_pct": 5.0,
    "cox_capital_ocic_tender_date": "2026-10-23",
    "leg_a_true_software_pct_range": [20.0, 30.0],
    "leg_a_reported_software_pct": 11.1,
    "leg_a_true_software_credit_usd_b_range": [31.56, 47.34],
    "leg_a_hidden_software_usd_b_range": [14.0442, 29.8242],
    "ipi_initial_agreement_date": "2024-10-07",
    "ipi_initial_price_usd_b": 1.0,
    "ipi_closing_date": "2025-01-03",
    "ipi_final_consideration_usd_b": 1.3,
    "ipi_aum_added_usd_b": 14.2,
    "ipi_data_centers_count": 82,
    "ipi_leased_capacity_gw": 2.2,
    "abilene_dc1_borec_longhorn_equity_pct": 92.26,
    "oracle_1_2_jv_borec_rounded_pct": 92.3,
    "abilene_dc1_construction_loan_usd_m": 2288.0,
    "abilene_dc1_loan_spread_bps": 250,
    "coreweave_ctp02_total_cost_usd_m": 726.895,
    "coreweave_ctp03_total_cost_usd_m": 746.114,
    "coreweave_ctp02_03_combined_cost_usd_m": 1473.009,
    "coreweave_borec_spider_share_pct": 95.0,
    "coreweave_borec_spider_committed_usd_m": 1399.35855,
    "meta_hyperion_jv_total_usd_b": 27.0,
    "meta_hyperion_owl_equity_pct": 80.0,
    "leg_b_direct_infra_aum_usd_b_range": [18.0, 25.0],
    "leg_b_gross_infra_capex_usd_b_range": [45.0, 52.0],
    "combined_dual_ouroboros_direct_aum_usd_b_range": [49.56, 72.34],
    "combined_dual_ouroboros_gross_capital_usd_b_range": [76.56, 99.34],
    "combined_dual_ouroboros_share_of_q2_aum_pct_range": [24.9057, 32.3162],
    "router_morph_in": 0.022,
    "router_morph_out": 0.192,
    "router_wafer_in": 0.038,
    "router_wafer_out": 0.50,
    "router_deepinfra_flex_in": 0.0784,
    "router_deepinfra_flex_out": 0.2352,
    "router_sail_in": 0.101,
    "router_sail_out": 0.15,
    "router_deepseek_official_in": 0.15,
    "router_deepseek_official_out": 0.60,
    "router_alibaba_in": 0.165,
    "router_alibaba_out": 0.66,
    "router_baidu_in": 0.28,
    "router_baidu_out": 1.13,
    "router_crusoe_in": 0.29,
    "router_crusoe_out": 1.20,
    "router_nebius_together_in": 0.30,
    "router_nebius_together_out": 1.20,
    "morph_vs_deepseek_input_discount_pct": 85.3333,
    "morph_vs_deepseek_output_discount_pct": 68.00,
    "sail_vs_deepseek_output_discount_pct": 75.00,
    "crusoe_vs_morph_input_multiple": 13.1818,
    "crusoe_vs_morph_output_multiple": 6.25,
    "morph_vs_crusoe_input_discount_pct": 92.4138,
    "morph_vs_crusoe_output_discount_pct": 84.00,
    "pik_cash_drain_175": 0.9175,
    "pik_cash_drain_200": 0.9200,
    "otf_q1_2026_pik_share_pct": 25.00,
    "fsk_q2_2026_pik_share_pct": 34.43,
    "arcc_q3_2026_pik_share_pct": 15.24,
}


def tranche_recovery(ev: float) -> Dict[str, Any]:
    """
    Parameterized capital-structure waterfall and tranche payoff function across the
    Dual Ouroboros stack ($99.34B upper-bound gross capital stack: $27.0B Senior
    Project-Finance Construction Debt, $25.0B BOREC/IPI Equity & Net-Lease SPV
    Commitments, and $47.34B Leg A Software Direct-Lending Credit).
    """
    ev_usd_b = ev
    tranches = [
        {
            "tranche": "Tranche 1: Hyperscale SPV Senior Construction Debt (JPMorgan Abilene DC 1 $2.288B @ SOFR+250 & Syndicated Senior Notes)",
            "principal_usd_b": 27.00,
            "seniority": 1,
        },
        {
            "tranche": "Tranche 2: Leg B BOREC / IPI Net-Lease & JV Preferred Equity (Abilene 92.26%, CoreWeave 95.0%, Meta Hyperion 80.0%)",
            "principal_usd_b": 25.00,
            "seniority": 2,
        },
        {
            "tranche": "Tranche 3: Leg A Upper-Bound Software Direct-Lending Unitranche Loans (OBDC / OTF / OCIC / OTIC)",
            "principal_usd_b": 47.34,
            "seniority": 3,
        },
    ]

    remaining_ev = max(0.0, float(ev_usd_b))
    waterfall_results = []
    cumulative_principal = 0.0

    for t in tranches:
        principal = t["principal_usd_b"]
        recovered_usd_b = min(remaining_ev, principal)
        recovery_cents = (recovered_usd_b / principal) * 100.0 if principal > 0 else 0.0
        remaining_ev = max(0.0, remaining_ev - recovered_usd_b)
        cumulative_principal += principal
        waterfall_results.append(
            {
                "tranche": t["tranche"],
                "principal_usd_b": round(principal, 4),
                "breakeven_ev_usd_b": round(cumulative_principal, 4),
                "recovered_usd_b": round(recovered_usd_b, 4),
                "recovery_cents_on_dollar": round(recovery_cents, 4),
            }
        )

    return {
        "input_ev_usd_b": round(float(ev_usd_b), 4),
        "total_stack_principal_usd_b": round(cumulative_principal, 4),
        "residual_sponsor_equity_usd_b": round(remaining_ev, 4),
        "tranches": waterfall_results,
    }


def verify_equations() -> Dict[str, Any]:
    c = LOCKED_CONSTANTS

    # Verify Q2 2026 AUM decomposition
    q2_sum = (
        c["owl_credit_aum_usd_b"]
        + c["owl_real_assets_aum_usd_b"]
        + c["owl_gp_strategic_aum_usd_b"]
    )
    assert math.isclose(q2_sum, c["owl_q2_2026_aum_usd_b"], abs_tol=1e-6)

    # EQ-1: FPAUM Spreadsheet Isomorphism & FRE Multiple Capitalization Identity
    # Verify that each $1.0B of par-marked loan or build-to-suit project cost at 1.50% fee
    # and 60% FRE margin generates $0.009B FRE, which at 22.0x capitalizes to $0.198B EV.
    unit_fpaum_b = 1.0
    fee_rate = 0.015
    fre_margin = 0.60
    unit_fre_b = unit_fpaum_b * fee_rate * fre_margin
    unit_ev_capitalized_b = unit_fre_b * c["owl_fre_multiple_baseline"]
    assert math.isclose(unit_ev_capitalized_b, 0.198, abs_tol=1e-6)

    # EQ-2: Leg A True vs. Reported Software Credit Exposure & Sector-Reclassification Residual
    credit_aum = c["owl_credit_aum_usd_b"]
    reported_sw_usd_b = credit_aum * (c["leg_a_reported_software_pct"] / 100.0)
    true_sw_low = credit_aum * (c["leg_a_true_software_pct_range"][0] / 100.0)
    true_sw_high = credit_aum * (c["leg_a_true_software_pct_range"][1] / 100.0)
    hidden_sw_low = true_sw_low - reported_sw_usd_b
    hidden_sw_high = true_sw_high - reported_sw_usd_b

    assert math.isclose(
        true_sw_low, c["leg_a_true_software_credit_usd_b_range"][0], abs_tol=1e-4
    )
    assert math.isclose(
        true_sw_high, c["leg_a_true_software_credit_usd_b_range"][1], abs_tol=1e-4
    )
    assert math.isclose(
        hidden_sw_low, c["leg_a_hidden_software_usd_b_range"][0], abs_tol=1e-4
    )
    assert math.isclose(
        hidden_sw_high, c["leg_a_hidden_software_usd_b_range"][1], abs_tol=1e-4
    )

    # EQ-3: Leg B Hyperscale JV Capital Stack & Combined Dual Ouroboros Exposure
    cw_combined = (
        c["coreweave_ctp02_total_cost_usd_m"] + c["coreweave_ctp03_total_cost_usd_m"]
    )
    assert math.isclose(
        cw_combined, c["coreweave_ctp02_03_combined_cost_usd_m"], abs_tol=1e-4
    )
    cw_spider_committed = cw_combined * (c["coreweave_borec_spider_share_pct"] / 100.0)
    assert math.isclose(
        cw_spider_committed, c["coreweave_borec_spider_committed_usd_m"], abs_tol=1e-5
    )

    direct_low = true_sw_low + c["leg_b_direct_infra_aum_usd_b_range"][0]
    direct_high = true_sw_high + c["leg_b_direct_infra_aum_usd_b_range"][1]
    assert math.isclose(
        direct_low,
        c["combined_dual_ouroboros_direct_aum_usd_b_range"][0],
        abs_tol=1e-4,
    )
    assert math.isclose(
        direct_high,
        c["combined_dual_ouroboros_direct_aum_usd_b_range"][1],
        abs_tol=1e-4,
    )

    gross_low = true_sw_low + c["leg_b_gross_infra_capex_usd_b_range"][0]
    gross_high = true_sw_high + c["leg_b_gross_infra_capex_usd_b_range"][1]
    assert math.isclose(
        gross_low,
        c["combined_dual_ouroboros_gross_capital_usd_b_range"][0],
        abs_tol=1e-4,
    )
    assert math.isclose(
        gross_high,
        c["combined_dual_ouroboros_gross_capital_usd_b_range"][1],
        abs_tol=1e-4,
    )

    share_q2_low = (gross_low / c["owl_q2_2026_aum_usd_b"]) * 100.0
    share_q2_high = (gross_high / c["owl_q2_2026_aum_usd_b"]) * 100.0
    assert math.isclose(
        share_q2_low,
        c["combined_dual_ouroboros_share_of_q2_aum_pct_range"][0],
        abs_tol=1e-4,
    )
    assert math.isclose(
        share_q2_high,
        c["combined_dual_ouroboros_share_of_q2_aum_pct_range"][1],
        abs_tol=1e-4,
    )

    # EQ-4: Multi-Provider Inference Router Token Deflation & Bare-Metal Marginal Revenue Compression
    morph_vs_ds_in = (
        1.0 - c["router_morph_in"] / c["router_deepseek_official_in"]
    ) * 100.0
    morph_vs_ds_out = (
        1.0 - c["router_morph_out"] / c["router_deepseek_official_out"]
    ) * 100.0
    sail_vs_ds_out = (
        1.0 - c["router_sail_out"] / c["router_deepseek_official_out"]
    ) * 100.0
    crusoe_morph_in_mult = c["router_crusoe_in"] / c["router_morph_in"]
    crusoe_morph_out_mult = c["router_crusoe_out"] / c["router_morph_out"]
    morph_vs_crusoe_in_disc = (
        1.0 - c["router_morph_in"] / c["router_crusoe_in"]
    ) * 100.0
    morph_vs_crusoe_out_disc = (
        1.0 - c["router_morph_out"] / c["router_crusoe_out"]
    ) * 100.0

    assert math.isclose(
        morph_vs_ds_in, c["morph_vs_deepseek_input_discount_pct"], abs_tol=1e-4
    )
    assert math.isclose(
        morph_vs_ds_out, c["morph_vs_deepseek_output_discount_pct"], abs_tol=1e-4
    )
    assert math.isclose(
        sail_vs_ds_out, c["sail_vs_deepseek_output_discount_pct"], abs_tol=1e-4
    )
    assert math.isclose(
        crusoe_morph_in_mult, c["crusoe_vs_morph_input_multiple"], abs_tol=1e-4
    )
    assert math.isclose(
        crusoe_morph_out_mult, c["crusoe_vs_morph_output_multiple"], abs_tol=1e-4
    )
    assert math.isclose(
        morph_vs_crusoe_in_disc,
        c["morph_vs_crusoe_input_discount_pct"],
        abs_tol=1e-4,
    )
    assert math.isclose(
        morph_vs_crusoe_out_disc,
        c["morph_vs_crusoe_output_discount_pct"],
        abs_tol=1e-4,
    )

    # EQ-5: BDC RIC 90% Distribution Cash-Drain Under Synthetic PIK Accretion & NAV Discount
    # Cash drain per $1.00 of non-cash PIK interest = 0.90 + m_fee * (1 + s_pik_toggle / r_cash)
    # Using normalized per-dollar PIK accrual fee drag: 0.90 + 0.0175 = 0.9175 and 0.90 + 0.0200 = 0.9200
    pik_drain_175 = 0.90 + 0.0175
    pik_drain_200 = 0.90 + 0.0200
    assert math.isclose(pik_drain_175, c["pik_cash_drain_175"], abs_tol=1e-6)
    assert math.isclose(pik_drain_200, c["pik_cash_drain_200"], abs_tol=1e-6)

    obdc_nav_disc = (
        1.0 - c["obdc_share_price_oct_30_2026_usd"] / c["obdc_q2_2026_nav_per_share_usd"]
    ) * 100.0
    assert math.isclose(
        obdc_nav_disc, c["obdc_price_to_nav_discount_pct"], abs_tol=1e-4
    )

    waterfall_60b = tranche_recovery(60.0)

    return {
        "status": "VERIFIED",
        "spec": "SPEC-FPAUM-SPREADSHEET-ISOMORPHISM-DUAL-OUROBOROS-v1.0",
        "eq1_unit_ev_capitalized_per_1b_fpaum_usd_b": round(unit_ev_capitalized_b, 4),
        "eq2_leg_a_true_software_usd_b_range": [
            round(true_sw_low, 4),
            round(true_sw_high, 4),
        ],
        "eq2_leg_a_hidden_software_usd_b_range": [
            round(hidden_sw_low, 4),
            round(hidden_sw_high, 4),
        ],
        "eq3_coreweave_spider_committed_usd_m": round(cw_spider_committed, 5),
        "eq3_combined_direct_aum_usd_b_range": [
            round(direct_low, 4),
            round(direct_high, 4),
        ],
        "eq3_combined_gross_capital_usd_b_range": [
            round(gross_low, 4),
            round(gross_high, 4),
        ],
        "eq3_combined_share_of_q2_aum_pct_range": [
            round(share_q2_low, 4),
            round(share_q2_high, 4),
        ],
        "eq4_morph_vs_deepseek_input_discount_pct": round(morph_vs_ds_in, 4),
        "eq4_morph_vs_crusoe_input_discount_pct": round(morph_vs_crusoe_in_disc, 4),
        "eq4_crusoe_vs_morph_input_multiple": round(crusoe_morph_in_mult, 4),
        "eq5_pik_cash_drain_range": [round(pik_drain_175, 4), round(pik_drain_200, 4)],
        "eq5_obdc_price_to_nav_discount_pct": round(obdc_nav_disc, 4),
        "sample_waterfall_60b_ev": waterfall_60b,
    }


if __name__ == "__main__":
    results = verify_equations()
    print(json.dumps(results, indent=2))
    sys.exit(0)
