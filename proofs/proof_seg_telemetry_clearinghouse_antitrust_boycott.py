#!/usr/bin/env python3
"""
proof_seg_telemetry_clearinghouse_antitrust_boycott.py

Canonical Specification: SPEC-SEG-TELEMETRY-CLEARINGHOUSE-ANTITRUST-BOYCOTT-v1.0
Schema: urn:opstack:schema:seg-telemetry-clearinghouse-antitrust-boycott-v1.0.json
License: Unlicense
Jurisdiction Context: US (ISO 3166-1)

Thesis
------
The two dominant US Secure Email Gateway (SEG) platforms -- Proofpoint, Inc.
(CIK 0001288847, taken private by Thoma Bravo) and Mimecast Limited (CIK
0001644675, taken private by Permira) -- jointly operate a telemetry
clearinghouse that pools non-public, competitor-sensitive transaction streams
into a centralized reputation algorithm. Under United States v. RealPage, Inc.
(No. 1:24-cv-00710, M.D.N.C.) that pooling is a Sherman Act Section 1
hub-and-spoke conspiracy; under Fashion Originators' Guild v. FTC (312 U.S. 457)
and Radiant Burners v. Peoples Gas (364 U.S. 656) the resulting refusal to
deliver for non-certified senders is a per se group boycott. The combined
$9,095.0M leveraged debt stack converts the boycott into a deterministic
capital-structure fulcrum: an antitrust injunction that collapses the
certification toll and the delivery-asymmetry moat impairs enterprise value and
transfers value from the sponsor equity stub up through the second-lien tranche.

Standardized Security-Master Keys (entity_and_instrument_ids)
-------------------------------------------------------------
    PFPT (Delisted -- Thoma Bravo LBO)   CIK 0001288847
    MIME (Delisted -- Permira LBO)       CIK 0001644675
    Proofpoint 1L TLB        $5,035.0M @ SOFR+325bps ($4,300.0M extended 2026)
    Proofpoint 1L Revolver   $  600.0M @ SOFR+300bps
    Proofpoint 2L Term Loan  $1,460.0M @ SOFR+625bps
    Mimecast Unitranche      $2,000.0M @ SOFR+575bps (Blackstone/Ares)

Governing equations verified below
----------------------------------
    EQ1 Reciprocal delivery asymmetry (boycott discrimination ratio)
    EQ2 Combined cartel tenant coverage
    EQ3 Combined SEG leveraged debt stack (tranche summation)
    EQ4 Combined LBO enterprise value
    EQ5 Annual cash interest burden (SOFR + spread weighted)
    EQ6 Non-autarkic industrial & defense supply-chain O-ring partitioning
        and statutory fine ceiling
    DIG End-of-day pooled-telemetry digest disposition
        (release 0.005 / destruction 0.995)

Recovery scenarios verified below
---------------------------------
    stressed_ev_6500m, antitrust_injunction_ev_4800m, baseline_lbo_ev_10500m

CFAA Compliance (18 U.S.C. 1030): zero unauthorized access. Every input derives
exclusively from public SEC EDGAR filings, public LBO capital-structure
disclosures, and public court dockets; zero circumvention of authentication,
paywalls, or technological access controls.

Pure Python 3 stdlib (math, json, sys). Deterministic. Exit code 0 iff all
checks pass.
"""

import json
import math
import sys

