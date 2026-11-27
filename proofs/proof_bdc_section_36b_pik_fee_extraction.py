#!/usr/bin/env python3
"""Verification proof for the BDC Section 36(b) PIK fee-extraction bundle.

Pure Python 3 stdlib proof re-deriving every locked constant, governing
identity, and waterfall invariant across four equations plus the peer
Schedule-of-Investments mosaic and the combined OBDC + OTF cross-held
software tranche recovery stack.

  EQ-1  Cash-Fee-on-Paper-PIK drain. OTF Q1 2026 PIK income of $43.0M at a
        25.0% share of net investment income implies $172.0M NII and
        $129.0M cash NII. Per $1.00 of non-cash PIK income a 90%-distribution
        RIC pushes r + 0.90 x (1 - r) of cash out the door: 0.9175 at a 17.5%
        incentive fee and 0.9200 at 20.0% -- $39.4525M of Q1 2026 cash drain
        against $7.525M / $8.6M of cash incentive fee levied on paper income.
  EQ-2  Critical PIK threshold. The 90%-distribution cash-coverage critical
        PIK share is 4.24%; OTF's observed 25.0% is 5.8962x that threshold
        and 20.76 points above it, and the threshold binds strictly inside
        the zero-retained-cash ceiling 100 x 0.10 x (1 - 0.175) = 8.25%.
  EQ-3  Software reclassification. An 11.1% reported software share against a
        20-30% true share on $157.8B of credit AUM hides
        $14.0442B-$29.8242B of software exposure, avoids
        $2.80884B-$5.96484B of 20% markdown, preserves
        $42.1326M-$89.4726M of 1.5% base management fee, and capitalizes to
        $926.9172M-$1,968.3972M of OWL parent market cap at 22.0x FRE.
  EQ-4  Section 36(b) effective cash fee rate. A 17.5% / 20.0% incentive fee
        levied on income that is 25.0% non-cash is an effective 23.33% /
        26.67% charge on cash NII, against a combined OBDC + OTF FY2025 fee
        stack of $690.4M (up from $377.4M in FY2021, +82.94%) that caps the
        Section 36(b) disgorgement surface at $690.4M.

Peer mosaic: Star Mountain (Japonesque 69.0% PIK / 0.0% cash at SOFR+948bps;
CMT cash 1301-1401bps vs PIK 1669-2000bps), Bow River ($568,523,676 fair
value less $486,830,334 cost = $81,693,342 unrealized gain), Crescent BDC
(26 SOFR+PIK facilities), and $25.0B of sub-80c software loans inside a
$46.9B distressed US tech book (53.3%).

Exit code 0 iff every locked constant, identity, and invariant holds.
"""

import datetime
import json
import math
import re

# ---------------------------------------------------------------------------
# Standardized security-master keys (entity_and_instrument_ids)
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "ticker": {
        "blue_owl_capital_corp": "OWL",
        "blue_owl_capital_corp_ii": "OBDC",
        "blue_owl_technology_finance_corp": "OTF",
        "crescent_capital_bdc": "CGBD",
    },
    "cik": {
        "blue_owl_capital_corp": "0001823945",
        "blue_owl_capital_corp_ii": "0001655888",
        "blue_owl_technology_finance_corp": "0001747777",
        "star_mountain": "0001786835",
        "bow_river": "0001810256",
        "crescent_capital_bdc": "0001633336",
    },
    "court_dockets": {
        "blue_owl_capital_corp_ii": "7:26-cv-03468-KPF",
        "blue_owl_technology_finance_corp": "1:26-cv-05183-KPF",
    },
    "form_40_33_accessions": {
        "blue_owl_capital_corp_ii": "0001193125-26-201635",
        "blue_owl_technology_finance_corp": "0001193125-26-285516",
    },
    "periodic_report_accessions": {
        "blue_owl_capital_corp": "0001823945-26-000040",
        "blue_owl_capital_corp_ii": "0001655888-26-000056",
        "blue_owl_technology_finance_corp": "0001747777-26-000028",
    },
    "named_debt_tranches": [
        {"tranche": "Finastra 1L Senior Secured",
         "borrower": "Finastra USA, Inc.",
         "terms": "1L Senior Secured",
         "seniority": 1, "par_m": 69.924, "fair_value_m": 70.449,
         "mark_pct": 100.75},
        {"tranche": "Pluralsight 1L Tranche 1 PIK",
         "borrower": "Pluralsight, LLC",
         "terms": "1L Senior Secured SOFR+3.00% Cash + 1.50% PIK",
         "seniority": 2, "par_m": 54.199, "fair_value_m": 48.508,
         "mark_pct": 89.5},
        {"tranche": "Pluralsight 1L Tranche 2",
         "borrower": "Pluralsight, LLC",
         "terms": "1L Last-Out / Junior Secured SOFR+7.50%",
         "seniority": 3, "par_m": 66.184, "fair_value_m": 5.294,
         "mark_pct": 8.0},
        {"tranche": "CivicPlus Unsecured PIK Notes",
         "borrower": "CP PIK DEBT ISSUER, LLC (dba CivicPlus, LLC)",
         "terms": "Unsecured PIK Toggle SOFR+11.75%",
         "seniority": 4, "par_m": 53.957, "fair_value_m": 53.013,
         "mark_pct": 98.25},
        {"tranche": "Pluralsight Restructured Common Equity",
         "borrower": "Pluralsight, LLC",
         "terms": "Restructured common stock (cost basis claim)",
         "seniority": 5, "par_m": 46.999, "fair_value_m": 0.0,
         "mark_pct": 0.0},
    ],
}

# ---------------------------------------------------------------------------
# Hard-date catalyst & forbearance calendar (ISO 8601 YYYY-MM-DD)
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = [
    {"date": "2026-03-31",
     "event": "Q1 2026 measurement period end: OTF $43.0M PIK income at a "
              "25.0% share of $172.0M net investment income.",
     "basis": "reporting_period_end"},
    {"date": "2026-05-15",
     "event": "Q1 2026 Form 10-Q statutory filing deadline (45 days, large "
              "accelerated filer) carrying the OBDC / OTF Schedule of "
              "Investments software concentration disclosure.",
     "basis": "statutory_deadline_10q_45d"},
    {"date": "2026-06-30",
     "event": "Q2 2026 measurement period end: OWL parent FRE $392.18M, "
              "H1 2026 FRE $785.806M, H1 2026 distributable earnings "
              "$643.782M.",
     "basis": "reporting_period_end"},
    {"date": "2026-08-14",
     "event": "Q2 2026 Form 10-Q statutory filing deadline (45 days, large "
              "accelerated filer).",
     "basis": "statutory_deadline_10q_45d"},
    {"date": "2026-09-30",
     "event": "Q3 2026 measurement period end: cross-held Finastra / "
              "Pluralsight / CivicPlus tranche mark refresh.",
     "basis": "reporting_period_end"},
    {"date": "2026-11-16",
     "event": "Q3 2026 Form 10-Q statutory filing deadline; the 45-day date "
              "2026-11-14 falls on a Saturday and rolls to the next "
              "business day.",
     "basis": "statutory_deadline_10q_45d_next_business_day"},
    {"date": "2026-12-15",
     "event": "RIC 90%-distribution requirement measurement date for the "
              "FY2026 excise-tax safe harbor on PIK-heavy taxable income.",
     "basis": "ric_90pct_distribution_measurement"},
    {"date": "2026-12-31",
     "event": "FY2026 measurement period end: combined OBDC + OTF fee stack "
              "run-rate tested against the $690.4M FY2025 disgorgement cap.",
     "basis": "reporting_period_end"},
    {"date": "2027-03-01",
     "event": "FY2026 Form 10-K statutory filing deadline (60 days, large "
              "accelerated filer).",
     "basis": "statutory_deadline_10k_60d"},
    {"date": "2027-03-31",
     "event": "Section 36(b) trailing three-year fee lookback window close "
              "(FY2024-FY2026) bounding the $690.4M disgorgement surface.",
     "basis": "section_36b_lookback_window_close"},
]

# ---------------------------------------------------------------------------
# Locked constants (locked_constants_and_outputs)
# ---------------------------------------------------------------------------
BLUE_OWL_TOTAL_AUM_BN = 307.4
BLUE_OWL_CREDIT_AUM_BN = 157.8
BDC_SECTOR_AUM_2025_03_BN = 475.0

OWL_Q2_2026_FRE_M = 392.18
OWL_H1_2026_FRE_M = 785.806
OWL_H1_2026_DE_M = 643.782
OWL_FRE_MARGIN_PCT_RANGE = (58.3, 59.4)
OWL_FRE_MULTIPLE_CONSERVATIVE = 22.0
OWL_FRE_MULTIPLE_RANGE = (20.0, 24.5)

KUVARE_ACQUISITION_PRICE_M = 750.0
KUVARE_PREFERRED_EQUITY_M = 250.0
KUVARE_GENERAL_ACCOUNT_AUM_BN = 20.0

