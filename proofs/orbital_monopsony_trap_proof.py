#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Orbital Monopsony Trap - deterministic locked-constants proof engine.

Canonical Specification: SPEC-ORBITAL-MONOPSONY-TRAP-v1.0
Canonical Schema: urn:opstack:schema:orbital_monopsony_trap.json

Verifies every locked numerical identity of the orbital monopsony trap
bundle to exact presentation precision:

1. NSSL Phase 3 Lane 2 inverse-cost viability transfer (10 U.S.C.
   Sec. 2273(b)(1)): 54 missions / $13,680.0M total award across SpaceX
   (28), ULA (19), and Blue Origin (7); per-mission prices, mission-share
   vs dollar-share spreads, and statutory competitor viability subsidies
   over the SpaceX per-mission baseline.
2. SpaceX (SPCX) Q3 2026 financials and FAR 15.404-4 / 10 U.S.C. Sec. 3702
   regulated defense-utility valuation compression of the $1,881,978.5M
   diluted market capitalization.
3. Parameterized absolute-priority fulcrum waterfall tranche_recovery(ev)
   across the $78,844.0M senior fixed-claim stack, including the Apollo
   Global Management 5-year GPU master finance lease for SpaceX.AI LLC /
   xAI compute (Form 8-K accession 0001104659-26-118614, 2026-10-26).
4. Alphabet (GOOGL) Note 12 / ASC 820-10-35-6B liquidity-blind
   restricted-security fair-value mark and the 2026-12-09 non-affiliate
   lockup overhang (551,189,500 Class A = 86.2731% of the 638,888,888-share
   IPO public float).

Pure Python 3 standard library only (json, math, sys, dataclasses,
typing). Emits a clean JSON proof receipt to stdout and exits 0 iff every
locked identity reproduces exactly.

Units: usd_m = USD millions; pct = percent; c_on_dollar = cents on the
dollar; x = multiple.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from typing import Any, Dict, List

TOL = 1e-9


def close(label: str, computed: float, locked: float, n: int = 4) -> float:
    """Assert `computed` equals `locked` at n-decimal presentation precision."""
    rc = round(float(computed), n)
    if math.fabs(rc - float(locked)) >= TOL:
        raise AssertionError(
            f"{label}: computed {rc!r} != locked {locked!r} (n={n})"
        )
    return rc


# ---------------------------------------------------------------------------
# Section 1 - NSSL Phase 3 Lane 2 inverse-cost viability transfer
#            (10 U.S.C. Sec. 2273(b)(1))
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Lane2Provider:
    provider: str
    missions: int
    award_usd_m: float

    @property
    def price_per_mission_usd_m(self) -> float:
        return self.award_usd_m / self.missions


LANE2_PROVIDERS: List[Lane2Provider] = [
    Lane2Provider("spacex", 28, 5920.0),
    Lane2Provider("ula", 19, 5370.0),
    Lane2Provider("blue_origin", 7, 2390.0),
]

LANE2_LOCKED_PRICE_USD_M: Dict[str, float] = {
    "spacex": 211.4286,
    "ula": 282.6316,
    "blue_origin": 341.4286,
}

LANE2_LOCKED_SHARES_PCT: Dict[str, Dict[str, float]] = {
    "spacex": {"mission_share_pct": 51.8519, "dollar_share_pct": 43.2749,
               "dollar_minus_mission_share_pct": -8.5770},
    "ula": {"mission_share_pct": 35.1852, "dollar_share_pct": 39.2544,
            "dollar_minus_mission_share_pct": 4.0692},
    "blue_origin": {"mission_share_pct": 12.9630, "dollar_share_pct": 17.4708,
                    "dollar_minus_mission_share_pct": 4.5078},
}

LANE2_LOCKED_SUBSIDY_USD_M: Dict[str, float] = {
    "spacex": 0.0,
    "ula": 1352.8571,
    "blue_origin": 910.0,
}


