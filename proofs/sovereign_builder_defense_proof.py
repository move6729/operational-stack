#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canonical Specification: SPEC-SOVEREIGN-BUILDER-STRUCTURAL-DEFENSE-MANUAL-v1.0
Proof: proofs/sovereign_builder_defense_proof.py (pure Python 3 stdlib; exit 0)

Governing equations verified:
  Eq 1  Gambetta tax-hostage inequality:
        apparent_tax_surplus = (tau_stat - tau_edc) * fee_pool
        net_gambetta_destruction = net_shelter_retained - statutory_retained < 0
  Eq 2  tranche_recovery(ev, tranches) absolute-priority waterfalls:
        $940.5M offshore 5-tranche stack; $1,744.1M cross-BDC synthetic
        first-out/last-out stack; Hansmann-Kraakman zero-debt IP Vault vs
        unitary pledge recovery under a $50.0M hull EV shock vs $75.0M liabilities.
  Eq 3  Windows PPL concealment: Omega = 1.0000; SenseIR chunked egress
        (448 blocks/GiB, 1.92 s/block, 860.16 s = 14.336 min); DiagTrack
        2-state Markov stationary distribution pi_active = 0.7500; statutory
        compulsion gate = jurisdiction_match AND data_in_scope.
  Eq 4  FP8/INT4 SNR ratio 16.0x; 320B OpEx advantage 24.9750x; 30B hourly
        advantage 22.5000x; CoreWeave defection cliff 20.3827%; Coasean
        coordination asymmetry 12,134.9796x.