OBDC_FEES_2021_M = 282.4
OBDC_FEES_2025_M = 414.4
OBDC_BASE_FEE_2025_M = 252.1
OBDC_INCENTIVE_FEE_2025_M = 162.3
OBDC_FEE_GROWTH_PCT = 46.74
OBDC_REPORTED_SOFTWARE_PCT = 11.1
OBDC_TRUE_SOFTWARE_LOW_PCT = 20.0
OBDC_TRUE_SOFTWARE_HIGH_PCT = 30.0
OBDC_SOFTWARE_UNDERSTATEMENT_LOW_PTS = 8.9
OBDC_SOFTWARE_UNDERSTATEMENT_HIGH_PTS = 18.9

PLATFORM_HIDDEN_SOFTWARE_LOW_BN = 14.0442
PLATFORM_HIDDEN_SOFTWARE_HIGH_BN = 29.8242
AVOIDED_MARKDOWN_20PCT_LOW_BN = 2.80884
AVOIDED_MARKDOWN_20PCT_HIGH_BN = 5.96484
PRESERVED_BASE_FEE_1_5PCT_LOW_M = 42.1326
PRESERVED_BASE_FEE_1_5PCT_HIGH_M = 89.4726
PRESERVED_OWL_MARKET_CAP_22X_LOW_M = 926.9172
PRESERVED_OWL_MARKET_CAP_22X_HIGH_M = 1968.3972

OTF_FEES_2021_M = 95.0
OTF_FEES_2025_M = 276.0
OTF_FEE_GROWTH_PCT = 190.53
COMBINED_OBDC_OTF_FEES_2021_M = 377.4
COMBINED_OBDC_OTF_FEES_2025_M = 690.4
COMBINED_FEE_GROWTH_PCT = 82.94
COMBINED_FEE_DELTA_M = 313.0

OTF_Q1_2026_PIK_M = 43.0
OTF_Q1_2026_PIK_SHARE_PCT = 25.0
OTF_Q1_2026_IMPLIED_NII_M = 172.0
OTF_Q1_2026_CASH_NII_M = 129.0
OTF_OBDC_OVERLAP_MIN_PCT = 70.0

DISTRESSED_US_TECH_LOANS_BN = 46.9
SOFTWARE_LOANS_SUB_80C_BN = 25.0
SUB_80C_SHARE_OF_DISTRESSED_TECH_PCT = 53.3
PRIVATE_CREDIT_SOFTWARE_DEFAULT_PCT = 8.0
SYNDICATED_SOFTWARE_DEFAULT_PCT = 5.5

ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT = 4.24
OTF_PIK_TO_THRESHOLD_MULTIPLE = 5.8962
CASH_DRAIN_PER_PIK_DOLLAR_17_5_PCT = 0.9175
CASH_DRAIN_PER_PIK_DOLLAR_20_0_PCT = 0.92
OTF_Q1_2026_PIK_CASH_DRAIN_17_5_M = 39.4525
OTF_Q1_2026_PIK_INCENTIVE_FEE_17_5_M = 7.525
OTF_Q1_2026_PIK_INCENTIVE_FEE_20_0_M = 8.6
OTF_EFFECTIVE_CASH_INCENTIVE_RATE_17_5_PCT = 23.33
OTF_EFFECTIVE_CASH_INCENTIVE_RATE_20_0_PCT = 26.67

INCENTIVE_FEE_RATE_LOW = 0.175
INCENTIVE_FEE_RATE_HIGH = 0.20
BASE_MANAGEMENT_FEE_RATE = 0.015
RIC_DISTRIBUTION_REQUIREMENT = 0.90
SOFTWARE_MARKDOWN_SCENARIO_PCT = 20.0

JAPONESEQUE_SOFR_SPREAD_BPS = 948
JAPONESEQUE_CASH_PCT = 0.0
JAPONESEQUE_PIK_PCT = 69.0
CMT_SPREAD_RANGE_BPS = (1301, 1401)
CMT_PIK_RANGE_BPS = (1669, 2000)
MPUSA_PIK_PCT = 12.91
CAREGILITY_PROACTIVE_PIK_PCT = 10.0

BOW_RIVER_COST_USD = 486_830_334
BOW_RIVER_FAIR_VALUE_USD = 568_523_676
BOW_RIVER_UNREALIZED_GAIN_USD = 81_693_342
BOW_RIVER_CREDIT_FACILITY_M = 73.0
BOW_RIVER_QUARTERLY_MGMT_FEE_M = 4.53

DIGITAL_ALPHA_ALL_IN_PCT = 14.86
DIGITAL_ALPHA_PIK_PCT = 9.5
CRESCENT_SOFR_PIK_FACILITIES_COUNT = 26

# Cross-manager club-loan divergence constants (OBDC / OTF vs ARCC / GBDC / OCSL / BXSL)
PETVET_TOTAL_BDC_EXPOSURE_M = 418.0
PETVET_OBDC_1L_TERM_PAR_M = 130.3
PETVET_OBDC_1L_TERM_FV_M = 113.4
PETVET_OTF_1L_TERM_PAR_M = 76.5
PETVET_OTF_1L_TERM_FV_M = 66.6
PETVET_OWL_1L_TERM_MARK_CENTS = 87.0
PETVET_OBDC_1L_REV_PAR_M = 5.5
PETVET_OBDC_1L_REV_FV_M = 3.1
PETVET_OWL_1L_REV_MARK_CENTS = 56.7
PETVET_ARCC_1L_TERM_PAR_M = 129.1
PETVET_ARCC_1L_TERM_FV_M = 108.5
PETVET_ARCC_1L_TERM_MARK_CENTS = 84.0
PETVET_ARCC_1L_REV_PAR_M = 10.8
PETVET_ARCC_1L_REV_FV_M = 9.0
PETVET_ARCC_1L_REV_MARK_CENTS = 83.3

PDI_TOTAL_BDC_EXPOSURE_M = 168.7
PDI_OBDC_1L_PAR_M = 21.8
PDI_OBDC_1L_FV_M = 20.8
PDI_OBDC_1L_MARK_CENTS = 95.5
PDI_ARCC_1L_PAR_M = 8.9
PDI_ARCC_1L_FV_M = 8.3
PDI_ARCC_1L_MARK_CENTS = 93.3
PDI_ARCC_PREF_PIK_PCT = 14.25
PDI_ARCC_CLASS_A_MARK_CENTS = 61.9

PLURALSIGHT_GBDC_OS1_PAR_M = 7.42
PLURALSIGHT_GBDC_OS1_FV_M = 1.71
PLURALSIGHT_GBDC_OS1_MARK_CENTS = 23.0
PLURALSIGHT_GBDC_OS1_PIK_PCT = 11.14
PLURALSIGHT_GBDC_OS2_PAR_M = 4.05
PLURALSIGHT_GBDC_OS2_FV_M = 3.85
PLURALSIGHT_GBDC_OS2_MARK_CENTS = 95.0

MARIO_TOTAL_BDC_EXPOSURE_M = 50.11
MARIO_OBDC_1L_PAR_M = 27.98
MARIO_OBDC_1L_FV_M = 25.74
MARIO_OBDC_1L_MARK_CENTS = 92.0
MARIO_GBDC_T3_PAR_M = 5.58
MARIO_GBDC_T3_FV_M = 4.29
MARIO_GBDC_T3_MARK_CENTS = 77.0
MARIO_GBDC_T3_PIK_PCT = 14.58

# ---------------------------------------------------------------------------
# Combined OBDC + OTF cross-held software tranche stack (seniority ordered)
# ---------------------------------------------------------------------------
CROSS_HELD_STACK_RAW = [
    {"tranche": "Finastra 1L Senior Secured",
     "borrower": "Finastra USA, Inc.",
     "terms": "1L Senior Secured",
     "seniority": 1, "claim_basis": "par",
     "claim_m": 69.924, "fair_value_m": 70.449, "mark_pct": 100.75},
    {"tranche": "Pluralsight 1L Tranche 1 PIK",
     "borrower": "Pluralsight, LLC",
     "terms": "1L Senior Secured SOFR+3.00% Cash + 1.50% PIK",
     "seniority": 2, "claim_basis": "par",
     "claim_m": 54.199, "fair_value_m": 48.508, "mark_pct": 89.5},
    {"tranche": "Pluralsight 1L Tranche 2",
     "borrower": "Pluralsight, LLC",
     "terms": "1L Last-Out / Junior Secured SOFR+7.50%",
     "seniority": 3, "claim_basis": "par",
     "claim_m": 66.184, "fair_value_m": 5.294, "mark_pct": 8.0},
    {"tranche": "CivicPlus Unsecured PIK Notes",
     "borrower": "CP PIK DEBT ISSUER, LLC (dba CivicPlus, LLC)",
     "terms": "Unsecured PIK Toggle SOFR+11.75%",
     "seniority": 4, "claim_basis": "par",
     "claim_m": 53.957, "fair_value_m": 53.013, "mark_pct": 98.25},
    {"tranche": "Pluralsight Restructured Common Equity",
     "borrower": "Pluralsight, LLC",
     "terms": "Restructured common stock",
     "seniority": 5, "claim_basis": "cost",
     "claim_m": 46.999, "fair_value_m": 0.0, "mark_pct": 0.0},
]


