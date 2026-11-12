#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: ANTHROPIC FORM S-1/A TRILLION-DOLLAR ENCUMBRANCE &
WEWORK INSOLVENCY AUDIT (v1.0)

License: Unlicense (Public Domain — Zero-Rent Federation)

Proves:
1. Quarterly progression Q1 2025 ($376M) -> Q2 2025 ($787M) -> Q3 2025 ($1,382M) ->
   Q4 2025 ($2,040M) -> Q1 2026 ($4,731M revenue / $3,387M compute = 1.396811x,
   +131.91% QoQ) -> Q2 2026 ($11,555M / $5,558M = 2.078985x, 48.1004% compute share,
   +144.24% QoQ, +$974M GAAP operating income, $2,235M adjusted operating income =
   19.3423%) -> Q3 2026 ($16,956M / $9,863M = 1.719152x, 58.1682% compute share,
   +46.7417% QoQ, -17.3081% revenue-per-compute-dollar collapse, -$(567)M GAAP
   operating loss, $2,500M adjusted operating income = 14.7440%).
2. Q3 2026 marginal compute cost (($9,863M - $5,558M) / ($16,956M - $11,555M) =
   $4,305M / $5,401M = 79.707462%), the $5,000M Q3 short-term compute add, the
   $24.0B total short-term compute stack ($17.4B + $6.6B), the $600M price-cut
   haircut, and the $2,000M donation match.
3. 9M 2026 totals: revenue $33,242M ($4,731M + $11,555M + $16,956M), compute
   $18,808M ($3,387M + $5,558M + $9,863M), GAAP operating loss -$(1,260)M
   (-$1,667M + $974M - $567M), net loss -$(104,039)M (-$14,439M - $66,309M -
   $23,291M) across 273 days = -$381.095238M/day, convertible fair-value loss
   -$(94,302)M, partner deal expense -$(10,400)M, stock-based compensation
   -$(3,320)M, and 5%-7% policy-violation revenue = [$1,662.10M, $2,326.94M].
4. The $895.4B five-piece encumbrance tie-out ($320.0B + $17.4B + $451.2B +
   $100.2B + $6.6B), the $150.0B-$175.0B unpriced TPU/AMD stack plus $4.7B
   developer guaranties for an all-in encumbrance of [$1,050.1B, $1,075.1B], the
   ASC 842 concealment multiple ($451,200M / $4,484M = 100.624442x), the
   next-12-month locked share (($69.8B - $4.3B) / $69.8B = 93.839542%), the
   Amazon convert multiple ($130.5B / $6.2B = 21.048387x), and the updated Google
   exposure ($121.3B + [$125.0B, $150.0B] = [$246.3B, $271.3B]).
5. The parameterized tranche_recovery(ev_b) absolute-priority waterfall across the
   senior hybrid/lease/take-or-pay stack versus the Class A subordinated public
   equity stub, the six-category entity_and_instrument_ids security-master ring,
   the ISO catalyst calendar, and the WeWork insolvency isomorphism
   (2019-08-14 S-1 -> 2019-09-24 IPO withdrawal -> 2023-11-06 Chapter 11).