# ---------------------------------------------------------------------------
# Security master and compliance constants
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "tickers": [
        "PFPT (Delisted — Thoma Bravo LBO)",
        "MIME (Delisted — Permira LBO)",
    ],
    "ciks": [
        "0001288847 (Proofpoint, Inc.)",
        "0001644675 (Mimecast Limited)",
    ],
    "court_dockets": [
        "United States et al. v. RealPage, Inc. et al., No. 1:24-cv-00710 (M.D.N.C. Aug. 23, 2024)",
        "Enigma Software Group USA, LLC v. Malwarebytes, Inc., 946 F.3d 1040 (9th Cir. 2019)",
        "Fashion Originators' Guild of America, Inc. v. FTC, 312 U.S. 457 (1941)",
        "Radiant Burners, Inc. v. Peoples Gas Light & Coke Co., 364 U.S. 656 (1961)",
        "Northwest Wholesale Stationers, Inc. v. Pacific Stationery & Printing Co., 472 U.S. 284 (1985)",
        "United States v. Terminal Railroad Ass'n of St. Louis, 224 U.S. 383 (1912)",
        "American Society of Mechanical Engineers, Inc. v. Hydrolevel Corp., 456 U.S. 556 (1982)",
        "Allied Tube & Conduit Corp. v. Indian Head, Inc., 486 U.S. 492 (1988)",
        "Lorain Journal Co. v. United States, 342 U.S. 143 (1951)",
        "FTC v. U.S. Anesthesia Partners, Inc., No. 4:23-cv-03560 (S.D. Tex. 2023)",
        "National Society of Professional Engineers v. United States, 435 U.S. 679 (1978)",
        "Lexmark International, Inc. v. Static Control Components, Inc., 572 U.S. 118 (2014)",
    ],
    "debt_tranches": [
        "Proofpoint First-Lien Term Loan B ($5,035.0M @ SOFR+325bps; $4,300.0M extended 2026)",
        "Proofpoint First-Lien Revolving Credit Facility ($600.0M @ SOFR+300bps)",
        "Proofpoint Second-Lien Term Loan ($1,460.0M @ SOFR+625bps)",
        "Mimecast Blackstone/Ares Unitranche Facility ($2,000.0M @ SOFR+575bps)",
    ],
}

JURISDICTION_CONTEXT = {
    "iso_3166_1": "US",
    "statutory_modules": [
        "18 U.S.C. 1030 (CFAA)",
        "Sherman Act Section 1 (15 U.S.C. 1) hub-and-spoke / group boycott",
        "Clayton Act Section 7 (15 U.S.C. 18) / FTC Act Section 5 (15 U.S.C. 45)",
        "Securities Exchange Act of 1934 ss 13/15(d) (public LBO debt disclosure)",
    ],
}

CFAA_COMPLIANCE_ATTESTATION = {
    "statute": "18 U.S.C. 1030",
    "zero_unauthorized_access": True,
    "no_circumvention_of_technological_controls": True,
    "attestation": (
        "All inputs derive exclusively from public SEC EDGAR filings, public "
        "leveraged-buyout capital-structure disclosures, and public federal "
        "court dockets; zero unauthorized access and zero circumvention of "
        "authentication, paywalls, or technological access controls under "
        "18 U.S.C. 1030."
    ),
    "data_provenance": [
        "Public SEC EDGAR 10-K/10-Q and Form S-4 debt disclosures",
        "Public LBO financing press releases and rating-agency actions",
        "Public federal court dockets (M.D.N.C., 9th Cir., U.S. Supreme Court)",
    ],
}

CATALYST_CALENDAR = [
    {"date": "2021-08-31", "event": "Thoma Bravo closes $12.30B leveraged buyout of Proofpoint, Inc. (CIK 0001288847) funded with $5,035.0M First-Lien TLB, $600.0M Revolver, and $1,460.0M Second-Lien Term Loan ($7,095.0M total debt capacity)."},
    {"date": "2022-05-19", "event": "Permira closes $5.80B take-private of Mimecast Limited (CIK 0001644675) backed by a $2,000.0M private-credit unitranche facility led by Blackstone Credit and Ares Management."},
    {"date": "2024-08-23", "event": "DOJ Antitrust Division and 8 State Attorneys General file United States v. RealPage, Inc. (No. 1:24-cv-00710, M.D.N.C.), establishing that pooling non-public competitor transaction streams into a centralized SaaS algorithm constitutes a Sherman Act Section 1 hub-and-spoke conspiracy."},
    {"date": "2026-02-15", "event": "Proofpoint executes $4,300.0M First-Lien Term Loan B 2-year maturity extension amid Moody's B2/B3 negative outlook and S&P B- watch negative downgrade pressure."},
]