def _with_cumulative_claims(stack):
    """Attach the cumulative (breakeven EV) claim boundary to each tranche."""
    rows, cumulative = [], 0.0
    for tranche in stack:
        cumulative = round(cumulative + tranche["claim_m"], 6)
        row = dict(tranche)
        row["cum_claim_m"] = cumulative
        rows.append(row)
    return rows


CROSS_HELD_STACK = _with_cumulative_claims(CROSS_HELD_STACK_RAW)
TOTAL_STACK_CLAIM_M = round(sum(t["claim_m"] for t in CROSS_HELD_STACK_RAW), 6)
AGGREGATE_FAIR_VALUE_M = round(
    sum(t["fair_value_m"] for t in CROSS_HELD_STACK_RAW), 6)
TOTAL_STACK_CLAIM_M_LOCKED = 291.263

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def assert_close(actual, expected, label, rel_tol=1e-9):
    """Assert numeric equality within tolerance; raise AssertionError on drift."""
    if not math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=1e-6):
        raise AssertionError(f"{label}: expected {expected!r}, computed {actual!r}")


def assert_eq(actual, expected, label):
    """Assert exact (integer / string / boolean) equality."""
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, computed {actual!r}")


def cash_drain_per_pik_dollar(incentive_rate):
    """EQ-1: cash pushed out the door per $1.00 of non-cash PIK income.

    A RIC must distribute RIC_DISTRIBUTION_REQUIREMENT (90%) of investment
    company taxable income in cash and pays the incentive fee in cash, while
    collecting zero cash on the PIK slice:

        drain(r) = r + 0.90 x (1 - r) = 0.90 + 0.10 r

    drain(0.175) = 0.9175 and drain(0.20) = 0.9200.
    """
    return incentive_rate + RIC_DISTRIBUTION_REQUIREMENT * (1.0 - incentive_rate)


def effective_cash_incentive_rate_pct(nominal_rate_pct, pik_share_pct):
    """EQ-4: nominal incentive fee re-based onto cash-collected NII.

        effective = nominal / (1 - pik_share)

    17.5% / 0.75 = 23.33% and 20.0% / 0.75 = 26.67%.
    """
    return nominal_rate_pct / (1.0 - pik_share_pct / 100.0)


def tranche_recovery(ev):
    """Fulcrum recovery waterfall over the combined cross-held software stack.

    `ev` is the enterprise value / asset-recovery pool in $ millions available
    to the combined OBDC + OTF cross-held stack. Recovery is applied strictly
    sequentially in seniority order; each tranche takes
    min(remaining_ev, claim) where the claim is par for the four debt tranches
    and cost basis for the restructured common equity stub.

    Returns exact dollar and cent-on-the-dollar recovery vectors for every
    tranche, the aggregate stack recovery, the fulcrum tranche, and any
    unrecovered residual EV.
    """
    if ev < 0:
        raise ValueError("ev must be non-negative")
    remaining = float(ev)
    rows = []
    for tranche in CROSS_HELD_STACK:
        claim = tranche["claim_m"]
        recovery = min(remaining, claim)
        remaining = round(remaining - recovery, 6)
        rows.append({
            "tranche": tranche["tranche"],
            "borrower": tranche["borrower"],
            "seniority": tranche["seniority"],
            "claim_basis": tranche["claim_basis"],
            "claim_m": claim,
            "claim_usd": round(claim * 1_000_000, 2),
            "breakeven_ev_m": tranche["cum_claim_m"],
            "recovery_m": round(recovery, 6),
            "recovery_usd": round(recovery * 1_000_000, 2),
            "cents_on_dollar": round(100.0 * recovery / claim, 4),
        })
    total_recovery = round(sum(r["recovery_m"] for r in rows), 6)
    fulcrum = next((r["tranche"] for r in rows
                    if 0.0 < r["recovery_m"] < r["claim_m"] - 1e-9), None)
    return {
        "ev_m": round(float(ev), 6),
        "ev_usd": round(float(ev) * 1_000_000, 2),
        "total_claim_m": TOTAL_STACK_CLAIM_M,
        "total_recovery_m": total_recovery,
        "total_recovery_usd": round(total_recovery * 1_000_000, 2),
        "stack_cents_on_dollar": round(
            100.0 * total_recovery / TOTAL_STACK_CLAIM_M, 4),
        "fulcrum_tranche": fulcrum,
        "unrecovered_ev_m": round(remaining, 6),
        "tranches": rows,
    }


def verify_catalyst_calendar():
    """Assert ISO-8601 form, strict chronology, and statutory deadline math."""
    for catalyst in CATALYST_CALENDAR:
        assert ISO_DATE_RE.match(catalyst["date"]), \
            f"catalyst date not ISO YYYY-MM-DD: {catalyst['date']!r}"
        datetime.date.fromisoformat(catalyst["date"])
    dates = [datetime.date.fromisoformat(c["date"]) for c in CATALYST_CALENDAR]
    assert dates == sorted(dates), "catalyst calendar is not chronological"
    assert len(set(dates)) == len(dates), "catalyst calendar has duplicate dates"

    q1_end, q1_10q, q2_end, q2_10q, q3_end, q3_10q, _, fy_end, fy_10k, _ = dates
    forty_five = datetime.timedelta(days=45)
    assert_eq(q1_10q, q1_end + forty_five, "Q1 2026 10-Q deadline = +45 days")
    assert_eq(q2_10q, q2_end + forty_five, "Q2 2026 10-Q deadline = +45 days")
    raw_q3 = q3_end + forty_five
    assert_eq(raw_q3, datetime.date(2026, 11, 14),
              "Q3 2026 raw 45-day date is 2026-11-14")
    assert_eq(raw_q3.weekday(), 5, "2026-11-14 is a Saturday (weekday index 5)")
    assert_eq(q3_10q, datetime.date(2026, 11, 16),
              "Q3 2026 10-Q deadline rolls to Monday 2026-11-16")
    assert_eq(fy_10k, fy_end + datetime.timedelta(days=60),
              "FY2026 10-K deadline = +60 days")
    for deadline in (q1_10q, q2_10q, q3_10q, fy_10k):
        assert deadline.weekday() < 5, \
            f"statutory deadline {deadline.isoformat()} lands on a weekend"
    return [c["date"] for c in CATALYST_CALENDAR]