def verify_lane2() -> Dict[str, Any]:
    total_missions = sum(p.missions for p in LANE2_PROVIDERS)
    total_award = sum(p.award_usd_m for p in LANE2_PROVIDERS)
    assert total_missions == 54
    close("lane2.total_award_usd_m", total_award, 13680.0, 1)

    baseline = LANE2_PROVIDERS[0].price_per_mission_usd_m
    providers: Dict[str, Any] = {}
    subsidy_total = 0.0
    for p in LANE2_PROVIDERS:
        mission_share = p.missions / total_missions * 100.0
        dollar_share = p.award_usd_m / total_award * 100.0
        # Locked sign convention: dollar_share - mission_share (negative =
        # per-mission price below the award's dollar-weighted share).
        spread = dollar_share - mission_share
        subsidy = p.missions * (p.price_per_mission_usd_m - baseline)
        lock = LANE2_LOCKED_SHARES_PCT[p.provider]
        close(f"lane2.{p.provider}.price_per_mission_usd_m",
              p.price_per_mission_usd_m, LANE2_LOCKED_PRICE_USD_M[p.provider])
        close(f"lane2.{p.provider}.mission_share_pct",
              mission_share, lock["mission_share_pct"])
        close(f"lane2.{p.provider}.dollar_share_pct",
              dollar_share, lock["dollar_share_pct"])
        close(f"lane2.{p.provider}.dollar_minus_mission_share_pct",
              spread, lock["dollar_minus_mission_share_pct"])
        close(f"lane2.{p.provider}.viability_subsidy_vs_spacex_baseline_usd_m",
              subsidy, LANE2_LOCKED_SUBSIDY_USD_M[p.provider])
        subsidy_total += subsidy
        providers[p.provider] = {
            "missions": p.missions,
            "award_usd_m": p.award_usd_m,
            "price_per_mission_usd_m": round(p.price_per_mission_usd_m, 4),
            "mission_share_pct": round(mission_share, 4),
            "dollar_share_pct": round(dollar_share, 4),
            "dollar_minus_mission_share_pct": round(spread, 4),
            "viability_subsidy_vs_spacex_baseline_usd_m": round(subsidy, 4),
        }

    close("lane2.statutory_competitor_viability_subsidy_total_usd_m",
          subsidy_total, 2262.8571)
    return {
        "statutory_basis": "10 U.S.C. Sec. 2273(b)(1)",
        "total_missions": total_missions,
        "total_award_usd_m": round(total_award, 1),
        "weighted_avg_price_per_mission_usd_m": close(
            "lane2.weighted_avg_price_per_mission_usd_m",
            total_award / total_missions, 253.3333),
        "spacex_baseline_price_per_mission_usd_m": round(baseline, 4),
        "providers": providers,
        "statutory_competitor_viability_subsidy_usd_m": {
            "ula": round(providers["ula"]
                         ["viability_subsidy_vs_spacex_baseline_usd_m"], 2),
            "blue_origin": round(providers["blue_origin"]
                                 ["viability_subsidy_vs_spacex_baseline_usd_m"], 2),
            "total": round(subsidy_total, 2),
        },
    }


# ---------------------------------------------------------------------------
# Section 2 - SpaceX Q3 2026 financials and FAR 15.404-4 valuation compression
# ---------------------------------------------------------------------------

SPACEX_IPO_DATE = "2026-06-12"
SPACEX_IPO_CLASS_A_SHARES = 638_888_888
SPACEX_IPO_PRICE_USD = 135.00
SPACEX_Q3_CLOSE_USD = 150.86
SPACEX_DILUTED_WASO_M = 12475.0
SPACEX_Q3_MARKET_CAP_USD_M = SPACEX_Q3_CLOSE_USD * SPACEX_DILUTED_WASO_M
BLENDED_UTILITY_CEILING_USD_M = 135000.0
FAR_EBIT_CAP_PCT = 12.5
STATUTORY_TAX_PCT = 21.0
DEFENSE_PRIME_EV_NOPAT_X = 18.0
ANNUALIZATION_FACTOR = 4.0


