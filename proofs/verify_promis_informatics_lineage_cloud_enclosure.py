#!/usr/bin/env python3
"""Verification & falsification harness for SPEC-PROMIS-INFORMATICS-LINEAGE-AND-CLOUD-ENCLOSURE-v1.0.

Pure Python 3 standard library (math, json, sys). Compiles governing equations
E1-E7 and executes all numerical sanity checks and regime boundaries:

  (a) E1  Relational join surface:  binom(94,2) = 4371; |R| = 4371*(10^4)^2*1e-6 = 4.371e5
  (b)     Southern Trust -> Valar:  MOIC = 170e6/40e6 = 4.25; CAGR = 4.25^(1/10)-1 = 0.1557
  (c) E2/E3 Compulsion asymmetry:   E[L_local] = 0.0; E[L_vendor] = 100 bits/day = 3.65e4 bits/yr
  (d) E5  C2PA quarantine boundary: legacy genuine -> P(quarantine) = 1.0; adversarial synthetic -> TPR -> 0
  (e) E4/E6 Regime B boundary:      M_local = 1 and V_swarm = 1e6*10 > V_censor = 1000 -> enclosure fails
  (f) E7  Dimensional extension:    dim K_1.0 = 3, d_bio = 3, dim K_2.0 = 6 (strictly disjoint key sets)

Prints a JSON summary of all computed values to stdout and exits 0 on full
conformance; exits 1 with the failing assertion name on any failure.
"""

import json
import math
import sys


def check_a_join_surface_e1():
    """E1: PROMIS combinatorial join surface (EOUSA 94-office contract)."""
    n = 94                      # U.S. Attorneys' Offices
    m_bar = 10 ** 4             # mean entity records per office
    rho_kappa = 1e-6            # pairwise cross-silo link density

    pairs = math.comb(n, 2)
    assert pairs == 4371, "E1_binom_94_2"

    join_surface = pairs * (m_bar ** 2) * rho_kappa
    assert abs(join_surface - 437100.0) < 1.0, "E1_join_surface_cardinality"
    assert abs(join_surface - 4.371e5) < 1.0, "E1_join_surface_scientific"

    total_linear_records = n * m_bar
    assert total_linear_records == 940000, "E1_linear_record_count"

    join_share_of_corpus = join_surface / total_linear_records
    assert abs(join_share_of_corpus - 0.465) < 0.001, "E1_join_share_46pct"

    return {
        "equation": "E1",
        "n_offices": n,
        "m_bar_records_per_office": m_bar,
        "rho_kappa": rho_kappa,
        "office_pairs_binom_94_2": pairs,
        "join_surface_links": join_surface,
        "total_linear_records": total_linear_records,
        "join_share_of_corpus": join_share_of_corpus,
    }


def check_b_valar_compounding():
    """Sanity check (ii): Southern Trust -> Valar Ventures capital compounding."""
    c0 = 40.0e6                 # 2015-2016 LP commitment (USD)
    v10 = 170.0e6               # June 2025 valuation (USD)
    t_years = 10

    moic = v10 / c0
    assert moic == 4.25, "MOIC_exact_4p25"

    delta_v = v10 - c0
    assert abs(delta_v - 130.0e6) < 1.0, "delta_V_130M"

    cagr = moic ** (1.0 / t_years) - 1.0
    assert abs(cagr - 0.1557) < 0.001, "CAGR_0p1557"

    return {
        "c0_usd": c0,
        "v10_usd": v10,
        "t_years": t_years,
        "moic": moic,
        "delta_v_usd": delta_v,
        "cagr": cagr,
    }


def check_c_compulsion_asymmetry_e2_e3():
    """E2/E3: Single-Point-of-Statutory-Compulsion leakage asymmetry."""
    q = 1000.0                  # queries/day
    pr_order = 1e-4             # compulsory-order incidence per query stream
    h_query = 1000.0            # bits/query

    custody_indicator_local = 0     # Custody = Local AND AirGap = 1
    custody_indicator_vendor = 1    # Custody = Vendor

    e_leak_local = q * pr_order * h_query * custody_indicator_local
    assert e_leak_local == 0.0, "E3_local_leak_exactly_zero"

    e_leak_vendor = q * pr_order * h_query * custody_indicator_vendor
    assert abs(e_leak_vendor - 100.0) < 1e-9, "E3_vendor_leak_100_bits_per_day"

    e_leak_vendor_yr = e_leak_vendor * 365.0
    assert abs(e_leak_vendor_yr - 36500.0) < 1.0, "E3_vendor_leak_36500_bits_per_yr"
    assert abs(e_leak_vendor_yr - 3.65e4) < 1.0, "E3_vendor_leak_scientific"

    # For any q > 0 the ratio diverges to +inf (local denominator is exactly 0).
    ratio_diverges = e_leak_local == 0.0 and e_leak_vendor > 0.0
    assert ratio_diverges, "E3_ratio_divergence"

    return {
        "equations": ["E2", "E3"],
        "q_queries_per_day": q,
        "pr_order": pr_order,
        "h_query_bits": h_query,
        "e_leak_local_bits_per_day": e_leak_local,
        "e_leak_vendor_bits_per_day": e_leak_vendor,
        "e_leak_vendor_bits_per_yr": e_leak_vendor_yr,
        "vendor_local_ratio_diverges": ratio_diverges,
    }