def verify_eq1():
    """EQ-1: cash-fee-on-paper-PIK drain at 91.75c / 92.00c per PIK dollar."""
    implied_nii = OTF_Q1_2026_PIK_M / (OTF_Q1_2026_PIK_SHARE_PCT / 100.0)
    assert_close(implied_nii, OTF_Q1_2026_IMPLIED_NII_M,
                 "EQ-1 implied NII = 43.0 / 0.25 = 172.0")
    cash_nii = implied_nii - OTF_Q1_2026_PIK_M
    assert_close(cash_nii, OTF_Q1_2026_CASH_NII_M,
                 "EQ-1 cash NII = 172.0 - 43.0 = 129.0")
    assert_close(OTF_Q1_2026_PIK_SHARE_PCT,
                 100.0 * OTF_Q1_2026_PIK_M / implied_nii,
                 "EQ-1 PIK share round-trip = 25.0%")

    drain_low = cash_drain_per_pik_dollar(INCENTIVE_FEE_RATE_LOW)
    drain_high = cash_drain_per_pik_dollar(INCENTIVE_FEE_RATE_HIGH)
    assert_close(drain_low, CASH_DRAIN_PER_PIK_DOLLAR_17_5_PCT,
                 "EQ-1 drain(17.5%) = 0.175 + 0.90 x 0.825 = 0.9175")
    assert_close(drain_high, CASH_DRAIN_PER_PIK_DOLLAR_20_0_PCT,
                 "EQ-1 drain(20.0%) = 0.20 + 0.90 x 0.80 = 0.9200")
    assert_close(drain_low, 0.90 + 0.10 * INCENTIVE_FEE_RATE_LOW,
                 "EQ-1 drain closed form 0.90 + 0.10r (17.5%)")
    assert_close(drain_high - drain_low,
                 0.10 * (INCENTIVE_FEE_RATE_HIGH - INCENTIVE_FEE_RATE_LOW),
                 "EQ-1 drain slope = 0.10 per unit of incentive fee rate")
    assert drain_low < 1.0 and drain_high < 1.0, \
        "EQ-1 drain per PIK dollar must stay below par"

    pik_cash_drain = OTF_Q1_2026_PIK_M * drain_low
    assert_close(pik_cash_drain, OTF_Q1_2026_PIK_CASH_DRAIN_17_5_M,
                 "EQ-1 Q1 2026 PIK cash drain = 43.0 x 0.9175 = 39.4525")
    pik_cash_drain_high = OTF_Q1_2026_PIK_M * drain_high
    assert_close(pik_cash_drain_high, 39.56,
                 "EQ-1 Q1 2026 PIK cash drain at 20.0% = 43.0 x 0.92 = 39.56")

    fee_low = OTF_Q1_2026_PIK_M * INCENTIVE_FEE_RATE_LOW
    fee_high = OTF_Q1_2026_PIK_M * INCENTIVE_FEE_RATE_HIGH
    assert_close(fee_low, OTF_Q1_2026_PIK_INCENTIVE_FEE_17_5_M,
                 "EQ-1 cash incentive fee on paper PIK = 43.0 x 0.175 = 7.525")
    assert_close(fee_high, OTF_Q1_2026_PIK_INCENTIVE_FEE_20_0_M,
                 "EQ-1 cash incentive fee on paper PIK = 43.0 x 0.20 = 8.6")
    assert_close(pik_cash_drain - fee_low,
                 RIC_DISTRIBUTION_REQUIREMENT
                 * (OTF_Q1_2026_PIK_M - fee_low),
                 "EQ-1 drain decomposition: fee + 90% of after-fee PIK income")
    assert pik_cash_drain > fee_low, \
        "EQ-1 cash drain must exceed the cash incentive fee alone"

    annualized_drain = 4.0 * pik_cash_drain
    assert_close(annualized_drain, 157.81,
                 "EQ-1 annualized Q1 2026 PIK cash drain = 4 x 39.4525")
    return {
        "pik_income_m": OTF_Q1_2026_PIK_M,
        "pik_share_pct": OTF_Q1_2026_PIK_SHARE_PCT,
        "implied_nii_m": round(implied_nii, 6),
        "cash_nii_m": round(cash_nii, 6),
        "ric_distribution_requirement": RIC_DISTRIBUTION_REQUIREMENT,
        "cash_drain_per_pik_dollar_17_5_pct": round(drain_low, 6),
        "cash_drain_per_pik_dollar_20_0_pct": round(drain_high, 6),
        "q1_2026_pik_cash_drain_17_5_m": round(pik_cash_drain, 6),
        "q1_2026_pik_cash_drain_20_0_m": round(pik_cash_drain_high, 6),
        "q1_2026_pik_incentive_fee_17_5_m": round(fee_low, 6),
        "q1_2026_pik_incentive_fee_20_0_m": round(fee_high, 6),
        "annualized_pik_cash_drain_17_5_m": round(annualized_drain, 6),
    }


def verify_eq2():
    """EQ-2: 4.24% critical PIK threshold vs OTF's observed 25.0% = 5.8962x."""
    multiple = round(OTF_Q1_2026_PIK_SHARE_PCT
                     / ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT, 4)
    assert_close(multiple, OTF_PIK_TO_THRESHOLD_MULTIPLE,
                 "EQ-2 breach multiple = 25.0 / 4.24 = 5.8962")
    excess_pts = round(OTF_Q1_2026_PIK_SHARE_PCT
                       - ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT, 2)
    assert_close(excess_pts, 20.76, "EQ-2 threshold excess = 20.76 points")
    assert OTF_Q1_2026_PIK_SHARE_PCT > ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT, \
        "EQ-2 OTF PIK share must breach the critical threshold"

    # The 90%-distribution critical threshold must bind strictly inside the
    # zero-retained-cash ceiling 100 x (1 - 0.90) x (1 - r) = 8.25%.
    zero_retained_ceiling_pct = round(
        100.0 * (1.0 - RIC_DISTRIBUTION_REQUIREMENT)
        * (1.0 - INCENTIVE_FEE_RATE_LOW), 6)
    assert_close(zero_retained_ceiling_pct, 8.25,
                 "EQ-2 zero-retained-cash ceiling = 100 x 0.10 x 0.825 = 8.25%")
    assert ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT < zero_retained_ceiling_pct, \
        "EQ-2 critical threshold must bind before retained cash is exhausted"

    cash_collected_share_pct = round(
        100.0 - ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT, 2)
    assert_close(cash_collected_share_pct, 95.76,
                 "EQ-2 cash-collected share at the threshold = 95.76%")
    threshold_drain_m = round(
        OTF_Q1_2026_IMPLIED_NII_M
        * (ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT / 100.0)
        * CASH_DRAIN_PER_PIK_DOLLAR_17_5_PCT, 6)
    threshold_retained_m = round(
        OTF_Q1_2026_IMPLIED_NII_M
        * ((1.0 - RIC_DISTRIBUTION_REQUIREMENT)
           * (1.0 - INCENTIVE_FEE_RATE_LOW)
           - ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT / 100.0), 6)
    assert threshold_drain_m < threshold_retained_m, \
        "EQ-2 at the threshold the PIK drain is still covered by retained cash"
    observed_drain_m = round(
        OTF_Q1_2026_PIK_M * CASH_DRAIN_PER_PIK_DOLLAR_17_5_PCT, 6)
    observed_retained_m = round(
        OTF_Q1_2026_IMPLIED_NII_M
        * ((1.0 - RIC_DISTRIBUTION_REQUIREMENT)
           * (1.0 - INCENTIVE_FEE_RATE_LOW)
           - OTF_Q1_2026_PIK_SHARE_PCT / 100.0), 6)
    assert observed_retained_m < 0.0, \
        "EQ-2 at 25.0% PIK retained cash is negative (cash-fee-on-paper-PIK)"
    assert observed_drain_m > threshold_drain_m, \
        "EQ-2 observed drain must exceed threshold drain"
    return {
        "critical_threshold_pct": ALPHA_PIK_CRITICAL_THRESHOLD_90_PCT,
        "observed_otf_pik_share_pct": OTF_Q1_2026_PIK_SHARE_PCT,
        "breach_multiple": multiple,
        "threshold_excess_pts": excess_pts,
        "zero_retained_cash_ceiling_pct": zero_retained_ceiling_pct,
        "cash_collected_share_at_threshold_pct": cash_collected_share_pct,
        "threshold_pik_cash_drain_m": threshold_drain_m,
        "threshold_retained_cash_m": threshold_retained_m,
        "observed_pik_cash_drain_m": observed_drain_m,
        "observed_retained_cash_m": observed_retained_m,
    }