def verify_spacex_q3_2026() -> Dict[str, Any]:
    q3_rev, q3_gross, q3_opinc = 14575.0, 9097.0, 2791.0
    m_rev, m_opinc, m_net = 27083.0, 705.0, -413.0

    close("spacex.q3_2026_market_cap_usd_m",
          SPACEX_Q3_MARKET_CAP_USD_M, 1881978.5, 1)
    close("spacex.ipo_gross_proceeds_usd_m",
          SPACEX_IPO_CLASS_A_SHARES * SPACEX_IPO_PRICE_USD / 1e6, 86250.0, 1)
    close("spacex.q3_2026_operating_margin_pct",
          q3_opinc / q3_rev * 100.0, 19.1492)
    close("spacex.q3_2026_gross_margin_pct",
          q3_gross / q3_rev * 100.0, 62.4151)

    annualized = q3_rev * ANNUALIZATION_FACTOR
    close("far.annualized_revenue_base_usd_m", annualized, 58300.0, 1)
    capped_ebit = annualized * FAR_EBIT_CAP_PCT / 100.0
    close("far.capped_ebit_usd_m", capped_ebit, 7287.5, 2)
    nopat = capped_ebit * (1.0 - STATUTORY_TAX_PCT / 100.0)
    close("far.nopat_usd_m", nopat, 5757.1, 1)
    regulated_ev = nopat * DEFENSE_PRIME_EV_NOPAT_X
    close("far.regulated_ev_usd_m", regulated_ev, 103628.25, 2)
    comp_high = (1.0 - regulated_ev / SPACEX_Q3_MARKET_CAP_USD_M) * 100.0
    comp_low = (1.0 - BLENDED_UTILITY_CEILING_USD_M /
                SPACEX_Q3_MARKET_CAP_USD_M) * 100.0
    close("far.multiple_compression_high_pct", comp_high, 94.5, 1)
    close("far.multiple_compression_low_pct", comp_low, 92.8, 1)

    return {
        "ipo_date": SPACEX_IPO_DATE,
        "ipo_class_a_shares": SPACEX_IPO_CLASS_A_SHARES,
        "ipo_price_per_share_usd": SPACEX_IPO_PRICE_USD,
        "ipo_gross_proceeds_usd_m": round(
            SPACEX_IPO_CLASS_A_SHARES * SPACEX_IPO_PRICE_USD / 1e6, 1),
        "q3_2026_close_price_usd": SPACEX_Q3_CLOSE_USD,
        "q3_2026_diluted_waso_m": SPACEX_DILUTED_WASO_M,
        "q3_2026_market_cap_usd_m": round(SPACEX_Q3_MARKET_CAP_USD_M, 1),
        "q3_2026_revenue_usd_m": q3_rev,
        "q3_2026_gross_profit_usd_m": q3_gross,
        "q3_2026_gross_margin_pct": round(q3_gross / q3_rev * 100.0, 4),
        "q3_2026_operating_income_usd_m": q3_opinc,
        "q3_2026_operating_margin_pct": round(q3_opinc / q3_rev * 100.0, 4),
        "nine_month_2026_revenue_usd_m": m_rev,
        "nine_month_2026_operating_income_usd_m": m_opinc,
        "nine_month_2026_gaap_net_loss_usd_m": m_net,
        "far_15_404_4_regulated_valuation": {
            "statutory_basis": "FAR 15.404-4 / 10 U.S.C. Sec. 3702",
            "annualized_revenue_base_usd_m": round(annualized, 1),
            "weighted_guidelines_ebit_cap_pct": FAR_EBIT_CAP_PCT,
            "capped_ebit_usd_m": round(capped_ebit, 2),
            "statutory_tax_rate_pct": STATUTORY_TAX_PCT,
            "nopat_usd_m": round(nopat, 1),
            "defense_prime_ev_nopat_multiple_x": DEFENSE_PRIME_EV_NOPAT_X,
            "regulated_ev_usd_m": round(regulated_ev, 2),
            "blended_utility_ceiling_usd_m": BLENDED_UTILITY_CEILING_USD_M,
            "multiple_compression_low_pct": round(comp_low, 1),
            "multiple_compression_high_pct": round(comp_high, 1),
        },
    }


