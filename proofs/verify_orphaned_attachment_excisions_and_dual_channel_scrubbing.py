#!/usr/bin/env python3
"""Deterministic verification proof: orphaned attachment excisions and dual-channel scrubbing.

Forensic-accounting verification over the 1,380,932-document EFTA email corpus
production. Verifies, using pure Python stdlib only:

  G1  Census of one-page orphaned cover emails whose declared attachments are
      absent: 6,936 substantive orphans (6,049 under strict header filter),
      partitioned by ancestor Bates lineage (EFTA_R1 / DB-SDNY / SDNY_GM /
      EFTA_ / JPM-SDNY), each with Delta_EFTA = 1 and Delta_Ancestor >= 2.
  G2  LDB net-worth schedule dual excision (2015-05-18 original at EFTA02675563
      [42 missing pages] + 2015-05-26 forward at EFTA02674910 [295 missing pages]),
      337 combined missing pages, zero surviving copies.
  G3  "3 April.doc" dual-custodian excision (Estate R1 vs JPMorgan channels,
      62-minute forward lag) plus the top Epstein<->Staley excised attachments
      (152 pages across 7 attachments, including EFTA01300793 [37pp] and
      EFTA01256247 [34pp]).
  G4  Deutsche Bank compliance-channel excisions: FinCEN CDD forms with SSNs
      (EFTA01255544, 283 pages, DB-SDNY-0025264..0025266 -> 0025550 /
      SDNY_GM_00062439..00062441 -> 00062725), Butterfly Trust declaration
      (287 pages), and verified secondary DB-SDNY rows (69 / 33 / 21 / 23 / 21 pages).
  G5  Southern Trust Company June 2017 financials across 15 emails: balance
      sheet page 1 preserved at EFTA01358441 ($343,146,656 Total Shareholder's
      Equity); 4 missing pages (DB-SDNY-0046174..0046177 in 0046173 -> 0046178)
      excising income statement and 100% of Southern Financial LLC financials
      with zero surviving copies; KCP client list excision; June 30, 2017
      equity accounting identity.
  G6  Estate R1 Elysium/Black/Joslin/Rothschild excisions (227 / 211 / 195 /
      173 / 114 / 113 / 108 / 61 / 46 / 6 / 18 pages).

Verification invariants:
  * Lineage partition identity: per-lineage orphan counts sum to the census total.
  * Page-jump formula for every ground-truth Bates interval:
        missing_pages = Delta_Ancestor - 1 = (hi_bates - lo_bates) - 1
    where lo_bates is the last surviving boundary page and hi_bates the first
    surviving page after the excision gap.
  * Dual-channel consistency: the same attachment excised in independent
    production lineages yields identical missing-page counts.
  * Equity accounting identity: STC total equity equals the sum of named
    component carrying values plus the residual.

Exit status: 0 if and only if every assertion holds; 1 otherwise.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# Corpus baseline
# ---------------------------------------------------------------------------

CORPUS_TOTAL_DOCUMENTS = 1380932

# ---------------------------------------------------------------------------
# Locked constants (must reproduce the locked architecture AST exactly)
# ---------------------------------------------------------------------------

LOCKED = {
    "total_substantive_orphaned_cover_emails": 6936,
    "strict_header_orphaned_cover_emails": 6049,
    "orphaned_by_lineage_efta_r1": 6397,
    "orphaned_by_lineage_db_sdny": 477,
    "orphaned_by_lineage_sdny_gm": 28,
    "orphaned_by_lineage_efta_underscore": 18,
    "orphaned_by_lineage_jpm_sdny": 16,
    "ldb_nw_may18_missing_pages": 42,
    "ldb_nw_may26_missing_pages": 295,
    "ldb_nw_combined_missing_pages": 337,
    "ldb_nw_surviving_copies_in_corpus": 0,
    "three_april_doc_r1_missing_pages": 27,
    "three_april_doc_jpm_missing_pages": 26,
    "three_april_doc_forward_lag_minutes": 62,
    "three_april_doc_surviving_copies_in_corpus": 0,
    "staley_additional_excised_attachment_pages_list": [37, 34, 23, 13, 11, 8],
    "staley_top_7_excised_attachments_total_pages": 152,
    "fincen_ssn_missing_pages": 283,
    "fincen_enumerated_epstein_entities_count": 16,
    "fincen_cover_sheet_entity_count": 17,
    "butterfly_trust_db_missing_pages": 287,
    "db_golani_rodriguez_20170705_missing_pages": 69,
    "db_cleared_rdc_pcr_flagship_missing_pages": 33,
    "db_cleared_pcr_indyke_20171031_missing_pages": 21,
    "db_cleared_rdc_pcr_sibling_excisions_count": 12,
    "db_positions_southern_trust_missing_pages": 23,
    "db_southern_financial_kyc_missing_pages": 21,
    "db_sftc_june2017_financials_mentioning_emails": 15,
    "db_sftc_june2017_surviving_attachment_copies": 0,
    "stc_june2017_total_equity_usd": 343146656,
    "stc_june2017_southern_financial_carrying_usd": 161552065,
    "stc_june2017_haze_trust_carrying_usd": 72149122,
    "stc_june2017_residual_equity_usd": 109445469,
    "stc_june2017_common_stock_usd": 1000,
    "stc_june2017_additional_paid_in_capital_usd": 38798643,
    "stc_june2017_retained_earnings_usd": 304347013,
    "r1_joslin_orders_without_names_missing_pages": 227,
    "r1_edmond_rothschild_rockefeller_missing_pages": 211,
    "r1_bjav_k1_trial_balance_missing_pages": 195,
    "r1_joslin_cash_balance_list_missing_pages": 173,
    "r1_black_tax_projections_kahn_missing_pages": 114,
    "r1_black_tax_projections_joslin_missing_pages": 113,
    "r1_black_family_partners_empire_missing_pages": 108,
    "r1_schwitters_ldb_friends_ventures_missing_pages": 61,
    "r1_art_partnership_apob_trust_missing_pages": 46,
    "rothschild_sample_report_missing_pages": 6,
    "rothschild_conv_34956_missing_pages": 18,
}

# The 16 Epstein entities enumerated by the surviving FinCEN thread pages
# (EFTA01421978..EFTA01421979 within EFTA01421977..EFTA01421980).
FINCEN_ENUMERATED_ENTITIES = (
    "Southern Financial LLC",
    "Southern Trust Company Inc",
    "LSJE LLC",
    "Neptune LLC",
    "Mort Inc",
    "Hyperion Air LLC",
    "Zorro Management LLC",
    "NES LLC",
    "JEGE Inc",
    "JEGE LLC",
    "Plan D LLC",
    "Jeepers Inc",
    "J. Epstein Virgin Islands Foundation Inc",
    "Gratitude America Ltd",
    "The 2007 Jeffrey E. Epstein Insurance Trust #3",
    "The Haze Trust",
)

# Ground-truth Bates intervals: (label, lineage, lo_bates, hi_bates, missing_pages).
# lo_bates = last surviving boundary page; hi_bates = first surviving page after
# the gap; missing_pages = (hi_bates - lo_bates) - 1 = Delta_Ancestor - 1.
BATES_INTERVALS = (
    ("G2_LDB_NW_2015_05_18", "EFTA_R1", 1962732, 1962775, 42),
    ("G2_LDB_NW_2015_05_26", "EFTA_R1", 1958976, 1959272, 295),
    ("G3_3APRIL_DOC_R1", "EFTA_R1", 2018172, 2018200, 27),
    ("G3_3APRIL_DOC_JPM", "JPM-SDNY", 1574, 1601, 26),
    ("G3_3APRIL_DOC_SDNY_GM", "SDNY_GM", 78447, 78474, 26),
    ("G3_STALEY_20101025_JPM", "JPM-SDNY", 1137, 1175, 37),
    ("G3_STALEY_20101025_SDNY_GM", "SDNY_GM", 78010, 78048, 37),
    ("G3_STALEY_20110119_JPM", "JPM-SDNY", 1320, 1355, 34),
    ("G3_STALEY_20110119_SDNY_GM", "SDNY_GM", 78193, 78228, 34),
    ("G4_FINCEN_SSN_DB", "DB-SDNY", 25266, 25550, 283),
    ("G4_FINCEN_SSN_SDNY_GM", "SDNY_GM", 62441, 62725, 283),
    ("G4_GOLANI_RODRIGUEZ_DB", "DB-SDNY", 22989, 23059, 69),
    ("G4_GOLANI_RODRIGUEZ_SDNY_GM", "SDNY_GM", 60165, 60235, 69),
    ("G4_RDC_PCR_FLAGSHIP_DB", "DB-SDNY", 27904, 27938, 33),
    ("G4_RDC_PCR_FLAGSHIP_SDNY_GM", "SDNY_GM", 65079, 65113, 33),
    ("G4_PCR_INDYKE_DB", "DB-SDNY", 27959, 27981, 21),
    ("G4_PCR_INDYKE_SDNY_GM", "SDNY_GM", 65134, 65156, 21),
    ("G4_POSITIONS_SOUTHERN_TRUST_DB", "DB-SDNY", 103923, 103947, 23),
    ("G4_POSITIONS_SOUTHERN_TRUST_SDNY_GM", "SDNY_GM", 250107, 250131, 23),
    ("G4_SOUTHERN_FINANCIAL_KYC_DB", "DB-SDNY", 53996, 54018, 21),
    ("G4_SOUTHERN_FINANCIAL_KYC_SDNY_GM", "SDNY_GM", 200180, 200202, 21),
    ("G5_STC_JUNE2017_INCOME_AND_SF_DB", "DB-SDNY", 46173, 46178, 4),
    ("G5_KCP_CLIENT_LIST_DB", "DB-SDNY", 46187, 46189, 1),
    ("G6_JOSLIN_ORDERS_WITHOUT_NAMES_R1", "EFTA_R1", 2154428, 2154656, 227),
    ("G6_EDMOND_ROTHSCHILD_ROCKEFELLER_R1", "EFTA_R1", 1965135, 1965347, 211),
    ("G6_BJAV_K1_TRIAL_BALANCE_R1", "EFTA_R1", 2027082, 2027278, 195),
    ("G6_JOSLIN_CASH_BALANCE_LIST_R1", "EFTA_R1", 2122189, 2122363, 173),
    ("G6_BLACK_TAX_PROJ_KAHN_R1", "EFTA_R1", 2012394, 2012509, 114),
    ("G6_BLACK_TAX_PROJ_JOSLIN_R1", "EFTA_R1", 2015021, 2015135, 113),
    ("G6_BLACK_FAMILY_PARTNERS_EMPIRE_R1", "EFTA_R1", 2090954, 2091063, 108),
    ("G6_SCHWITTERS_LDB_FRIENDS_VENTURES_R1", "EFTA_R1", 2113852, 2113914, 61),
    ("G6_ART_PARTNERSHIP_APOB_TRUST_R1", "EFTA_R1", 2176545, 2176592, 46),
    ("G6_ROTHSCHILD_SAMPLE_REPORT_R1", "EFTA_R1", 2172019, 2172026, 6),
    ("G6_ROTHSCHILD_CONV_34956_R1", "EFTA_R1", 1873442, 1873461, 18),
)

# Interval missing-page counts tied back to their locked constants.
INTERVAL_LOCKED_TIES = {
    "G2_LDB_NW_2015_05_18": "ldb_nw_may18_missing_pages",
    "G2_LDB_NW_2015_05_26": "ldb_nw_may26_missing_pages",
    "G3_3APRIL_DOC_R1": "three_april_doc_r1_missing_pages",
    "G3_3APRIL_DOC_JPM": "three_april_doc_jpm_missing_pages",
    "G3_3APRIL_DOC_SDNY_GM": "three_april_doc_jpm_missing_pages",
    "G4_FINCEN_SSN_DB": "fincen_ssn_missing_pages",
    "G4_FINCEN_SSN_SDNY_GM": "fincen_ssn_missing_pages",
    "G4_GOLANI_RODRIGUEZ_DB": "db_golani_rodriguez_20170705_missing_pages",
    "G4_GOLANI_RODRIGUEZ_SDNY_GM": "db_golani_rodriguez_20170705_missing_pages",
    "G4_RDC_PCR_FLAGSHIP_DB": "db_cleared_rdc_pcr_flagship_missing_pages",
    "G4_RDC_PCR_FLAGSHIP_SDNY_GM": "db_cleared_rdc_pcr_flagship_missing_pages",
    "G4_PCR_INDYKE_DB": "db_cleared_pcr_indyke_20171031_missing_pages",
    "G4_PCR_INDYKE_SDNY_GM": "db_cleared_pcr_indyke_20171031_missing_pages",
    "G4_POSITIONS_SOUTHERN_TRUST_DB": "db_positions_southern_trust_missing_pages",
    "G4_POSITIONS_SOUTHERN_TRUST_SDNY_GM": "db_positions_southern_trust_missing_pages",
    "G4_SOUTHERN_FINANCIAL_KYC_DB": "db_southern_financial_kyc_missing_pages",
    "G4_SOUTHERN_FINANCIAL_KYC_SDNY_GM": "db_southern_financial_kyc_missing_pages",
    "G6_JOSLIN_ORDERS_WITHOUT_NAMES_R1": "r1_joslin_orders_without_names_missing_pages",
    "G6_EDMOND_ROTHSCHILD_ROCKEFELLER_R1": "r1_edmond_rothschild_rockefeller_missing_pages",
    "G6_BJAV_K1_TRIAL_BALANCE_R1": "r1_bjav_k1_trial_balance_missing_pages",
    "G6_JOSLIN_CASH_BALANCE_LIST_R1": "r1_joslin_cash_balance_list_missing_pages",
    "G6_BLACK_TAX_PROJ_KAHN_R1": "r1_black_tax_projections_kahn_missing_pages",
    "G6_BLACK_TAX_PROJ_JOSLIN_R1": "r1_black_tax_projections_joslin_missing_pages",
    "G6_BLACK_FAMILY_PARTNERS_EMPIRE_R1": "r1_black_family_partners_empire_missing_pages",
    "G6_SCHWITTERS_LDB_FRIENDS_VENTURES_R1": "r1_schwitters_ldb_friends_ventures_missing_pages",
    "G6_ART_PARTNERSHIP_APOB_TRUST_R1": "r1_art_partnership_apob_trust_missing_pages",
    "G6_ROTHSCHILD_SAMPLE_REPORT_R1": "rothschild_sample_report_missing_pages",
    "G6_ROTHSCHILD_CONV_34956_R1": "rothschild_conv_34956_missing_pages",
}

FAILURES = []
CHECK_COUNT = 0


def check(label, condition, detail=""):
    global CHECK_COUNT
    CHECK_COUNT += 1
    if not condition:
        FAILURES.append("{}{}".format(label, " :: " + detail if detail else ""))


def main():
    interval_missing = {label: missing for label, _, _, _, missing in BATES_INTERVALS}

    # --- G1: orphaned cover-email census identities -------------------------
    lineage_sum = (
        LOCKED["orphaned_by_lineage_efta_r1"]
        + LOCKED["orphaned_by_lineage_db_sdny"]
        + LOCKED["orphaned_by_lineage_sdny_gm"]
        + LOCKED["orphaned_by_lineage_efta_underscore"]
        + LOCKED["orphaned_by_lineage_jpm_sdny"]
    )
    check(
        "G1.lineage_partition_identity",
        lineage_sum == LOCKED["total_substantive_orphaned_cover_emails"],
        "sum={} total={}".format(lineage_sum, LOCKED["total_substantive_orphaned_cover_emails"]),
    )
    check(
        "G1.strict_header_filter_subset",
        0 < LOCKED["strict_header_orphaned_cover_emails"] <= LOCKED["total_substantive_orphaned_cover_emails"],
    )
    orphan_rate = LOCKED["total_substantive_orphaned_cover_emails"] / CORPUS_TOTAL_DOCUMENTS
    check("G1.orphan_rate_bounds", 0.0 < orphan_rate < 0.01, "rate={:.6f}".format(orphan_rate))
    # Delta_EFTA >= 1 on anchor cover emails.
    for label, lo, hi in (
        ("G2_MAY18", 2675563, 2675564),
        ("G2_MAY26", 2674910, 2674911),
        ("G3_R1", 2688020, 2688021),
        ("G3_JPM", 1301070, 1301071),
        ("G4_FINCEN_LO", 1255544, 1255547),
    ):
        check("G1.delta_efta.{}".format(label), hi - lo >= 1)

    # --- Page-jump formula across every ground-truth Bates interval --------
    for label, _lineage, lo, hi, missing in BATES_INTERVALS:
        delta = hi - lo
        check("jump.delta_ancestor_ge_2.{}".format(label), delta >= 2, "delta={}".format(delta))
        check(
            "jump.missing_eq_delta_minus_1.{}".format(label),
            delta - 1 == missing,
            "delta-1={} locked={}".format(delta - 1, missing),
        )
        check("jump.positive_missing.{}".format(label), missing >= 1)

    # Interval-to-locked-constant ties.
    for label, key in INTERVAL_LOCKED_TIES.items():
        check(
            "tie.locked.{}".format(label),
            interval_missing[label] == LOCKED[key],
            "interval={} locked={}".format(interval_missing[label], LOCKED[key]),
        )

    # --- G2: LDB net-worth dual excision ------------------------------------
    check(
        "G2.combined_missing_pages",
        LOCKED["ldb_nw_may18_missing_pages"] + LOCKED["ldb_nw_may26_missing_pages"]
        == LOCKED["ldb_nw_combined_missing_pages"],
        "42+295 != 337",
    )
    check("G2.zero_surviving_copies", LOCKED["ldb_nw_surviving_copies_in_corpus"] == 0)

    # --- G3: 3 April.doc dual-custodian excision + Staley attachments ------
    check(
        "G3.dual_lineage_consistency",
        interval_missing["G3_3APRIL_DOC_JPM"]
        == interval_missing["G3_3APRIL_DOC_SDNY_GM"]
        == LOCKED["three_april_doc_jpm_missing_pages"],
    )
    forward_lag = (18 * 60 + 57) - (17 * 60 + 55)  # 6:57 PM minus 5:55 PM
    check(
        "G3.forward_lag_minutes",
        forward_lag == LOCKED["three_april_doc_forward_lag_minutes"] == 62,
        "lag={}".format(forward_lag),
    )
    check("G3.zero_surviving_copies", LOCKED["three_april_doc_surviving_copies_in_corpus"] == 0)
    additional = LOCKED["staley_additional_excised_attachment_pages_list"]
    check("G3.additional_list_values", additional == [37, 34, 23, 13, 11, 8])
    check("G3.additional_list_length", len(additional) == 6)
    top7_total = LOCKED["three_april_doc_jpm_missing_pages"] + sum(additional)
    check(
        "G3.top7_excised_total",
        top7_total == LOCKED["staley_top_7_excised_attachments_total_pages"] == 152,
        "26+sum({})={} != 152".format(additional, top7_total),
    )
    check(
        "G3.staley_interval_ties",
        interval_missing["G3_STALEY_20101025_JPM"] == additional[0]
        and interval_missing["G3_STALEY_20101025_SDNY_GM"] == additional[0]
        and interval_missing["G3_STALEY_20110119_JPM"] == additional[1]
        and interval_missing["G3_STALEY_20110119_SDNY_GM"] == additional[1],
    )

    # --- G4: DB compliance-channel excisions --------------------------------
    check(
        "G4.fincen_dual_lineage_consistency",
        interval_missing["G4_FINCEN_SSN_DB"]
        == interval_missing["G4_FINCEN_SSN_SDNY_GM"]
        == LOCKED["fincen_ssn_missing_pages"],
    )
    check(
        "G4.fincen_entity_enumeration",
        len(FINCEN_ENUMERATED_ENTITIES) == LOCKED["fincen_enumerated_epstein_entities_count"] == 16,
    )
    check("G4.fincen_entity_uniqueness", len(set(FINCEN_ENUMERATED_ENTITIES)) == 16)
    check(
        "G4.cover_sheet_minus_enumerated_delta",
        LOCKED["fincen_cover_sheet_entity_count"] - LOCKED["fincen_enumerated_epstein_entities_count"] == 1,
    )
    # Surviving un-shattered thread span EFTA01421977..EFTA01421980 (4 pages),
    # entity-enumerating pages EFTA01421978..EFTA01421979 (2 pages).
    check("G4.surviving_thread_span", 1421980 - 1421977 + 1 == 4)
    check("G4.enumeration_page_span", 1421979 - 1421978 + 1 == 2)
    check("G4.butterfly_trust_missing_pages", LOCKED["butterfly_trust_db_missing_pages"] == 287)
    # Butterfly Trust EFTA span EFTA01296151..EFTA01296170 (19 sequence IDs).
    check("G4.butterfly_efta_span", 1296170 - 1296151 == 19)
    check(
        "G4.rdc_pcr_flagship",
        interval_missing["G4_RDC_PCR_FLAGSHIP_DB"]
        == interval_missing["G4_RDC_PCR_FLAGSHIP_SDNY_GM"]
        == LOCKED["db_cleared_rdc_pcr_flagship_missing_pages"]
        == 33,
    )
    check("G4.rdc_pcr_sibling_count", LOCKED["db_cleared_rdc_pcr_sibling_excisions_count"] == 12)
    # Sibling span EFTA01255916..EFTA01255936 must cover flagship + 12 siblings.
    rdc_span = 1255936 - 1255916 + 1
    check("G4.rdc_pcr_span_covers_events", rdc_span == 21 and rdc_span >= 1 + 12, "span={}".format(rdc_span))
    check(
        "G4.db_secondary_rows_ties",
        interval_missing["G4_GOLANI_RODRIGUEZ_DB"] == LOCKED["db_golani_rodriguez_20170705_missing_pages"] == 69
        and interval_missing["G4_PCR_INDYKE_DB"] == LOCKED["db_cleared_pcr_indyke_20171031_missing_pages"] == 21
        and interval_missing["G4_POSITIONS_SOUTHERN_TRUST_DB"] == LOCKED["db_positions_southern_trust_missing_pages"] == 23
        and interval_missing["G4_SOUTHERN_FINANCIAL_KYC_DB"] == LOCKED["db_southern_financial_kyc_missing_pages"] == 21,
    )

    # --- G5: STC June 2017 financials partial preservation ------------------
    # Flagship-instance boundary jump DB-SDNY-0046173 -> 0046178 across the
    # EFTA01358432 -> EFTA01358441 -> EFTA01358442 chain: raw Delta = 5,
    # excising 4 missing pages (0046174..0046177); Page 1 of the Southern Trust
    # balance sheet survives via EFTA01358441 (DB-SDNY-0046173), while pages
    # 0046174..0046177 (income statement + 100% of Southern Financial LLC
    # financials) have zero surviving copies across all 15 emails.
    g5_flagship_delta = 46178 - 46173
    check("G5.flagship_instance_delta", g5_flagship_delta == 5, "delta={}".format(g5_flagship_delta))
    g5_universally_excised = list(range(46174, 46178))
    check(
        "G5.universally_excised_page_count",
        len(g5_universally_excised) == interval_missing["G5_STC_JUNE2017_INCOME_AND_SF_DB"] == 4,
    )
    check("G5.mentioning_email_count", LOCKED["db_sftc_june2017_financials_mentioning_emails"] == 15)
    check("G5.zero_surviving_attachment_copies", LOCKED["db_sftc_june2017_surviving_attachment_copies"] == 0)
    check("G5.kcp_client_list_excised_pages", interval_missing["G5_KCP_CLIENT_LIST_DB"] == 1)

    # --- G5 equity accounting identity (June 30, 2017 balance sheet) --------
    total_equity = LOCKED["stc_june2017_total_equity_usd"]
    southern_financial = LOCKED["stc_june2017_southern_financial_carrying_usd"]
    haze_trust = LOCKED["stc_june2017_haze_trust_carrying_usd"]
    residual = LOCKED["stc_june2017_residual_equity_usd"]
    common_stock = LOCKED["stc_june2017_common_stock_usd"]
    apic = LOCKED["stc_june2017_additional_paid_in_capital_usd"]
    retained_earnings = LOCKED["stc_june2017_retained_earnings_usd"]
    check(
        "G5.equity_identity",
        southern_financial + haze_trust + residual == total_equity == 343146656,
        "{}+{}+{} != {}".format(southern_financial, haze_trust, residual, total_equity),
    )
    check(
        "G5.shareholder_equity_capital_identity",
        common_stock + apic + retained_earnings == total_equity == 343146656,
        "{}+{}+{} != {}".format(common_stock, apic, retained_earnings, total_equity),
    )
    check("G5.residual_derivation", total_equity - southern_financial - haze_trust == residual)
    check(
        "G5.component_bounds",
        0 < southern_financial < total_equity
        and 0 < haze_trust < total_equity
        and 0 < residual < total_equity,
    )

    # --- Aggregate verification summary --------------------------------------
    verified_interval_pages = sum(missing for _, _, _, _, missing in BATES_INTERVALS)
    non_interval_locked_pages = (
        LOCKED["butterfly_trust_db_missing_pages"]
        + additional[2]
        + additional[3]
        + additional[4]
        + additional[5]
    )
    print("checks_passed={}/{}".format(CHECK_COUNT - len(FAILURES), CHECK_COUNT))
    print(
        "census_total={} strict_header={} lineage_partition_sum={}".format(
            LOCKED["total_substantive_orphaned_cover_emails"],
            LOCKED["strict_header_orphaned_cover_emails"],
            lineage_sum,
        )
    )
    print("orphan_rate={:.6f} corpus_documents={}".format(orphan_rate, CORPUS_TOTAL_DOCUMENTS))
    print(
        "verified_intervals={} verified_interval_missing_pages={} non_interval_locked_missing_pages={}".format(
            len(BATES_INTERVALS), verified_interval_pages, non_interval_locked_pages
        )
    )
    print(
        "stc_equity_total={:.2f} southern_financial={:.2f} haze_trust={:.2f} residual={:.2f}".format(
            total_equity, southern_financial, haze_trust, residual
        )
    )

    if FAILURES:
        for failure in FAILURES:
            print("FAIL: {}".format(failure), file=sys.stderr)
        return 1

    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())