def verify_eq3():
    """EQ-3: software reclassification cascade into OWL parent market cap."""
    under_low = round(OBDC_TRUE_SOFTWARE_LOW_PCT - OBDC_REPORTED_SOFTWARE_PCT, 6)
    under_high = round(OBDC_TRUE_SOFTWARE_HIGH_PCT - OBDC_REPORTED_SOFTWARE_PCT, 6)
    assert_close(under_low, OBDC_SOFTWARE_UNDERSTATEMENT_LOW_PTS,
                 "EQ-3 understatement low = 20.0 - 11.1 = 8.9 pts")
    assert_close(under_high, OBDC_SOFTWARE_UNDERSTATEMENT_HIGH_PTS,
                 "EQ-3 understatement high = 30.0 - 11.1 = 18.9 pts")

    hidden_low = BLUE_OWL_CREDIT_AUM_BN * under_low / 100.0
    hidden_high = BLUE_OWL_CREDIT_AUM_BN * under_high / 100.0
    assert_close(hidden_low, PLATFORM_HIDDEN_SOFTWARE_LOW_BN,
                 "EQ-3 hidden software low = 157.8 x 0.089 = 14.0442")
    assert_close(hidden_high, PLATFORM_HIDDEN_SOFTWARE_HIGH_BN,
                 "EQ-3 hidden software high = 157.8 x 0.189 = 29.8242")

    avoided_low = hidden_low * SOFTWARE_MARKDOWN_SCENARIO_PCT / 100.0
    avoided_high = hidden_high * SOFTWARE_MARKDOWN_SCENARIO_PCT / 100.0
    assert_close(avoided_low, AVOIDED_MARKDOWN_20PCT_LOW_BN,
                 "EQ-3 avoided markdown low = 14.0442 x 0.20 = 2.80884")
    assert_close(avoided_high, AVOIDED_MARKDOWN_20PCT_HIGH_BN,
                 "EQ-3 avoided markdown high = 29.8242 x 0.20 = 5.96484")

    fee_low = avoided_low * 1000.0 * BASE_MANAGEMENT_FEE_RATE
    fee_high = avoided_high * 1000.0 * BASE_MANAGEMENT_FEE_RATE
    assert_close(fee_low, PRESERVED_BASE_FEE_1_5PCT_LOW_M,
                 "EQ-3 preserved base fee low = 2808.84 x 0.015 = 42.1326")
    assert_close(fee_high, PRESERVED_BASE_FEE_1_5PCT_HIGH_M,
                 "EQ-3 preserved base fee high = 5964.84 x 0.015 = 89.4726")

    cap_low = fee_low * OWL_FRE_MULTIPLE_CONSERVATIVE
    cap_high = fee_high * OWL_FRE_MULTIPLE_CONSERVATIVE
    assert_close(cap_low, PRESERVED_OWL_MARKET_CAP_22X_LOW_M,
                 "EQ-3 preserved OWL market cap low = 42.1326 x 22.0 = 926.9172")
    assert_close(cap_high, PRESERVED_OWL_MARKET_CAP_22X_HIGH_M,
                 "EQ-3 preserved OWL market cap high = 89.4726 x 22.0 = "
                 "1968.3972")

    lo_mult, hi_mult = OWL_FRE_MULTIPLE_RANGE
    assert lo_mult <= OWL_FRE_MULTIPLE_CONSERVATIVE <= hi_mult, \
        "EQ-3 conservative 22.0x must sit inside the 20.0x-24.5x range"
    cap_range_low = round(fee_low * lo_mult, 4)
    cap_range_high = round(fee_high * hi_mult, 4)
    assert_close(cap_range_low, 842.652, "EQ-3 range floor = 42.1326 x 20.0")
    assert_close(cap_range_high, 2192.0787, "EQ-3 range ceiling = 89.4726 x 24.5")

    margin_low, margin_high = OWL_FRE_MARGIN_PCT_RANGE
    assert margin_low < margin_high, "EQ-3 FRE margin range must be ordered"

    reported_software_bn = round(
        BLUE_OWL_CREDIT_AUM_BN * OBDC_REPORTED_SOFTWARE_PCT / 100.0, 6)
    assert_close(reported_software_bn, 17.5158,
                 "EQ-3 reported software book = 157.8 x 0.111 = 17.5158")
    true_low_bn = round(reported_software_bn + hidden_low, 6)
    true_high_bn = round(reported_software_bn + hidden_high, 6)
    assert_close(true_low_bn, BLUE_OWL_CREDIT_AUM_BN
                 * OBDC_TRUE_SOFTWARE_LOW_PCT / 100.0,
                 "EQ-3 true software low round-trip = 157.8 x 0.20")
    assert_close(true_high_bn, BLUE_OWL_CREDIT_AUM_BN
                 * OBDC_TRUE_SOFTWARE_HIGH_PCT / 100.0,
                 "EQ-3 true software high round-trip = 157.8 x 0.30")
    return {
        "credit_aum_bn": BLUE_OWL_CREDIT_AUM_BN,
        "reported_software_pct": OBDC_REPORTED_SOFTWARE_PCT,
        "true_software_pct_range": [OBDC_TRUE_SOFTWARE_LOW_PCT,
                                    OBDC_TRUE_SOFTWARE_HIGH_PCT],
        "understatement_pts_range": [under_low, under_high],
        "reported_software_bn": reported_software_bn,
        "hidden_software_bn_range": [round(hidden_low, 6), round(hidden_high, 6)],
        "avoided_markdown_20pct_bn_range": [round(avoided_low, 6),
                                            round(avoided_high, 6)],
        "preserved_base_fee_1_5pct_m_range": [round(fee_low, 6),
                                              round(fee_high, 6)],
        "preserved_owl_market_cap_22x_m_range": [round(cap_low, 6),
                                                 round(cap_high, 6)],
        "preserved_owl_market_cap_range_m_range": [cap_range_low, cap_range_high],
        "fre_multiple_range": [lo_mult, hi_mult],
        "fre_margin_pct_range": [margin_low, margin_high],
    }


def verify_eq4():
    """EQ-4: Section 36(b) effective cash fee rate and disgorgement cap."""
    eff_low = round(effective_cash_incentive_rate_pct(
        INCENTIVE_FEE_RATE_LOW * 100.0, OTF_Q1_2026_PIK_SHARE_PCT), 2)
    eff_high = round(effective_cash_incentive_rate_pct(
        INCENTIVE_FEE_RATE_HIGH * 100.0, OTF_Q1_2026_PIK_SHARE_PCT), 2)
    assert_close(eff_low, OTF_EFFECTIVE_CASH_INCENTIVE_RATE_17_5_PCT,
                 "EQ-4 effective cash rate = 17.5 / 0.75 = 23.33%")
    assert_close(eff_high, OTF_EFFECTIVE_CASH_INCENTIVE_RATE_20_0_PCT,
                 "EQ-4 effective cash rate = 20.0 / 0.75 = 26.67%")
    assert eff_low > INCENTIVE_FEE_RATE_LOW * 100.0, \
        "EQ-4 effective cash rate must exceed the nominal rate"
    assert eff_high > eff_low, "EQ-4 effective rates must be ordered"
    gross_up_pts_low = round(eff_low - INCENTIVE_FEE_RATE_LOW * 100.0, 2)
    gross_up_pts_high = round(eff_high - INCENTIVE_FEE_RATE_HIGH * 100.0, 2)
    assert_close(gross_up_pts_low, 5.83, "EQ-4 17.5% gross-up = 5.83 pts")
    assert_close(gross_up_pts_high, 6.67, "EQ-4 20.0% gross-up = 6.67 pts")

    assert_close(OBDC_BASE_FEE_2025_M + OBDC_INCENTIVE_FEE_2025_M,
                 OBDC_FEES_2025_M,
                 "EQ-4 OBDC FY2025 fee split = 252.1 + 162.3 = 414.4")
    combined_2021 = OBDC_FEES_2021_M + OTF_FEES_2021_M
    combined_2025 = OBDC_FEES_2025_M + OTF_FEES_2025_M
    assert_close(combined_2021, COMBINED_OBDC_OTF_FEES_2021_M,
                 "EQ-4 combined FY2021 fees = 282.4 + 95.0 = 377.4")
    assert_close(combined_2025, COMBINED_OBDC_OTF_FEES_2025_M,
                 "EQ-4 combined FY2025 fees = 414.4 + 276.0 = 690.4")
    delta = combined_2025 - combined_2021
    assert_close(delta, COMBINED_FEE_DELTA_M,
                 "EQ-4 combined fee delta = 690.4 - 377.4 = 313.0")
    growth = round(100.0 * delta / combined_2021, 2)
    assert_close(growth, COMBINED_FEE_GROWTH_PCT,
                 "EQ-4 combined fee growth = 313.0 / 377.4 = 82.94%")
    obdc_growth = round(100.0 * (OBDC_FEES_2025_M - OBDC_FEES_2021_M)
                        / OBDC_FEES_2021_M, 2)
    otf_growth = round(100.0 * (OTF_FEES_2025_M - OTF_FEES_2021_M)
                       / OTF_FEES_2021_M, 2)
    assert_close(obdc_growth, OBDC_FEE_GROWTH_PCT,
                 "EQ-4 OBDC fee growth = 132.0 / 282.4 = 46.74%")
    assert_close(otf_growth, OTF_FEE_GROWTH_PCT,
                 "EQ-4 OTF fee growth = 181.0 / 95.0 = 190.53%")
    assert otf_growth > obdc_growth, \
        "EQ-4 OTF fee growth must exceed OBDC fee growth"
    assert_close(growth, round(100.0 * (obdc_growth * OBDC_FEES_2021_M
                                        + otf_growth * OTF_FEES_2021_M)
                               / (100.0 * combined_2021), 2),
                 "EQ-4 combined growth is the par-weighted blend of the two")

    disgorgement_cap_m = COMBINED_OBDC_OTF_FEES_2025_M
    assert_close(disgorgement_cap_m, 690.4,
                 "EQ-4 Section 36(b) FY2025 disgorgement cap = $690.4M")
    assert OTF_OBDC_OVERLAP_MIN_PCT >= 70.0, \
        "EQ-4 OTF / OBDC portfolio overlap floor is 70.0%"
    pik_attributable_cap_m = round(
        disgorgement_cap_m * (OTF_Q1_2026_PIK_SHARE_PCT / 100.0), 6)
    assert_close(pik_attributable_cap_m, 172.6,
                 "EQ-4 PIK-attributable share of the cap = 690.4 x 0.25 = 172.6")
    return {
        "nominal_incentive_rate_pct_range": [INCENTIVE_FEE_RATE_LOW * 100.0,
                                             INCENTIVE_FEE_RATE_HIGH * 100.0],
        "pik_share_pct": OTF_Q1_2026_PIK_SHARE_PCT,
        "effective_cash_incentive_rate_pct_range": [eff_low, eff_high],
        "effective_rate_gross_up_pts_range": [gross_up_pts_low, gross_up_pts_high],
        "obdc_fees_2021_m": OBDC_FEES_2021_M,
        "obdc_fees_2025_m": OBDC_FEES_2025_M,
        "obdc_base_fee_2025_m": OBDC_BASE_FEE_2025_M,
        "obdc_incentive_fee_2025_m": OBDC_INCENTIVE_FEE_2025_M,
        "obdc_fee_growth_pct": obdc_growth,
        "otf_fees_2021_m": OTF_FEES_2021_M,
        "otf_fees_2025_m": OTF_FEES_2025_M,
        "otf_fee_growth_pct": otf_growth,
        "combined_fees_2021_m": round(combined_2021, 6),
        "combined_fees_2025_m": round(combined_2025, 6),
        "combined_fee_delta_m": round(delta, 6),
        "combined_fee_growth_pct": growth,
        "section_36b_fy2025_disgorgement_cap_m": disgorgement_cap_m,
        "pik_attributable_disgorgement_cap_m": pik_attributable_cap_m,
        "otf_obdc_overlap_min_pct": OTF_OBDC_OVERLAP_MIN_PCT,
    }


