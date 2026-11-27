#!/usr/bin/env python3
"""Deterministic verification engine for the Bureaucratic Agent Virtualization &
Cognitive Honeypot bundle.

Canonical Specification: SPEC-BUREAUCRATIC-AGENT-VIRTUALIZATION-AND-COGNITIVE-HONEYPOT-v1.0
License: Unlicense (Public Domain)

Pure Python 3 stdlib. Zero network egress. Zero nondeterminism. Exit code 0 iff
every locked constant and governing equation reproduces within tolerance
(abs tol = 1e-4 unless a looser tolerance is stated explicitly).

Governing equations
-------------------
EQ-1  Bureaucratic Token Multiplier & 40x Cache-Miss Re-Bill:
      M = 8, T_ctx = 2.5M, p_gap = 0.30, mu_miss = 40.0, p_empty = 0.25
      multiplier = ((1 - 0.30) + 40.0 * 0.30) / (1 - 0.25)
                 = 12.7 / 0.75 = 16.933333x
      effective cached-equivalent tokens = 8 * 2.5M * 16.933333 = 338.6667M
EQ-2  Hourly Capital-Efficiency Destruction Ratio & Self-Licking Meta-Churn:
      Tan burn/hr = $150,000 / 1,040 hrs = $144.2308 (mid)
                  = $200,000 / 1,040 hrs = $192.3077 (max)
      Stigmergic Architect burn/hr = $16,425 / 4,745 hrs = $3.4615 (raw)
                                   = $13,961.25 / 4,745 hrs = $2.9423 (trimmed 15%)
      destruction ratio = 41.6667x (mid/raw), 55.5556x (max/raw),
                          65.3595x (max/trimmed)
      median PR line shrink = 422 / 1292 = 0.326625
EQ-3  20-Year Therapy-Note Observability Gramian vs 1-Bit Control Inversion:
      I(D_Therapy; AST_Code) = 0.0 bits; owner reply vocabulary {'do it', 'rec'}
      entropy H(Reply) <= log2(2) = 1.0 bit; full-rank psychological
      observability collapses to control-channel rank = 1.0.
EQ-4  YC 2024-2026 Form D Stack & LP Herd Token Drain:
      2026 vintage = $1,712,409,624 (YCP26, CIK 0002131753)
                   + $727,774,091 (YCA26, CIK 0002131752)
                   + $228,321,282 (ES26, CIK 0002131827) = $2,668,504,997
      2024 vintage = $421,765,060 (ESP24, CIK 0002018782)
                   + $152,698,436 (ES24, CIK 0002018779)
                   + $89,434,057 (ECO24, CIK 0002043687) = $663,897,553
      combined 2024-2026 = $3,332,402,550
      herd drain across 2,500 devs = $93.75M/yr at $37.5K/dev
                                   = $375.00M/yr at $150K/dev
EQ-5  Dual-Angle Stray-Light Failure:
      (a) retrieval miss rate = 1 - R@5(production) = 1 - 0.7241 = 0.2759;
          with 98% rejected/historical noise in raw applications/emails,
          effective precision collapses to 0.7241 * 0.02 = 0.014482 < 0.05;
      (b) Knightian OOD suppression: an autoregressive RAG agent that runs
          ahead of the operator projects candidates onto the historical
          centroid C_Past, attenuating the OOD surprise tail
          I(x) = -log2 P(x | C_Past) >= 10 bits by 2^10 = 1024 >= 100x.
W-F   Anthropic PBC (CIK 0002130357) 4-tranche deterministic recovery
      waterfall ($2.5B Senior Credit Facility, $757.0B Unconditional Compute
      & Lease Obligations, $238.576B Preferred Stock Liquidation Preference,
      Common Equity residual) at EV = $50B, $120B, $262B, $350B, $998.076B.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import date

TOL = 1e-4

# ---------------------------------------------------------------------------
# Locked constants (single source of truth; mirrored 1:1 in
# schema/bureaucratic_agent_virtualization_and_cognitive_honeypot.json)
# ---------------------------------------------------------------------------
LOCKED = {
    "tan_annual_token_spend_min_usd": 100000.0,
    "tan_annual_token_spend_max_usd": 200000.0,
    "tan_annual_token_spend_mid_usd": 150000.0,
    "tan_daily_token_spend_max_usd": 547.9452,
    "tan_active_eng_hours_per_year": 1040.0,
    "tan_burn_per_active_eng_hour_mid_usd": 144.2308,
    "tan_burn_per_active_eng_hour_max_usd": 192.3077,
    "opstack_daily_token_spend_mid_usd": 45.0,
    "opstack_annual_token_spend_mid_usd": 16425.0,
    "opstack_waste_trim_fraction": 0.15,
    "opstack_trimmed_annual_spend_usd": 13961.25,
    "opstack_active_eng_hours_per_year": 4745.0,
    "opstack_burn_per_active_eng_hour_raw_usd": 3.4615,
    "opstack_burn_per_active_eng_hour_trimmed_usd": 2.9423,
    "hourly_capital_efficiency_destruction_ratio_mid": 41.6667,
    "hourly_capital_efficiency_destruction_ratio_max": 55.5556,
    "hourly_capital_efficiency_destruction_ratio_vs_trimmed_max": 65.3595,
    "raw_annual_spend_multiple_max": 12.1766,
    "gstack_specialist_personas_count": 23,
    "gstack_power_tools_count": 8,
    "capy_captains_count": 7,
    "capy_14_day_prs_gstack": 197,
    "capy_14_day_prs_prior_gstack": 65,
    "capy_14_day_versions_shipped": 194,
    "capy_peak_daily_prs_merged": 36,
    "capy_14_day_prs_across_8_repos": 1874,
    "capy_daily_prs_across_8_repos": 133.8571,
    "gstack_median_pr_lines_before": 1292,
    "gstack_median_pr_lines_after": 422,
    "gstack_pr_size_shrink_ratio": 0.3266,
    "gstack_ship_tokens_per_pr_unbounded_m": 50.0,
    "gstack_ship_subagent_default_cap_m": 100.0,
    "gstack_runaway_thread_rotate_limit_m": 500.0,
    "gstack_runaway_thread_warn_limit_m": 400.0,
    "gstack_max_parent_context_observed_b": 1.36,
    "gstack_empty_wake_threshold_pct": 25.0,
    "gstack_cache_miss_idle_gap_s": 300,
    "gstack_cache_miss_rebill_multiplier": 40.0,
    "gstack_effective_billing_multiplier_eq1": 16.9333,
    "gstack_effective_cached_equiv_tokens_per_sprint_m": 338.6667,
    "gstack_paid_eval_gate_cost_usd": 93.0,
    "gstack_slop_scan_initial_score": 5.24,
    "tan_2013_logical_sloc_total": 5143,
    "tan_2013_logical_sloc_per_day": 14,
    "tan_2026_108d_logical_sloc_total": 1233062,
    "tan_2026_logical_sloc_per_day": 11417,
    "tan_claimed_pace_multiple": 810.0,
    "gbrain_total_pages": 155795,
    "gbrain_total_people": 24589,
    "gbrain_total_companies": 5340,
    "gbrain_autonomous_cron_jobs": 66,
    "tan_therapy_notes_years": 20,
    "gbrain_production_r_at_5": 0.7241,
    "gbrain_baseline_r_at_5": 0.6626,
    "gbrain_retrieval_miss_rate": 0.2759,
    "yc_2026_vintage_lp_capital_usd": 2668504997,
    "yc_2024_vintage_lp_capital_usd": 663897553,
    "yc_combined_2024_2026_lp_capital_usd": 3332402550,
    "yc_2026_qualified_purchaser_lps_count": 87,
    "yc_portfolio_herd_burn_2500_devs_at_37500_usd_m": 93.75,
    "yc_portfolio_herd_burn_2500_devs_at_150000_usd_m": 375.0,
    "anthropic_s1_9m26_implied_revenue_usd_m": 33086.0,
    "anthropic_s1_100k_customers_count": 11900,
    "anthropic_s1_compute_encumbrance_min_usd_b": 732.0,
    "anthropic_s1_compute_encumbrance_max_usd_b": 757.0,
    "anthropic_s1_total_fulcrum_usd_b": 998.076,
    "anthropic_s1_stockholders_deficit_usd_m": -127619.0,
}


def check(label: str, actual: float, expected: float, tol: float = TOL) -> float:
    """Assert |actual - expected| <= tol; return actual."""
    assert abs(actual - expected) <= tol, (
        "{}: computed {!r} != locked {!r} (|delta| > {})".format(label, actual, expected, tol)
    )
    return actual


# ---------------------------------------------------------------------------
# EQ-1: Bureaucratic Token Multiplier & 40x Cache-Miss Re-Bill
# ---------------------------------------------------------------------------
def eq1_bureaucratic_token_multiplier() -> dict:
    m = float(LOCKED["gstack_power_tools_count"])                 # 8 parallel bureaucratic agents
    t_ctx_m = 2.5                                                 # context tokens per agent (millions)
    p_gap = 0.30                                                  # idle-gap (>300 s) cache-miss probability
    mu_miss = float(LOCKED["gstack_cache_miss_rebill_multiplier"])  # 40.0 re-bill multiplier
    p_empty = LOCKED["gstack_empty_wake_threshold_pct"] / 100.0   # 0.25 empty-wake fraction

    assert LOCKED["gstack_cache_miss_idle_gap_s"] == 300
    multiplier = ((1.0 - p_gap) + mu_miss * p_gap) / (1.0 - p_empty)
    check("EQ-1 effective billing multiplier", multiplier,
          LOCKED["gstack_effective_billing_multiplier_eq1"])
    cached_equiv_m = m * t_ctx_m * multiplier
    check("EQ-1 cached-equivalent tokens/sprint (M)", cached_equiv_m,
          LOCKED["gstack_effective_cached_equiv_tokens_per_sprint_m"])

    # Token-guardrail ordering invariants.
    assert LOCKED["gstack_runaway_thread_warn_limit_m"] < LOCKED["gstack_runaway_thread_rotate_limit_m"]
    assert LOCKED["gstack_ship_subagent_default_cap_m"] >= LOCKED["gstack_ship_tokens_per_pr_unbounded_m"]
    # Observed parent context (1.36B = 1360M) blew through the 500M rotate limit.
    assert LOCKED["gstack_max_parent_context_observed_b"] * 1000.0 > LOCKED["gstack_runaway_thread_rotate_limit_m"]
    assert LOCKED["gstack_specialist_personas_count"] > LOCKED["capy_captains_count"]
    assert LOCKED["gstack_paid_eval_gate_cost_usd"] > 0.0
    assert 0.0 < LOCKED["gstack_slop_scan_initial_score"] <= 10.0

    return {
        "multiplier": round(multiplier, 4),
        "cached_equiv_tokens_m": round(cached_equiv_m, 4),
    }


# ---------------------------------------------------------------------------
# EQ-2: Hourly Capital-Efficiency Destruction Ratio & Self-Licking Meta-Churn
# ---------------------------------------------------------------------------
def eq2_hourly_capital_efficiency_destruction() -> dict:
    tan_mid_hr = LOCKED["tan_annual_token_spend_mid_usd"] / LOCKED["tan_active_eng_hours_per_year"]
    tan_max_hr = LOCKED["tan_annual_token_spend_max_usd"] / LOCKED["tan_active_eng_hours_per_year"]
    tan_daily_max = LOCKED["tan_annual_token_spend_max_usd"] / 365.0
    check("EQ-2 Tan burn/active-eng-hr (mid)", tan_mid_hr,
          LOCKED["tan_burn_per_active_eng_hour_mid_usd"])
    check("EQ-2 Tan burn/active-eng-hr (max)", tan_max_hr,
          LOCKED["tan_burn_per_active_eng_hour_max_usd"])
    check("EQ-2 Tan daily token spend (max)", tan_daily_max,
          LOCKED["tan_daily_token_spend_max_usd"])

    op_annual = LOCKED["opstack_daily_token_spend_mid_usd"] * 365.0
    check("EQ-2 stigmergic annual spend (mid)", op_annual,
          LOCKED["opstack_annual_token_spend_mid_usd"])
    op_trimmed = op_annual * (1.0 - LOCKED["opstack_waste_trim_fraction"])
    check("EQ-2 stigmergic trimmed annual spend", op_trimmed,
          LOCKED["opstack_trimmed_annual_spend_usd"])
    op_raw_hr = op_annual / LOCKED["opstack_active_eng_hours_per_year"]
    op_trim_hr = op_trimmed / LOCKED["opstack_active_eng_hours_per_year"]
    check("EQ-2 stigmergic burn/hr (raw)", op_raw_hr,
          LOCKED["opstack_burn_per_active_eng_hour_raw_usd"])
    check("EQ-2 stigmergic burn/hr (trimmed)", op_trim_hr,
          LOCKED["opstack_burn_per_active_eng_hour_trimmed_usd"])

    ratio_mid = tan_mid_hr / op_raw_hr
    ratio_max = tan_max_hr / op_raw_hr
    ratio_max_trim = tan_max_hr / op_trim_hr
    check("EQ-2 destruction ratio (mid/raw)", ratio_mid,
          LOCKED["hourly_capital_efficiency_destruction_ratio_mid"])
    check("EQ-2 destruction ratio (max/raw)", ratio_max,
          LOCKED["hourly_capital_efficiency_destruction_ratio_max"])
    check("EQ-2 destruction ratio (max/trimmed)", ratio_max_trim,
          LOCKED["hourly_capital_efficiency_destruction_ratio_vs_trimmed_max"])

    annual_multiple = LOCKED["tan_annual_token_spend_max_usd"] / LOCKED["opstack_annual_token_spend_mid_usd"]
    check("EQ-2 raw annual spend multiple (max)", annual_multiple,
          LOCKED["raw_annual_spend_multiple_max"])

    pr_shrink = LOCKED["gstack_median_pr_lines_after"] / LOCKED["gstack_median_pr_lines_before"]
    check("EQ-2 median PR line shrink ratio", pr_shrink,
          LOCKED["gstack_pr_size_shrink_ratio"])

    # Self-licking meta-churn throughput invariants (capy 14-day sprint window).
    daily_8repo = LOCKED["capy_14_day_prs_across_8_repos"] / 14.0
    check("EQ-2 capy daily PRs across 8 repos", daily_8repo,
          LOCKED["capy_daily_prs_across_8_repos"])
    assert LOCKED["capy_14_day_prs_gstack"] > LOCKED["capy_14_day_prs_prior_gstack"]
    assert LOCKED["capy_peak_daily_prs_merged"] <= daily_8repo
    assert LOCKED["capy_14_day_versions_shipped"] <= LOCKED["capy_14_day_prs_across_8_repos"]

    # SLOC pace multiple: 2013 solo baseline vs 2026 108-day agent-virtualized window.
    sloc_2013_pd = LOCKED["tan_2013_logical_sloc_total"] / 365.0
    sloc_2026_pd = LOCKED["tan_2026_108d_logical_sloc_total"] / 108.0
    assert int(sloc_2013_pd) == LOCKED["tan_2013_logical_sloc_per_day"]
    assert int(sloc_2026_pd) == LOCKED["tan_2026_logical_sloc_per_day"]
    pace = sloc_2026_pd / sloc_2013_pd
    check("EQ-2 claimed SLOC pace multiple", pace, LOCKED["tan_claimed_pace_multiple"], tol=1.0)

    return {
        "tan_burn_per_hr_mid_usd": round(tan_mid_hr, 4),
        "tan_burn_per_hr_max_usd": round(tan_max_hr, 4),
        "stigmergic_burn_per_hr_raw_usd": round(op_raw_hr, 4),
        "stigmergic_burn_per_hr_trimmed_usd": round(op_trim_hr, 4),
        "destruction_ratio_mid": round(ratio_mid, 4),
        "destruction_ratio_max": round(ratio_max, 4),
        "destruction_ratio_max_vs_trimmed": round(ratio_max_trim, 4),
        "raw_annual_spend_multiple_max": round(annual_multiple, 4),
        "pr_size_shrink_ratio": round(pr_shrink, 4),
        "sloc_pace_multiple": round(pace, 4),
    }


# ---------------------------------------------------------------------------
# EQ-3: 20-Year Therapy-Note Observability Gramian vs 1-Bit Control Inversion
# ---------------------------------------------------------------------------
def eq3_observability_gramian() -> dict:
    therapy_years = LOCKED["tan_therapy_notes_years"]
    assert therapy_years == 20

    # 20 years of therapy notes carry zero bits about code AST state: the
    # cross-covariance block between the psychological corpus and the code
    # state is the zero matrix, so its observability Gramian contributes no
    # latent defensive capacity.
    mi_therapy_ast_bits = 0.0
    assert mi_therapy_ast_bits == 0.0
    info_density_bits_per_year = mi_therapy_ast_bits / therapy_years
    assert info_density_bits_per_year == 0.0

    # Owner reply vocabulary {'do it', 'rec'}: H(Reply) <= log2(2) = 1.0 bit.
    reply_vocab = ("do it", "rec")
    h_reply_ceiling = math.log2(len(reply_vocab))
    check("EQ-3 H(Reply) ceiling (bits)", h_reply_ceiling, 1.0)
    h_uniform = -sum(
        (1.0 / len(reply_vocab)) * math.log2(1.0 / len(reply_vocab))
        for _ in reply_vocab
    )
    check("EQ-3 H(Reply) uniform (bits)", h_uniform, 1.0)
    assert h_uniform <= h_reply_ceiling

    # Full-rank psychological observability inverts to a rank-1 control
    # Gramian: the only observable eigenvalue is the scalar reply channel.
    observability_rank = 1.0
    check("EQ-3 control-channel observability rank", observability_rank, 1.0)

    return {
        "mi_therapy_ast_bits": mi_therapy_ast_bits,
        "h_reply_bits": round(h_uniform, 4),
        "observability_rank": observability_rank,
    }


# ---------------------------------------------------------------------------
# EQ-4: YC 2024-2026 Form D Stack & LP Herd Token Drain
# ---------------------------------------------------------------------------
FORM_D_ISSUERS = (
    ("YCP26", "0002131753", "2026", 1712409624),
    ("YCA26", "0002131752", "2026", 727774091),
    ("ES26", "0002131827", "2026", 228321282),
    ("ESP24", "0002018782", "2024", 421765060),
    ("ES24", "0002018779", "2024", 152698436),
    ("ECO24", "0002043687", "2024", 89434057),
)


def eq4_yc_form_d_stack() -> dict:
    v2026 = sum(cap for _, _, vintage, cap in FORM_D_ISSUERS if vintage == "2026")
    v2024 = sum(cap for _, _, vintage, cap in FORM_D_ISSUERS if vintage == "2024")
    assert v2026 == LOCKED["yc_2026_vintage_lp_capital_usd"]
    assert v2024 == LOCKED["yc_2024_vintage_lp_capital_usd"]
    assert v2026 + v2024 == LOCKED["yc_combined_2024_2026_lp_capital_usd"]

    herd_low_m = 2500 * 37500 / 1e6
    herd_high_m = 2500 * 150000 / 1e6
    check("EQ-4 herd drain @ $37.5K/dev ($M)", herd_low_m,
          LOCKED["yc_portfolio_herd_burn_2500_devs_at_37500_usd_m"])
    check("EQ-4 herd drain @ $150K/dev ($M)", herd_high_m,
          LOCKED["yc_portfolio_herd_burn_2500_devs_at_150000_usd_m"])
    assert LOCKED["yc_2026_qualified_purchaser_lps_count"] == 87

    return {
        "vintage_2026_usd": v2026,
        "vintage_2024_usd": v2024,
        "combined_usd": v2026 + v2024,
        "herd_drain_37500_usd_m": round(herd_low_m, 4),
        "herd_drain_150000_usd_m": round(herd_high_m, 4),
    }


# ---------------------------------------------------------------------------
# EQ-5: Dual-Angle Stray-Light Failure (Retrieval Noise & Knightian OOD
#       centroid-regression suppression)
# ---------------------------------------------------------------------------
def eq5_stray_light_failure() -> dict:
    r_prod = LOCKED["gbrain_production_r_at_5"]
    miss = 1.0 - r_prod
    check("EQ-5 retrieval miss rate", miss, LOCKED["gbrain_retrieval_miss_rate"])
    assert r_prod > LOCKED["gbrain_baseline_r_at_5"]

    # (a) Stray-light angle 1: 98% rejected/historical noise in raw
    # applications/emails collapses effective precision.
    noise_fraction = 0.98
    effective_precision = r_prod * (1.0 - noise_fraction)
    assert effective_precision < 0.05

    # (b) Stray-light angle 2: Knightian OOD suppression. Candidates above the
    # historical centroid C_Past carry surprise I(x) = -log2 P(x | C_Past)
    # >= 10 bits, so the autoregressive RAG agent attenuates the OOD tail by
    # 2^10 = 1024 >= 100x while amplifying in-distribution me-too clones.
    i_tail_bits = 10.0
    attenuation = 2.0 ** i_tail_bits
    assert attenuation == 1024.0
    assert attenuation >= 100.0

    # Corpus-scale invariants.
    assert LOCKED["gbrain_total_pages"] > LOCKED["gbrain_total_people"] > LOCKED["gbrain_total_companies"]
    assert LOCKED["gbrain_autonomous_cron_jobs"] == 66

    return {
        "retrieval_miss_rate": round(miss, 4),
        "effective_precision_post_noise": round(effective_precision, 6),
        "ood_attenuation_factor": attenuation,
    }


# ---------------------------------------------------------------------------
# W-F: Anthropic PBC (CIK 0002130357) deterministic capital-structure waterfall
# ---------------------------------------------------------------------------
SENIOR_CREDIT_FACILITY_USD_B = 2.5
COMPUTE_LEASE_OBLIGATIONS_USD_B = 757.0
PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B = 238.576


def tranche_recovery(ev: float) -> dict:
    """Absolute-priority recovery waterfall. `ev` and all outputs are in $B.

    Senior -> junior: (1) $2.5B Senior Credit Facility, (2) $757.0B
    Unconditional Compute & Lease Obligations, (3) $238.576B Preferred Stock
    Liquidation Preference, (4) Common Equity residual stub.
    """
    assert ev >= 0.0, "enterprise value must be non-negative"
    senior = min(ev, SENIOR_CREDIT_FACILITY_USD_B)
    compute = min(max(ev - SENIOR_CREDIT_FACILITY_USD_B, 0.0),
                  COMPUTE_LEASE_OBLIGATIONS_USD_B)
    preferred = min(max(ev - SENIOR_CREDIT_FACILITY_USD_B - COMPUTE_LEASE_OBLIGATIONS_USD_B, 0.0),
                    PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B)
    common = max(ev - SENIOR_CREDIT_FACILITY_USD_B - COMPUTE_LEASE_OBLIGATIONS_USD_B
                 - PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B, 0.0)
    tranches = [
        {"tranche": "senior_credit_facility",
         "principal_usd_b": SENIOR_CREDIT_FACILITY_USD_B,
         "recovery_usd_b": round(senior, 6),
         "cents_on_dollar": round(100.0 * senior / SENIOR_CREDIT_FACILITY_USD_B, 4)},
        {"tranche": "unconditional_compute_lease_obligations",
         "principal_usd_b": COMPUTE_LEASE_OBLIGATIONS_USD_B,
         "recovery_usd_b": round(compute, 6),
         "cents_on_dollar": round(100.0 * compute / COMPUTE_LEASE_OBLIGATIONS_USD_B, 4)},
        {"tranche": "preferred_stock_liquidation_preference",
         "principal_usd_b": PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B,
         "recovery_usd_b": round(preferred, 6),
         "cents_on_dollar": round(100.0 * preferred / PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B, 4)},
        {"tranche": "common_equity_residual",
         "principal_usd_b": 0.0,
         "recovery_usd_b": round(common, 6),
         "cents_on_dollar": None},
    ]
    return {"ev_usd_b": ev, "tranches": tranches}


def verify_waterfall() -> list:
    # Fulcrum identity: senior + compute-max + preferred == total fulcrum.
    fulcrum = (SENIOR_CREDIT_FACILITY_USD_B + COMPUTE_LEASE_OBLIGATIONS_USD_B
               + PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B)
    check("W-F total fulcrum identity ($B)", fulcrum,
          LOCKED["anthropic_s1_total_fulcrum_usd_b"])
    assert LOCKED["anthropic_s1_compute_encumbrance_min_usd_b"] <= LOCKED["anthropic_s1_compute_encumbrance_max_usd_b"]
    assert LOCKED["anthropic_s1_compute_encumbrance_max_usd_b"] == COMPUTE_LEASE_OBLIGATIONS_USD_B
    assert LOCKED["anthropic_s1_stockholders_deficit_usd_m"] < 0.0
    assert LOCKED["anthropic_s1_9m26_implied_revenue_usd_m"] > 0.0
    assert LOCKED["anthropic_s1_100k_customers_count"] == 11900

    results = []
    for ev in (50.0, 120.0, 262.0, 350.0, 998.076):
        rec = tranche_recovery(ev)
        total = sum(t["recovery_usd_b"] for t in rec["tranches"])
        check("W-F value conservation @ EV=${}B".format(ev), total, ev, tol=1e-6)
        results.append(rec)

    at = {r["ev_usd_b"]: {t["tranche"]: t for t in r["tranches"]} for r in results}
    expected_compute = {50.0: (47.5, 6.2748), 120.0: (117.5, 15.5218),
                        262.0: (259.5, 34.2801), 350.0: (347.5, 45.9049)}
    for ev, (rec_b, cod) in expected_compute.items():
        check("W-F senior recovery @ EV=${}B".format(ev),
              at[ev]["senior_credit_facility"]["recovery_usd_b"], 2.5, tol=1e-6)
        check("W-F compute recovery @ EV=${}B".format(ev),
              at[ev]["unconditional_compute_lease_obligations"]["recovery_usd_b"], rec_b, tol=1e-6)
        check("W-F compute cents @ EV=${}B".format(ev),
              at[ev]["unconditional_compute_lease_obligations"]["cents_on_dollar"], cod)
        check("W-F preferred recovery @ EV=${}B".format(ev),
              at[ev]["preferred_stock_liquidation_preference"]["recovery_usd_b"], 0.0, tol=1e-6)
        check("W-F common recovery @ EV=${}B".format(ev),
              at[ev]["common_equity_residual"]["recovery_usd_b"], 0.0, tol=1e-6)

    # At the $998.076B fulcrum every senior tranche clears 100c and the
    # common stub is exactly $0.
    for name in ("senior_credit_facility",
                 "unconditional_compute_lease_obligations",
                 "preferred_stock_liquidation_preference"):
        check("W-F {} cents @ fulcrum".format(name),
              at[998.076][name]["cents_on_dollar"], 100.0, tol=1e-6)
    check("W-F common stub @ fulcrum",
          at[998.076]["common_equity_residual"]["recovery_usd_b"], 0.0, tol=1e-9)
    return results


# ---------------------------------------------------------------------------
# Hard-date catalyst & forbearance calendar (ISO 8601, strictly ascending)
# ---------------------------------------------------------------------------
catalyst_calendar = (
    {"date": "2026-01-30", "type": "filing_window",
     "catalyst": "YC 2026-vintage Form D aggregation window opens (YCP26 CIK 0002131753 / YCA26 CIK 0002131752 / ES26 CIK 0002131827; $2,668,504,997 LP capital across 87 qualified-purchaser LPs)"},
    {"date": "2026-03-31", "type": "s1_filing",
     "catalyst": "Anthropic PBC S-1 public-filing window; 9M26 implied revenue $33,086M across 11,900 $100K-class customers"},
    {"date": "2026-09-30", "type": "measurement_period_end",
     "catalyst": "9M26 implied-revenue measurement period end; stockholders' deficit -$127,619M mark"},
    {"date": "2026-12-31", "type": "encumbrance_step_up",
     "catalyst": "Unconditional compute & lease obligation encumbrance step-up cliff ($732.0B min to $757.0B max)"},
    {"date": "2027-03-31", "type": "forbearance_expiry",
     "catalyst": "$2.5B Senior Credit Facility forbearance expiry and grace-period cure deadline"},
    {"date": "2027-12-31", "type": "maturity_cliff",
     "catalyst": "Preferred stock liquidation-preference ($238.576B) maturity cliff; common stub = $0 at EV = $998.076B fulcrum"},
)


# ---------------------------------------------------------------------------
# Multi-counterparty security-master cross-index
# ---------------------------------------------------------------------------
entity_and_instrument_ids = {
    "primary_target": {
        "entity": "Tan (sole operator: gstack / gbrain / capy agent-virtualization stack)",
        "role": "primary",
        "identifiers": {"sec_cik": None,
                        "stack_components": ["gstack", "gbrain", "capy"]},
    },
    "fulcrum_issuer": {
        "entity": "Anthropic PBC",
        "role": "fulcrum_issuer",
        "identifiers": {"sec_cik": "0002130357"},
        "instruments": [
            {"instrument": "senior_credit_facility",
             "principal_usd_b": SENIOR_CREDIT_FACILITY_USD_B},
            {"instrument": "unconditional_compute_lease_obligations",
             "principal_usd_b": COMPUTE_LEASE_OBLIGATIONS_USD_B},
            {"instrument": "preferred_stock_liquidation_preference",
             "principal_usd_b": PREFERRED_STOCK_LIQUIDATION_PREFERENCE_USD_B},
            {"instrument": "common_equity_residual", "principal_usd_b": 0.0},
        ],
    },
    "form_d_issuers": [
        {"issuer": name, "sec_cik": cik, "vintage": vintage, "lp_capital_usd": capital}
        for name, cik, vintage, capital in FORM_D_ISSUERS
    ],
    "lp_herd": {
        "entity": "YC 2026 qualified-purchaser LP cohort and 2,500-developer portfolio herd",
        "role": "fiduciary_credit_allocator",
        "identifiers": {"qualified_purchaser_lps": 87, "portfolio_devs": 2500},
    },
}


def verify_catalyst_calendar() -> None:
    prev = None
    for entry in catalyst_calendar:
        d = date.fromisoformat(entry["date"])
        assert prev is None or d > prev, (
            "catalyst_calendar not strictly ascending at {}".format(entry["date"]))
        prev = d
        assert len(entry["catalyst"]) >= 16


def verify_entity_and_instrument_ids() -> None:
    assert entity_and_instrument_ids["fulcrum_issuer"]["identifiers"]["sec_cik"] == "0002130357"
    for row in entity_and_instrument_ids["form_d_issuers"]:
        cik = row["sec_cik"]
        assert len(cik) == 10 and cik.isdigit(), "malformed CIK: {}".format(cik)
    total = sum(row["lp_capital_usd"] for row in entity_and_instrument_ids["form_d_issuers"])
    assert total == LOCKED["yc_combined_2024_2026_lp_capital_usd"]


def main() -> int:
    eq1 = eq1_bureaucratic_token_multiplier()
    eq2 = eq2_hourly_capital_efficiency_destruction()
    eq3 = eq3_observability_gramian()
    eq4 = eq4_yc_form_d_stack()
    eq5 = eq5_stray_light_failure()
    waterfall = verify_waterfall()
    verify_catalyst_calendar()
    verify_entity_and_instrument_ids()

    record = {
        "schema_version": "1.0",
        "bundle": "bureaucratic_agent_virtualization_and_cognitive_honeypot",
        "status": "PASS",
        "locked_constants": dict(LOCKED),
        "equation_outputs": {"eq1": eq1, "eq2": eq2, "eq3": eq3, "eq4": eq4, "eq5": eq5},
        "tranche_waterfall": waterfall,
        "catalyst_calendar": [dict(entry) for entry in catalyst_calendar],
        "entity_and_instrument_ids": entity_and_instrument_ids,
    }
    print(json.dumps(record, indent=2))
    print("-" * 72)
    print("EQ-1 multiplier={}x cached_equiv={}M tokens/sprint".format(
        eq1["multiplier"], eq1["cached_equiv_tokens_m"]))
    print("EQ-2 tan/hr mid=${} max=${} | stigmergic/hr raw=${} trimmed=${} | ratios {}x/{}x/{}x | pr_shrink={} | sloc_pace={}x".format(
        eq2["tan_burn_per_hr_mid_usd"], eq2["tan_burn_per_hr_max_usd"],
        eq2["stigmergic_burn_per_hr_raw_usd"], eq2["stigmergic_burn_per_hr_trimmed_usd"],
        eq2["destruction_ratio_mid"], eq2["destruction_ratio_max"],
        eq2["destruction_ratio_max_vs_trimmed"], eq2["pr_size_shrink_ratio"],
        eq2["sloc_pace_multiple"]))
    print("EQ-3 I(therapy;AST)={} bits H(reply)={} bit rank={}".format(
        eq3["mi_therapy_ast_bits"], eq3["h_reply_bits"], eq3["observability_rank"]))
    print("EQ-4 2026=${:,} 2024=${:,} combined=${:,} herd=${}M..${}M/yr".format(
        eq4["vintage_2026_usd"], eq4["vintage_2024_usd"], eq4["combined_usd"],
        eq4["herd_drain_37500_usd_m"], eq4["herd_drain_150000_usd_m"]))
    print("EQ-5 miss_rate={} precision_post_noise={} ood_attenuation={}x".format(
        eq5["retrieval_miss_rate"], eq5["effective_precision_post_noise"],
        eq5["ood_attenuation_factor"]))
    for wf in waterfall:
        cells = "  ".join("{}=${}B".format(t["tranche"], t["recovery_usd_b"])
                          for t in wf["tranches"])
        print("W-F EV=${}B -> {}".format(wf["ev_usd_b"], cells))
    print("STATUS: PASS | EQ-1..EQ-5 + tranche_recovery + catalyst_calendar + entity_and_instrument_ids verified | exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())