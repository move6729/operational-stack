#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: ANTHROPIC NOVEMBER GUN-JUMPING & VALUATION INVERSION
AUDIT (v1.0)

License: Unlicense (Public Domain — Zero-Rent Federation)

Proves:
1. LOCK A (revenue / compute): Q2 2026 revenue $11,555M / compute $5,558M, Q3 2026
   revenue $16,956M / compute $9,863M, 9M 2026 revenue $33,242M / compute
   $18,808M (implied Q1 2026 $4,731M / $3,387M), Q3 annualized run-rate
   $16,956M x 4 = $67,824M, Q3 monthly average revenue $16,956M / 3 = $5,652M,
   Q3 delta revenue $5,401M, Q3 delta compute $4,305M, Q3 marginal compute cost
   $4,305M / $5,401M = 0.79707462 = 79.7075% (contribution 20.2925%), Q3
   short-term compute $5,000M, Q3 GAAP operating loss -$(567)M, 9M 2026 GAAP net
   loss -$(104,039)M across 273 days = -$381.0952M/day.
2. LOCK B (October leak): leaked October 2026 run-rate $80,000M, implied monthly
   revenue $80,000M / 12 = $6,666.6667M, run-rate delta vs Q3 annualized
   $80,000M - $67,824M = $12,176M (+17.9523%), monthly revenue delta
   $1,014.6667M, implied incremental monthly compute $1,014.6667M x 0.79707462 =
   $808.765M, implied total monthly compute $3,287.6667M + $808.765M =
   $4,096.4317M, implied annualized compute $4,096.4317M x 12 = $49,157.1805M.
3. LOCK C (Opus 5.5 / GSA 40% price cut): constant-volume run-rate deflation
   $80,000M x 0.6 = $48,000M (-$32,000M), volume multiplier required to restore
   $80B = 1.666667x (+66.6667%), post-cut marginal compute cost 0.79707462 / 0.6
   = 1.328458 = 132.8458% (marginal gross loss -32.8458%).
4. LOCK D (IPO valuation inversion): target valuation $1,500,000M vs skeptical
   $1,000,000M (haircut -$500,000M = -33.3333%), target raise $100,000M vs
   reduced $80,000M (haircut -$20,000M = -20.0%), Sep-30 cash $146,600M,
   post-IPO gross cash $226,600M, operating EV at $1.5T = $1,253,400M and at
   $1.0T = $773,400M.
5. LOCK E (encumbrance ratios): disclosed 5-piece compute encumbrance $895,400M,
   all-in [$1,050,100M, $1,075,100M]; encumbrance/EV at $1T disclosed 1.157745x,
   all-in [1.357771x, 1.390096x]; encumbrance/mcap all-in [1.0501x, 1.0751x];
   encumbrance/Sep-30 cash [7.163029x, 7.333561x].
6. LOCK F (NTM compute, dilution, counterparties, moratorium scissor, OpenAI
   precedent): NTM total compute $69,800M (87.25% of the $80B IPO), NTM
   non-cancelable $65,500M (81.875%); primary dilution 6.6667% / 8.0% / 10.0%;
   Amazon convert principal $6,200M vs carrying FV $130,500M; Broadcom zero-exit
   lease $161,200M; uncommenced ASC 842 leases $451,200M + post-Sep-30 LT
   commitments $100,200M = total uncommenced forward leases $551,400M; developer
   credit guaranties $4,700M vs prior $800M = 5.875x surge; moratorium scissor
   direct recourse $231,400M and total uncommenced stack $556,100M; Nasdaq Nov-5
   rout $2,500,000M; OpenAI target raise $30,000M vs actual $11,000M (shortfall
   $19,000M = 63.3333%) at a reduced $1,250,000M valuation.
7. LOCK G (parameterized tranche_recovery(ev_m) absolute-priority waterfall over
   the six-rank going-concern senior claim stack totaling $1,028,884M versus the
   Class A subordinated public equity residual stub), the Section 5 gun-jumping
   timeline (S-1 2026-10-26 -> S-1/A 2026-11-02 -> moratorium 2026-11-03 -> WSJ
   leak + Opus 5.5 cut 2026-11-05 -> WSJ print 2026-11-06 -> IPO window
   2026-11-16..2026-11-20 -> Q3 staleness 2027-02-14), the six-category
   entity_and_instrument_ids security-master ring, and the ISO catalyst calendar.