# ---------------------------------------------------------------------------
# Section 3 - Parameterized fulcrum waterfall tranche_recovery(ev)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WaterfallTranche:
    key: str
    claim_usd_m: float


WATERFALL_TRANCHES: List[WaterfallTranche] = [
    WaterfallTranche("t1_senior_secured_term_debt_and_revolver", 18844.0),
    WaterfallTranche("t2_equipment_and_launch_pad_finance_leases", 20000.0),
    WaterfallTranche("t3_apollo_gpu_master_finance_lease", 40000.0),
]

TRANCHE_KEY_ABBREV = {
    "t1": "t1_senior_secured_term_debt_and_revolver",
    "t2": "t2_equipment_and_launch_pad_finance_leases",
    "t3": "t3_apollo_gpu_master_finance_lease",
    "t4": "t4_class_a_and_b_common_equity",
}


def tranche_recovery(ev_usd_m: float) -> Dict[str, Dict[str, float]]:
    """Parameterized absolute-priority fulcrum waterfall.

    Strict sequential allocation: T1 -> T2 -> T3, residual dollars to the
    T4 Class A & B common equity stack (12,475M diluted shares burdened by
    $48,423M non-recoverable xAI merger goodwill and -$37,448M accumulated
    deficit). Cents on the dollar for T1-T3 are measured against par
    claims; T4 cents are measured against the Q3 2026 diluted market
    capitalization (12,475M sh x $150.86 = $1,881,978.5M).
    """
    residual = float(ev_usd_m)
    out: Dict[str, Dict[str, float]] = {}
    for t in WATERFALL_TRANCHES:
        pay = max(min(residual, t.claim_usd_m), 0.0)
        out[t.key] = {
            "recovery_usd_m": round(pay, 4),
            "c_on_dollar": round(pay / t.claim_usd_m * 100.0, 4),
        }
        residual -= pay
    residual = max(residual, 0.0)
    out[TRANCHE_KEY_ABBREV["t4"]] = {
        "recovery_usd_m": round(residual, 4),
        "c_on_dollar": round(
            residual / SPACEX_Q3_MARKET_CAP_USD_M * 100.0, 4),
        "residual_per_diluted_share_usd": round(
            residual / SPACEX_DILUTED_WASO_M, 4),
    }
    return out


WATERFALL_LOCKED: Dict[float, Dict[str, tuple]] = {
    40000.0: {"t1": (18844.0, 100.0), "t2": (20000.0, 100.0),
              "t3": (1156.0, 2.89), "t4": (0.0, 0.0)},
    65000.0: {"t1": (18844.0, 100.0), "t2": (20000.0, 100.0),
              "t3": (26156.0, 65.39), "t4": (0.0, 0.0)},
    100000.0: {"t1": (18844.0, 100.0), "t2": (20000.0, 100.0),
               "t3": (40000.0, 100.0), "t4": (21156.0, 1.1241)},
    135000.0: {"t1": (18844.0, 100.0), "t2": (20000.0, 100.0),
               "t3": (40000.0, 100.0), "t4": (56156.0, 2.9839)},
}