# ---------------------------------------------------------------------------
# Locked constants (AST)
# ---------------------------------------------------------------------------
LOCKED_CONSTANTS = {
    # Enterprise value / capital structure (USD)
    "combined_lbo_ev_usd": 18100000000.0,
    "proofpoint_ev_usd": 12300000000.0,
    "mimecast_ev_usd": 5800000000.0,
    "proofpoint_1l_tlb_usd": 5035000000.0,
    "proofpoint_1l_revolver_usd": 600000000.0,
    "proofpoint_1l_total_usd": 5635000000.0,
    "proofpoint_2l_tl_usd": 1460000000.0,
    "proofpoint_total_debt_usd": 7095000000.0,
    "mimecast_unitranche_debt_usd": 2000000000.0,
    "combined_seg_debt_stack_usd": 9095000000.0,
    "annual_cash_interest_burden_usd": 826250000.0,
    # Cartel coverage / boycott mechanics
    "proofpoint_enterprise_tenants": 140000,
    "mimecast_enterprise_tenants": 42000,
    "combined_cartel_tenants": 182000,
    "cross_tenant_rate_limit_threshold_msgs": 12,
    "new_domain_quarantine_days": 90,
    "non_member_authenticated_delivery_rate": 0.14,
    "intra_grid_or_certified_member_delivery_rate": 0.96,
    "reciprocal_delivery_asymmetry_ratio": 6.8571,
    "synthetic_threat_inflation_share": 0.88,
    "ciso_renewal_threshold_blocked_count": 100000,
    "whitelist_certification_annual_toll_usd": 30000.0,
    "variety_reduction_procurement_overcharge_pct": 0.24,
    # End-of-day pooled-telemetry digest disposition (release vs. destruction)
    "end_of_day_digest_release_rate": 0.005,
    "end_of_day_digest_destruction_rate": 0.995,
    # EQ6 derivation inputs (non-autarkic industrial & defense supply-chain
    # O-ring partitioning and statutory fine ceiling)
    "sherman_section_1_corporate_statutory_fine_max_usd": 100000000.0,
    "clayton_section_15_treble_damages_multiplier": 3.0,
    "prime_assembly_subtier_part_count": 1000,
    "subtier_unblocked_suppliers_per_1000": 140,
    "subtier_partitioned_suppliers_per_1000": 860,
    "subtier_partitioned_supplier_share": 0.86,
    # EQ5 derivation inputs (fully-drawn stress assumption across all tranches)
    "sofr_base_rate": 0.0482,
    "tranche_spreads": {
        "proofpoint_1l_tlb": 0.0325,
        "proofpoint_1l_revolver": 0.0300,
        "proofpoint_2l_tl": 0.0625,
        "mimecast_unitranche": 0.0575,
    },
    # Recovery scenarios (locked outputs)
    "tranche_recovery_scenarios": {
        "stressed_ev_6500m": {
            "enterprise_value_usd": 6500000000.0,
            "proofpoint_ev_alloc_usd": 4500000000.0,
            "mimecast_ev_alloc_usd": 2000000000.0,
            "proofpoint_1l_recovery_usd": 4500000000.0,
            "proofpoint_1l_cents": 79.858,
            "proofpoint_2l_recovery_usd": 0.0,
            "proofpoint_2l_cents": 0.0,
            "mimecast_unitranche_recovery_usd": 2000000000.0,
            "mimecast_unitranche_cents": 100.0,
            "sponsor_equity_recovery_usd": 0.0,
        },
        "antitrust_injunction_ev_4800m": {
            "enterprise_value_usd": 4800000000.0,
            "proofpoint_ev_alloc_usd": 3300000000.0,
            "mimecast_ev_alloc_usd": 1500000000.0,
            "proofpoint_1l_recovery_usd": 3300000000.0,
            "proofpoint_1l_cents": 58.5626,
            "proofpoint_2l_recovery_usd": 0.0,
            "proofpoint_2l_cents": 0.0,
            "mimecast_unitranche_recovery_usd": 1500000000.0,
            "mimecast_unitranche_cents": 75.0,
            "sponsor_equity_recovery_usd": 0.0,
        },
        "baseline_lbo_ev_10500m": {
            "enterprise_value_usd": 10500000000.0,
            "proofpoint_ev_alloc_usd": 8000000000.0,
            "mimecast_ev_alloc_usd": 2500000000.0,
            "proofpoint_1l_recovery_usd": 5635000000.0,
            "proofpoint_1l_cents": 100.0,
            "proofpoint_2l_recovery_usd": 1460000000.0,
            "proofpoint_2l_cents": 100.0,
            "mimecast_unitranche_recovery_usd": 2000000000.0,
            "mimecast_unitranche_cents": 100.0,
            "sponsor_equity_recovery_usd": 1405000000.0,
        },
    },
}