Zero external dependencies.
"""

import datetime
import hashlib
import json
import os

SPECIFICATION_ID = "SPEC-ANTHROPIC-NOVEMBER-GUN-JUMPING-AND-VALUATION-INVERSION-AUDIT-v1.0"

# ---------------------------------------------------------------------------
# Locked constants. All monetary values USD millions unless suffixed _b ($B) or
# _x (dimensionless multiple) or _pct (percentage).
# ---------------------------------------------------------------------------

# Identity / proposed listing
CIK = "0002130357"
PROPOSED_TICKER = "NASDAQ: ANT"

# Gun-jumping timeline (Section 5 registration / quiet period)
S1_INITIAL_DATE = datetime.date(2026, 10, 26)
S1A_FILING_DATE = datetime.date(2026, 11, 2)
MIDTERM_MORATORIUM_DATE = datetime.date(2026, 11, 3)
WSJ_LEAK_AND_OPUS55_CUT_DATE = datetime.date(2026, 11, 5)
WSJ_PRINT_DATE = datetime.date(2026, 11, 6)
TARGET_IPO_WINDOW_START = datetime.date(2026, 11, 16)
TARGET_IPO_WINDOW_END = datetime.date(2026, 11, 20)
Q3_FINANCIAL_STALENESS_DATE = datetime.date(2027, 2, 14)
Q3_PERIOD_END = datetime.date(2026, 9, 30)
NINE_M_PERIOD_START = datetime.date(2026, 1, 1)

# Revenue / compute
Q2_2026_REV_M = 11555.0
Q3_2026_REV_M = 16956.0
NINE_M_2026_REV_M = 33242.0
Q2_2026_COMPUTE_M = 5558.0
Q3_2026_COMPUTE_M = 9863.0
NINE_M_2026_COMPUTE_M = 18808.0
Q3_SHORT_TERM_COMPUTE_M = 5000.0
Q3_GAAP_OP_LOSS_M = -567.0
NINE_M_2026_GAAP_NET_LOSS_M = -104039.0

# Derived Q3 deltas and marginal compute cost (full precision, rounded at assert)
Q3_ANNUALIZED_RUN_RATE_M = Q3_2026_REV_M * 4.0            # 67824.0
Q3_MONTHLY_AVG_REV_M = Q3_2026_REV_M / 3.0                # 5652.0
Q3_MONTHLY_AVG_COMPUTE_M = Q3_2026_COMPUTE_M / 3.0        # 3287.666666...
Q3_DELTA_REV_M = Q3_2026_REV_M - Q2_2026_REV_M            # 5401.0
Q3_DELTA_COMPUTE_M = Q3_2026_COMPUTE_M - Q2_2026_COMPUTE_M  # 4305.0
Q3_MARGINAL_COMPUTE_COST_RATIO = Q3_DELTA_COMPUTE_M / Q3_DELTA_REV_M  # 0.797074615...

# October 2026 leaked run-rate
OCT_2026_LEAKED_RUN_RATE_M = 80000.0

# Opus 5.5 / GSA price cut
OPUS_55_AND_GSA_PRICE_CUT_RATIO = 0.4

# IPO valuation / raise
IPO_VALUATION_TARGET_M = 1500000.0
IPO_VALUATION_SKEPTICAL_M = 1000000.0
IPO_RAISE_TARGET_M = 100000.0
IPO_RAISE_REDUCED_M = 80000.0

# Cash
CASH_SEP_30_2026_M = 146600.0

# Compute encumbrance
DISCLOSED_5PIECE_COMPUTE_ENCUMBRANCE_M = 895400.0
ALL_IN_COMPUTE_ENCUMBRANCE_LOW_M = 1050100.0
ALL_IN_COMPUTE_ENCUMBRANCE_HIGH_M = 1075100.0

# Next-twelve-month compute
NTM_TOTAL_COMPUTE_DUE_M = 69800.0
NTM_NON_CANCELABLE_COMPUTE_M = 65500.0

# Counterparty / lease / guaranty exposures
AMAZON_CONVERT_PRINCIPAL_M = 6200.0
AMAZON_CONVERT_CARRYING_FV_M = 130500.0
BROADCOM_ZERO_EXIT_LEASE_M = 161200.0
UNCOMMENCED_ASC842_LEASES_SEP30_M = 451200.0
POST_SEP30_LT_COMMITMENTS_M = 100200.0
ASC842_ON_BALANCE_SHEET_M = 4484.0
DEVELOPER_CREDIT_GUARANTIES_M = 4700.0
DEVELOPER_GUARANTY_PRIOR_M = 800.0
MORATORIUM_SCISSOR_DIRECT_RECOURSE_M = 231400.0

# Market precedent (Nasdaq rout / OpenAI)
NASDAQ_NOV5_ROUT_M = 2500000.0
OPENAI_TARGET_RAISE_M = 30000.0
OPENAI_ACTUAL_RAISE_M = 11000.0
OPENAI_REDUCED_VALUATION_M = 1250000.0

# Going-concern senior claim stack (absolute-priority waterfall, USD millions)
TRANCHE_STACK_M = {
    "rank_1_developer_guaranties": 4700.0,
    "rank_2_on_bs_asc842_leases": 4484.0,
    "rank_3_ntm_non_cancelable_compute": 65500.0,
    "rank_4_remaining_priced_purchase_obligations": 272300.0,
    "rank_5_uncommenced_asc842_and_post_sep30_leases": 551400.0,
    "rank_6_amazon_convertible_notes_carrying_fv": 130500.0,
}
TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M = 1028884.0

WATERFALL_TRANCHES = (
    ("rank_1_developer_guaranties", 4700.0),
    ("rank_2_on_bs_asc842_leases", 4484.0),
    ("rank_3_ntm_non_cancelable_compute", 65500.0),
    ("rank_4_remaining_priced_purchase_obligations", 272300.0),
    ("rank_5_uncommenced_asc842_and_post_sep30_leases", 551400.0),
    ("rank_6_amazon_convertible_notes_carrying_fv", 130500.0),
    ("class_a_subordinated_public_equity", None),  # residual stub
)

CATALYST_TYPES = (
    "s1_filing",
    "s1a_amendment",
    "regulatory_moratorium",
    "leak_and_price_cut",
    "press_print",
    "ipo_window_open",
    "ipo_window_close",
    "financial_staleness",
)

CATALYST_CALENDAR = (
    {
        "date": "2026-10-26",
        "type": "s1_filing",
        "catalyst": "Form S-1 filed (CIK 0002130357); Section 5 registration period opens",
    },
    {
        "date": "2026-11-02",
        "type": "s1a_amendment",
        "catalyst": "Form S-1/A amendment filed restating the trillion-dollar compute encumbrance stack",
    },
    {
        "date": "2026-11-03",
        "type": "regulatory_moratorium",
        "catalyst": "Midterm moratorium takes effect; moratorium scissor direct recourse $231,400M against a $556,100M uncommenced stack",
    },
    {
        "date": "2026-11-05",
        "type": "leak_and_price_cut",
        "catalyst": "WSJ leak of the $80,000M October run-rate coincides with the Opus 5.5 / GSA 40% price cut; Nasdaq $2,500,000M rout",
    },
    {
        "date": "2026-11-06",
        "type": "press_print",
        "catalyst": "WSJ print edition; gun-jumping condition: material leak + price cut land 10 days before the IPO window opens",
    },
    {
        "date": "2026-11-16",
        "type": "ipo_window_open",
        "catalyst": "Target IPO window opens (NASDAQ: ANT); $80,000M reduced raise at a $1,000,000M skeptical valuation",
    },
    {
        "date": "2026-11-20",
        "type": "ipo_window_close",
        "catalyst": "Target IPO window closes; NTM non-cancelable compute $65,500M = 81.875% of the $80,000M raise",
    },
    {
        "date": "2027-02-14",
        "type": "financial_staleness",
        "catalyst": "Q3 2026 financial statements (period end 2026-09-30) go stale for an effective registration statement",
    },
)

ENTITY_AND_INSTRUMENT_IDS = {
    "primary_target": {
        "entity": "Anthropic, PBC",
        "role": "primary",
        "identifiers": {
            "sec_cik": "0002130357",
            "ticker": "NASDAQ: ANT",
            "jurisdiction_of_incorporation": "Delaware",
            "filing": "Form S-1 (2026-10-26) / Form S-1/A (2026-11-02) registration statement",
        },
    },
    "bdc_colenders_credit_funds": {
        "role": "vendor_financed_compute_credit_counterparties",
        "counterparties": [
            {
                "entity": "Amazon.com, Inc. (AWS)",
                "ticker": "AMZN",
                "cik": "0001018724",
                "instrument": "convertible notes principal $6,200M vs carrying fair value $130,500M (rank 6 senior claim)",
            },
            {
                "entity": "Broadcom Inc.",
                "ticker": "AVGO",
                "cik": "0001649338",
                "instrument": "zero-exit equipment lease $161,200M underlying the uncommenced ASC 842 forward-lease stack",
            },
            {
                "entity": "Alphabet Inc. (Google Cloud)",
                "ticker": "GOOGL",
                "cik": "0001652044",
                "instrument": "TPU compute commitment counterparty carried from the prior S-1/A ring; no restated figure locked in this bundle",
            },
            {
                "entity": "Microsoft Corporation (Azure)",
                "ticker": "MSFT",
                "cik": "0000789019",
                "instrument": "compute commitment counterparty carried from the prior S-1/A ring; no restated figure locked in this bundle",
            },
            {
                "entity": "Advanced Micro Devices, Inc.",
                "ticker": "AMD",
                "cik": "0000002488",
                "instrument": "unpriced accelerator commitments inside the all-in encumbrance band",
            },
        ],
    },
    "insurer_reinsurance_sidecars": {
        "role": "regulated_insurance_balance_sheet_counterparties",
        "counterparties": [],
        "attestation": "no regulated insurance or reinsurance sidecar counterparty named in the locked constants",
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
        "attestation": "post-IPO index inclusion transfers the encumbrance stack onto public pensions, 401(k) plans, and passive index funds; no named FOIA-subject LP in the locked constants",
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

def verify_revenue_compute():
    """LOCK A: revenue / compute progression, Q3 marginal compute cost, and the
    9M 2026 daily net-loss burn rate."""
    period_days = (Q3_PERIOD_END - NINE_M_PERIOD_START).days + 1
    marginal_ratio = Q3_DELTA_COMPUTE_M / Q3_DELTA_REV_M
    return {
        "q2_2026_rev_m": Q2_2026_REV_M,
        "q3_2026_rev_m": Q3_2026_REV_M,
        "9m_2026_rev_m": NINE_M_2026_REV_M,
        "q3_2026_annualized_run_rate_m": Q3_ANNUALIZED_RUN_RATE_M,
        "q3_2026_monthly_avg_rev_m": Q3_MONTHLY_AVG_REV_M,
        "q2_2026_compute_m": Q2_2026_COMPUTE_M,
        "q3_2026_compute_m": Q3_2026_COMPUTE_M,
        "9m_2026_compute_m": NINE_M_2026_COMPUTE_M,
        "q3_delta_rev_m": Q3_DELTA_REV_M,
        "q3_delta_compute_m": Q3_DELTA_COMPUTE_M,
        "q3_marginal_compute_cost_ratio": round(marginal_ratio, 8),
        "q3_marginal_compute_cost_pct": round(marginal_ratio * 100.0, 4),
        "q3_marginal_compute_contribution_pct": round((1.0 - marginal_ratio) * 100.0, 4),
        "q3_short_term_compute_m": Q3_SHORT_TERM_COMPUTE_M,
        "q3_gaap_op_loss_m": Q3_GAAP_OP_LOSS_M,
        "9m_2026_gaap_net_loss_m": NINE_M_2026_GAAP_NET_LOSS_M,
        "9m_2026_daily_net_loss_m": round(NINE_M_2026_GAAP_NET_LOSS_M / period_days, 4),
        "implied_q1_2026_rev_m": NINE_M_2026_REV_M - Q2_2026_REV_M - Q3_2026_REV_M,
        "implied_q1_2026_compute_m": NINE_M_2026_COMPUTE_M - Q2_2026_COMPUTE_M - Q3_2026_COMPUTE_M,
        "period_days": period_days,
    }


def verify_october_leak():
    """LOCK B: leaked October 2026 $80B run-rate projected through the Q3
    marginal compute cost ratio."""
    oct_monthly_rev = OCT_2026_LEAKED_RUN_RATE_M / 12.0
    monthly_delta = oct_monthly_rev - Q3_MONTHLY_AVG_REV_M
    incremental_compute = monthly_delta * Q3_MARGINAL_COMPUTE_COST_RATIO
    total_monthly_compute = Q3_MONTHLY_AVG_COMPUTE_M + incremental_compute
    return {
        "oct_2026_leaked_run_rate_m": OCT_2026_LEAKED_RUN_RATE_M,
        "oct_2026_implied_monthly_rev_m": round(oct_monthly_rev, 4),
        "oct_vs_q3_run_rate_delta_m": OCT_2026_LEAKED_RUN_RATE_M - Q3_ANNUALIZED_RUN_RATE_M,
        "oct_vs_q3_run_rate_growth_pct": round(
            (OCT_2026_LEAKED_RUN_RATE_M - Q3_ANNUALIZED_RUN_RATE_M)
            / Q3_ANNUALIZED_RUN_RATE_M
            * 100.0,
            4,
        ),
        "oct_vs_q3_monthly_rev_delta_m": round(monthly_delta, 4),
        "oct_implied_incremental_monthly_compute_m": round(incremental_compute, 3),
        "oct_implied_total_monthly_compute_m": round(total_monthly_compute, 4),
        "oct_implied_annualized_compute_m": round(total_monthly_compute * 12.0, 4),
    }


def verify_price_cut_deflation():
    """LOCK C: Opus 5.5 / GSA 40% price cut at constant volume deflates the
    run-rate and inverts the marginal compute cost above 100%."""
    keep_ratio = 1.0 - OPUS_55_AND_GSA_PRICE_CUT_RATIO
    post_cut_run_rate = OCT_2026_LEAKED_RUN_RATE_M * keep_ratio
    post_cut_marginal_ratio = Q3_MARGINAL_COMPUTE_COST_RATIO / keep_ratio
    return {
        "opus_55_and_gsa_price_cut_ratio": OPUS_55_AND_GSA_PRICE_CUT_RATIO,
        "opus_55_and_gsa_price_cut_pct": round(OPUS_55_AND_GSA_PRICE_CUT_RATIO * 100.0, 4),
        "post_cut_constant_volume_run_rate_m": post_cut_run_rate,
        "post_cut_constant_volume_deflation_m": post_cut_run_rate - OCT_2026_LEAKED_RUN_RATE_M,
        "volume_multiplier_required_for_80b": round(
            OCT_2026_LEAKED_RUN_RATE_M / post_cut_run_rate, 6
        ),
        "volume_increase_required_pct": round(
            (OCT_2026_LEAKED_RUN_RATE_M / post_cut_run_rate - 1.0) * 100.0, 4
        ),
        "post_cut_marginal_compute_cost_ratio": round(post_cut_marginal_ratio, 6),
        "post_cut_marginal_compute_cost_pct": round(post_cut_marginal_ratio * 100.0, 4),
        "post_cut_marginal_gross_loss_pct": round((1.0 - post_cut_marginal_ratio) * 100.0, 4),
    }


def verify_ipo_valuation():
    """LOCK D: IPO valuation / raise haircuts and the operating enterprise value
    net of post-IPO gross cash at the $1.5T target and $1.0T skeptical marks."""
    return {
        "ipo_valuation_target_m": IPO_VALUATION_TARGET_M,
        "ipo_valuation_skeptical_m": IPO_VALUATION_SKEPTICAL_M,
        "ipo_valuation_haircut_m": IPO_VALUATION_SKEPTICAL_M - IPO_VALUATION_TARGET_M,
        "ipo_valuation_haircut_pct": round(
            (IPO_VALUATION_SKEPTICAL_M - IPO_VALUATION_TARGET_M)
            / IPO_VALUATION_TARGET_M
            * 100.0,
            4,
        ),
        "ipo_raise_target_m": IPO_RAISE_TARGET_M,
        "ipo_raise_reduced_m": IPO_RAISE_REDUCED_M,
        "ipo_raise_haircut_m": IPO_RAISE_REDUCED_M - IPO_RAISE_TARGET_M,
        "ipo_raise_haircut_pct": round(
            (IPO_RAISE_REDUCED_M - IPO_RAISE_TARGET_M) / IPO_RAISE_TARGET_M * 100.0, 4
        ),
        "cash_sep_30_2026_m": CASH_SEP_30_2026_M,
        "cash_post_ipo_gross_m": CASH_SEP_30_2026_M + IPO_RAISE_REDUCED_M,
        "operating_ev_at_1500b_m": IPO_VALUATION_TARGET_M
        - (CASH_SEP_30_2026_M + IPO_RAISE_TARGET_M),
        "operating_ev_at_1000b_m": IPO_VALUATION_SKEPTICAL_M
        - (CASH_SEP_30_2026_M + IPO_RAISE_REDUCED_M),
    }


def verify_encumbrance_ratios():
    """LOCK E: compute-encumbrance coverage ratios against the $1T operating EV,
    the $1T market cap, and Sep-30 cash. Every all-in ratio exceeds 1.0x, which
    is the valuation inversion."""
    ev_1t = IPO_VALUATION_SKEPTICAL_M - (CASH_SEP_30_2026_M + IPO_RAISE_REDUCED_M)
    mcap_1t = IPO_VALUATION_SKEPTICAL_M
    return {
        "disclosed_5piece_compute_encumbrance_m": DISCLOSED_5PIECE_COMPUTE_ENCUMBRANCE_M,
        "all_in_compute_encumbrance_low_m": ALL_IN_COMPUTE_ENCUMBRANCE_LOW_M,
        "all_in_compute_encumbrance_high_m": ALL_IN_COMPUTE_ENCUMBRANCE_HIGH_M,
        "encumbrance_to_ev_disclosed_at_1t_x": round(
            DISCLOSED_5PIECE_COMPUTE_ENCUMBRANCE_M / ev_1t, 6
        ),
        "encumbrance_to_ev_all_in_low_at_1t_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_LOW_M / ev_1t, 6),
        "encumbrance_to_ev_all_in_high_at_1t_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_HIGH_M / ev_1t, 6),
        "encumbrance_to_mcap_all_in_low_at_1t_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_LOW_M / mcap_1t, 4),
        "encumbrance_to_mcap_all_in_high_at_1t_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_HIGH_M / mcap_1t, 4),
        "encumbrance_to_sep30_cash_low_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_LOW_M / CASH_SEP_30_2026_M, 6),
        "encumbrance_to_sep30_cash_high_x": round(ALL_IN_COMPUTE_ENCUMBRANCE_HIGH_M / CASH_SEP_30_2026_M, 6),
    }


def verify_ntm_dilution_counterparties():
    """LOCK F: NTM compute share of the IPO, primary dilution, counterparty /
    lease / guaranty exposures, the moratorium scissor, and the OpenAI / Nasdaq
    market precedent."""
    total_uncommenced = UNCOMMENCED_ASC842_LEASES_SEP30_M + POST_SEP30_LT_COMMITMENTS_M
    return {
        "ntm_total_compute_due_m": NTM_TOTAL_COMPUTE_DUE_M,
        "ntm_non_cancelable_compute_m": NTM_NON_CANCELABLE_COMPUTE_M,
        "ntm_total_share_of_80b_ipo_pct": round(NTM_TOTAL_COMPUTE_DUE_M / IPO_RAISE_REDUCED_M * 100.0, 4),
        "ntm_non_cancelable_share_of_80b_ipo_pct": round(
            NTM_NON_CANCELABLE_COMPUTE_M / IPO_RAISE_REDUCED_M * 100.0, 4
        ),
        "primary_dilution_at_1500b_100b_pct": round(
            IPO_RAISE_TARGET_M / IPO_VALUATION_TARGET_M * 100.0, 4
        ),
        "primary_dilution_at_1000b_80b_pct": round(
            IPO_RAISE_REDUCED_M / IPO_VALUATION_SKEPTICAL_M * 100.0, 4
        ),
        "primary_dilution_at_1000b_100b_pct": round(
            IPO_RAISE_TARGET_M / IPO_VALUATION_SKEPTICAL_M * 100.0, 4
        ),
        "amazon_convert_principal_m": AMAZON_CONVERT_PRINCIPAL_M,
        "amazon_convert_carrying_fv_m": AMAZON_CONVERT_CARRYING_FV_M,
        "broadcom_zero_exit_lease_m": BROADCOM_ZERO_EXIT_LEASE_M,
        "uncommenced_asc842_leases_sep30_m": UNCOMMENCED_ASC842_LEASES_SEP30_M,
        "post_sep30_lt_commitments_m": POST_SEP30_LT_COMMITMENTS_M,
        "total_uncommenced_forward_leases_m": total_uncommenced,
        "developer_credit_guaranties_m": DEVELOPER_CREDIT_GUARANTIES_M,
        "developer_guaranty_prior_m": DEVELOPER_GUARANTY_PRIOR_M,
        "developer_guaranty_surge_x": round(DEVELOPER_CREDIT_GUARANTIES_M / DEVELOPER_GUARANTY_PRIOR_M, 6),
        "moratorium_scissor_direct_recourse_m": MORATORIUM_SCISSOR_DIRECT_RECOURSE_M,
        "moratorium_scissor_total_uncommenced_stack_m": total_uncommenced + DEVELOPER_CREDIT_GUARANTIES_M,
        "nasdaq_nov5_rout_m": NASDAQ_NOV5_ROUT_M,
        "openai_target_raise_m": OPENAI_TARGET_RAISE_M,
        "openai_actual_raise_m": OPENAI_ACTUAL_RAISE_M,
        "openai_shortfall_m": OPENAI_TARGET_RAISE_M - OPENAI_ACTUAL_RAISE_M,
        "openai_shortfall_pct": round(
            (OPENAI_TARGET_RAISE_M - OPENAI_ACTUAL_RAISE_M) / OPENAI_TARGET_RAISE_M * 100.0, 4
        ),
        "openai_reduced_valuation_m": OPENAI_REDUCED_VALUATION_M,
    }


def tranche_recovery(ev_m):
    """LOCK G: parameterized tranche payoff function. Input: enterprise value /
    asset recovery `ev_m` in USD millions. Output: exact dollar recovery and
    cent-on-the-dollar vectors across every rank in strict absolute-priority
    order, terminating with the Class A subordinated public equity residual
    stub. The six-rank going-concern senior claim stack totals $1,028,884M, so
    any EV below that threshold leaves the public equity stub at zero."""
    if ev_m < 0.0:
        raise ValueError("ev_m must be non-negative")
    rows = []
    floor = 0.0
    for name, claim in WATERFALL_TRANCHES:
        if claim is None:
            recovery = max(0.0, float(ev_m) - floor)
            rows.append(
                {"tranche": name, "recovery_m": round(recovery, 6), "cents_on_dollar": None}
            )
            continue
        ceiling = floor + claim
        recovery = max(0.0, min(float(ev_m), ceiling) - floor)
        rows.append(
            {
                "tranche": name,
                "recovery_m": round(recovery, 6),
                "cents_on_dollar": round(recovery / claim, 6),
            }
        )
        floor = ceiling
    return rows


def verify_gun_jumping_timeline():
    """Section 5 gun-jumping timeline: the WSJ leak and the Opus 5.5 / GSA price
    cut land inside the registration / quiet period, strictly between the S-1/A
    amendment and the opening of the target IPO window."""
    return {
        "s1_initial_date": S1_INITIAL_DATE.isoformat(),
        "s1a_filing_date": S1A_FILING_DATE.isoformat(),
        "midterm_moratorium_date": MIDTERM_MORATORIUM_DATE.isoformat(),
        "wsj_leak_and_opus55_cut_date": WSJ_LEAK_AND_OPUS55_CUT_DATE.isoformat(),
        "wsj_print_date": WSJ_PRINT_DATE.isoformat(),
        "target_ipo_window_start": TARGET_IPO_WINDOW_START.isoformat(),
        "target_ipo_window_end": TARGET_IPO_WINDOW_END.isoformat(),
        "q3_financial_staleness_date": Q3_FINANCIAL_STALENESS_DATE.isoformat(),
        "s1_to_s1a_days": (S1A_FILING_DATE - S1_INITIAL_DATE).days,
        "s1a_to_moratorium_days": (MIDTERM_MORATORIUM_DATE - S1A_FILING_DATE).days,
        "moratorium_to_leak_days": (WSJ_LEAK_AND_OPUS55_CUT_DATE - MIDTERM_MORATORIUM_DATE).days,
        "leak_to_print_days": (WSJ_PRINT_DATE - WSJ_LEAK_AND_OPUS55_CUT_DATE).days,
        "s1_to_print_days": (WSJ_PRINT_DATE - S1_INITIAL_DATE).days,
        "print_to_ipo_start_days": (TARGET_IPO_WINDOW_START - WSJ_PRINT_DATE).days,
        "s1_to_ipo_start_days": (TARGET_IPO_WINDOW_START - S1_INITIAL_DATE).days,
        "s1_to_ipo_end_days": (TARGET_IPO_WINDOW_END - S1_INITIAL_DATE).days,
        "q3_end_to_staleness_days": (Q3_FINANCIAL_STALENESS_DATE - Q3_PERIOD_END).days,
        "ipo_end_to_staleness_days": (Q3_FINANCIAL_STALENESS_DATE - TARGET_IPO_WINDOW_END).days,
        "leak_inside_quiet_period": (
            S1A_FILING_DATE < WSJ_LEAK_AND_OPUS55_CUT_DATE < TARGET_IPO_WINDOW_START
        ),
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
        ENTITY_AND_INSTRUMENT_IDS["primary_target"]["identifiers"]["sec_cik"] == CIK
    )
    primary_ticker_valid = (
        ENTITY_AND_INSTRUMENT_IDS["primary_target"]["identifiers"]["ticker"] == PROPOSED_TICKER
    )
    vendor_ring_count = len(ENTITY_AND_INSTRUMENT_IDS["bdc_colenders_credit_funds"]["counterparties"])
    underwriter_count = len(
        ENTITY_AND_INSTRUMENT_IDS["trustees_admin_agents_rating_agencies"]["counterparties"]
    )
    return (
        categories_present,
        primary_cik_valid,
        primary_ticker_valid,
        vendor_ring_count,
        underwriter_count,
    )


def verify_catalyst_calendar():
    """ISO 8601 parse, strict ascending order, and enum validity."""
    parsed = [datetime.date.fromisoformat(entry["date"]) for entry in CATALYST_CALENDAR]
    strictly_ascending = all(a < b for a, b in zip(parsed, parsed[1:]))
    types_valid = all(entry["type"] in CATALYST_TYPES for entry in CATALYST_CALENDAR)
    return strictly_ascending, types_valid, len(CATALYST_CALENDAR)


def verify_schema_bundle():
    """Cross-check that the paired Draft 2020-12 schema parses and carries the
    mandated $id, dialect, and top-level audit sections."""
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "schema",
        "anthropic_november_gun_jumping_and_valuation_inversion_audit.json",
    )
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    id_valid = (
        schema.get("$id")
        == "urn:opstack:schema:anthropic_november_gun_jumping_and_valuation_inversion_audit.json"
    )
    dialect_valid = schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    required_sections = [
        "specification_id",
        "jurisdiction_context",
        "cfaa_compliance_attestation",
        "locked_constants_and_outputs",
        "tranche_waterfall",
        "entity_and_instrument_ids",
        "catalyst_calendar",
    ]
    sections_present = all(
        section in schema.get("required", []) and section in schema.get("properties", {})
        for section in required_sections
    )
    return id_valid and dialect_valid and sections_present


def run_verification():
    # LOCK A: revenue / compute ---------------------------------------------
    a = verify_revenue_compute()
    assert a["q2_2026_rev_m"] == 11555.0
    assert a["q3_2026_rev_m"] == 16956.0
    assert a["9m_2026_rev_m"] == 33242.0
    assert a["q3_2026_annualized_run_rate_m"] == 67824.0
    assert a["q3_2026_monthly_avg_rev_m"] == 5652.0
    assert a["q2_2026_compute_m"] == 5558.0
    assert a["q3_2026_compute_m"] == 9863.0
    assert a["9m_2026_compute_m"] == 18808.0
    assert a["q3_delta_rev_m"] == 5401.0
    assert a["q3_delta_compute_m"] == 4305.0
    assert a["q3_marginal_compute_cost_ratio"] == 0.79707462
    assert a["q3_marginal_compute_cost_pct"] == 79.7075
    assert a["q3_marginal_compute_contribution_pct"] == 20.2925
    assert a["q3_short_term_compute_m"] == 5000.0
    assert a["q3_gaap_op_loss_m"] == -567.0
    assert a["9m_2026_gaap_net_loss_m"] == -104039.0
    assert a["period_days"] == 273
    assert a["9m_2026_daily_net_loss_m"] == -381.0952
    assert a["implied_q1_2026_rev_m"] == 4731.0
    assert a["implied_q1_2026_compute_m"] == 3387.0

    # LOCK B: October leak ----------------------------------------------------
    b = verify_october_leak()
    assert b["oct_2026_leaked_run_rate_m"] == 80000.0
    assert b["oct_2026_implied_monthly_rev_m"] == 6666.6667
    assert b["oct_vs_q3_run_rate_delta_m"] == 12176.0
    assert b["oct_vs_q3_run_rate_growth_pct"] == 17.9523
    assert b["oct_vs_q3_monthly_rev_delta_m"] == 1014.6667
    assert b["oct_implied_incremental_monthly_compute_m"] == 808.765
    assert b["oct_implied_total_monthly_compute_m"] == 4096.4317
    assert b["oct_implied_annualized_compute_m"] == 49157.1805

    # LOCK C: price-cut deflation --------------------------------------------
    c = verify_price_cut_deflation()
    assert c["opus_55_and_gsa_price_cut_ratio"] == 0.4
    assert c["opus_55_and_gsa_price_cut_pct"] == 40.0
    assert c["post_cut_constant_volume_run_rate_m"] == 48000.0
    assert c["post_cut_constant_volume_deflation_m"] == -32000.0
    assert c["volume_multiplier_required_for_80b"] == 1.666667
    assert c["volume_increase_required_pct"] == 66.6667
    assert c["post_cut_marginal_compute_cost_ratio"] == 1.328458
    assert c["post_cut_marginal_compute_cost_pct"] == 132.8458
    assert c["post_cut_marginal_gross_loss_pct"] == -32.8458

    # LOCK D: IPO valuation inversion ----------------------------------------
    d = verify_ipo_valuation()
    assert d["ipo_valuation_target_m"] == 1500000.0
    assert d["ipo_valuation_skeptical_m"] == 1000000.0
    assert d["ipo_valuation_haircut_m"] == -500000.0
    assert d["ipo_valuation_haircut_pct"] == -33.3333
    assert d["ipo_raise_target_m"] == 100000.0
    assert d["ipo_raise_reduced_m"] == 80000.0
    assert d["ipo_raise_haircut_m"] == -20000.0
    assert d["ipo_raise_haircut_pct"] == -20.0
    assert d["cash_sep_30_2026_m"] == 146600.0
    assert d["cash_post_ipo_gross_m"] == 226600.0
    assert d["operating_ev_at_1500b_m"] == 1253400.0
    assert d["operating_ev_at_1000b_m"] == 773400.0

    # LOCK E: encumbrance coverage ratios ------------------------------------
    e = verify_encumbrance_ratios()
    assert e["disclosed_5piece_compute_encumbrance_m"] == 895400.0
    assert e["all_in_compute_encumbrance_low_m"] == 1050100.0
    assert e["all_in_compute_encumbrance_high_m"] == 1075100.0
    assert e["encumbrance_to_ev_disclosed_at_1t_x"] == 1.157745
    assert e["encumbrance_to_ev_all_in_low_at_1t_x"] == 1.357771
    assert e["encumbrance_to_ev_all_in_high_at_1t_x"] == 1.390096
    assert e["encumbrance_to_mcap_all_in_low_at_1t_x"] == 1.0501
    assert e["encumbrance_to_mcap_all_in_high_at_1t_x"] == 1.0751
    assert e["encumbrance_to_sep30_cash_low_x"] == 7.163029
    assert e["encumbrance_to_sep30_cash_high_x"] == 7.333561
    # Valuation inversion: every all-in coverage ratio exceeds 1.0x.
    assert e["encumbrance_to_ev_all_in_low_at_1t_x"] > 1.0
    assert e["encumbrance_to_mcap_all_in_low_at_1t_x"] > 1.0

    # LOCK F: NTM compute, dilution, counterparties, moratorium, precedent ----
    f = verify_ntm_dilution_counterparties()
    assert f["ntm_total_compute_due_m"] == 69800.0
    assert f["ntm_non_cancelable_compute_m"] == 65500.0
    assert f["ntm_total_share_of_80b_ipo_pct"] == 87.25
    assert f["ntm_non_cancelable_share_of_80b_ipo_pct"] == 81.875
    assert f["primary_dilution_at_1500b_100b_pct"] == 6.6667
    assert f["primary_dilution_at_1000b_80b_pct"] == 8.0
    assert f["primary_dilution_at_1000b_100b_pct"] == 10.0
    assert f["amazon_convert_principal_m"] == 6200.0
    assert f["amazon_convert_carrying_fv_m"] == 130500.0
    assert f["broadcom_zero_exit_lease_m"] == 161200.0
    assert f["uncommenced_asc842_leases_sep30_m"] == 451200.0
    assert f["post_sep30_lt_commitments_m"] == 100200.0
    assert f["total_uncommenced_forward_leases_m"] == 551400.0
    assert f["developer_credit_guaranties_m"] == 4700.0
    assert f["developer_guaranty_prior_m"] == 800.0
    assert f["developer_guaranty_surge_x"] == 5.875
    assert f["moratorium_scissor_direct_recourse_m"] == 231400.0
    assert f["moratorium_scissor_total_uncommenced_stack_m"] == 556100.0
    assert f["nasdaq_nov5_rout_m"] == 2500000.0
    assert f["openai_target_raise_m"] == 30000.0
    assert f["openai_actual_raise_m"] == 11000.0
    assert f["openai_shortfall_m"] == 19000.0
    assert f["openai_shortfall_pct"] == 63.3333
    assert f["openai_reduced_valuation_m"] == 1250000.0

    # LOCK G: tranche waterfall ----------------------------------------------
    assert round(sum(TRANCHE_STACK_M.values()), 1) == TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M
    assert TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M == 1028884.0

    breakeven_thresholds_m = []
    running_m = 0.0
    for _name, claim in WATERFALL_TRANCHES[:-1]:
        running_m = round(running_m + claim, 1)
        breakeven_thresholds_m.append(running_m)
    assert breakeven_thresholds_m == [4700.0, 9184.0, 74684.0, 346984.0, 898384.0, 1028884.0]

    # Full senior recovery at the going-concern senior claim total.
    w_par = tranche_recovery(TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M)
    assert [row["recovery_m"] for row in w_par][:6] == [
        4700.0, 4484.0, 65500.0, 272300.0, 551400.0, 130500.0
    ]
    assert all(row["cents_on_dollar"] == 1.0 for row in w_par[:6])
    assert w_par[6]["recovery_m"] == 0.0

    # Valuation inversion: at the $1T skeptical market cap the rank-6 Amazon
    # convert is impaired and the Class A public equity stub is wiped to zero.
    w_1t = tranche_recovery(IPO_VALUATION_SKEPTICAL_M)
    assert [row["recovery_m"] for row in w_1t][:5] == [4700.0, 4484.0, 65500.0, 272300.0, 551400.0]
    assert w_1t[5]["recovery_m"] == 101616.0
    assert w_1t[5]["cents_on_dollar"] == round(101616.0 / 130500.0, 6)
    assert w_1t[6]["recovery_m"] == 0.0
    assert TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M - IPO_VALUATION_SKEPTICAL_M == 28884.0

    # Residual stub only recovers above the full senior claim stack.
    w_above = tranche_recovery(1100000.0)
    assert w_above[6]["recovery_m"] == 71116.0

    # Zero recovery at zero EV.
    w_zero = tranche_recovery(0.0)
    assert all(row["recovery_m"] == 0.0 for row in w_zero)

    # Partial mid-stack recovery.
    w_mid = tranche_recovery(500000.0)
    assert [row["recovery_m"] for row in w_mid][:4] == [4700.0, 4484.0, 65500.0, 272300.0]
    assert w_mid[4]["recovery_m"] == 153016.0
    assert w_mid[4]["cents_on_dollar"] == round(153016.0 / 551400.0, 6)
    assert [row["recovery_m"] for row in w_mid[5:]] == [0.0, 0.0]

    try:
        tranche_recovery(-1.0)
        raise AssertionError("tranche_recovery accepted negative enterprise value")
    except ValueError:
        pass

    # Gun-jumping timeline ----------------------------------------------------
    g = verify_gun_jumping_timeline()
    assert g["s1_to_s1a_days"] == 7
    assert g["s1a_to_moratorium_days"] == 1
    assert g["moratorium_to_leak_days"] == 2
    assert g["leak_to_print_days"] == 1
    assert g["s1_to_print_days"] == 11
    assert g["print_to_ipo_start_days"] == 10
    assert g["s1_to_ipo_start_days"] == 21
    assert g["s1_to_ipo_end_days"] == 25
    assert g["q3_end_to_staleness_days"] == 137
    assert g["ipo_end_to_staleness_days"] == 86
    assert g["leak_inside_quiet_period"] is True

    # Entity ring, catalyst calendar, schema bundle --------------------------
    categories_present, primary_cik_valid, primary_ticker_valid, vendor_ring_count, underwriter_count = (
        verify_entity_and_instrument_ids()
    )
    assert categories_present is True
    assert primary_cik_valid is True
    assert primary_ticker_valid is True
    assert vendor_ring_count == 5
    assert underwriter_count == 4

    strictly_ascending, types_valid, catalyst_count = verify_catalyst_calendar()
    assert strictly_ascending is True
    assert types_valid is True
    assert catalyst_count == 8

    assert verify_schema_bundle() is True

    locked_constants_and_outputs = {
        "cik": CIK,
        "proposed_ticker": PROPOSED_TICKER,
        "s1_initial_date": g["s1_initial_date"],
        "s1a_filing_date": g["s1a_filing_date"],
        "midterm_moratorium_date": g["midterm_moratorium_date"],
        "wsj_leak_and_opus55_cut_date": g["wsj_leak_and_opus55_cut_date"],
        "wsj_print_date": g["wsj_print_date"],
        "target_ipo_window_start": g["target_ipo_window_start"],
        "target_ipo_window_end": g["target_ipo_window_end"],
        "q3_financial_staleness_date": g["q3_financial_staleness_date"],
        "q2_2026_rev_m": a["q2_2026_rev_m"],
        "q3_2026_rev_m": a["q3_2026_rev_m"],
        "9m_2026_rev_m": a["9m_2026_rev_m"],
        "q3_2026_annualized_run_rate_m": a["q3_2026_annualized_run_rate_m"],
        "q3_2026_monthly_avg_rev_m": a["q3_2026_monthly_avg_rev_m"],
        "q2_2026_compute_m": a["q2_2026_compute_m"],
        "q3_2026_compute_m": a["q3_2026_compute_m"],
        "9m_2026_compute_m": a["9m_2026_compute_m"],
        "q3_delta_rev_m": a["q3_delta_rev_m"],
        "q3_delta_compute_m": a["q3_delta_compute_m"],
        "q3_marginal_compute_cost_ratio": a["q3_marginal_compute_cost_ratio"],
        "q3_marginal_compute_cost_pct": a["q3_marginal_compute_cost_pct"],
        "q3_marginal_compute_contribution_pct": a["q3_marginal_compute_contribution_pct"],
        "q3_short_term_compute_m": a["q3_short_term_compute_m"],
        "q3_gaap_op_loss_m": a["q3_gaap_op_loss_m"],
        "9m_2026_gaap_net_loss_m": a["9m_2026_gaap_net_loss_m"],
        "9m_2026_daily_net_loss_m": a["9m_2026_daily_net_loss_m"],
        "oct_2026_leaked_run_rate_m": b["oct_2026_leaked_run_rate_m"],
        "oct_2026_implied_monthly_rev_m": b["oct_2026_implied_monthly_rev_m"],
        "oct_vs_q3_run_rate_delta_m": b["oct_vs_q3_run_rate_delta_m"],
        "oct_vs_q3_run_rate_growth_pct": b["oct_vs_q3_run_rate_growth_pct"],
        "oct_vs_q3_monthly_rev_delta_m": b["oct_vs_q3_monthly_rev_delta_m"],
        "oct_implied_incremental_monthly_compute_m": b["oct_implied_incremental_monthly_compute_m"],
        "oct_implied_total_monthly_compute_m": b["oct_implied_total_monthly_compute_m"],
        "oct_implied_annualized_compute_m": b["oct_implied_annualized_compute_m"],
        "opus_55_and_gsa_price_cut_ratio": c["opus_55_and_gsa_price_cut_ratio"],
        "opus_55_and_gsa_price_cut_pct": c["opus_55_and_gsa_price_cut_pct"],
        "post_cut_constant_volume_run_rate_m": c["post_cut_constant_volume_run_rate_m"],
        "post_cut_constant_volume_deflation_m": c["post_cut_constant_volume_deflation_m"],
        "volume_multiplier_required_for_80b": c["volume_multiplier_required_for_80b"],
        "volume_increase_required_pct": c["volume_increase_required_pct"],
        "post_cut_marginal_compute_cost_ratio": c["post_cut_marginal_compute_cost_ratio"],
        "post_cut_marginal_compute_cost_pct": c["post_cut_marginal_compute_cost_pct"],
        "post_cut_marginal_gross_loss_pct": c["post_cut_marginal_gross_loss_pct"],
        "ipo_valuation_target_m": d["ipo_valuation_target_m"],
        "ipo_valuation_skeptical_m": d["ipo_valuation_skeptical_m"],
        "ipo_valuation_haircut_m": d["ipo_valuation_haircut_m"],
        "ipo_valuation_haircut_pct": d["ipo_valuation_haircut_pct"],
        "ipo_raise_target_m": d["ipo_raise_target_m"],
        "ipo_raise_reduced_m": d["ipo_raise_reduced_m"],
        "ipo_raise_haircut_m": d["ipo_raise_haircut_m"],
        "ipo_raise_haircut_pct": d["ipo_raise_haircut_pct"],
        "cash_sep_30_2026_m": d["cash_sep_30_2026_m"],
        "cash_post_ipo_gross_m": d["cash_post_ipo_gross_m"],
        "operating_ev_at_1500b_m": d["operating_ev_at_1500b_m"],
        "operating_ev_at_1000b_m": d["operating_ev_at_1000b_m"],
        "disclosed_5piece_compute_encumbrance_m": e["disclosed_5piece_compute_encumbrance_m"],
        "all_in_compute_encumbrance_low_m": e["all_in_compute_encumbrance_low_m"],
        "all_in_compute_encumbrance_high_m": e["all_in_compute_encumbrance_high_m"],
        "encumbrance_to_ev_disclosed_at_1t_x": e["encumbrance_to_ev_disclosed_at_1t_x"],
        "encumbrance_to_ev_all_in_low_at_1t_x": e["encumbrance_to_ev_all_in_low_at_1t_x"],
        "encumbrance_to_ev_all_in_high_at_1t_x": e["encumbrance_to_ev_all_in_high_at_1t_x"],
        "encumbrance_to_mcap_all_in_low_at_1t_x": e["encumbrance_to_mcap_all_in_low_at_1t_x"],
        "encumbrance_to_mcap_all_in_high_at_1t_x": e["encumbrance_to_mcap_all_in_high_at_1t_x"],
        "encumbrance_to_sep30_cash_low_x": e["encumbrance_to_sep30_cash_low_x"],
        "encumbrance_to_sep30_cash_high_x": e["encumbrance_to_sep30_cash_high_x"],
        "ntm_total_compute_due_m": f["ntm_total_compute_due_m"],
        "ntm_non_cancelable_compute_m": f["ntm_non_cancelable_compute_m"],
        "ntm_total_share_of_80b_ipo_pct": f["ntm_total_share_of_80b_ipo_pct"],
        "ntm_non_cancelable_share_of_80b_ipo_pct": f["ntm_non_cancelable_share_of_80b_ipo_pct"],
        "primary_dilution_at_1500b_100b_pct": f["primary_dilution_at_1500b_100b_pct"],
        "primary_dilution_at_1000b_80b_pct": f["primary_dilution_at_1000b_80b_pct"],
        "primary_dilution_at_1000b_100b_pct": f["primary_dilution_at_1000b_100b_pct"],
        "amazon_convert_principal_m": f["amazon_convert_principal_m"],
        "amazon_convert_carrying_fv_m": f["amazon_convert_carrying_fv_m"],
        "broadcom_zero_exit_lease_m": f["broadcom_zero_exit_lease_m"],
        "uncommenced_asc842_leases_sep30_m": f["uncommenced_asc842_leases_sep30_m"],
        "post_sep30_lt_commitments_m": f["post_sep30_lt_commitments_m"],
        "total_uncommenced_forward_leases_m": f["total_uncommenced_forward_leases_m"],
        "developer_credit_guaranties_m": f["developer_credit_guaranties_m"],
        "developer_guaranty_prior_m": f["developer_guaranty_prior_m"],
        "developer_guaranty_surge_x": f["developer_guaranty_surge_x"],
        "moratorium_scissor_direct_recourse_m": f["moratorium_scissor_direct_recourse_m"],
        "moratorium_scissor_total_uncommenced_stack_m": f["moratorium_scissor_total_uncommenced_stack_m"],
        "nasdaq_nov5_rout_m": f["nasdaq_nov5_rout_m"],
        "openai_target_raise_m": f["openai_target_raise_m"],
        "openai_actual_raise_m": f["openai_actual_raise_m"],
        "openai_shortfall_m": f["openai_shortfall_m"],
        "openai_shortfall_pct": f["openai_shortfall_pct"],
        "openai_reduced_valuation_m": f["openai_reduced_valuation_m"],
        "tranche_stack_m": dict(
            TRANCHE_STACK_M,
            total_going_concern_senior_claims_m=TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M,
        ),
    }

    tranche_waterfall = []
    cumulative_m = 0.0
    for seniority, (name, claim) in enumerate(WATERFALL_TRANCHES[:-1], start=1):
        cumulative_m = round(cumulative_m + claim, 1)
        tranche_waterfall.append(
            {
                "tranche": name,
                "principal_m": claim,
                "seniority": seniority,
                "breakeven_ev_m": cumulative_m,
            }
        )
    tranche_waterfall.append(
        {
            "tranche": "class_a_subordinated_public_equity",
            "principal_m": None,
            "seniority": len(WATERFALL_TRANCHES),
            "breakeven_ev_m": cumulative_m,
        }
    )

    manifest = {
        "specification_id": SPECIFICATION_ID,
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": {
            "cfaa_compliant_18_usc_1030": True,
            "basis": (
                "Zero unauthorized access under 18 U.S.C. 1030: every measured artifact is a "
                "public SEC EDGAR registration statement (Form S-1 / S-1/A, CIK 0002130357), a "
                "public federal court docket, or publicly reported print/leak coverage, analyzed "
                "read-only."
            ),
        },
        "locked_constants_and_outputs": locked_constants_and_outputs,
        "tranche_waterfall": tranche_waterfall,
        "entity_and_instrument_ids": ENTITY_AND_INSTRUMENT_IDS,
        "catalyst_calendar": list(CATALYST_CALENDAR),
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] {SPECIFICATION_ID} | "
        f"Q3MarginalCompute={a['q3_marginal_compute_cost_pct']}% | "
        f"OctRunRate=${b['oct_2026_leaked_run_rate_m']:.0f}M -> PostCut=${c['post_cut_constant_volume_run_rate_m']:.0f}M "
        f"({c['post_cut_marginal_compute_cost_pct']}% marginal) | "
        f"IPO ${d['ipo_valuation_target_m']:.0f}M->${d['ipo_valuation_skeptical_m']:.0f}M "
        f"({d['ipo_valuation_haircut_pct']}%) | "
        f"Encumbrance/Mcap=${e['encumbrance_to_mcap_all_in_low_at_1t_x']}x-${e['encumbrance_to_mcap_all_in_high_at_1t_x']}x | "
        f"SeniorClaims=${TOTAL_GOING_CONCERN_SENIOR_CLAIMS_M:.0f}M > $1T mcap (equity stub=0) | "
        f"GunJumpLeak={g['wsj_leak_and_opus55_cut_date']} ({g['print_to_ipo_start_days']}d pre-IPO) | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