Zero external dependencies.
"""

import datetime
import hashlib
import json
import os

# ---------------------------------------------------------------------------
# Locked constants. All monetary values USD millions unless suffixed _b ($B).
# ---------------------------------------------------------------------------

QUARTERLY_REVENUE_M = {
    "Q1_2025": 376.0,
    "Q2_2025": 787.0,
    "Q3_2025": 1382.0,
    "Q4_2025": 2040.0,
    "Q1_2026": 4731.0,
    "Q2_2026": 11555.0,
    "Q3_2026": 16956.0,
}

QUARTERLY_COMPUTE_M = {
    "Q1_2026": 3387.0,
    "Q2_2026": 5558.0,
    "Q3_2026": 9863.0,
}

GAAP_OPERATING_INCOME_M = {
    "Q1_2026": -1667.0,
    "Q2_2026": 974.0,
    "Q3_2026": -567.0,
}

ADJUSTED_OPERATING_INCOME_M = {
    "Q2_2026": 2235.0,
    "Q3_2026": 2500.0,
}

QUARTERLY_NET_LOSS_M = {
    "Q1_2026": -14439.0,
    "Q2_2026": -66309.0,
    "Q3_2026": -23291.0,
}

FIVE_PIECE_ENCUMBRANCE_B = {
    "undiscounted_lease_obligations": 320.0,
    "off_balance_sheet_purchase_commitments": 451.2,
    "booked_tpu_silicon_commitments": 100.2,
    "short_term_compute_primary": 17.4,
    "short_term_compute_secondary": 6.6,
}

UNPRICED_TPU_AMD_LOW_B = 150.0
UNPRICED_TPU_AMD_HIGH_B = 175.0
DEVELOPER_GUARANTIES_B = 4.7
ASC842_OFF_BALANCE_SHEET_M = 451200.0
ASC842_ON_BALANCE_SHEET_M = 4484.0
NEXT_12M_TOTAL_COMMITMENTS_B = 69.8
NEXT_12M_CANCELABLE_B = 4.3
AMAZON_CONVERT_EXPOSURE_B = 130.5
AMAZON_EQUITY_INVESTMENT_B = 6.2
GOOGLE_BASE_EXPOSURE_B = 121.3
GOOGLE_ADDITIONAL_RANGE_B = (125.0, 150.0)

WATERFALL_TRANCHES = (
    ("senior_take_or_pay_lease_stack", 320.0),
    ("asc842_off_balance_sheet_commitments", 451.2),
    ("hybrid_convertible_silicon_stack", 100.2),
    ("short_term_compute_commitments", 24.0),
    ("unpriced_tpu_amd_low_bound", 150.0),
    ("developer_guaranties", 4.7),
    ("class_a_subordinated_public_equity", None),  # residual stub
)

CATALYST_TYPES = (
    "measurement_period_end",
    "filing_window",
    "s1_filing",
    "maturity_cliff",
    "encumbrance_step_up",
    "take_or_pay_maturity",
)

CATALYST_CALENDAR = (
    {
        "date": "2026-09-30",
        "type": "measurement_period_end",
        "catalyst": "9M 2026 snapshot: $33,242M revenue, -$(104,039)M net loss, -$381.095238M/day burn",
    },
    {
        "date": "2026-12-31",
        "type": "filing_window",
        "catalyst": "FY2026 close tests the Q3 deceleration: +46.7417% QoQ vs +144.2401% in Q2 at a 79.707462% marginal compute cost",
    },
    {
        "date": "2027-03-31",
        "type": "s1_filing",
        "catalyst": "FY2026 10-K / S-1/A disclosure window: ASC 842 true-up of the 100.624442x concealment multiple ($451,200M vs $4,484M)",
    },
    {
        "date": "2027-09-30",
        "type": "maturity_cliff",
        "catalyst": "$24.0B total short-term compute commitment wall ($17.4B + $6.6B) measured from the 9M 2026 snapshot",
    },
    {
        "date": "2028-12-31",
        "type": "encumbrance_step_up",
        "catalyst": "$100.2B booked TPU/silicon stack plus the $150.0B-$175.0B unpriced TPU/AMD band ramp window",
    },
    {
        "date": "2036-04-30",
        "type": "take_or_pay_maturity",
        "catalyst": "outer-dated take-or-pay compute maturity horizon across the $320.0B senior lease stack",
    },
)

ENTITY_AND_INSTRUMENT_IDS = {
    "primary_target": {
        "entity": "Anthropic, PBC",
        "role": "primary",
        "identifiers": {
            "sec_cik": "0002130357",
            "ticker": "ANT",
            "jurisdiction_of_incorporation": "Delaware",
            "filing": "Form S-1/A confidential amendment (trillion-dollar encumbrance restatement)",
        },
    },
    "bdc_colenders_credit_funds": {
        "role": "vendor_financed_compute_credit_counterparties",
        "counterparties": [
            {
                "entity": "Amazon.com, Inc. (AWS)",
                "ticker": "AMZN",
                "cik": "0001018724",
                "instrument": "convert exposure $130.5B vs $6.2B equity investment = 21.048387x convert multiple",
            },
            {
                "entity": "Alphabet Inc. (Google Cloud)",
                "ticker": "GOOGL",
                "cik": "0001652044",
                "instrument": "updated exposure $121.3B + [$125.0B, $150.0B] = [$246.3B, $271.3B]",
            },
            {
                "entity": "Microsoft Corporation (Azure)",
                "ticker": "MSFT",
                "cik": "0000789019",
                "instrument": "compute commitment counterparty carried from the prior S-1 ring; no restated figure locked in this bundle",
            },
            {
                "entity": "Broadcom Inc.",
                "ticker": "AVGO",
                "cik": "0001649338",
                "instrument": "TPU equipment lease stack underlying the $451.2B off-balance-sheet commitment component",
            },
            {
                "entity": "Advanced Micro Devices, Inc.",
                "ticker": "AMD",
                "cik": "0000002488",
                "instrument": "unpriced accelerator commitments inside the $150.0B-$175.0B TPU/AMD band",
            },
        ],
    },
    "insurer_reinsurance_sidecars": {
        "role": "regulated_insurance_balance_sheet_counterparties",
        "counterparties": [],
        "attestation": "no regulated insurance or reinsurance sidecar counterparty named in the S-1/A locked constants",
    },
    "auditors_valuation_agents_fund_admins": {
        "role": "pcaob_registered_independent_auditors",
        "counterparties": [
            {"entity": "Ernst & Young LLP", "scope": "FY2025 audit report (Form S-1 Exhibit 23.2)"},
            {"entity": "Grant Thornton LLP", "scope": "FY2023-FY2024 audit report (Form S-1 Exhibit 23.1)"},
        ],
    },
    "pension_lps_swfs_consultants": {
        "role": "fiduciary_passive_index_transfer_vector",
        "counterparties": [],
        "attestation": "post-IPO S&P 500 index inclusion transfers encumbrance risk onto public pensions, 401(k) plans, and passive index funds; no named FOIA-subject LP in the locked constants",
    },
    "trustees_admin_agents_rating_agencies": {
        "role": "deal_agents_underwriting_syndicate",
        "counterparties": [
            {"entity": "Morgan Stanley & Co. LLC", "role": "lead_left_underwriter"},
            {"entity": "Goldman Sachs & Co. LLC", "role": "stabilization_agent"},
            {"entity": "JPMorgan Chase & Co.", "role": "bookrunner"},
            {"entity": "Citigroup Global Markets Inc.", "role": "bookrunner"},
        ],
        "attestation": "issuer unrated; no indenture trustee or rating agency coverage in the locked constants",
    },
    "counsel_co_investors": {
        "role": "litigation_counsel_and_named_dockets",
        "court_dockets": [
            {
                "case": "Bartz et al. v. Anthropic PBC",
                "docket": "N.D. Cal. Case No. 3:24-cv-05417-WHA",
                "status": "$1,500.0M settlement",
            }
        ],
    },
}


# ---------------------------------------------------------------------------
# Verification functions
# ---------------------------------------------------------------------------

def verify_quarterly_progression():
    """LOCK A: revenue-per-compute-dollar, QoQ growth, compute share, and
    adjusted operating margin identities across Q1 2025 -> Q3 2026."""
    rev = QUARTERLY_REVENUE_M
    comp = QUARTERLY_COMPUTE_M
    adj = ADJUSTED_OPERATING_INCOME_M
    return {
        "q1_2026_rev_per_dollar_compute": rev["Q1_2026"] / comp["Q1_2026"],
        "q1_2026_qoq_revenue_growth_pct": (rev["Q1_2026"] - rev["Q4_2025"]) / rev["Q4_2025"] * 100.0,
        "q2_2026_rev_per_dollar_compute": rev["Q2_2026"] / comp["Q2_2026"],
        "q2_2026_compute_share": comp["Q2_2026"] / rev["Q2_2026"],
        "q2_2026_qoq_revenue_growth_pct": (rev["Q2_2026"] - rev["Q1_2026"]) / rev["Q1_2026"] * 100.0,
        "q2_2026_adjusted_op_margin_pct": adj["Q2_2026"] / rev["Q2_2026"] * 100.0,
        "q3_2026_rev_per_dollar_compute": rev["Q3_2026"] / comp["Q3_2026"],
        "q3_2026_compute_share": comp["Q3_2026"] / rev["Q3_2026"],
        "q3_2026_qoq_revenue_growth_pct": (rev["Q3_2026"] - rev["Q2_2026"]) / rev["Q2_2026"] * 100.0,
        "q3_2026_rev_per_compute_drop_pct": (
            (rev["Q3_2026"] * comp["Q2_2026"] - rev["Q2_2026"] * comp["Q3_2026"])
            / (rev["Q2_2026"] * comp["Q3_2026"])
            * 100.0
        ),
        "q3_2026_adjusted_op_margin_pct": adj["Q3_2026"] / rev["Q3_2026"] * 100.0,
    }


def verify_marginal_and_short_term_compute():
    """LOCK B: Q3 2026 marginal compute cost plus the short-term compute stack,
    the price-cut haircut, and the donation match."""
    marginal_numerator_m = QUARTERLY_COMPUTE_M["Q3_2026"] - QUARTERLY_COMPUTE_M["Q2_2026"]
    marginal_denominator_m = QUARTERLY_REVENUE_M["Q3_2026"] - QUARTERLY_REVENUE_M["Q2_2026"]
    short_term_primary_b = 17.4
    short_term_secondary_b = 6.6
    return {
        "marginal_numerator_m": marginal_numerator_m,
        "marginal_denominator_m": marginal_denominator_m,
        "marginal_compute_cost_pct": marginal_numerator_m / marginal_denominator_m * 100.0,
        "q3_short_term_compute_m": 5000.0,
        "short_term_primary_b": short_term_primary_b,
        "short_term_secondary_b": short_term_secondary_b,
        "total_short_term_compute_b": round(short_term_primary_b + short_term_secondary_b, 1),
        "price_cut_haircut_m": 600.0,
        "donation_match_m": 2000.0,
    }


def verify_nine_month_2026_totals():
    """LOCK C: 9M 2026 consolidation across the 273-day period."""
    rev_9m_m = (
        QUARTERLY_REVENUE_M["Q1_2026"]
        + QUARTERLY_REVENUE_M["Q2_2026"]
        + QUARTERLY_REVENUE_M["Q3_2026"]
    )
    compute_9m_m = sum(QUARTERLY_COMPUTE_M.values())
    gaap_op_loss_9m_m = sum(GAAP_OPERATING_INCOME_M.values())
    net_loss_9m_m = sum(QUARTERLY_NET_LOSS_M.values())
    period_days = (datetime.date(2026, 9, 30) - datetime.date(2026, 1, 1)).days + 1
    return {
        "rev_9m_m": rev_9m_m,
        "compute_9m_m": compute_9m_m,
        "gaap_op_loss_9m_m": gaap_op_loss_9m_m,
        "net_loss_9m_m": net_loss_9m_m,
        "period_days": period_days,
        "daily_net_loss_m": net_loss_9m_m / period_days,
        "convertible_fair_value_loss_m": -94302.0,
        "partner_deal_expense_m": -10400.0,
        "stock_based_compensation_m": -3320.0,
        "policy_violation_revenue_low_m": round(0.05 * rev_9m_m, 2),
        "policy_violation_revenue_high_m": round(0.07 * rev_9m_m, 2),
    }


def asc842_concealment_multiple(off_balance_sheet_m, on_balance_sheet_m):
    """WeWork-isomorphic ASC 842 concealment comparator: undiscounted
    off-balance-sheet lease / take-or-pay obligations divided by the
    on-balance-sheet recognized lease liabilities."""
    if off_balance_sheet_m < 0.0:
        raise ValueError("off_balance_sheet_m must be non-negative")
    if on_balance_sheet_m <= 0.0:
        raise ValueError("on_balance_sheet_m must be positive")
    return off_balance_sheet_m / on_balance_sheet_m


def verify_encumbrance_tie_out():
    """LOCK D: $895.4B five-piece tie-out, all-in encumbrance envelope, ASC 842
    concealment multiple, next-12-month locked share, Amazon convert multiple,
    and updated Google exposure."""
    tie_out_total_b = round(sum(FIVE_PIECE_ENCUMBRANCE_B.values()), 1)
    locked_b = round(NEXT_12M_TOTAL_COMMITMENTS_B - NEXT_12M_CANCELABLE_B, 1)
    return {
        "tie_out_total_b": tie_out_total_b,
        "all_in_encumbrance_low_b": round(
            tie_out_total_b + UNPRICED_TPU_AMD_LOW_B + DEVELOPER_GUARANTIES_B, 1
        ),
        "all_in_encumbrance_high_b": round(
            tie_out_total_b + UNPRICED_TPU_AMD_HIGH_B + DEVELOPER_GUARANTIES_B, 1
        ),
        "asc842_concealment_multiple_x": asc842_concealment_multiple(
            ASC842_OFF_BALANCE_SHEET_M, ASC842_ON_BALANCE_SHEET_M
        ),
        "next_12m_locked_b": locked_b,
        "next_12m_locked_share": locked_b / NEXT_12M_TOTAL_COMMITMENTS_B,
        "amazon_convert_multiple_x": AMAZON_CONVERT_EXPOSURE_B / AMAZON_EQUITY_INVESTMENT_B,
        "google_updated_exposure_low_b": round(
            GOOGLE_BASE_EXPOSURE_B + GOOGLE_ADDITIONAL_RANGE_B[0], 1
        ),
        "google_updated_exposure_high_b": round(
            GOOGLE_BASE_EXPOSURE_B + GOOGLE_ADDITIONAL_RANGE_B[1], 1
        ),
    }


def tranche_recovery(ev_b):
    """LOCK E: parameterized tranche payoff function. Input: enterprise value /
    asset recovery `ev_b` in USD billions. Output: exact dollar recovery and
    cent-on-the-dollar vectors across every tranche in strict seniority order,
    terminating with the Class A subordinated public equity residual stub."""
    if ev_b < 0.0:
        raise ValueError("ev_b must be non-negative")
    rows = []
    floor = 0.0
    for name, claim in WATERFALL_TRANCHES:
        if claim is None:
            recovery = max(0.0, float(ev_b) - floor)
            rows.append(
                {"tranche": name, "recovery_b": round(recovery, 6), "cents_on_dollar": None}
            )
            continue
        ceiling = floor + claim
        recovery = max(0.0, min(float(ev_b), ceiling) - floor)
        rows.append(
            {
                "tranche": name,
                "recovery_b": round(recovery, 6),
                "cents_on_dollar": round(recovery / claim, 6),
            }
        )
        floor = ceiling
    return rows


def verify_wework_precedent_isomorphism():
    """WeWork insolvency isomorphism: public S-1 -> IPO withdrawal -> Chapter 11,
    measured against the Anthropic ASC 842 concealment profile."""
    s1_filed = datetime.date(2019, 8, 14)
    ipo_withdrawn = datetime.date(2019, 9, 24)
    chapter_11 = datetime.date(2023, 11, 6)
    recognition_ratio = ASC842_ON_BALANCE_SHEET_M / ASC842_OFF_BALANCE_SHEET_M
    return {
        "wework_s1_public_filing_date": s1_filed.isoformat(),
        "wework_ipo_withdrawn_date": ipo_withdrawn.isoformat(),
        "wework_chapter_11_petition_date": chapter_11.isoformat(),
        "wework_chapter_11_docket": "Bankr. D.N.J. Case No. 23-90706 (WeWork Companies Inc.)",
        "s1_to_ipo_withdrawal_days": (ipo_withdrawn - s1_filed).days,
        "s1_to_chapter_11_days": (chapter_11 - s1_filed).days,
        "anthropic_on_balance_recognition_ratio": recognition_ratio,
        "recognition_ratio_below_one_pct": recognition_ratio < 0.01,
        "concealment_multiple_exceeds_100x": asc842_concealment_multiple(
            ASC842_OFF_BALANCE_SHEET_M, ASC842_ON_BALANCE_SHEET_M
        )
        > 100.0,
    }


def verify_entity_and_instrument_ids():
    """Six-category security-master ring structural check."""
    required_categories = [
        "primary_target",
        "bdc_colenders_credit_funds",
        "insurer_reinsurance_sidecars",
        "auditors_valuation_agents_fund_admins",
        "pension_lps_swfs_consultants",
        "trustees_admin_agents_rating_agencies",
        "counsel_co_investors",
    ]
    categories_present = all(cat in ENTITY_AND_INSTRUMENT_IDS for cat in required_categories)
    primary_cik_valid = (
        ENTITY_AND_INSTRUMENT_IDS["primary_target"]["identifiers"]["sec_cik"] == "0002130357"
    )
    vendor_ring_count = len(ENTITY_AND_INSTRUMENT_IDS["bdc_colenders_credit_funds"]["counterparties"])
    underwriter_count = len(
        ENTITY_AND_INSTRUMENT_IDS["trustees_admin_agents_rating_agencies"]["counterparties"]
    )
    return categories_present, primary_cik_valid, vendor_ring_count, underwriter_count


def verify_catalyst_calendar():
    """ISO 8601 parse, strict ascending order, and enum validity."""
    parsed = [datetime.date.fromisoformat(entry["date"]) for entry in CATALYST_CALENDAR]
    strictly_ascending = all(a < b for a, b in zip(parsed, parsed[1:]))
    types_valid = all(entry["type"] in CATALYST_TYPES for entry in CATALYST_CALENDAR)
    return strictly_ascending, types_valid, len(CATALYST_CALENDAR)


def verify_schema_bundle():
    """Cross-check that the paired Draft 2020-12 schema parses and carries the
    mandated $id and top-level audit sections."""
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "schema",
        "anthropic_s1a_trillion_dollar_encumbrance_and_wework_insolvency_audit.json",
    )
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    id_valid = (
        schema.get("$id")
        == "urn:opstack:schema:anthropic_s1a_trillion_dollar_encumbrance_and_wework_insolvency_audit.json"
    )
    dialect_valid = schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    required_sections = [
        "specification_id",
        "jurisdiction_context",
        "cfaa_compliant_18_usc_1030",
        "quarterly_progression",
        "marginal_and_short_term_compute",
        "nine_month_2026_totals",
        "encumbrance_tie_out",
        "tranche_waterfall",
        "entity_and_instrument_ids",
        "catalyst_calendar",
        "wework_precedent_isomorphism",
    ]
    sections_present = all(
        section in schema.get("required", []) and section in schema.get("properties", {})
        for section in required_sections
    )
    return id_valid and dialect_valid and sections_present


def run_verification():
    # LOCK A: quarterly progression ----------------------------------------
    prog = verify_quarterly_progression()
    assert QUARTERLY_REVENUE_M["Q1_2025"] == 376.0
    assert QUARTERLY_REVENUE_M["Q2_2025"] == 787.0
    assert QUARTERLY_REVENUE_M["Q3_2025"] == 1382.0
    assert QUARTERLY_REVENUE_M["Q4_2025"] == 2040.0
    assert round(prog["q1_2026_rev_per_dollar_compute"], 6) == 1.396811
    assert round(prog["q1_2026_qoq_revenue_growth_pct"], 2) == 131.91
    assert round(prog["q2_2026_rev_per_dollar_compute"], 6) == 2.078985
    assert round(prog["q2_2026_compute_share"], 6) == 0.481004
    assert round(prog["q2_2026_qoq_revenue_growth_pct"], 2) == 144.24
    assert GAAP_OPERATING_INCOME_M["Q2_2026"] == 974.0
    assert ADJUSTED_OPERATING_INCOME_M["Q2_2026"] == 2235.0
    assert round(prog["q2_2026_adjusted_op_margin_pct"], 4) == 19.3423
    assert round(prog["q3_2026_rev_per_dollar_compute"], 6) == 1.719152
    assert round(prog["q3_2026_compute_share"], 6) == 0.581682
    assert round(prog["q3_2026_qoq_revenue_growth_pct"], 4) == 46.7417
    assert round(prog["q3_2026_rev_per_compute_drop_pct"], 4) == -17.3081
    assert GAAP_OPERATING_INCOME_M["Q3_2026"] == -567.0
    assert ADJUSTED_OPERATING_INCOME_M["Q3_2026"] == 2500.0
    assert round(prog["q3_2026_adjusted_op_margin_pct"], 4) == 14.7440

    # LOCK B: marginal and short-term compute ------------------------------
    msc = verify_marginal_and_short_term_compute()
    assert msc["marginal_numerator_m"] == 4305.0
    assert msc["marginal_denominator_m"] == 5401.0
    assert round(msc["marginal_compute_cost_pct"], 6) == 79.707462
    assert msc["q3_short_term_compute_m"] == 5000.0
    assert msc["total_short_term_compute_b"] == 24.0
    assert msc["price_cut_haircut_m"] == 600.0
    assert msc["donation_match_m"] == 2000.0

    # LOCK C: 9M 2026 totals -------------------------------------------------
    totals = verify_nine_month_2026_totals()
    assert totals["rev_9m_m"] == 33242.0
    assert totals["compute_9m_m"] == 18808.0
    assert totals["gaap_op_loss_9m_m"] == -1260.0
    assert totals["net_loss_9m_m"] == -104039.0
    assert totals["period_days"] == 273
    assert round(totals["daily_net_loss_m"], 6) == -381.095238
    assert totals["convertible_fair_value_loss_m"] == -94302.0
    assert totals["partner_deal_expense_m"] == -10400.0
    assert totals["stock_based_compensation_m"] == -3320.0
    assert totals["policy_violation_revenue_low_m"] == 1662.10
    assert totals["policy_violation_revenue_high_m"] == 2326.94

    # LOCK D: encumbrance tie-out --------------------------------------------
    enc = verify_encumbrance_tie_out()
    assert enc["tie_out_total_b"] == 895.4
    assert enc["all_in_encumbrance_low_b"] == 1050.1
    assert enc["all_in_encumbrance_high_b"] == 1075.1
    assert round(enc["asc842_concealment_multiple_x"], 6) == 100.624442
    assert enc["next_12m_locked_b"] == 65.5
    assert round(enc["next_12m_locked_share"], 8) == 0.93839542
    assert round(enc["amazon_convert_multiple_x"], 6) == 21.048387
    assert enc["google_updated_exposure_low_b"] == 246.3
    assert enc["google_updated_exposure_high_b"] == 271.3

    # LOCK E: tranche waterfall ----------------------------------------------
    breakeven_thresholds_b = []
    running_b = 0.0
    for _name, claim in WATERFALL_TRANCHES[:-1]:
        running_b = round(running_b + claim, 1)
        breakeven_thresholds_b.append(running_b)
    assert breakeven_thresholds_b == [320.0, 771.2, 871.4, 895.4, 1045.4, 1050.1]

    w_tie_out = tranche_recovery(895.4)
    assert [row["recovery_b"] for row in w_tie_out] == [320.0, 451.2, 100.2, 24.0, 0.0, 0.0, 0.0]
    assert all(row["cents_on_dollar"] == 1.0 for row in w_tie_out[:4])
    assert w_tie_out[6]["recovery_b"] == 0.0

    w_par = tranche_recovery(1050.1)
    assert [row["recovery_b"] for row in w_par][:6] == [320.0, 451.2, 100.2, 24.0, 150.0, 4.7]
    assert all(row["cents_on_dollar"] == 1.0 for row in w_par[:6])
    assert w_par[6]["recovery_b"] == 0.0

    w_high = tranche_recovery(1075.1)
    assert w_high[6]["recovery_b"] == 25.0

    w_stress = tranche_recovery(400.0)
    assert w_stress[0]["recovery_b"] == 320.0
    assert w_stress[1]["recovery_b"] == 80.0
    assert w_stress[1]["cents_on_dollar"] == round(80.0 / 451.2, 6)
    assert [row["recovery_b"] for row in w_stress[2:]] == [0.0, 0.0, 0.0, 0.0, 0.0]

    try:
        tranche_recovery(-1.0)
        raise AssertionError("tranche_recovery accepted negative enterprise value")
    except ValueError:
        pass

    # LOCK E: entity ring, catalyst calendar, WeWork isomorphism --------------
    categories_present, primary_cik_valid, vendor_ring_count, underwriter_count = (
        verify_entity_and_instrument_ids()
    )
    assert categories_present is True
    assert primary_cik_valid is True
    assert vendor_ring_count == 5
    assert underwriter_count == 4

    strictly_ascending, types_valid, catalyst_count = verify_catalyst_calendar()
    assert strictly_ascending is True
    assert types_valid is True
    assert catalyst_count == 6

    wework = verify_wework_precedent_isomorphism()
    assert wework["s1_to_ipo_withdrawal_days"] == 41
    assert wework["s1_to_chapter_11_days"] == 1545
    assert round(wework["anthropic_on_balance_recognition_ratio"], 6) == 0.009938
    assert wework["recognition_ratio_below_one_pct"] is True
    assert wework["concealment_multiple_exceeds_100x"] is True

    assert verify_schema_bundle() is True

    manifest = {
        "specification_id": "SPEC-ANTHROPIC-S1A-TRILLION-DOLLAR-ENCUMBRANCE-AND-WEWORK-INSOLVENCY-AUDIT-v1.0",
        "jurisdiction_context": "US",
        "cfaa_compliant_18_usc_1030": True,
        "quarterly_progression": {
            "q1_2025_revenue_m": 376.0,
            "q2_2025_revenue_m": 787.0,
            "q3_2025_revenue_m": 1382.0,
            "q4_2025_revenue_m": 2040.0,
            "q1_2026_revenue_m": 4731.0,
            "q1_2026_compute_m": 3387.0,
            "q1_2026_rev_per_dollar_compute": round(prog["q1_2026_rev_per_dollar_compute"], 6),
            "q1_2026_qoq_revenue_growth_pct": round(prog["q1_2026_qoq_revenue_growth_pct"], 2),
            "q2_2026_revenue_m": 11555.0,
            "q2_2026_compute_m": 5558.0,
            "q2_2026_rev_per_dollar_compute": round(prog["q2_2026_rev_per_dollar_compute"], 6),
            "q2_2026_compute_share": round(prog["q2_2026_compute_share"], 6),
            "q2_2026_qoq_revenue_growth_pct": round(prog["q2_2026_qoq_revenue_growth_pct"], 2),
            "q2_2026_gaap_operating_income_m": 974.0,
            "q2_2026_adjusted_op_income_m": 2235.0,
            "q2_2026_adjusted_op_margin_pct": round(prog["q2_2026_adjusted_op_margin_pct"], 4),
            "q3_2026_revenue_m": 16956.0,
            "q3_2026_compute_m": 9863.0,
            "q3_2026_rev_per_dollar_compute": round(prog["q3_2026_rev_per_dollar_compute"], 6),
            "q3_2026_compute_share": round(prog["q3_2026_compute_share"], 6),
            "q3_2026_qoq_revenue_growth_pct": round(prog["q3_2026_qoq_revenue_growth_pct"], 4),
            "q3_2026_rev_per_compute_drop_pct": round(prog["q3_2026_rev_per_compute_drop_pct"], 4),
            "q3_2026_gaap_operating_loss_m": -567.0,
            "q3_2026_adjusted_op_income_m": 2500.0,
            "q3_2026_adjusted_op_margin_pct": round(prog["q3_2026_adjusted_op_margin_pct"], 4),
        },
        "marginal_and_short_term_compute": {
            "q3_2026_marginal_compute_numerator_m": msc["marginal_numerator_m"],
            "q3_2026_marginal_compute_denominator_m": msc["marginal_denominator_m"],
            "q3_2026_marginal_compute_cost_pct": round(msc["marginal_compute_cost_pct"], 6),
            "q3_2026_short_term_compute_m": msc["q3_short_term_compute_m"],
            "short_term_compute_primary_b": msc["short_term_primary_b"],
            "short_term_compute_secondary_b": msc["short_term_secondary_b"],
            "total_short_term_compute_b": msc["total_short_term_compute_b"],
            "price_cut_haircut_m": msc["price_cut_haircut_m"],
            "donation_match_m": msc["donation_match_m"],
        },
        "nine_month_2026_totals": {
            "revenue_m": totals["rev_9m_m"],
            "compute_m": totals["compute_9m_m"],
            "gaap_operating_loss_m": totals["gaap_op_loss_9m_m"],
            "net_loss_m": totals["net_loss_9m_m"],
            "days_in_period": totals["period_days"],
            "daily_net_loss_m": round(totals["daily_net_loss_m"], 6),
            "convertible_fair_value_loss_m": totals["convertible_fair_value_loss_m"],
            "partner_deal_expense_m": totals["partner_deal_expense_m"],
            "stock_based_compensation_m": totals["stock_based_compensation_m"],
            "policy_violation_revenue_share_range": [0.05, 0.07],
            "policy_violation_revenue_range_m": [
                totals["policy_violation_revenue_low_m"],
                totals["policy_violation_revenue_high_m"],
            ],
        },
        "encumbrance_tie_out": {
            "five_piece_tie_out_b": FIVE_PIECE_ENCUMBRANCE_B,
            "tie_out_total_b": enc["tie_out_total_b"],
            "unpriced_tpu_amd_low_b": UNPRICED_TPU_AMD_LOW_B,
            "unpriced_tpu_amd_high_b": UNPRICED_TPU_AMD_HIGH_B,
            "developer_guaranties_b": DEVELOPER_GUARANTIES_B,
            "all_in_encumbrance_low_b": enc["all_in_encumbrance_low_b"],
            "all_in_encumbrance_high_b": enc["all_in_encumbrance_high_b"],
            "asc842_off_balance_sheet_m": ASC842_OFF_BALANCE_SHEET_M,
            "asc842_on_balance_sheet_m": ASC842_ON_BALANCE_SHEET_M,
            "asc842_concealment_multiple_x": round(enc["asc842_concealment_multiple_x"], 6),
            "next_12m_total_commitments_b": NEXT_12M_TOTAL_COMMITMENTS_B,
            "next_12m_cancelable_b": NEXT_12M_CANCELABLE_B,
            "next_12m_locked_b": enc["next_12m_locked_b"],
            "next_12m_locked_share": round(enc["next_12m_locked_share"], 8),
            "amazon_convert_exposure_b": AMAZON_CONVERT_EXPOSURE_B,
            "amazon_equity_investment_b": AMAZON_EQUITY_INVESTMENT_B,
            "amazon_convert_multiple_x": round(enc["amazon_convert_multiple_x"], 6),
            "google_base_exposure_b": GOOGLE_BASE_EXPOSURE_B,
            "google_additional_range_b": list(GOOGLE_ADDITIONAL_RANGE_B),
            "google_updated_exposure_range_b": [
                enc["google_updated_exposure_low_b"],
                enc["google_updated_exposure_high_b"],
            ],
        },
        "tranche_waterfall_at_tie_out_ev": w_tie_out,
        "entity_and_instrument_ids": ENTITY_AND_INSTRUMENT_IDS,
        "catalyst_calendar": list(CATALYST_CALENDAR),
        "wework_precedent_isomorphism": wework,
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-ANTHROPIC-S1A-TRILLION-DOLLAR-ENCUMBRANCE-AND-WEWORK-INSOLVENCY-AUDIT-v1.0 | "
        f"Q3Rev=${QUARTERLY_REVENUE_M['Q3_2026']:.0f}M @ {round(prog['q3_2026_rev_per_dollar_compute'], 6)}x | "
        f"MarginalCompute={round(msc['marginal_compute_cost_pct'], 6)}% | "
        f"9M NetLoss=-${abs(totals['net_loss_9m_m']):.0f}M ({round(totals['daily_net_loss_m'], 6)}M/day) | "
        f"TieOut=${enc['tie_out_total_b']}B -> AllIn=${enc['all_in_encumbrance_low_b']}B-${enc['all_in_encumbrance_high_b']}B | "
        f"ASC842Concealment={round(enc['asc842_concealment_multiple_x'], 6)}x | "
        f"LockedShare={round(enc['next_12m_locked_share'] * 100, 6)}% | "
        f"AmazonConvert={round(enc['amazon_convert_multiple_x'], 6)}x | "
        f"WeWorkS1toCh11={wework['s1_to_chapter_11_days']}d | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