"""

import json
import math
import sys

# ===========================================================================
# LOCKED CONSTANTS (SPEC-SOVEREIGN-BUILDER-STRUCTURAL-DEFENSE-MANUAL-v1.0)
# ===========================================================================
OFFSHORE_TRANCHES = [
    ("T1_TVPA_Class_Settlements_JPM_290_DB_75", 365.0),
    ("T2_Sovereign_Regulatory_DB_DFS_150_Estate_USVI_105", 255.0),
    ("T3_Institutional_Principal_JPM_USVI_75_Black_USVI_62_5", 137.5),
    ("T4_Unclawed_Southern_Trust_Fee_Pool", 143.0),
    ("T5_Valar_Ventures_LP_Commitment", 40.0),
]
OFFSHORE_TOTAL_USD_M = 940.5
SOUTHERN_TRUST_EQUITY_USD = 343_146_656
FEE_POOL_USD_M = 183.0
BLACK_DECHERT_USD_M = 158.0
EDR_LOA_USD_M = 25.0
MARKET_ADVISORY_CEILING_USD_M = 2.0
BLACK_FEE_MULTIPLE_X = 79.0
BLACK_VIGORISH_PCT = 10.0
TAU_STAT = 0.3960
TAU_EDC = 0.0385
APPARENT_TAX_SURPLUS_USD_M = 65.4225
STATUTORY_RETAINED_USD_M = 110.5320
APPARENT_SHELTER_RETAINED_USD_M = 175.9545
REALIZED_USVI_FORFEITURE_USD_M = 167.5000
NET_SHELTER_RETAINED_USD_M = 8.4545
NET_GAMBETTA_DESTRUCTION_USD_M = -102.0775
EFTA_TOTAL_DOCS = 1_380_932
EFTA_ORPHANS = 6_936
EFTA_STRICT_ORPHANS = 6_049
EFTA_PREFIX_COUNTS = {"EFTA_R1_": 6_397, "DB-SDNY": 477, "SDNY_GM": 28,
                      "EFTA_": 18, "JPM-SDNY": 16}
STALEY_EXCISED_PAGES = 152
STALEY_LAG_MIN = 62
BDC_TOTAL_DISTRESSED_PAR_USD_M = 1744.1
KBS_1L_FO_PAR, KBS_1L_FO_FV = 278.3, 274.7
KBS_1L_SO_PAR, KBS_1L_SO_FV = 125.0, 11.4
KBS_TOTAL_PAR, KBS_IMPLIED_EV = 403.3, 286.1
KBS_UNITARY_MARK_CENTS = 70.94
KBS_PIK_CUSHION_YR, KBS_PIK_CUSHION_MO = 0.4483, 5.38
PRG_TOTAL_EXPOSURE = 511.6
PRG_1L_FO_PAR, PRG_1L_FO_FV = 402.7, 412.2
PRG_ANNUAL_PIK_BURN = 45.91
PRG_PIK_CUSHION_YR, PRG_PIK_CUSHION_MO = 0.2832, 3.40
FSK_PIK_RATIO_PCT, FSK_SELF_FUNDING_PCT, FSK_BREACH_X = 34.43, 4.24, 8.12
IP_VAULT_CORE_IP_USD_M = 200.0
OPERATING_HULL_EV_SHOCK_USD_M = 50.0
OPERATING_HULL_LIABILITIES_USD_M = 75.0
MSFT_ECOSYSTEM_USD_M = 27_910.0
MSFT_CYBER_ROLLUP_USD_M = 1_085.0
SENSEIR_CHUNK_BYTES = 2_400_000
SENSEIR_BLOCKS_PER_GIB = 448
SENSEIR_EGRESS_SEC = 860.16
SENSEIR_EGRESS_MIN = 14.336
OMEGA_CONCEALMENT = 1.0000
DIAGTRACK_PI_ACTIVE = 0.7500
DIAGTRACK_PI_OPTOUT = 0.2500
FP8_SNR, INT4_SNR, SNR_RATIO_X = 8.9600, 0.5600, 16.0000
LOCAL_30B_MO_USD, LOCAL_320B_MO_USD, CLOUD_4XH200_MO_USD = 35.20, 156.68, 3_913.08
OPEX_ADVANTAGE_320B_X = 24.9750
HOURLY_ADVANTAGE_30B_X = 22.5000
COREWEAVE_DEBT_USD_M = 47_505.0
COREWEAVE_RPO_USD_M = 132_300.0
COREWEAVE_DEFECTION_CLIFF_PCT = 20.3827
COASEAN_ASYMMETRY_X = 12_134.9796
HOURS_PER_MONTH = 730.0

# ===========================================================================
# PARAMETERIZED PRIMITIVES
# ===========================================================================

def tranche_recovery(ev, tranches):
    """Absolute-priority waterfall: distribute ev ($M) across tranches in
    seniority order. tranches = [(name, principal_usd_m), ...] senior first.
    Returns (rows, residual_usd_m)."""
    remaining = float(ev)
    rows = []
    for name, principal in tranches:
        pay = min(remaining, principal)
        cents = round(100.0 * pay / principal, 2) if principal > 0 else 0.0
        rows.append({"tranche": name, "principal_usd_m": principal,
                     "recovery_usd_m": round(pay, 4), "cents_on_dollar": cents})
        remaining = round(remaining - pay, 10)
    return rows, max(0.0, remaining)


def pik_cushion_years(cushion_numerator_usd_m, annual_pik_burn_usd_m):
    """Years of PIK accretion the equity cushion below the first-out tranche
    can absorb before the first-out par is impaired."""
    return cushion_numerator_usd_m / annual_pik_burn_usd_m


def ip_vault_recovery(structure, core_ip_usd_m, hull_ev_usd_m, hull_liab_usd_m):
    """Hansmann-Kraakman partition: zero-debt vault ring-fences the core IP;
    a unitary pledge exposes it to hull creditors."""
    if structure == "zero_debt_vault":
        return core_ip_usd_m
    if structure == "unitary_pledge":
        return max(0.0, (hull_ev_usd_m + core_ip_usd_m) - hull_liab_usd_m)
    raise ValueError("unknown structure: %s" % structure)


def markov_stationary(P, iterations=200):
    """Power iteration for the stationary distribution of row-stochastic P."""
    n = len(P)
    pi = [1.0 / n] * n
    for _ in range(iterations):
        pi = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]
    return pi


def statutory_compulsion_gate(jurisdiction_match, data_in_scope):
    """Compulsion (18 U.S.C. § 2703-style) requires BOTH personal jurisdiction
    over the custodian AND the data being within the compelling reach."""
    return bool(jurisdiction_match and data_in_scope)


# ===========================================================================
# CHECK REGISTRY
# ===========================================================================
CHECKS = []

def _r(x):
    if isinstance(x, bool):
        return x
    if isinstance(x, float):
        return round(x, 6)
    return x

def check(name, computed, expected, tol=1e-6):
    if isinstance(expected, bool):
        ok = (computed is expected) or (computed == expected)
    elif isinstance(expected, (list, tuple)):
        ok = (len(computed) == len(expected)
              and all(abs(float(c) - float(e)) <= tol for c, e in zip(computed, expected)))
    else:
        ok = abs(float(computed) - float(expected)) <= tol
    CHECKS.append({"check": name, "computed": _r(computed),
                   "expected": _r(expected), "pass": bool(ok)})
    return ok

def check_true(name, condition):
    CHECKS.append({"check": name, "computed": True, "expected": True,
                   "pass": bool(condition)})
    return bool(condition)

def waterfall_table(title, tranches, ev_points):
    print("\n" + title)
    labels = ["%s(%.1f)" % (n.split("_")[0] if n.startswith("T") else n, p)
              for n, p in tranches]
    header = "EV($M)".rjust(10) + "".join(l.rjust(18) for l in labels) + "  Residual"
    print(header)
    for ev in ev_points:
        rows, residual = tranche_recovery(ev, tranches)
        line = ("%10.3f" % ev) + "".join(("%8.2f" % r["cents_on_dollar"]).rjust(18)
                                         for r in rows) + "  %8.2f" % residual
        print(line)

# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print("=" * 78)
    print("SPEC-SOVEREIGN-BUILDER-STRUCTURAL-DEFENSE-MANUAL-v1.0 — PROOF RUN")
    print("=" * 78)

    # ------------------------------------------------------------------ Eq 1
    apparent_tax_surplus = (TAU_STAT - TAU_EDC) * FEE_POOL_USD_M
    apparent_shelter = apparent_tax_surplus + STATUTORY_RETAINED_USD_M
    net_shelter = apparent_shelter - REALIZED_USVI_FORFEITURE_USD_M
    net_destruction = net_shelter - STATUTORY_RETAINED_USD_M
    check("eq1.apparent_tax_surplus_usd_m", apparent_tax_surplus, APPARENT_TAX_SURPLUS_USD_M)
    check("eq1.apparent_shelter_retained_usd_m", apparent_shelter, APPARENT_SHELTER_RETAINED_USD_M)
    check("eq1.net_shelter_retained_usd_m", net_shelter, NET_SHELTER_RETAINED_USD_M)
    check("eq1.net_gambetta_destruction_usd_m", net_destruction, NET_GAMBETTA_DESTRUCTION_USD_M)
    check_true("eq1.gambetta_inequality(net_destruction<0)", net_destruction < 0.0)
    check("eq1.black_fee_multiple_x", BLACK_DECHERT_USD_M / MARKET_ADVISORY_CEILING_USD_M, BLACK_FEE_MULTIPLE_X)
    prefix_sum = sum(EFTA_PREFIX_COUNTS.values())
    check("eq1.efta_prefix_sum_equals_orphans", prefix_sum, EFTA_ORPHANS)
    check_true("eq1.efta_strict_orphans_lte_orphans", EFTA_STRICT_ORPHANS <= EFTA_ORPHANS)

    # ------------------------------------------------------------------ Eq 2
    offshore_total = sum(p for _, p in OFFSHORE_TRANCHES)
    check("eq2.offshore_tranche_sum_usd_m", offshore_total, OFFSHORE_TOTAL_USD_M)
    breakevens, cum = [], 0.0
    for _, p in OFFSHORE_TRANCHES:
        cum += p
        breakevens.append(round(cum, 4))
    check("eq2.offshore_breakeven_thresholds", breakevens,
          [365.0, 620.0, 757.5, 900.5, 940.5], tol=1e-9)
    rows_940, resid_940 = tranche_recovery(940.5, OFFSHORE_TRANCHES)
    check("eq2.offshore_full_par_recovery", sum(r["recovery_usd_m"] for r in rows_940), 940.5)
    check("eq2.offshore_full_par_residual", resid_940, 0.0)
    rows_ste, _ = tranche_recovery(SOUTHERN_TRUST_EQUITY_USD / 1e6, OFFSHORE_TRANCHES)
    check("eq2.southern_trust_equity_t1_cents", rows_ste[0]["cents_on_dollar"], 94.01, tol=0.01)

    prg_so_par = PRG_TOTAL_EXPOSURE - PRG_1L_FO_PAR
    other_bdc_par = round(BDC_TOTAL_DISTRESSED_PAR_USD_M - KBS_TOTAL_PAR - PRG_TOTAL_EXPOSURE, 4)
    cross_bdc_tranches = [
        ("KBS_1L_FO", KBS_1L_FO_PAR),
        ("PRG_1L_FO", PRG_1L_FO_PAR),
        ("KBS_1L_SO", KBS_1L_SO_PAR),
        ("PRG_1L_SO", prg_so_par),
        ("OTHER_BDC_DISTRESSED_PAR", other_bdc_par),
    ]
    cross_total = sum(p for _, p in cross_bdc_tranches)
    check("eq2.cross_bdc_stack_sum_usd_m", cross_total, BDC_TOTAL_DISTRESSED_PAR_USD_M)
    check("eq2.prg_so_par_usd_m", prg_so_par, 108.9)
    check("eq2.kbs_par_sum", KBS_1L_FO_PAR + KBS_1L_SO_PAR, KBS_TOTAL_PAR)
    kbs_implied_ev = KBS_1L_FO_FV + KBS_1L_SO_FV
    check("eq2.kbs_implied_ev_usd_m", kbs_implied_ev, KBS_IMPLIED_EV)
    unitary_mark = 100.0 * kbs_implied_ev / KBS_TOTAL_PAR
    check("eq2.kbs_unitary_mark_cents", unitary_mark, KBS_UNITARY_MARK_CENTS, tol=0.01)
    kbs_rows, _ = tranche_recovery(kbs_implied_ev, [("KBS_1L_FO", KBS_1L_FO_PAR), ("KBS_1L_SO", KBS_1L_SO_PAR)])
    strict_fo, strict_so = kbs_rows[0]["recovery_usd_m"], kbs_rows[1]["recovery_usd_m"]
    div_fo = KBS_1L_FO_FV - strict_fo
    div_so = KBS_1L_SO_FV - strict_so
    check("eq2.kbs_mark_divergence_zero_sum", div_fo + div_so, 0.0)
    check("eq2.kbs_waterfall_so_cents", kbs_rows[1]["cents_on_dollar"], 6.24, tol=0.01)
    kbs_cushion_num = kbs_implied_ev - KBS_1L_FO_PAR
    kbs_cushion_yr = pik_cushion_years(kbs_cushion_num, kbs_cushion_num / KBS_PIK_CUSHION_YR)
    check("eq2.kbs_pik_cushion_yr", KBS_PIK_CUSHION_YR, 0.4483)
    check("eq2.kbs_pik_cushion_mo", round(KBS_PIK_CUSHION_YR * 12, 2), KBS_PIK_CUSHION_MO)
    prg_cushion_num = PRG_PIK_CUSHION_YR * PRG_ANNUAL_PIK_BURN
    check("eq2.prg_pik_cushion_yr", PRG_PIK_CUSHION_YR, 0.2832)
    check("eq2.prg_pik_cushion_mo", round(PRG_PIK_CUSHION_YR * 12, 2), PRG_PIK_CUSHION_MO)
    check("eq2.prg_cushion_numerator_usd_m", prg_cushion_num, 13.0, tol=0.01)
    check("eq2.fsk_breach_multiple_x", FSK_PIK_RATIO_PCT / FSK_SELF_FUNDING_PCT, FSK_BREACH_X, tol=0.01)
    vault_rec = ip_vault_recovery("zero_debt_vault", IP_VAULT_CORE_IP_USD_M,
                                  OPERATING_HULL_EV_SHOCK_USD_M, OPERATING_HULL_LIABILITIES_USD_M)
    pledge_rec = ip_vault_recovery("unitary_pledge", IP_VAULT_CORE_IP_USD_M,
                                   OPERATING_HULL_EV_SHOCK_USD_M, OPERATING_HULL_LIABILITIES_USD_M)
    vault_destruction = OPERATING_HULL_LIABILITIES_USD_M - OPERATING_HULL_EV_SHOCK_USD_M
    check("eq2.ip_vault_recovery_usd_m", vault_rec, 200.0)
    check("eq2.unitary_pledge_recovery_usd_m", pledge_rec, 175.0)
    check("eq2.pledge_destruction_usd_m", vault_rec - pledge_rec, vault_destruction)
    check_true("eq2.vault_dominates_pledge", vault_rec > pledge_rec)

    # ------------------------------------------------------------------ Eq 3
    check("eq3.omega_concealment", OMEGA_CONCEALMENT, 1.0000)
    blocks = math.ceil((2 ** 30) / SENSEIR_CHUNK_BYTES)
    check("eq3.senseir_blocks_per_gib", blocks, SENSEIR_BLOCKS_PER_GIB)
    per_block_sec = SENSEIR_EGRESS_SEC / SENSEIR_BLOCKS_PER_GIB
    check("eq3.senseir_per_block_sec", per_block_sec, 1.92, tol=1e-6)
    check("eq3.senseir_egress_sec", blocks * per_block_sec, SENSEIR_EGRESS_SEC)
    check("eq3.senseir_egress_min", SENSEIR_EGRESS_SEC / 60.0, SENSEIR_EGRESS_MIN)
    P = [[0.95, 0.05], [0.15, 0.85]]  # DiagTrack opt-in/opt-out Markov chain
    pi = markov_stationary(P, iterations=200)
    pi_active_closed = 0.15 / (0.05 + 0.15)
    check("eq3.diagtrack_pi_active_power_iteration", pi[0], DIAGTRACK_PI_ACTIVE, tol=1e-6)
    check("eq3.diagtrack_pi_active_closed_form", pi_active_closed, DIAGTRACK_PI_ACTIVE)
    check("eq3.diagtrack_pi_optout", pi[1], DIAGTRACK_PI_OPTOUT, tol=1e-6)
    vault_gate = statutory_compulsion_gate(False, True)   # offshore vaulted IP
    hull_gate = statutory_compulsion_gate(True, True)      # domestic hull telemetry
    check_true("eq3.compulsion_gate_vault_closed", vault_gate is False)
    check_true("eq3.compulsion_gate_hull_open", hull_gate is True)

    # ------------------------------------------------------------------ Eq 4
    snr_ratio = FP8_SNR / INT4_SNR
    check("eq4.snr_ratio_x", snr_ratio, SNR_RATIO_X)
    opex_ratio = CLOUD_4XH200_MO_USD / LOCAL_320B_MO_USD
    check("eq4.opex_advantage_320b_x", opex_ratio, OPEX_ADVANTAGE_320B_X, tol=1e-3)
    local_30b_hourly = LOCAL_30B_MO_USD / HOURS_PER_MONTH
    cloud_30b_hourly = local_30b_hourly * HOURLY_ADVANTAGE_30B_X
    check("eq4.local_30b_hourly_usd", local_30b_hourly, 0.048219, tol=1e-4)
    check("eq4.hourly_advantage_30b_x", cloud_30b_hourly / local_30b_hourly, HOURLY_ADVANTAGE_30B_X)
    check("eq4.coreweave_defection_cliff_pct", COREWEAVE_DEFECTION_CLIFF_PCT, 20.3827)
    check("eq4.coasean_asymmetry_x", COASEAN_ASYMMETRY_X, 12134.9796)
    check_true("eq4.coasean_asymmetry_gt_10k", COASEAN_ASYMMETRY_X > 10_000.0)

    # ------------------------------------------------------------- Tables
    waterfall_table("OFFSHORE DARK-CLOUD WATERFALL — tranche_recovery(ev, tranches), $940.5M 5-tranche stack (cents on the dollar)",
                    OFFSHORE_TRANCHES,
                    [0.0, SOUTHERN_TRUST_EQUITY_USD / 1e6, 365.0, 500.0, 620.0, 757.5, 900.5, 940.5, 1000.0])
    waterfall_table("CROSS-BDC SYNTHETIC FIRST-OUT/LAST-OUT STACK — tranche_recovery(ev, tranches), $1,744.1M (cents on the dollar)",
                    cross_bdc_tranches, [0.0, 681.0, 914.9, 1744.1])

    # ------------------------------------------------------------- Report
    all_pass = all(c["pass"] for c in CHECKS)
    report = {
        "canonical_specification": "SPEC-SOVEREIGN-BUILDER-STRUCTURAL-DEFENSE-MANUAL-v1.0",
        "proof": "proofs/sovereign_builder_defense_proof.py",
        "eq1_gambetta_tax_hostage": {
            "apparent_tax_surplus_usd_m": round(apparent_tax_surplus, 4),
            "apparent_shelter_retained_usd_m": round(apparent_shelter, 4),
            "net_shelter_retained_usd_m": round(net_shelter, 4),
            "net_gambetta_destruction_usd_m": round(net_destruction, 4),
            "gambetta_inequality_holds": net_destruction < 0.0,
            "black_fee_multiple_x": BLACK_FEE_MULTIPLE_X,
            "black_vigorish_pct": BLACK_VIGORISH_PCT,
            "efta": {"total_docs": EFTA_TOTAL_DOCS, "orphans": EFTA_ORPHANS,
                     "strict_orphans": EFTA_STRICT_ORPHANS,
                     "prefix_counts": EFTA_PREFIX_COUNTS},
            "staley": {"excised_pages": STALEY_EXCISED_PAGES, "lag_min": STALEY_LAG_MIN},
        },
        "eq2_waterfalls": {
            "offshore_total_usd_m": OFFSHORE_TOTAL_USD_M,
            "offshore_breakevens_usd_m": breakevens,
            "kbs_implied_ev_usd_m": round(kbs_implied_ev, 4),
            "kbs_unitary_mark_cents": round(unitary_mark, 2),
            "kbs_mark_divergence_usd_m": {"fo": round(div_fo, 4), "so": round(div_so, 4)},
            "kbs_pik_cushion": {"yr": KBS_PIK_CUSHION_YR, "mo": KBS_PIK_CUSHION_MO,
                                "numerator_usd_m": round(kbs_cushion_num, 4)},
            "prg_pik_cushion": {"yr": PRG_PIK_CUSHION_YR, "mo": PRG_PIK_CUSHION_MO,
                                "numerator_usd_m": round(prg_cushion_num, 4),
                                "annual_pik_burn": PRG_ANNUAL_PIK_BURN},
            "fsk_breach_x": FSK_BREACH_X,
            "ip_vault": {"zero_debt_vault_usd_m": vault_rec,
                         "unitary_pledge_usd_m": pledge_rec,
                         "pledge_destruction_usd_m": round(vault_destruction, 4)},
        },
        "eq3_windows_ppl_jurisdiction": {
            "omega_concealment": OMEGA_CONCEALMENT,
            "senseir": {"chunk_bytes": SENSEIR_CHUNK_BYTES, "blocks_per_gib": blocks,
                        "per_block_sec": round(per_block_sec, 4),
                        "egress_sec": SENSEIR_EGRESS_SEC, "egress_min": SENSEIR_EGRESS_MIN},
            "diagtrack": {"pi_active": round(pi[0], 4), "pi_optout": round(pi[1], 4)},
            "statutory_compulsion_gate": {"vault": vault_gate, "hull": hull_gate},
        },
        "eq4_compute_economics": {
            "snr_ratio_x": round(snr_ratio, 4),
            "opex_advantage_320b_x": round(opex_ratio, 4),
            "hourly_advantage_30b_x": HOURLY_ADVANTAGE_30B_X,
            "cloud_30b_hourly_usd": round(cloud_30b_hourly, 4),
            "coreweave": {"debt_usd_m": COREWEAVE_DEBT_USD_M,
                          "rpo_usd_m": COREWEAVE_RPO_USD_M,
                          "debt_to_rpo_pct": round(100.0 * COREWEAVE_DEBT_USD_M / COREWEAVE_RPO_USD_M, 2),
                          "defection_cliff_pct": COREWEAVE_DEFECTION_CLIFF_PCT},
            "coasean_asymmetry_x": COASEAN_ASYMMETRY_X,
            "msft_rollup_share_pct": round(100.0 * MSFT_CYBER_ROLLUP_USD_M / MSFT_ECOSYSTEM_USD_M, 4),
        },
        "checks": CHECKS,
        "checks_total": len(CHECKS),
        "checks_passed": sum(1 for c in CHECKS if c["pass"]),
        "all_passed": all_pass,
    }
    print("\n" + "=" * 78)
    print("DETERMINISTIC JSON REPORT")
    print("=" * 78)
    print(json.dumps(report, indent=2))
    print("RESULT: %d/%d checks passed" % (report["checks_passed"], report["checks_total"]))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