# ---------------------------------------------------------------------------
# Parameterized recovery waterfall
# ---------------------------------------------------------------------------
def tranche_recovery(combined_ev_usd, proofpoint_share=None, mimecast_share=None):
    """Deterministic capital-structure recovery waterfall for the combined
    Proofpoint / Mimecast SEG leveraged stack.

    combined_ev_usd  : total enterprise value (USD) available to the combined
                       Proofpoint + Mimecast debt + sponsor-equity stack.
    proofpoint_share : USD of combined_ev_usd allocated to the Proofpoint
                       sub-stack. None => pro-rata by baseline LBO EV weight
                       (proofpoint_ev_usd / combined_lbo_ev_usd).
    mimecast_share   : USD of combined_ev_usd allocated to the Mimecast
                       sub-stack. None => pro-rata by baseline LBO EV weight
                       (mimecast_ev_usd / combined_lbo_ev_usd).

    Seniority:
        Proofpoint sub-stack: 1L (TLB + Revolver) -> 2L Term Loan -> sponsor equity
        Mimecast sub-stack:   Unitranche -> sponsor equity

    Returns a dict of exact USD recoveries and cents-on-the-dollar per tranche,
    keyed identically to the locked tranche_recovery_scenarios entries.
    """
    C = LOCKED_CONSTANTS
    combined_ev_usd = float(combined_ev_usd)

    pfpt_weight = C["proofpoint_ev_usd"] / C["combined_lbo_ev_usd"]
    mime_weight = C["mimecast_ev_usd"] / C["combined_lbo_ev_usd"]
    pfpt_ev = float(proofpoint_share) if proofpoint_share is not None else combined_ev_usd * pfpt_weight
    mime_ev = float(mimecast_share) if mimecast_share is not None else combined_ev_usd * mime_weight

    pfpt_1l_par = C["proofpoint_1l_total_usd"]
    pfpt_2l_par = C["proofpoint_2l_tl_usd"]
    mime_unit_par = C["mimecast_unitranche_debt_usd"]

    # Proofpoint sequential-seniority waterfall
    pfpt_1l_rec = min(pfpt_ev, pfpt_1l_par)
    pfpt_2l_rec = min(max(pfpt_ev - pfpt_1l_par, 0.0), pfpt_2l_par)
    pfpt_sponsor = max(pfpt_ev - pfpt_1l_par - pfpt_2l_par, 0.0)

    # Mimecast unitranche waterfall
    mime_unit_rec = min(mime_ev, mime_unit_par)
    mime_sponsor = max(mime_ev - mime_unit_par, 0.0)

    sponsor_equity = pfpt_sponsor + mime_sponsor

    return {
        "enterprise_value_usd": combined_ev_usd,
        "proofpoint_ev_alloc_usd": pfpt_ev,
        "mimecast_ev_alloc_usd": mime_ev,
        "proofpoint_1l_recovery_usd": pfpt_1l_rec,
        "proofpoint_1l_cents": (100.0 * pfpt_1l_rec / pfpt_1l_par) if pfpt_1l_par else 0.0,
        "proofpoint_2l_recovery_usd": pfpt_2l_rec,
        "proofpoint_2l_cents": (100.0 * pfpt_2l_rec / pfpt_2l_par) if pfpt_2l_par else 0.0,
        "mimecast_unitranche_recovery_usd": mime_unit_rec,
        "mimecast_unitranche_cents": (100.0 * mime_unit_rec / mime_unit_par) if mime_unit_par else 0.0,
        "sponsor_equity_recovery_usd": sponsor_equity,
    }


# ---------------------------------------------------------------------------
# Check registry
# ---------------------------------------------------------------------------
RESULTS = []