def verify_waterfall() -> Dict[str, Any]:
    claims = {t.key: t.claim_usd_m for t in WATERFALL_TRANCHES}
    total_claims = sum(claims.values())
    close("waterfall.total_senior_fixed_claims_usd_m", total_claims, 78844.0, 1)
    close("waterfall.combined_on_bs_debt_and_finance_leases_usd_m",
          claims["t1_senior_secured_term_debt_and_revolver"] +
          claims["t2_equipment_and_launch_pad_finance_leases"], 38844.0, 1)

    vectors: Dict[str, Any] = {}
    for ev, locked in WATERFALL_LOCKED.items():
        rec = tranche_recovery(ev)
        for abbrev, (locked_usd_m, locked_cents) in locked.items():
            full = TRANCHE_KEY_ABBREV[abbrev]
            close(f"waterfall.ev_{int(ev)}.{abbrev}.recovery_usd_m",
                  rec[full]["recovery_usd_m"], locked_usd_m)
            close(f"waterfall.ev_{int(ev)}.{abbrev}.c_on_dollar",
                  rec[full]["c_on_dollar"], locked_cents)
        vectors[f"ev_{int(ev)}"] = rec

    return {
        "allocation_rule": "absolute_priority_sequential_t1_t2_t3_residual_to_t4",
        "tranche_claim_stack_usd_m": {
            **{k: round(v, 1) for k, v in claims.items()},
            "combined_on_balance_sheet_debt_and_finance_leases":
                round(claims["t1_senior_secured_term_debt_and_revolver"] +
                      claims["t2_equipment_and_launch_pad_finance_leases"], 1),
            "total_senior_fixed_claims": round(total_claims, 1),
        },
        "breakeven_full_recovery_ev_usd_m": round(total_claims, 1),
        "t4_cents_denominator_market_cap_usd_m":
            round(SPACEX_Q3_MARKET_CAP_USD_M, 1),
        "recovery_vectors": vectors,
    }


# ---------------------------------------------------------------------------
# Section 4 - Alphabet Note 12 / ASC 820-10-35-6B lockup overhang
# ---------------------------------------------------------------------------

GOOGL_13G_DATE = "2026-08-14"
GOOGL_13G_SHARES = 551_189_500
GOOGL_PCT_OF_CLASS_A = 7.2
GOOGL_JAN_2015_COST_BASIS_USD_M = 900.0
GOOGL_RESTRICTED_SHARES = 498_480_000
GOOGL_DILUTED_SHARES = 12_485_000_000
GOOGL_MARKETABLE_EQUITY_LOSS_USD_M = 12400.0  # Alphabet's -$12.4B Q3 2026 loss
TAX_EFFECT_RETENTION = 1.0 - 0.182
LOCKUP_EXPIRY = "2026-12-09"


def verify_alphabet_note12() -> Dict[str, Any]:
    unlocked = GOOGL_13G_SHARES - GOOGL_RESTRICTED_SHARES
    assert unlocked == 52_709_500, unlocked

    restricted_value_m = GOOGL_RESTRICTED_SHARES * SPACEX_Q3_CLOSE_USD / 1e6
    unlocked_value_m = unlocked * SPACEX_Q3_CLOSE_USD / 1e6
    close("googl.restricted_fair_value_usd_m", restricted_value_m, 75200.69, 2)
    close("googl.unlocked_fair_value_usd_m", unlocked_value_m, 7951.76, 2)

    drop_per_share = SPACEX_Q3_CLOSE_USD - 170.86
    close("googl.q3_2026_price_drop_per_share_usd", drop_per_share, -20.0, 2)
    pretax_mark_loss_m = GOOGL_13G_SHARES * drop_per_share / 1e6
    close("googl.pretax_mark_loss_usd_m", pretax_mark_loss_m, -11023.79, 2)

    pct_of_googl_loss = math.fabs(pretax_mark_loss_m) / \
        GOOGL_MARKETABLE_EQUITY_LOSS_USD_M * 100.0
    close("googl.pct_of_googl_q3_2026_marketable_equity_loss_pct",
          pct_of_googl_loss, 88.90, 2)

    eps_sens = GOOGL_13G_SHARES * TAX_EFFECT_RETENTION / GOOGL_DILUTED_SHARES
    close("googl.eps_sensitivity_per_1d_spcx_move_usd", eps_sens, 0.036113, 6)

    overhang_pct = GOOGL_13G_SHARES / SPACEX_IPO_CLASS_A_SHARES * 100.0
    close("googl.lockup_overhang_ratio_pct", overhang_pct, 86.2731)

    return {
        "schedule_13g_date": GOOGL_13G_DATE,
        "asc_820_10_35_6b_measurement_basis":
            "liquidity_blind_restricted_security_fair_value_at_close_price",
        "schedule_13g_class_a_shares": GOOGL_13G_SHARES,
        "pct_of_class_a_pct": GOOGL_PCT_OF_CLASS_A,
        "jan_2015_cost_basis_usd_m": GOOGL_JAN_2015_COST_BASIS_USD_M,
        "q3_2026_spcx_close_price_usd": SPACEX_Q3_CLOSE_USD,
        "restricted_shares": GOOGL_RESTRICTED_SHARES,
        "restricted_fair_value_usd_m": round(restricted_value_m, 2),
        "unlocked_shares_q3_2026": unlocked,
        "unlocked_fair_value_usd_m": round(unlocked_value_m, 2),
        "q3_2026_price_drop_from_usd": 170.86,
        "q3_2026_price_drop_per_share_usd": round(drop_per_share, 2),
        "pretax_mark_loss_usd_m": round(pretax_mark_loss_m, 2),
        "pct_of_googl_q3_2026_marketable_equity_loss_pct":
            round(pct_of_googl_loss, 2),
        "googl_diluted_shares": GOOGL_DILUTED_SHARES,
        "tax_effected_retention_pct": round(TAX_EFFECT_RETENTION * 100.0, 1),
        "eps_sensitivity_per_1d_spcx_move_usd": round(eps_sens, 6),
        "lockup_expiration_date": LOCKUP_EXPIRY,
        "lockup_overhang_ratio_pct": round(overhang_pct, 4),
    }


