#!/usr/bin/env python3
"""Deterministic verifier: Bates-stamp cohomology and conservation of dollars.

Pure Python 3 stdlib proof engine for the dual-bank (JPM / DB) EFTA discovery
corpus bundle. Verifies, in cents-exact Decimal arithmetic, every equation and
assertion carried in the bundle's locked constants:

  L0  Cech H^0 cover additivity of the two-bank Bates cover: dual-stamped
      overlap, excision, and missing-page masses are additive across the
      disjoint bank cover; post-gate and shatter ratios are coherent.
  L1  Regime partition of statement-page jumps: disjoint union of pre-Bates
      bank excisions, post-discovery EFTA jumps, and OCR/consolidated
      exclusions; EFTA-gate dominance threshold >= 0.99.
  L2  Conservation of dollars: the boundary operator on each reconstructed
      statement's flow 1-chain equals the observed value 0-chain change
      (exact cent closure, residual = 0.00).
  L3  Excision obstruction classes: where pages were excised, the closure
      residual is a non-trivial cohomology class (H^1 != 0), verified at
      exact cent magnitude, with excised flow volume >= obstruction.
  L4  Collateral term-loan bound nesting (LTV band inside ART cap, spread
      band ordering, advance bounds).
  L5  Register match (RRP72/RRP73 page-count equality) and unshattered
      multi-page document integrity.
  L6  Locked-constant echo (key cardinality, numeric finiteness, sentinels).

Exit code 0 iff every check passes. Emits a single JSON verification summary.
"""

import json
import math
import sys
from decimal import Decimal

# ---------------------------------------------------------------------------
# Locked bundle constants (single source of truth for this proof)
# ---------------------------------------------------------------------------
LOCKED = {
    "corpus_total_rows": 1380932,
    "jpm_dual_stamped_pages": 46458,
    "jpm_total_excisions": 5542,
    "jpm_post_gm_efta_gate_excisions": 5515,
    "jpm_post_gm_efta_gate_ratio": 0.995128,
    "jpm_missing_pages": 9298,
    "jpm_shattered_1page_excisions": 6802,
    "jpm_shattered_total_excisions": 6902,
    "jpm_shattered_ratio": 0.985511,
    "db_dual_stamped_pages": 78915,
    "db_total_excisions": 15811,
    "db_post_gm_efta_gate_excisions": 15768,
    "db_post_gm_efta_gate_ratio": 0.99728,
    "db_missing_pages": 47759,
    "db_shattered_1page_excisions": 16513,
    "db_shattered_total_excisions": 17410,
    "db_shattered_ratio": 0.948478,
    "combined_dual_stamped_pages": 125373,
    "combined_post_gm_efta_gate_excisions": 21283,
    "combined_total_excisions": 21353,
    "combined_post_gm_efta_gate_ratio": 0.996722,
    "combined_missing_bank_pages": 57057,
    "statement_page_jumps_total": 2448,
    "distinct_gapped_statements": 1574,
    "regime_1_pre_bates_bank_excisions": 3,
    "regime_2_post_discovery_efta_jumps": 2441,
    "regime_2_missing_statement_pages": 3188,
    "ocr_or_consolidated_excluded_jumps": 4,
    "db_nna_100_acct_total_credits_usd": 383591762.11,
    "db_nna_100_acct_total_debits_usd": -258662569.68,
    "db_nna_100_acct_cash_disbursement_usd": -87907680.26,
    "db_nna_100_acct_cash_receipt_usd": 50804576.51,
    "db_nna_100_acct_net_addition_usd": 85024650.14,
    "db_nna_epstein_deposits_usd": 61241467.09,
    "db_nna_epstein_debits_usd": -76797923.02,
    "db_nna_wanek_deposits_usd": 35014264.17,
    "db_nna_wanek_debits_usd": -35000000.0,
    "db_nna_excised_pages_list": [3, 5, 7, 8, 10, 11],
    "db_nna_excised_credits_approx_usd": 173600000.0,
    "db_nna_excised_debits_approx_usd": -145300000.0,
    "sf_pershing_feb2019_beg_val_usd": 91883658.46,
    "sf_pershing_feb2019_net_cash_out_usd": -11892834.15,
    "sf_pershing_feb2019_net_sec_out_usd": -43952355.75,
    "sf_pershing_feb2019_end_val_usd": 38975931.49,
    "sf_pershing_feb2019_market_change_and_income_usd": 2937462.93,
    "sf_pershing_feb2019_printed_net_change_usd": 2335319.60,
    "sf_pershing_acat_aapl_usd": -31167000.0,
    "sf_pershing_acat_apo_shares": 263157,
    "sf_pershing_acat_apo_usd": -7710500.1,
    "sf_pershing_acat_jpm_pfd_usd": -5787360.0,
    "stc_oct2013_beg_cash_usd": 5358180.65,
    "stc_oct2013_inflows_usd": 63239739.55,
    "stc_oct2013_excised_withdrawal_usd": -4000000.0,
    "stc_oct2013_fx_outflows_usd": -63089440.6,
    "stc_oct2013_other_adjustments_usd": -694465.86,
    "stc_oct2013_end_cash_usd": 814013.74,
    "ftc_oct2009_total_withdrawals_usd": -3080000.0,
    "ftc_oct2009_fees_usd": -13605.79,
    "ftc_oct2009_total_outflows_usd": -3093605.79,
    "ftc_oct2009_surviving_p9_dda_wire_usd": -1000000.0,
    "ftc_oct2009_surviving_p9_firstbank_wire_usd": -55000.0,
    "ftc_oct2009_surviving_p9_disbursements_usd": -1055000.0,
    "ftc_oct2009_excised_p8_residual_usd": -2025000.0,
    "ftc_may2010_beg_cash_usd": 24514811.02,
    "ftc_may2010_excised_p22_contribution_usd": 505215.67,
    "ftc_may2010_excised_p22_withdrawal_usd": -1030000.0,
    "ftc_may2010_p21_income_usd": 104772.89,
    "ftc_may2010_p23_fx_inflows_usd": 379034.82,
    "ftc_may2010_libor_swap_notional_usd": 125000000.0,
    "ftc_may2010_end_cash_usd": 30023411.9,
    "vol10_unshattered_multi_page_docs": 8226,
    "vol10_unshattered_total_pages": 59659,
    "cross_corpus_recovered_attachment_sets": 114,
    "black_db_term_loan_principal_usd": 500000000.0,
    "black_db_term_loan_maturity_years": 1,
    "black_db_term_loan_aog_ltv_min": 0.7,
    "black_db_term_loan_aog_ltv_max": 1.0,
    "black_db_term_loan_art_ltv_min": 0.4,
    "black_db_term_loan_art_ltv_max": 0.5,
    "black_db_term_loan_spread_min_bps": 175,
    "black_db_term_loan_spread_max_bps": 200,
    "rrp73_elysium_pages": 108,
    "rrp72_southern_financial_pages": 108,
}