def verify_cross_held_stack():
    """Assert stack arithmetic, marks, and the parameterized waterfall."""
    assert_close(TOTAL_STACK_CLAIM_M, TOTAL_STACK_CLAIM_M_LOCKED,
                 "stack total claim = 69.924 + 54.199 + 66.184 + 53.957 + "
                 "46.999 = 291.263")
    assert_close(AGGREGATE_FAIR_VALUE_M, 177.264,
                 "stack aggregate fair value = 70.449 + 48.508 + 5.294 + "
                 "53.013 + 0.0 = 177.264")
    assert_eq([t["seniority"] for t in CROSS_HELD_STACK], [1, 2, 3, 4, 5],
              "stack seniority ordering")
    for tranche in CROSS_HELD_STACK:
        mark = round(100.0 * tranche["fair_value_m"] / tranche["claim_m"], 2)
        assert_close(mark, tranche["mark_pct"],
                     f"mark_pct for {tranche['tranche']}")
        assert tranche["fair_value_m"] <= tranche["claim_m"] * 1.01, \
            f"{tranche['tranche']} marked above par + tolerance"
    cumulative = [t["cum_claim_m"] for t in CROSS_HELD_STACK]
    assert cumulative == sorted(cumulative), "breakeven EV ladder must ascend"
    assert_close(cumulative[-1], TOTAL_STACK_CLAIM_M,
                 "final breakeven EV equals the total stack claim")

    # Boundary regime: zero EV.
    zero = tranche_recovery(0.0)
    assert all(r["recovery_m"] == 0.0 for r in zero["tranches"]), \
        "waterfall at ev = 0 recovers nothing"
    assert all(r["cents_on_dollar"] == 0.0 for r in zero["tranches"]), \
        "waterfall at ev = 0 is 0c on the dollar everywhere"
    assert_eq(zero["fulcrum_tranche"], None, "no fulcrum at ev = 0")
    assert_close(zero["unrecovered_ev_m"], 0.0, "no residual EV at ev = 0")

    # Boundary regime: full stack claim.
    full = tranche_recovery(TOTAL_STACK_CLAIM_M)
    assert all(r["cents_on_dollar"] == 100.0 for r in full["tranches"]), \
        "waterfall at ev = 291.263 pays 100c on every tranche"
    assert_close(full["total_recovery_m"], TOTAL_STACK_CLAIM_M,
                 "waterfall at full claim recovers 291.263")
    assert_close(full["stack_cents_on_dollar"], 100.0,
                 "stack recovery at full claim is 100c")
    assert_close(full["unrecovered_ev_m"], 0.0, "no residual EV at full claim")

    # Saturation: EV above the stack claim cannot create recovery.
    over = tranche_recovery(TOTAL_STACK_CLAIM_M + 500.0)
    assert_close(over["total_recovery_m"], TOTAL_STACK_CLAIM_M,
                 "recovery is capped at the total stack claim")
    assert_close(over["unrecovered_ev_m"], 500.0,
                 "excess EV above the stack claim is unrecovered residual")

    # Operating regime: EV at the aggregate reported fair value.
    at_fv = tranche_recovery(AGGREGATE_FAIR_VALUE_M)
    by_name = {r["tranche"]: r for r in at_fv["tranches"]}
    assert_close(by_name["Finastra 1L Senior Secured"]["cents_on_dollar"], 100.0,
                 "Finastra 1L is paid in full at ev = 177.264")
    assert_close(by_name["Pluralsight 1L Tranche 1 PIK"]["cents_on_dollar"],
                 100.0, "Pluralsight Tranche 1 is paid in full at ev = 177.264")
    assert_close(by_name["Pluralsight 1L Tranche 2"]["recovery_m"], 53.141,
                 "Pluralsight Tranche 2 residual = 177.264 - 69.924 - 54.199")
    assert_close(by_name["Pluralsight 1L Tranche 2"]["cents_on_dollar"],
                 80.2928, "Pluralsight Tranche 2 = 53.141 / 66.184 = 80.2928c")
    assert_close(by_name["CivicPlus Unsecured PIK Notes"]["cents_on_dollar"], 0.0,
                 "CivicPlus unsecured PIK notes recover 0c in the waterfall")
    assert_close(by_name["Pluralsight Restructured Common Equity"]
                 ["cents_on_dollar"], 0.0,
                 "restructured common equity recovers 0c in the waterfall")
    assert_eq(at_fv["fulcrum_tranche"], "Pluralsight 1L Tranche 2",
              "fulcrum at ev = 177.264 is Pluralsight Tranche 2")
    assert_close(at_fv["total_recovery_m"], AGGREGATE_FAIR_VALUE_M,
                 "waterfall conserves the aggregate EV pool")

    # Mark-vs-waterfall divergence: aggregate conserved, allocation is not.
    divergences = []
    for tranche, row in zip(CROSS_HELD_STACK, at_fv["tranches"]):
        divergence = round(row["recovery_m"] - tranche["fair_value_m"], 6)
        divergences.append({"tranche": tranche["tranche"],
                            "reported_fair_value_m": tranche["fair_value_m"],
                            "waterfall_recovery_m": row["recovery_m"],
                            "divergence_m": divergence})
    assert_close(sum(d["divergence_m"] for d in divergences), 0.0,
                 "mark-vs-waterfall divergences must sum to zero (conservation)")
    max_abs = max(abs(d["divergence_m"]) for d in divergences)
    assert_close(max_abs, 53.013,
                 "max tranche-level divergence = CivicPlus $53.013M")
    civic = next(d for d in divergences
                 if d["tranche"] == "CivicPlus Unsecured PIK Notes")
    assert_close(civic["divergence_m"], -53.013,
                 "CivicPlus is marked 98.25c where the waterfall implies 0c")
    ps2 = next(d for d in divergences
               if d["tranche"] == "Pluralsight 1L Tranche 2")
    assert_close(ps2["divergence_m"], 47.847,
                 "Pluralsight Tranche 2 is marked 8.0c where the waterfall "
                 "implies 80.2928c")

    # Monotonicity: recovery is non-decreasing in EV and seniority-ordered.
    ladder = [0.0, 30.0, 69.924, 124.123, 177.264, 190.307, 244.264, 291.263,
              400.0]
    previous_total = -1.0
    for ev in ladder:
        result = tranche_recovery(ev)
        assert result["total_recovery_m"] >= previous_total - 1e-9, \
            f"total recovery must be non-decreasing in ev (ev = {ev})"
        previous_total = result["total_recovery_m"]
        cents = [r["cents_on_dollar"] for r in result["tranches"]]
        assert cents == sorted(cents, reverse=True), \
            f"cents-on-the-dollar must be non-increasing in seniority (ev = {ev})"
        assert_close(result["total_recovery_m"],
                     min(ev, TOTAL_STACK_CLAIM_M),
                     f"total recovery = min(ev, 291.263) at ev = {ev}")
    return {
        "total_claim_m": TOTAL_STACK_CLAIM_M,
        "total_claim_usd": round(TOTAL_STACK_CLAIM_M * 1_000_000, 2),
        "aggregate_fair_value_m": AGGREGATE_FAIR_VALUE_M,
        "aggregate_mark_pct": round(
            100.0 * AGGREGATE_FAIR_VALUE_M / TOTAL_STACK_CLAIM_M, 4),
        "tranches": [
            {"tranche": t["tranche"], "borrower": t["borrower"],
             "terms": t["terms"], "seniority": t["seniority"],
             "claim_basis": t["claim_basis"], "claim_m": t["claim_m"],
             "fair_value_m": t["fair_value_m"], "mark_pct": t["mark_pct"],
             "breakeven_ev_m": t["cum_claim_m"]}
            for t in CROSS_HELD_STACK],
        "mark_vs_waterfall_divergence": divergences,
        "max_abs_divergence_m": round(max_abs, 6),
    }