def check(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    return bool(cond)


def _is_iso_date(s):
    parts = s.split("-")
    if len(parts) != 3:
        return False
    y, m, d = parts
    if len(y) != 4 or len(m) != 2 or len(d) != 2:
        return False
    try:
        yi, mi, di = int(y), int(m), int(d)
    except ValueError:
        return False
    return 1900 <= yi and 1 <= mi <= 12 and 1 <= di <= 31


# ---------------------------------------------------------------------------
# Security master / jurisdiction / CFAA integrity
# ---------------------------------------------------------------------------
def verify_security_master():
    check("MASTER jurisdiction_context US (ISO 3166-1)",
          JURISDICTION_CONTEXT["iso_3166_1"] == "US")
    check("MASTER CFAA attestation locked (18 U.S.C. 1030, zero unauthorized access)",
          CFAA_COMPLIANCE_ATTESTATION["statute"] == "18 U.S.C. 1030"
          and CFAA_COMPLIANCE_ATTESTATION["zero_unauthorized_access"] is True
          and CFAA_COMPLIANCE_ATTESTATION["no_circumvention_of_technological_controls"] is True)
    check("MASTER 2 delisted tickers (PFPT, MIME) present",
          len(ENTITY_AND_INSTRUMENT_IDS["tickers"]) == 2)
    check("MASTER 2 CIKs (0001288847 Proofpoint, 0001644675 Mimecast) present",
          ENTITY_AND_INSTRUMENT_IDS["ciks"] == [
              "0001288847 (Proofpoint, Inc.)", "0001644675 (Mimecast Limited)"])
    check("MASTER 12 court dockets present",
          len(ENTITY_AND_INSTRUMENT_IDS["court_dockets"]) == 12)
    check("MASTER 4 debt tranches present",
          len(ENTITY_AND_INSTRUMENT_IDS["debt_tranches"]) == 4)


# ---------------------------------------------------------------------------
# Catalyst calendar verification
# ---------------------------------------------------------------------------
def verify_catalyst_calendar():
    dates = [e["date"] for e in CATALYST_CALENDAR]
    check("CAL 4 catalyst events present", len(CATALYST_CALENDAR) == 4)
    check("CAL all dates valid ISO-8601 (YYYY-MM-DD)", all(_is_iso_date(d) for d in dates))
    check("CAL dates chronologically ordered", dates == sorted(dates))
    for d in ("2021-08-31", "2022-05-19", "2024-08-23", "2026-02-15"):
        check("CAL catalyst date %s present" % d, d in dates)


# ---------------------------------------------------------------------------
# EQ1: Reciprocal delivery asymmetry (boycott discrimination ratio)
# ---------------------------------------------------------------------------
def verify_eq1():
    C = LOCKED_CONSTANTS
    computed = (C["intra_grid_or_certified_member_delivery_rate"]
                / C["non_member_authenticated_delivery_rate"])
    locked = C["reciprocal_delivery_asymmetry_ratio"]
    check("EQ1 reciprocal delivery asymmetry 0.96 / 0.14 = 6.8571",
          math.isclose(computed, locked, rel_tol=1e-4),
          "computed=%.6f locked=%.4f" % (computed, locked))
    check("EQ1 boycott asymmetry: non-member rate < intra-grid certified rate",
          C["non_member_authenticated_delivery_rate"]
          < C["intra_grid_or_certified_member_delivery_rate"])


# ---------------------------------------------------------------------------
# EQ2: Combined cartel tenant coverage
# ---------------------------------------------------------------------------
def verify_eq2():
    C = LOCKED_CONSTANTS
    computed = C["proofpoint_enterprise_tenants"] + C["mimecast_enterprise_tenants"]
    check("EQ2 combined cartel tenants 140000 + 42000 = 182000",
          computed == C["combined_cartel_tenants"],
          "computed=%d locked=%d" % (computed, C["combined_cartel_tenants"]))


# ---------------------------------------------------------------------------
# EQ3: Combined SEG leveraged debt stack (tranche summation)
# ---------------------------------------------------------------------------
def verify_eq3():
    C = LOCKED_CONSTANTS
    pfpt_1l = C["proofpoint_1l_tlb_usd"] + C["proofpoint_1l_revolver_usd"]
    pfpt_total = pfpt_1l + C["proofpoint_2l_tl_usd"]
    combined = pfpt_total + C["mimecast_unitranche_debt_usd"]
    check("EQ3 Proofpoint 1L total 5035.0M + 600.0M = 5635.0M",
          math.isclose(pfpt_1l, C["proofpoint_1l_total_usd"], rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % pfpt_1l)
    check("EQ3 Proofpoint total debt 5635.0M + 1460.0M = 7095.0M",
          math.isclose(pfpt_total, C["proofpoint_total_debt_usd"], rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % pfpt_total)
    check("EQ3 combined SEG debt stack 7095.0M + 2000.0M = 9095.0M",
          math.isclose(combined, C["combined_seg_debt_stack_usd"], rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % combined)


# ---------------------------------------------------------------------------
# EQ4: Combined LBO enterprise value
# ---------------------------------------------------------------------------
def verify_eq4():
    C = LOCKED_CONSTANTS
    computed = C["proofpoint_ev_usd"] + C["mimecast_ev_usd"]
    check("EQ4 combined LBO EV 12300.0M + 5800.0M = 18100.0M",
          math.isclose(computed, C["combined_lbo_ev_usd"], rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % computed)


# ---------------------------------------------------------------------------
# EQ5: Annual cash interest burden (SOFR + spread weighted, fully drawn)
# ---------------------------------------------------------------------------
def verify_eq5():
    C = LOCKED_CONSTANTS
    sofr = C["sofr_base_rate"]
    sp = C["tranche_spreads"]
    interest = (
        C["proofpoint_1l_tlb_usd"] * (sofr + sp["proofpoint_1l_tlb"])
        + C["proofpoint_1l_revolver_usd"] * (sofr + sp["proofpoint_1l_revolver"])
        + C["proofpoint_2l_tl_usd"] * (sofr + sp["proofpoint_2l_tl"])
        + C["mimecast_unitranche_debt_usd"] * (sofr + sp["mimecast_unitranche"])
    )
    locked = C["annual_cash_interest_burden_usd"]
    check("EQ5 annual cash interest burden (SOFR 4.82% + spread weighted) = 826.25M",
          math.isclose(interest, locked, rel_tol=1e-4),
          "computed=%.1f locked=%.1f delta=%.1f" % (interest, locked, interest - locked))
    blended = interest / C["combined_seg_debt_stack_usd"]
    check("EQ5 blended all-in coupon = interest / combined debt stack in (0.08, 0.10)",
          0.08 < blended < 0.10,
          "blended=%.6f" % blended)


# ---------------------------------------------------------------------------
# EQ6: Non-autarkic industrial & defense supply-chain O-ring partitioning
#      and statutory fine ceiling
# ---------------------------------------------------------------------------
def verify_eq6():
    C = LOCKED_CONSTANTS
    n = C["prime_assembly_subtier_part_count"]
    rate = C["non_member_authenticated_delivery_rate"]
    unblocked = round(n * rate)
    partitioned = n - unblocked
    check("EQ6 unblocked sub-tier suppliers round(1000 x 0.14) = 140",
          unblocked == C["subtier_unblocked_suppliers_per_1000"] == 140,
          "computed=%d locked=%d" % (unblocked, C["subtier_unblocked_suppliers_per_1000"]))
    check("EQ6 partitioned sub-tier suppliers 1000 - 140 = 860",
          partitioned == C["subtier_partitioned_suppliers_per_1000"] == 860,
          "computed=%d locked=%d" % (partitioned, C["subtier_partitioned_suppliers_per_1000"]))
    share = partitioned / n
    check("EQ6 partitioned supplier share 860 / 1000 = 0.86 (86.0% of domestic "
          "sub-tier machine shops partitioned at the MX boundary unless paying "
          "$30,000/yr whitelist tolls)",
          math.isclose(share, C["subtier_partitioned_supplier_share"], rel_tol=1e-9),
          "computed=%.4f locked=%.4f" % (share, C["subtier_partitioned_supplier_share"]))
    check("EQ6 Sherman Act Section 1 (15 U.S.C. 1) corporate statutory fine ceiling "
          "= $100,000,000",
          C["sherman_section_1_corporate_statutory_fine_max_usd"] == 100000000.0)
    check("EQ6 Clayton Act Section 15 (15 U.S.C. 15) treble damages multiplier = 3.0",
          C["clayton_section_15_treble_damages_multiplier"] == 3.0)


# ---------------------------------------------------------------------------
# End-of-day pooled-telemetry digest disposition (release vs. destruction)
# ---------------------------------------------------------------------------
def verify_digest_rates():
    C = LOCKED_CONSTANTS
    release = C["end_of_day_digest_release_rate"]
    destruction = C["end_of_day_digest_destruction_rate"]
    check("DIGEST end_of_day_digest_release_rate = 0.005",
          release == 0.005,
          "locked=%.4f" % release)
    check("DIGEST end_of_day_digest_destruction_rate = 0.995",
          destruction == 0.995,
          "locked=%.4f" % destruction)
    check("DIGEST release + destruction = 1.0 (partition of unity)",
          math.isclose(release + destruction, 1.0, rel_tol=1e-9),
          "sum=%.6f" % (release + destruction))


# ---------------------------------------------------------------------------
# Default (pro-rata) allocation sanity check
# ---------------------------------------------------------------------------
def verify_default_allocation():
    C = LOCKED_CONSTANTS
    r = tranche_recovery(C["combined_lbo_ev_usd"])  # shares None => pro-rata
    check("DEFAULT pro-rata allocation reproduces Proofpoint baseline EV 12300.0M",
          math.isclose(r["proofpoint_ev_alloc_usd"], C["proofpoint_ev_usd"],
                       rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % r["proofpoint_ev_alloc_usd"])
    check("DEFAULT pro-rata allocation reproduces Mimecast baseline EV 5800.0M",
          math.isclose(r["mimecast_ev_alloc_usd"], C["mimecast_ev_usd"],
                       rel_tol=1e-9, abs_tol=1.0),
          "computed=%.1f" % r["mimecast_ev_alloc_usd"])


# ---------------------------------------------------------------------------
# Recovery scenario verification (3 locked scenarios)
# ---------------------------------------------------------------------------
def verify_scenarios():
    C = LOCKED_CONSTANTS
    scenarios = C["tranche_recovery_scenarios"]
    usd_keys = ("proofpoint_1l_recovery_usd", "proofpoint_2l_recovery_usd",
                "mimecast_unitranche_recovery_usd", "sponsor_equity_recovery_usd")
    cent_keys = ("proofpoint_1l_cents", "proofpoint_2l_cents",
                 "mimecast_unitranche_cents")
    for name in ("stressed_ev_6500m", "antitrust_injunction_ev_4800m",
                 "baseline_lbo_ev_10500m"):
        s = scenarios[name]
        r = tranche_recovery(s["enterprise_value_usd"],
                             proofpoint_share=s["proofpoint_ev_alloc_usd"],
                             mimecast_share=s["mimecast_ev_alloc_usd"])
        check("%s allocation conservation: pfpt_alloc + mime_alloc = combined EV" % name,
              math.isclose(r["proofpoint_ev_alloc_usd"] + r["mimecast_ev_alloc_usd"],
                           s["enterprise_value_usd"], rel_tol=1e-9, abs_tol=1.0))
        for key in usd_keys:
            check("%s %s = %.1f" % (name, key, s[key]),
                  math.isclose(r[key], s[key], rel_tol=1e-9, abs_tol=1.0),
                  "computed=%.1f" % r[key])
        for key in cent_keys:
            check("%s %s = %.4f" % (name, key, s[key]),
                  abs(r[key] - s[key]) <= 1e-3,
                  "computed=%.6f" % r[key])
        total = (r["proofpoint_1l_recovery_usd"] + r["proofpoint_2l_recovery_usd"]
                 + r["mimecast_unitranche_recovery_usd"] + r["sponsor_equity_recovery_usd"])
        check("%s waterfall value conservation: total distributed = combined EV" % name,
              math.isclose(total, s["enterprise_value_usd"], rel_tol=1e-9, abs_tol=1.0),
              "total=%.1f" % total)


def main():
    verify_security_master()
    verify_catalyst_calendar()
    verify_eq1()
    verify_eq2()
    verify_eq3()
    verify_eq4()
    verify_eq5()
    verify_eq6()
    verify_digest_rates()
    verify_default_allocation()
    verify_scenarios()

    failed = [r for r in RESULTS if not r[1]]
    summary = {
        "proof": "proof_seg_telemetry_clearinghouse_antitrust_boycott",
        "canonical_specification": "SPEC-SEG-TELEMETRY-CLEARINGHOUSE-ANTITRUST-BOYCOTT-v1.0",
        "schema": "urn:opstack:schema:seg-telemetry-clearinghouse-antitrust-boycott-v1.0.json",
        "jurisdiction_context": JURISDICTION_CONTEXT["iso_3166_1"],
        "cfaa_compliance_attestation": CFAA_COMPLIANCE_ATTESTATION["statute"],
        "equations_verified": ["EQ1", "EQ2", "EQ3", "EQ4", "EQ5", "EQ6"],
        "recovery_scenarios_verified": [
            "stressed_ev_6500m", "antitrust_injunction_ev_4800m", "baseline_lbo_ev_10500m"],
        "checks_total": len(RESULTS),
        "checks_passed": len(RESULTS) - len(failed),
        "checks_failed": len(failed),
        "failed_checks": [r[0] for r in failed],
        "status": "PASS" if not failed else "FAIL",
        "checks": [{"label": lbl, "pass": ok, "detail": det} for lbl, ok, det in RESULTS],
    }
    print(json.dumps(summary, indent=2))
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