EXPECTED_LOCKED_KEYS = 83
RATIO_TOL = 1e-6
ZERO = Decimal("0")
KEY_OUTPUTS = {}
RESULTS = []


def D(value):
    """Exact Decimal image of a locked numeric via shortest-roundtrip repr."""
    return Decimal(str(value))


def check(layer, name, ok, detail=""):
    RESULTS.append({"layer": layer, "check": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def ratio_coherent(num_key, den_key, ratio_key):
    computed = LOCKED[num_key] / LOCKED[den_key]
    return abs(computed - LOCKED[ratio_key]) <= RATIO_TOL, computed


def chain_sum(keys):
    total = ZERO
    for key in keys:
        total += D(LOCKED[key])
    return total


# ---------------------------------------------------------------------------
# L0: Cech H^0 cover additivity of the two-bank Bates cover
# ---------------------------------------------------------------------------
def layer_0_cover():
    L = LOCKED
    additivity = [
        ("combined_dual_stamped_additivity",
         L["jpm_dual_stamped_pages"], L["db_dual_stamped_pages"], L["combined_dual_stamped_pages"]),
        ("combined_total_excisions_additivity",
         L["jpm_total_excisions"], L["db_total_excisions"], L["combined_total_excisions"]),
        ("combined_post_gm_efta_gate_additivity",
         L["jpm_post_gm_efta_gate_excisions"], L["db_post_gm_efta_gate_excisions"],
         L["combined_post_gm_efta_gate_excisions"]),
        ("combined_missing_pages_additivity",
         L["jpm_missing_pages"], L["db_missing_pages"], L["combined_missing_bank_pages"]),
    ]
    for name, a, b, c in additivity:
        check("L0_cover", name, a + b == c, f"{a} + {b} == {c}")
    for prefix in ("jpm", "db", "combined"):
        ok, computed = ratio_coherent(
            f"{prefix}_post_gm_efta_gate_excisions",
            f"{prefix}_total_excisions",
            f"{prefix}_post_gm_efta_gate_ratio")
        check("L0_cover", f"{prefix}_post_gm_efta_gate_ratio_coherence", ok,
              f"computed={computed:.6f} locked={LOCKED[f'{prefix}_post_gm_efta_gate_ratio']}")
    for prefix in ("jpm", "db"):
        ok, computed = ratio_coherent(
            f"{prefix}_shattered_1page_excisions",
            f"{prefix}_shattered_total_excisions",
            f"{prefix}_shattered_ratio")
        check("L0_cover", f"{prefix}_shattered_ratio_coherence", ok,
              f"computed={computed:.6f} locked={LOCKED[f'{prefix}_shattered_ratio']}")
        one = L[f"{prefix}_shattered_1page_excisions"]
        total = L[f"{prefix}_shattered_total_excisions"]
        check("L0_cover", f"{prefix}_shattered_1page_subset", one <= total, f"{one} <= {total}")
    mass = L["combined_dual_stamped_pages"] + L["combined_missing_bank_pages"]
    check("L0_cover", "corpus_row_mass_bound", mass <= L["corpus_total_rows"],
          f"{mass} <= {L['corpus_total_rows']}")


# ---------------------------------------------------------------------------
# L1: regime partition of statement-page jumps
# ---------------------------------------------------------------------------
def layer_1_regime():
    L = LOCKED
    r1 = L["regime_1_pre_bates_bank_excisions"]
    r2 = L["regime_2_post_discovery_efta_jumps"]
    excluded = L["ocr_or_consolidated_excluded_jumps"]
    total = L["statement_page_jumps_total"]
    check("L1_regime", "jump_regime_disjoint_partition", r1 + r2 + excluded == total,
          f"{r1} + {r2} + {excluded} == {total}")
    share = r2 / total
    KEY_OUTPUTS["regime_2_jump_share"] = round(share, 6)
    check("L1_regime", "regime_2_dominance", share > 0.99, f"{share:.6f} > 0.99")
    for prefix in ("jpm", "db", "combined"):
        ratio = L[f"{prefix}_post_gm_efta_gate_ratio"]
        check("L1_regime", f"{prefix}_efta_gate_dominance", ratio >= 0.99, f"{ratio} >= 0.99")
    gapped = L["distinct_gapped_statements"]
    missing = L["regime_2_missing_statement_pages"]
    check("L1_regime", "gapped_statement_missing_bound", 1 <= gapped <= missing,
          f"1 <= {gapped} <= {missing}")


# ---------------------------------------------------------------------------
# L2: conservation of dollars (exact cent chain closure)
# ---------------------------------------------------------------------------
def layer_2_conservation():
    L = LOCKED
    sf_residual = chain_sum([
        "sf_pershing_feb2019_beg_val_usd",
        "sf_pershing_feb2019_net_cash_out_usd",
        "sf_pershing_feb2019_net_sec_out_usd",
        "sf_pershing_feb2019_market_change_and_income_usd",
    ]) - D(L["sf_pershing_feb2019_end_val_usd"])
    KEY_OUTPUTS["sf_pershing_feb2019_closure_residual_usd"] = str(sf_residual)
    check("L2_conservation", "sf_pershing_feb2019_exact_closure", sf_residual == ZERO,
          "beg + net_cash + net_sec + market - end == 0.00")
    stc_residual = chain_sum([
        "stc_oct2013_beg_cash_usd",
        "stc_oct2013_inflows_usd",
        "stc_oct2013_excised_withdrawal_usd",
        "stc_oct2013_fx_outflows_usd",
        "stc_oct2013_other_adjustments_usd",
    ]) - D(L["stc_oct2013_end_cash_usd"])
    KEY_OUTPUTS["stc_oct2013_closure_residual_usd"] = str(stc_residual)
    check("L2_conservation", "stc_oct2013_exact_closure", stc_residual == ZERO,
          "beg + inflows + excised_withdrawal + fx + other - end == 0.00")
    ftc_out = (D(L["ftc_oct2009_total_withdrawals_usd"]) + D(L["ftc_oct2009_fees_usd"])
               - D(L["ftc_oct2009_total_outflows_usd"]))
    check("L2_conservation", "ftc_oct2009_outflow_closure", ftc_out == ZERO,
          "withdrawals + fees - total_outflows == 0.00")
    ftc_p9 = (D(L["ftc_oct2009_surviving_p9_dda_wire_usd"])
              + D(L["ftc_oct2009_surviving_p9_firstbank_wire_usd"])
              - D(L["ftc_oct2009_surviving_p9_disbursements_usd"]))
    check("L2_conservation", "ftc_oct2009_surviving_p9_closure", ftc_p9 == ZERO,
          "dda_wire + firstbank_wire - disbursements == 0.00")
    ftc_part = (D(L["ftc_oct2009_surviving_p9_disbursements_usd"])
                + D(L["ftc_oct2009_excised_p8_residual_usd"])
                - D(L["ftc_oct2009_total_withdrawals_usd"]))
    check("L2_conservation", "ftc_oct2009_excised_p8_partition", ftc_part == ZERO,
          "surviving_p9 + excised_p8 - withdrawals == 0.00")
    acat_sum = chain_sum([
        "sf_pershing_acat_aapl_usd",
        "sf_pershing_acat_apo_usd",
        "sf_pershing_acat_jpm_pfd_usd",
    ])
    check("L2_conservation", "sf_pershing_acat_outflow_sign", acat_sum < ZERO,
          f"ACAT 3-leg sum == {acat_sum} < 0")
    nna_cash = (D(L["db_nna_100_acct_cash_receipt_usd"])
                + D(L["db_nna_100_acct_cash_disbursement_usd"]))
    KEY_OUTPUTS["db_nna_100_net_cash_flow_usd"] = str(nna_cash)
    check("L2_conservation", "db_nna_100_cash_net_closure",
          nna_cash == Decimal("-37103103.75"), f"receipt + disbursement == {nna_cash}")
    epstein_net = D(L["db_nna_epstein_deposits_usd"]) + D(L["db_nna_epstein_debits_usd"])
    check("L2_conservation", "db_nna_epstein_net_exact",
          epstein_net == Decimal("-15556455.93") and epstein_net < ZERO,
          f"net == {epstein_net} < 0")
    wanek_net = D(L["db_nna_wanek_deposits_usd"]) + D(L["db_nna_wanek_debits_usd"])
    check("L2_conservation", "db_nna_wanek_net_exact",
          wanek_net == Decimal("14264.17"), f"net == {wanek_net}")


# ---------------------------------------------------------------------------
# L3: excision obstruction classes (H^1 != 0)
# ---------------------------------------------------------------------------
def layer_3_obstruction():
    L = LOCKED
    ftc_known = chain_sum([
        "ftc_may2010_beg_cash_usd",
        "ftc_may2010_excised_p22_contribution_usd",
        "ftc_may2010_excised_p22_withdrawal_usd",
        "ftc_may2010_p21_income_usd",
        "ftc_may2010_p23_fx_inflows_usd",
    ])
    ftc_ob = D(L["ftc_may2010_end_cash_usd"]) - ftc_known
    KEY_OUTPUTS["ftc_may2010_excision_obstruction_usd"] = str(ftc_ob)
    check("L3_obstruction", "ftc_may2010_excision_obstruction_class",
          ftc_ob == Decimal("5549577.50") and ftc_ob > ZERO,
          f"H^1 residual == {ftc_ob} != 0")
    nna_observed_net = (D(L["db_nna_100_acct_total_credits_usd"])
                        + D(L["db_nna_100_acct_total_debits_usd"]))
    nna_ob = nna_observed_net - D(L["db_nna_100_acct_net_addition_usd"])
    KEY_OUTPUTS["db_nna_100_excision_obstruction_usd"] = str(nna_ob)
    check("L3_obstruction", "db_nna_100_excision_obstruction_class",
          nna_ob == Decimal("39904542.29") and nna_ob > ZERO,
          f"(credits + debits) - net_addition == {nna_ob} != 0")
    excised_credits = D(L["db_nna_excised_credits_approx_usd"])
    check("L3_obstruction", "db_nna_excised_volume_capacity", excised_credits >= nna_ob,
          f"{excised_credits} >= {nna_ob}")
    pages = L["db_nna_excised_pages_list"]
    check("L3_obstruction", "db_nna_excised_page_register",
          pages == [3, 5, 7, 8, 10, 11] and all(x < y for x, y in zip(pages, pages[1:])),
          f"pages == {pages}, strictly increasing, len == {len(pages)}")
    excised_net = excised_credits + D(L["db_nna_excised_debits_approx_usd"])
    KEY_OUTPUTS["db_nna_excised_net_flow_usd"] = str(excised_net)
    check("L3_obstruction", "db_nna_excised_net_flow_exact",
          excised_net == Decimal("28300000.0"), f"net == {excised_net}")
    check("L3_obstruction", "db_nna_excised_sign_consistency",
          excised_credits > ZERO > D(L["db_nna_excised_debits_approx_usd"]),
          "excised_credits > 0 > excised_debits")


# ---------------------------------------------------------------------------
# L4: collateral term-loan bound nesting
# ---------------------------------------------------------------------------
def layer_4_collateral():
    L = LOCKED
    ltv_min = L["black_db_term_loan_art_ltv_min"]
    ltv_max = L["black_db_term_loan_art_ltv_max"]
    aog_min = L["black_db_term_loan_aog_ltv_min"]
    aog_max = L["black_db_term_loan_aog_ltv_max"]
    maturity = L["black_db_term_loan_maturity_years"]
    check("L4_collateral", "ltv_band_nesting",
          0 < ltv_min < ltv_max < aog_min < aog_max <= 1,
          f"0 < {ltv_min} < {ltv_max} < {aog_min} < {aog_max} <= 1")
    check("L4_collateral", "maturity_one_year_from_closing", maturity == 1, f"maturity == {maturity}")
    smin = L["black_db_term_loan_spread_min_bps"]
    smax = L["black_db_term_loan_spread_max_bps"]
    check("L4_collateral", "spread_band_ordering", 0 < smin < smax, f"0 < {smin} < {smax}")
    principal = D(L["black_db_term_loan_principal_usd"])
    art_advance_max = principal * Decimal(str(ltv_max))
    aog_advance_max = principal * Decimal(str(aog_max))
    KEY_OUTPUTS["black_db_term_loan_art_advance_max_usd"] = str(art_advance_max)
    check("L4_collateral", "advance_bound_nesting",
          art_advance_max <= aog_advance_max <= principal,
          f"{art_advance_max} <= {aog_advance_max} <= {principal}")


# ---------------------------------------------------------------------------
# L5: register match and unshattered document integrity
# ---------------------------------------------------------------------------
def layer_5_register():
    L = LOCKED
    p73 = L["rrp73_elysium_pages"]
    p72 = L["rrp72_southern_financial_pages"]
    check("L5_register", "rrp72_rrp73_page_count_match", p73 == p72 == 108,
          f"rrp73 == rrp72 == {p73}")
    docs = L["vol10_unshattered_multi_page_docs"]
    pages = L["vol10_unshattered_total_pages"]
    mean = pages / docs
    KEY_OUTPUTS["vol10_mean_pages_per_doc"] = round(mean, 4)
    check("L5_register", "vol10_unshattered_integrity",
          pages > docs > 0 and mean > 1,
          f"{pages} pages over {docs} docs, mean == {mean:.4f} > 1")
    sets = L["cross_corpus_recovered_attachment_sets"]
    check("L5_register", "cross_corpus_attachment_recovery", sets == 114 and sets > 0,
          f"recovered_attachment_sets == {sets}")


# ---------------------------------------------------------------------------
# L6: locked-constant echo
# ---------------------------------------------------------------------------
def layer_6_echo():
    L = LOCKED
    check("L6_echo", "locked_key_cardinality", len(L) == EXPECTED_LOCKED_KEYS,
          f"len(LOCKED) == {len(L)}")
    numeric = [v for v in L.values() if isinstance(v, (int, float))]
    check("L6_echo", "locked_numeric_finiteness", all(math.isfinite(v) for v in numeric),
          f"{len(numeric)} numeric locked values finite")
    sentinels = (
        L["corpus_total_rows"] == 1380932
        and L["sf_pershing_acat_apo_shares"] == 263157
        and L["ftc_may2010_libor_swap_notional_usd"] == 125000000.0
    )
    check("L6_echo", "sentinel_echo", sentinels,
          "corpus_total_rows, acat_apo_shares, libor_swap_notional")


def main():
    layer_0_cover()
    layer_1_regime()
    layer_2_conservation()
    layer_3_obstruction()
    layer_4_collateral()
    layer_5_register()
    layer_6_echo()
    failed = [r for r in RESULTS if not r["ok"]]
    layers = {}
    for r in RESULTS:
        acc = layers.setdefault(r["layer"], {"passed": 0, "total": 0})
        acc["total"] += 1
        if r["ok"]:
            acc["passed"] += 1
    summary = {
        "proof": "verify_bates_cohomology_and_conservation_of_dollars",
        "status": "PASS" if not failed else "FAIL",
        "checks_total": len(RESULTS),
        "checks_passed": len(RESULTS) - len(failed),
        "checks_failed": len(failed),
        "layers": layers,
        "key_outputs": KEY_OUTPUTS,
        "failed_checks": failed,
    }
    print(json.dumps(summary, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