# ---------------------------------------------------------------------------
# 6-Category multi-counterparty security-master cross-index
# ---------------------------------------------------------------------------

ENTITY_AND_INSTRUMENT_IDS: Dict[str, Any] = {
    "ring_1_primary_target_gp_sponsor": {
        "ring_description":
            "Primary launch-service targets: NSSL Phase 3 Lane 2 awardees and the SPCX IPO issuer.",
        "entities": [
            {"legal_name": "SpaceX", "ticker": "SPCX", "cik": "0001181412",
             "instrument_or_mandate":
                 "NSSL Phase 3 Lane 2 (28 missions / $5,920.0M); Class A IPO "
                 "2026-06-12 (638,888,888 sh @ $135.00)"},
            {"legal_name": "United Launch Alliance LLC",
             "instrument_or_mandate":
                 "NSSL Phase 3 Lane 2 (19 missions / $5,370.0M); JV of Boeing "
                 "(BA, CIK 0000012927) and Lockheed Martin (LMT, CIK 0000936468)"},
            {"legal_name": "Blue Origin LLC",
             "instrument_or_mandate":
                 "NSSL Phase 3 Lane 2 (7 missions / $2,390.0M)"},
        ],
    },
    "ring_2_public_bdc_co_lenders_and_credit_funds": {
        "ring_description":
            "Public BDC / credit-fund co-lender Schedule-of-Investments cross-index (NPORT-P / 10-Q).",
        "entities": [
            {"legal_name": "SPCX senior facility co-lender syndicate "
                           "(undisclosed in the Q3 2026 10-Q debt footnote)",
             "instrument_or_mandate":
                 "Tranche 1 $18,844.0M senior secured term debt and revolving "
                 "credit / working capital facilities; Schedule of Investments "
                 "cross-index reserved (OBDC / ARCC / FSK / BXSL / PSEC class)"},
        ],
    },
    "ring_3_regulated_insurer_and_bermuda_sidecar_counterparties": {
        "ring_description":
            "NAIC / Schedule BA regulated balance sheets and Bermuda sidecar counterparties.",
        "entities": [
            {"legal_name": "Apollo Global Management, Inc.",
             "ticker": "APO", "cik": "0001858681",
             "instrument_or_mandate":
                 "Tranche 3 five-year GPU master finance lease, $40,000.0M "
                 "(SpaceX.AI LLC / xAI compute; Form 8-K accession "
                 "0001104659-26-118614, 2026-10-26)"},
        ],
    },
    "ring_4_pcaob_auditors_valuation_agents_and_fund_admins": {
        "ring_description":
            "PCAOB auditors, valuation agents, and fund administrators for the SPCX IPO and Q3 2026 10-Q.",
        "entities": [
            {"legal_name": "SPCX IPO underwriter syndicate and PCAOB "
                           "independent auditor (per FY2026 10-K signature)",
             "instrument_or_mandate":
                 "IPO due-diligence comfort letters and PCAOB audit opinions "
                 "over the $78,844.0M senior fixed-claim stack"},
        ],
    },
    "ring_5_foia_subject_public_pension_lp_swf_and_gatekeeper_consultants": {
        "ring_description":
            "FOIA-subject public pension LP, SWF, and gatekeeper consultant exposure to pre-IPO SpaceX paper.",
        "entities": [
            {"legal_name": "Pre-IPO SpaceX / xAI fund holders surfaced via "
                           "Alphabet Schedule 13G (2026-08-14) and FOIA-subject LP packets",
             "instrument_or_mandate":
                 "551,189,500 SPCX Class A (7.2% of Class A; $900.0M Jan 2015 "
                 "cost basis); DPI / TVPI committee packets (CalPERS / CalSTRS "
                 "/ WSIB / PSERS class)"},
        ],
    },
    "ring_6_indenture_trustees_admin_agents_rating_agencies_and_restructuring_counsel": {
        "ring_description":
            "Indenture trustees, administrative agents, rating agencies, and restructuring / litigation counsel.",
        "entities": [
            {"legal_name": "Tranche 1-3 indenture trustees and administrative "
                           "agents (per Q3 2026 10-Q and 8-K 0001104659-26-118614)",
             "instrument_or_mandate":
                 "Apollo GPU master lease admin agent and senior facility agent "
                 "roles; rating agency coverage reserved (Moody's / S&P / KBRA / "
                 "Egan-Jones); Wilmington Trust / U.S. Bank class"},
        ],
    },
}