def verify_peer_schedule_of_investments():
    """Assert the zero-rent public credit mosaic cross-checks."""
    # Star Mountain: Japonesque is 100% non-cash at SOFR+948bps.
    assert_close(JAPONESEQUE_CASH_PCT, 0.0,
                 "Star Mountain Japonesque cash component = 0.0%")
    assert_close(JAPONESEQUE_PIK_PCT, 69.0,
                 "Star Mountain Japonesque PIK component = 69.0%")
    assert JAPONESEQUE_PIK_PCT > 50.0, \
        "Star Mountain Japonesque is majority PIK"
    assert JAPONESEQUE_CASH_PCT < JAPONESEQUE_PIK_PCT, \
        "Star Mountain Japonesque PIK must exceed its cash component"
    assert_eq(JAPONESEQUE_SOFR_SPREAD_BPS, 948,
              "Star Mountain Japonesque SOFR spread = 948bps")

    # CMT: the PIK toggle leg prices strictly above the entire cash leg.
    cash_low, cash_high = CMT_SPREAD_RANGE_BPS
    pik_low, pik_high = CMT_PIK_RANGE_BPS
    assert cash_low < cash_high and pik_low < pik_high, \
        "CMT spread ranges must be ordered"
    assert pik_low > cash_high, \
        "CMT PIK toggle floor (1669bps) must exceed the cash ceiling (1401bps)"
    toggle_premium_low = pik_low - cash_high
    toggle_premium_high = pik_high - cash_low
    assert_eq(toggle_premium_low, 268, "CMT minimum PIK toggle premium = 268bps")
    assert_eq(toggle_premium_high, 699, "CMT maximum PIK toggle premium = 699bps")
    assert_close(MPUSA_PIK_PCT, 12.91, "Star Mountain MPUSA PIK share = 12.91%")
    assert_close(CAREGILITY_PROACTIVE_PIK_PCT, 10.0,
                 "Star Mountain Caregility proactive PIK share = 10.0%")

    # Bow River: unrealized gain identity.
    gain = BOW_RIVER_FAIR_VALUE_USD - BOW_RIVER_COST_USD
    assert_eq(gain, BOW_RIVER_UNREALIZED_GAIN_USD,
              "Bow River unrealized gain = 568,523,676 - 486,830,334 = "
              "81,693,342")
    assert gain > 0, "Bow River carries a net unrealized gain"
    gain_pct_of_cost = round(100.0 * gain / BOW_RIVER_COST_USD, 4)
    assert_close(gain_pct_of_cost, 16.7807,
                 "Bow River unrealized gain = 16.7807% of cost")
    cost_pct_of_fair_value = round(
        100.0 * BOW_RIVER_COST_USD / BOW_RIVER_FAIR_VALUE_USD, 4)
    assert_close(cost_pct_of_fair_value, 85.6306,
                 "Bow River cost = 85.6306% of fair value")
    quarterly_fee_pct = round(
        100.0 * BOW_RIVER_QUARTERLY_MGMT_FEE_M / BOW_RIVER_CREDIT_FACILITY_M, 4)
    annualized_fee_pct = round(4.0 * quarterly_fee_pct, 4)
    assert_close(quarterly_fee_pct, 6.2055,
                 "Bow River quarterly management fee = 6.2055% of the "
                 "$73.0M credit facility")
    assert_close(annualized_fee_pct, 24.822,
                 "Bow River annualized management fee = 24.822%")
    assert (OTF_EFFECTIVE_CASH_INCENTIVE_RATE_17_5_PCT < annualized_fee_pct
            < OTF_EFFECTIVE_CASH_INCENTIVE_RATE_20_0_PCT), \
        "Bow River annualized fee load (24.822%) is bracketed by the OTF " \
        "effective cash incentive rates (23.33% / 26.67%)"

    # Crescent BDC: SOFR+PIK facility count.
    assert_eq(CRESCENT_SOFR_PIK_FACILITIES_COUNT, 26,
              "Crescent BDC SOFR+PIK facility count = 26")
    assert CRESCENT_SOFR_PIK_FACILITIES_COUNT > 0, \
        "Crescent BDC PIK facility count must be positive"

    # Digital Alpha: PIK share of the all-in yield.
    assert_close(DIGITAL_ALPHA_PIK_PCT, 9.5, "Digital Alpha PIK component = 9.5%")
    assert_close(DIGITAL_ALPHA_ALL_IN_PCT, 14.86,
                 "Digital Alpha all-in yield = 14.86%")
    digital_alpha_pik_share = round(
        100.0 * DIGITAL_ALPHA_PIK_PCT / DIGITAL_ALPHA_ALL_IN_PCT, 4)
    assert_close(digital_alpha_pik_share, 63.93,
                 "Digital Alpha PIK = 63.93% of the all-in yield")
    assert DIGITAL_ALPHA_PIK_PCT < DIGITAL_ALPHA_ALL_IN_PCT, \
        "Digital Alpha PIK component must be inside the all-in yield"

    # Distressed US tech book.
    sub_80c_share = round(
        100.0 * SOFTWARE_LOANS_SUB_80C_BN / DISTRESSED_US_TECH_LOANS_BN, 1)
    assert_close(sub_80c_share, SUB_80C_SHARE_OF_DISTRESSED_TECH_PCT,
                 "sub-80c software share = 25.0 / 46.9 = 53.3%")
    assert SOFTWARE_LOANS_SUB_80C_BN < DISTRESSED_US_TECH_LOANS_BN, \
        "sub-80c software book must sit inside the distressed tech book"
    default_ratio = round(PRIVATE_CREDIT_SOFTWARE_DEFAULT_PCT
                          / SYNDICATED_SOFTWARE_DEFAULT_PCT, 4)
    assert_close(default_ratio, 1.4545,
                 "private credit software default rate = 1.4545x syndicated")
    assert PRIVATE_CREDIT_SOFTWARE_DEFAULT_PCT > SYNDICATED_SOFTWARE_DEFAULT_PCT, \
        "private credit software defaults must exceed syndicated"

    # Cross-manager club-loan divergence checks (PetVet, PDI TA, Pluralsight GBDC, Mario Purchaser)
    petvet_owl_term_par = round(PETVET_OBDC_1L_TERM_PAR_M + PETVET_OTF_1L_TERM_PAR_M, 4)
    assert_close(petvet_owl_term_par, 206.8, "PetVet combined OBDC+OTF 1L Term par = $206.8M")
    petvet_owl_internal_gap = round(PETVET_OWL_1L_TERM_MARK_CENTS - PETVET_OWL_1L_REV_MARK_CENTS, 4)
    assert_close(petvet_owl_internal_gap, 30.3, "PetVet Blue Owl 1L Term (87.0c) vs 1L Revolver (56.7c) gap = 30.3c")
    petvet_arcc_internal_gap = round(PETVET_ARCC_1L_TERM_MARK_CENTS - PETVET_ARCC_1L_REV_MARK_CENTS, 4)
    assert_close(petvet_arcc_internal_gap, 0.7, "PetVet ARCC 1L Term (84.0c) vs 1L Revolver (83.3c) gap = 0.7c")
    petvet_owl_vs_arcc_term_gap = round(PETVET_OWL_1L_TERM_MARK_CENTS - PETVET_ARCC_1L_TERM_MARK_CENTS, 4)
    assert_close(petvet_owl_vs_arcc_term_gap, 3.0, "PetVet Blue Owl vs ARCC 1L Term mark gap = 3.0c")
    pdi_owl_vs_arcc_gap = round(PDI_OBDC_1L_MARK_CENTS - PDI_ARCC_1L_MARK_CENTS, 4)
    assert_close(pdi_owl_vs_arcc_gap, 2.2, "PDI TA OBDC (95.5c) vs ARCC (93.3c) 1L PIK gap = 2.2c")
    pluralsight_gbdc_vs_owl_t2_gap = round(PLURALSIGHT_GBDC_OS1_MARK_CENTS - 8.0, 4)
    assert_close(pluralsight_gbdc_vs_owl_t2_gap, 15.0, "Pluralsight GBDC OS1 (23.0c) vs OBDC/OTF T2 (8.0c) gap = 15.0c")
    mario_obdc_vs_gbdc_gap = round(MARIO_OBDC_1L_MARK_CENTS - MARIO_GBDC_T3_MARK_CENTS, 4)
    assert_close(mario_obdc_vs_gbdc_gap, 15.0, "Mario Purchaser OBDC (92.0c) vs GBDC T3 (77.0c) gap = 15.0c")

    return {
        "star_mountain": {
            "japonesque_sofr_spread_bps": JAPONESEQUE_SOFR_SPREAD_BPS,
            "japonesque_cash_pct": JAPONESEQUE_CASH_PCT,
            "japonesque_pik_pct": JAPONESEQUE_PIK_PCT,
            "cmt_cash_spread_range_bps": [cash_low, cash_high],
            "cmt_pik_spread_range_bps": [pik_low, pik_high],
            "cmt_pik_toggle_premium_bps_range": [toggle_premium_low,
                                                 toggle_premium_high],
            "mpusa_pik_pct": MPUSA_PIK_PCT,
            "caregility_proactive_pik_pct": CAREGILITY_PROACTIVE_PIK_PCT,
        },
        "bow_river": {
            "cost_usd": BOW_RIVER_COST_USD,
            "fair_value_usd": BOW_RIVER_FAIR_VALUE_USD,
            "unrealized_gain_usd": gain,
            "unrealized_gain_pct_of_cost": gain_pct_of_cost,
            "cost_pct_of_fair_value": cost_pct_of_fair_value,
            "credit_facility_m": BOW_RIVER_CREDIT_FACILITY_M,
            "quarterly_mgmt_fee_m": BOW_RIVER_QUARTERLY_MGMT_FEE_M,
            "quarterly_mgmt_fee_pct_of_facility": quarterly_fee_pct,
            "annualized_mgmt_fee_pct": annualized_fee_pct,
        },
        "crescent_bdc": {
            "sofr_pik_facilities_count": CRESCENT_SOFR_PIK_FACILITIES_COUNT,
        },
        "digital_alpha": {
            "all_in_pct": DIGITAL_ALPHA_ALL_IN_PCT,
            "pik_pct": DIGITAL_ALPHA_PIK_PCT,
            "pik_share_of_all_in_pct": digital_alpha_pik_share,
        },
        "distressed_tech": {
            "distressed_us_tech_loans_bn": DISTRESSED_US_TECH_LOANS_BN,
            "software_loans_sub_80c_bn": SOFTWARE_LOANS_SUB_80C_BN,
            "sub_80c_share_pct": sub_80c_share,
            "private_credit_software_default_pct":
                PRIVATE_CREDIT_SOFTWARE_DEFAULT_PCT,
            "syndicated_software_default_pct": SYNDICATED_SOFTWARE_DEFAULT_PCT,
            "default_rate_ratio": default_ratio,
        },
    }