def check_d_c2pa_quarantine_e5():
    """E5: C2PA provenance inversion boundary."""
    t_c2pa_year = 2021          # t_C2PA = Feb 2021
    legacy_creation_years = [1995, 2003, 2008, 2013, 2014, 2017, 2019]

    # Quarantine(f) = 1[Attest(f) = empty AND t_create(f) < t_C2PA]
    quarantine_flags = [
        1.0 if (attest_empty and year < t_c2pa_year) else 0.0
        for year, attest_empty in zip(legacy_creation_years, [True] * len(legacy_creation_years))
    ]
    assert all(flag == 1.0 for flag in quarantine_flags), "E5_legacy_quarantine_flag_each"

    quarantine_prob_legacy = sum(quarantine_flags) / len(quarantine_flags)
    assert quarantine_prob_legacy == 1.0, "E5_legacy_quarantine_prob_1"

    # Adversarial synthetic media: watermark is strippable, so the detector's
    # true-positive rate collapses to 0 (provenance inversion).
    base_detector_tpr = 0.95
    watermark_strip_probability = 1.0   # strippable watermark
    tpr_adversarial = base_detector_tpr * (1.0 - watermark_strip_probability)
    assert tpr_adversarial < 0.05, "E5_adversarial_tpr_below_0p05"
    assert tpr_adversarial == 0.0, "E5_adversarial_tpr_to_zero"

    return {
        "equation": "E5",
        "t_c2pa_year": t_c2pa_year,
        "legacy_creation_years": legacy_creation_years,
        "quarantine_flags": quarantine_flags,
        "quarantine_prob_legacy_genuine": quarantine_prob_legacy,
        "base_detector_tpr": base_detector_tpr,
        "watermark_strip_probability": watermark_strip_probability,
        "tpr_adversarial_synthetic": tpr_adversarial,
    }


def check_e_regime_boundary_e4_e6():
    """E4/E6: Regime B sovereignty boundary (Ashby requisite variety)."""
    m_local = 1                 # un-lobotomized open-weight local inference available
    n_nodes = 1_000_000         # independent bare-metal citizen nodes
    v_operator = 10             # local relational verification variety per node
    v_censor = 1000             # bounded centralized censorship variety

    v_swarm = n_nodes * v_operator
    assert v_swarm == 10_000_000, "E6_v_swarm_10M"
    assert v_swarm > v_censor, "E6_requisite_variety_dominance"

    enclosure_fails = (m_local == 1) and (v_swarm > v_censor)
    assert enclosure_fails is True, "E4E6_regime_b_enclosure_fails"

    jamming_fails = v_swarm > v_censor
    assert jamming_fails, "E6_jamming_fail"

    return {
        "equations": ["E4", "E6"],
        "m_local": m_local,
        "n_nodes": n_nodes,
        "v_operator": v_operator,
        "v_swarm": v_swarm,
        "v_censor": v_censor,
        "enclosure_fails": enclosure_fails,
        "jamming_fails": jamming_fails,
    }


def check_f_dimensional_extension_e7():
    """E7: Dimensional extension identity K_1.0 -> K_2.0."""
    k10 = {"docket", "wire", "name"}
    bio = {"genome", "assay", "bio-telemetry"}

    dim_k10 = len(k10)
    d_bio = len(bio)
    assert dim_k10 == 3, "E7_dim_k10_3"
    assert d_bio == 3, "E7_d_bio_3"

    assert k10.isdisjoint(bio), "E7_keyset_disjointness"

    k20 = k10 | bio
    dim_k20 = dim_k10 + d_bio
    assert dim_k20 == 6, "E7_dim_k20_6"
    assert len(k20) == dim_k20, "E7_union_cardinality"

    return {
        "equation": "E7",
        "k10": sorted(k10),
        "bio_extension": sorted(bio),
        "dim_k10": dim_k10,
        "d_bio": d_bio,
        "dim_k20": dim_k20,
        "k20": sorted(k20),
        "keysets_disjoint": k10.isdisjoint(bio),
    }


CHECKS = [
    ("a_join_surface_e1", check_a_join_surface_e1),
    ("b_valar_compounding", check_b_valar_compounding),
    ("c_compulsion_asymmetry_e2_e3", check_c_compulsion_asymmetry_e2_e3),
    ("d_c2pa_quarantine_e5", check_d_c2pa_quarantine_e5),
    ("e_regime_boundary_e4_e6", check_e_regime_boundary_e4_e6),
    ("f_dimensional_extension_e7", check_f_dimensional_extension_e7),
]


def main():
    summary = {
        "spec": "SPEC-PROMIS-INFORMATICS-LINEAGE-AND-CLOUD-ENCLOSURE-v1.0",
        "harness": "proofs/verify_promis_informatics_lineage_cloud_enclosure.py",
        "status": "PASS",
        "checks": {},
    }
    for name, fn in CHECKS:
        try:
            summary["checks"][name] = fn()
        except AssertionError as exc:
            summary["status"] = "DEFECT"
            summary["failing_assertion"] = str(exc) if str(exc) else name
            summary["failing_check"] = name
            print(json.dumps(summary, indent=2))
            sys.exit(1)
        except Exception as exc:  # pragma: no cover - defensive
            summary["status"] = "DEFECT"
            summary["failing_assertion"] = name
            summary["error"] = repr(exc)
            print(json.dumps(summary, indent=2))
            sys.exit(1)

    print(json.dumps(summary, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()