CATALYST_CALENDAR: List[Dict[str, str]] = [
    {"date": "2026-06-12",
     "event": "SPCX IPO: 638,888,888 Class A @ $135.00 ($86,250.0M gross proceeds)."},
    {"date": "2026-08-14",
     "event": "Alphabet Schedule 13G: 551,189,500 SPCX Class A (7.2% of Class A; "
              "$900.0M Jan 2015 cost basis)."},
    {"date": "2026-09-30",
     "event": "Q3 2026 close: SPCX $150.86; 12,475M diluted WASO; "
              "$1,881,978.5M market cap; Note 12 restricted mark $75.2B."},
    {"date": "2026-10-26",
     "event": "Form 8-K accession 0001104659-26-118614: Apollo 5-year GPU "
              "master finance lease, $40,000.0M (SpaceX.AI LLC compute)."},
    {"date": "2026-12-09",
     "event": "180-day IPO lockup expiration: 551,189,500 non-affiliate shares "
              "= 86.2731% of the 638,888,888-share IPO float."},
    {"date": "2026-12-31",
     "event": "FY2026 Form 10-K filing window: FAR 15.404-4 weighted-guidelines "
              "repricing data for the regulated defense-utility ceiling."},
    {"date": "2027-09-30",
     "event": "Q3 2027 YoY NSSL Phase 3 Lane 2 task-order burn-down review "
              "(10 U.S.C. Sec. 2273(b)(1) inverse-cost viability transfer re-test)."},
]


def main() -> int:
    receipt: Dict[str, Any] = {
        "specification_id": "SPEC-ORBITAL-MONOPSONY-TRAP-v1.0",
        "schema_id": "urn:opstack:schema:orbital_monopsony_trap.json",
        "proof_engine": "proofs/orbital_monopsony_trap_proof.py",
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "itar_ear_public_domain_attestation": True,
        "entity_and_instrument_ids": ENTITY_AND_INSTRUMENT_IDS,
        "nssl_phase3_lane2_procurement_matrix": verify_lane2(),
        "spacex_q3_2026_valuation_compression": verify_spacex_q3_2026(),
        "tranche_recovery_waterfall": verify_waterfall(),
        "alphabet_note12_asc820_overhang": verify_alphabet_note12(),
        "catalyst_calendar": CATALYST_CALENDAR,
        "all_locked_identities_verified": True,
    }
    sys.stdout.write(json.dumps(receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())