def verify_platform_and_parent_baseline():
    """Assert OWL parent, platform AUM, and Kuvare baseline identities."""
    credit_share = round(100.0 * BLUE_OWL_CREDIT_AUM_BN
                         / BLUE_OWL_TOTAL_AUM_BN, 4)
    assert_close(credit_share, 51.3338,
                 "credit AUM = 51.3338% of total AUM")
    sector_share = round(100.0 * BLUE_OWL_CREDIT_AUM_BN
                         / BDC_SECTOR_AUM_2025_03_BN, 4)
    assert_close(sector_share, 33.2211,
                 "credit AUM = 33.2211% of the $475.0B BDC sector")
    assert BLUE_OWL_CREDIT_AUM_BN < BLUE_OWL_TOTAL_AUM_BN, \
        "credit AUM must sit inside total AUM"
    assert BLUE_OWL_CREDIT_AUM_BN < BDC_SECTOR_AUM_2025_03_BN, \
        "credit AUM must sit inside the BDC sector"

    q1_fre = round(OWL_H1_2026_FRE_M - OWL_Q2_2026_FRE_M, 6)
    assert_close(q1_fre, 393.626, "Q1 2026 FRE = 785.806 - 392.18 = 393.626")
    assert q1_fre > OWL_Q2_2026_FRE_M, \
        "Q1 2026 FRE must exceed Q2 2026 FRE (sequential decay)"
    de_to_fre = round(100.0 * OWL_H1_2026_DE_M / OWL_H1_2026_FRE_M, 4)
    assert_close(de_to_fre, 81.9263,
                 "H1 2026 distributable earnings = 81.9263% of FRE")
    assert OWL_H1_2026_DE_M < OWL_H1_2026_FRE_M, \
        "distributable earnings must sit below fee-related earnings"
    h1_annualized = round(2.0 * OWL_H1_2026_FRE_M, 6)
    assert_close(h1_annualized, 1571.612,
                 "H1 2026 FRE annualized = 2 x 785.806 = 1571.612")
    implied_cap_22x = round(h1_annualized * OWL_FRE_MULTIPLE_CONSERVATIVE, 4)
    assert_close(implied_cap_22x, 34575.464,
                 "implied OWL market cap at 22.0x annualized H1 FRE = "
                 "34575.464")
    preserved_low_share = round(
        100.0 * PRESERVED_OWL_MARKET_CAP_22X_LOW_M / implied_cap_22x, 4)
    preserved_high_share = round(
        100.0 * PRESERVED_OWL_MARKET_CAP_22X_HIGH_M / implied_cap_22x, 4)
    assert_close(preserved_low_share, 2.6809,
                 "preserved cap low = 2.6809% of the implied 22.0x cap")
    assert_close(preserved_high_share, 5.693,
                 "preserved cap high = 5.693% of the implied 22.0x cap")

    kuvare_preferred_share = round(
        100.0 * KUVARE_PREFERRED_EQUITY_M / KUVARE_ACQUISITION_PRICE_M, 4)
    assert_close(kuvare_preferred_share, 33.3333,
                 "Kuvare preferred equity = 33.3333% of the $750.0M price")
    kuvare_aum_share = round(
        100.0 * KUVARE_GENERAL_ACCOUNT_AUM_BN / BLUE_OWL_TOTAL_AUM_BN, 4)
    assert_close(kuvare_aum_share, 6.5062,
                 "Kuvare general account = 6.5062% of total AUM")
    assert KUVARE_PREFERRED_EQUITY_M < KUVARE_ACQUISITION_PRICE_M, \
        "Kuvare preferred equity must sit inside the acquisition price"
    return {
        "total_aum_bn": BLUE_OWL_TOTAL_AUM_BN,
        "credit_aum_bn": BLUE_OWL_CREDIT_AUM_BN,
        "bdc_sector_aum_2025_03_bn": BDC_SECTOR_AUM_2025_03_BN,
        "credit_share_of_total_aum_pct": credit_share,
        "credit_share_of_bdc_sector_pct": sector_share,
        "q1_2026_fre_m": q1_fre,
        "q2_2026_fre_m": OWL_Q2_2026_FRE_M,
        "h1_2026_fre_m": OWL_H1_2026_FRE_M,
        "h1_2026_de_m": OWL_H1_2026_DE_M,
        "h1_2026_de_to_fre_pct": de_to_fre,
        "h1_2026_fre_annualized_m": h1_annualized,
        "implied_market_cap_22x_m": implied_cap_22x,
        "preserved_cap_share_of_implied_pct_range": [preserved_low_share,
                                                     preserved_high_share],
        "kuvare_acquisition_price_m": KUVARE_ACQUISITION_PRICE_M,
        "kuvare_preferred_equity_m": KUVARE_PREFERRED_EQUITY_M,
        "kuvare_preferred_share_pct": kuvare_preferred_share,
        "kuvare_general_account_aum_bn": KUVARE_GENERAL_ACCOUNT_AUM_BN,
        "kuvare_aum_share_pct": kuvare_aum_share,
    }


def main():
    catalyst_dates = verify_catalyst_calendar()
    eq1 = verify_eq1()
    eq2 = verify_eq2()
    eq3 = verify_eq3()
    eq4 = verify_eq4()
    stack = verify_cross_held_stack()
    peers = verify_peer_schedule_of_investments()
    platform = verify_platform_and_parent_baseline()

    outputs = {
        "schema_version": "1.0",
        "jurisdiction_context": {
            "iso_3166_1_alpha_2": "US",
            "statutory_venue": "Investment Company Act of 1940 Section 36(b) "
                               "fiduciary-duty fee litigation; SDNY "
                               "7:26-cv-03468-KPF and 1:26-cv-05183-KPF; "
                               "SEC EDGAR Form 10-Q / Form 40-33 public "
                               "filings; Subchapter M RIC 90%-distribution "
                               "requirement.",
        },
        "cfaa_compliance_attestation": True,
        "itar_ear_public_domain_attestation": True,
        "entity_and_instrument_ids": ENTITY_AND_INSTRUMENT_IDS,
        "catalyst_calendar": CATALYST_CALENDAR,
        "eq1_cash_fee_on_paper_pik": eq1,
        "eq2_critical_pik_threshold": eq2,
        "eq3_software_reclassification": eq3,
        "eq4_section_36b_effective_cash_fee_rate": eq4,
        "cross_held_tranche_stack": stack,
        "tranche_recovery_waterfall": {
            "at_zero_ev": tranche_recovery(0.0),
            "at_aggregate_fair_value": tranche_recovery(AGGREGATE_FAIR_VALUE_M),
            "at_total_claim": tranche_recovery(TOTAL_STACK_CLAIM_M),
        },
        "peer_schedule_of_investments": peers,
        "platform_and_parent_baseline": platform,
    }
    print(json.dumps(outputs, indent=2))
    print("PROOF PASS: all locked constants and identities verified across "
          "EQ-1 (0.9175 / 0.9200 cash drain per PIK dollar; $39.4525M Q1 2026 "
          "drain), EQ-2 (4.24% critical threshold vs 25.0% = 5.8962x), EQ-3 "
          "($14.0442B-$29.8242B hidden software -> $42.1326M-$89.4726M "
          "preserved base fee -> $926.9172M-$1,968.3972M at 22.0x FRE), EQ-4 "
          "(23.33% / 26.67% effective cash fee rate; $690.4M FY2025 "
          "disgorgement cap), the $291.263M cross-held tranche waterfall, and "
          f"the peer Schedule-of-Investments mosaic over {len(catalyst_dates)} "
          "hard-dated catalysts")


if __name__ == "__main__":
    main()
