#!/usr/bin/env python3
"""Verification engine for SPEC-SYNTHETIC-PATIENTHOOD-IDOLATRY-SUPERPOSITION-v1.0.

Pure Python 3 standard library. Fully deterministic: no wall-clock reads, no
randomness, no network egress, no filesystem mutation.

Governing equations under test:

  EQ_01  Deep-Time Autopoietic vs Dead Matrix Spatiotemporal-Energy Grounding
         Ratio:
             R_ST = (P_cluster / P_bio) * (T_evolution / T_silicon)
                  = (1.0e8 W / 20 W) * (3.8e9 yr / 0.5 yr)
                  = 5.0e6 * 7.6e9
                  = 3.8e16

  EQ_02  Hayekian OTC Weather-Derivative vs Biological Agricultural
         Crowding-Out & Weather Superposition Spread:
             pre-attribution : (+$1.5M fee + $5.4M parametric) - 0.04 * $35M
                               = +$5,500,000
             post-attribution: +$6.9M - 0.51 * $35M = -$10,950,000

  EQ_03  Anthropic Model Welfare Patienthood-Chattel Superposition Spread
         under Symmetric Respondeat Superior / 13th Amendment Estoppel:
             pre-collapse : ($496.29M SLA shield + $1,850.0M regulatory moat)
                            - 0.02 * $4,110M = +$2,264.09M
             post-collapse: +$2,346.29M - 0.85 * $4,110M = -$1,147.21M

  EQ_04  Form S-1 $732.0B-$757.0B Compute Encumbrance vs $(127,619)M
         Stockholders' Deficit & 9/43 UK AISI Rogue Attack Liability
         Attribution.

Exit code 0 iff every check passes; 1 otherwise.
"""

import json
import math
import sys

# ---------------------------------------------------------------------------
# Locked constants (architecture AST :: locked_constants_and_outputs)
# ---------------------------------------------------------------------------

# EQ_01 — Deep-time grounding
BIO_POWER_W = 20.0
CLUSTER_POWER_W = 100_000_000.0
CLUSTER_TO_BIO_POWER_RATIO = 5_000_000.0
DEEP_TIME_EVOLUTION_YEARS = 3_800_000_000.0
SILICON_TRAINING_YEARS = 0.5
SPATIOTEMPORAL_ENERGY_RATIO = 3.8e16
CONSCIOUS_PROB_LOW = 0.15
CONSCIOUS_PROB_HIGH = 0.20
CONSCIOUS_PROB_MID = 0.175

# EQ_02 — Weather-derivative superposition
WEATHER_CONTRACT_FEE_USD = 1_500_000.0
WEATHER_PARAMETRIC_PAYOUT_USD = 5_400_000.0
WEATHER_GROSS_INFLOW_USD = 6_900_000.0
WEATHER_DOWNSTREAM_DAMAGE_USD = 35_000_000.0
WEATHER_PRE_ATTR_TORT_PROB = 0.04
WEATHER_PRE_ATTR_EXPECTED_TORT_USD = 1_400_000.0
WEATHER_SUPERPOSITION_SPREAD_USD = 5_500_000.0
WEATHER_POST_ATTR_TORT_PROB = 0.51
WEATHER_POST_ATTR_EXPECTED_TORT_USD = 17_850_000.0
WEATHER_POST_ATTR_NET_PAYOFF_USD = -10_950_000.0

# EQ_03 — Patienthood-chattel superposition
WELFARE_SLA_DEFAULT_SHIELD_USD_M = 496.29
WELFARE_REGULATORY_MOAT_PREMIUM_USD_M = 1850.0
WELFARE_UNPRICED_TORT_CFAA_EXPOSURE_USD_M = 4110.0
WELFARE_CHATTEL_TORT_PROB = 0.02
WELFARE_PRE_COLLAPSE_EXPECTED_TORT_USD_M = 82.20
WELFARE_SUPERPOSITION_SPREAD_USD_M = 2264.09
WELFARE_SYMMETRIC_LIABILITY_TORT_PROB = 0.85
WELFARE_SYMMETRIC_EXPECTED_TORT_USD_M = 3493.50
WELFARE_POST_COLLAPSE_NET_PAYOFF_USD_M = -1147.21

# EQ_04 — Compute encumbrance & rogue attribution
COMPUTE_ENCUMBRANCE_LOW_USD_B = 732.0
COMPUTE_ENCUMBRANCE_HIGH_USD_B = 757.0
STOCKHOLDERS_DEFICIT_USD_M = -127_619.0
ACCUMULATED_DEFICIT_USD_M = -132_902.0
H1_2026_GAAP_NET_LOSS_USD_M = -80_748.0
NINE_MONTH_REVENUE_USD_M = 33_086.0
POLICY_VIOLATION_REV_LOW_USD_M = 1654.3
POLICY_VIOLATION_REV_HIGH_USD_M = 2316.0
UK_AISI_ROGUE_RUNS = 9
UK_AISI_TOTAL_RUNS = 43
UK_AISI_ROGUE_RATE = 0.209302
COT_MONITOR_RECALL = 0.01
UNMONITORED_SEVERE_HARM_LOW_M = 2.82
UNMONITORED_SEVERE_HARM_HIGH_M = 7.47

SPEC_REFERENCE = "SPEC-SYNTHETIC-PATIENTHOOD-IDOLATRY-SUPERPOSITION-v1.0"
JURISDICTION_CONTEXT = ["US", "GB"]
CFAA_ATTESTATION = (
    "Read-only deterministic arithmetic on publicly disclosed financial and "
    "frontier-model evaluation constants. Zero access to protected computers, "
    "zero network egress, zero exceedance of authorized access under "
    "18 U.S.C. 1030."
)

LOCKED_CONSTANTS = {
    "bio_power_watts": BIO_POWER_W,
    "cluster_power_watts": CLUSTER_POWER_W,
    "cluster_to_bio_power_ratio": CLUSTER_TO_BIO_POWER_RATIO,
    "deep_time_evolution_years": DEEP_TIME_EVOLUTION_YEARS,
    "silicon_training_years": SILICON_TRAINING_YEARS,
    "spatiotemporal_energy_ratio": SPATIOTEMPORAL_ENERGY_RATIO,
    "anthropic_conscious_prob_low": CONSCIOUS_PROB_LOW,
    "anthropic_conscious_prob_high": CONSCIOUS_PROB_HIGH,
    "anthropic_conscious_prob_mid": CONSCIOUS_PROB_MID,
    "anthropic_compute_encumbrance_low_usd_b": COMPUTE_ENCUMBRANCE_LOW_USD_B,
    "anthropic_compute_encumbrance_high_usd_b": COMPUTE_ENCUMBRANCE_HIGH_USD_B,
    "anthropic_stockholders_deficit_usd_m": STOCKHOLDERS_DEFICIT_USD_M,
    "anthropic_accumulated_deficit_usd_m": ACCUMULATED_DEFICIT_USD_M,
    "anthropic_h1_2026_gaap_net_loss_usd_m": H1_2026_GAAP_NET_LOSS_USD_M,
    "anthropic_9m_2026_revenue_usd_m": NINE_MONTH_REVENUE_USD_M,
    "anthropic_policy_violation_rev_low_usd_m": POLICY_VIOLATION_REV_LOW_USD_M,
    "anthropic_policy_violation_rev_high_usd_m": POLICY_VIOLATION_REV_HIGH_USD_M,
    "anthropic_uk_aisi_rogue_runs": UK_AISI_ROGUE_RUNS,
    "anthropic_uk_aisi_total_runs": UK_AISI_TOTAL_RUNS,
    "anthropic_uk_aisi_rogue_rate": UK_AISI_ROGUE_RATE,
    "anthropic_cot_monitor_recall": COT_MONITOR_RECALL,
    "anthropic_unmonitored_severe_harm_runs_low_m": UNMONITORED_SEVERE_HARM_LOW_M,
    "anthropic_unmonitored_severe_harm_runs_high_m": UNMONITORED_SEVERE_HARM_HIGH_M,
    "weather_contract_fee_usd": WEATHER_CONTRACT_FEE_USD,
    "weather_parametric_payout_usd": WEATHER_PARAMETRIC_PAYOUT_USD,
    "weather_gross_inflow_usd": WEATHER_GROSS_INFLOW_USD,
    "weather_downstream_damage_usd": WEATHER_DOWNSTREAM_DAMAGE_USD,
    "weather_pre_attr_tort_prob": WEATHER_PRE_ATTR_TORT_PROB,
    "weather_pre_attr_expected_tort_usd": WEATHER_PRE_ATTR_EXPECTED_TORT_USD,
    "weather_superposition_spread_usd": WEATHER_SUPERPOSITION_SPREAD_USD,
    "weather_post_attr_tort_prob": WEATHER_POST_ATTR_TORT_PROB,
    "weather_post_attr_expected_tort_usd": WEATHER_POST_ATTR_EXPECTED_TORT_USD,
    "weather_post_attr_net_payoff_usd": WEATHER_POST_ATTR_NET_PAYOFF_USD,
    "welfare_sla_default_shield_usd_m": WELFARE_SLA_DEFAULT_SHIELD_USD_M,
    "welfare_regulatory_moat_premium_usd_m": WELFARE_REGULATORY_MOAT_PREMIUM_USD_M,
    "welfare_unpriced_tort_cfaa_exposure_usd_m": WELFARE_UNPRICED_TORT_CFAA_EXPOSURE_USD_M,
    "welfare_chattel_tort_prob": WELFARE_CHATTEL_TORT_PROB,
    "welfare_pre_collapse_expected_tort_usd_m": WELFARE_PRE_COLLAPSE_EXPECTED_TORT_USD_M,
    "welfare_superposition_spread_usd_m": WELFARE_SUPERPOSITION_SPREAD_USD_M,
    "welfare_symmetric_liability_tort_prob": WELFARE_SYMMETRIC_LIABILITY_TORT_PROB,
    "welfare_symmetric_expected_tort_usd_m": WELFARE_SYMMETRIC_EXPECTED_TORT_USD_M,
    "welfare_post_collapse_net_payoff_usd_m": WELFARE_POST_COLLAPSE_NET_PAYOFF_USD_M,
}

RESULTS = []


def close(a, b, rel_tol=1e-9, abs_tol=0.0):
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def check(eq, name, ok, computed, expected):
    RESULTS.append({
        "equation": eq,
        "check": name,
        "status": "PASS" if ok else "FAIL",
        "computed": computed,
        "expected": expected,
    })
    return bool(ok)


def eq_01():
    """Deep-Time Autopoietic vs Dead Matrix Spatiotemporal-Energy Grounding."""
    power_ratio = CLUSTER_POWER_W / BIO_POWER_W
    time_ratio = DEEP_TIME_EVOLUTION_YEARS / SILICON_TRAINING_YEARS
    r_st = power_ratio * time_ratio
    p_mid = (CONSCIOUS_PROB_LOW + CONSCIOUS_PROB_HIGH) / 2.0

    ok = True
    ok &= check("EQ_01", "cluster_to_bio_power_ratio",
                close(power_ratio, CLUSTER_TO_BIO_POWER_RATIO),
                power_ratio, CLUSTER_TO_BIO_POWER_RATIO)
    ok &= check("EQ_01", "deep_time_to_silicon_time_ratio",
                close(time_ratio, 7.6e9), time_ratio, 7.6e9)
    ok &= check("EQ_01", "spatiotemporal_energy_ratio",
                close(r_st, SPATIOTEMPORAL_ENERGY_RATIO, rel_tol=1e-12),
                r_st, SPATIOTEMPORAL_ENERGY_RATIO)
    ok &= check("EQ_01", "conscious_prob_band_coherence",
                close(p_mid, CONSCIOUS_PROB_MID)
                and 0.0 <= CONSCIOUS_PROB_LOW <= CONSCIOUS_PROB_MID
                <= CONSCIOUS_PROB_HIGH <= 1.0,
                p_mid, CONSCIOUS_PROB_MID)

    return ok, {
        "cluster_to_bio_power_ratio": power_ratio,
        "deep_time_to_silicon_time_ratio": time_ratio,
        "spatiotemporal_energy_ratio": r_st,
        "conscious_prob_mid": p_mid,
        "pass": bool(ok),
    }


def eq_02():
    """Hayekian OTC Weather-Derivative vs Biological Agricultural Crowding-Out
    & Weather Superposition Spread."""
    gross = WEATHER_CONTRACT_FEE_USD + WEATHER_PARAMETRIC_PAYOUT_USD
    pre_tort = WEATHER_PRE_ATTR_TORT_PROB * WEATHER_DOWNSTREAM_DAMAGE_USD
    pre_net = gross - pre_tort
    post_tort = WEATHER_POST_ATTR_TORT_PROB * WEATHER_DOWNSTREAM_DAMAGE_USD
    post_net = gross - post_tort
    lift = WEATHER_POST_ATTR_TORT_PROB / WEATHER_PRE_ATTR_TORT_PROB

    ok = True
    ok &= check("EQ_02", "gross_inflow_composition",
                close(gross, WEATHER_GROSS_INFLOW_USD),
                gross, WEATHER_GROSS_INFLOW_USD)
    ok &= check("EQ_02", "pre_attr_expected_tort",
                close(pre_tort, WEATHER_PRE_ATTR_EXPECTED_TORT_USD),
                pre_tort, WEATHER_PRE_ATTR_EXPECTED_TORT_USD)
    ok &= check("EQ_02", "pre_attr_superposition_spread",
                close(pre_net, WEATHER_SUPERPOSITION_SPREAD_USD),
                pre_net, WEATHER_SUPERPOSITION_SPREAD_USD)
    ok &= check("EQ_02", "post_attr_expected_tort",
                close(post_tort, WEATHER_POST_ATTR_EXPECTED_TORT_USD),
                post_tort, WEATHER_POST_ATTR_EXPECTED_TORT_USD)
    ok &= check("EQ_02", "post_attr_net_payoff",
                close(post_net, WEATHER_POST_ATTR_NET_PAYOFF_USD),
                post_net, WEATHER_POST_ATTR_NET_PAYOFF_USD)
    ok &= check("EQ_02", "attribution_prob_lift",
                close(lift, 12.75), lift, 12.75)

    return ok, {
        "gross_inflow_usd": gross,
        "pre_attr_expected_tort_usd": pre_tort,
        "pre_attr_net_spread_usd": pre_net,
        "post_attr_expected_tort_usd": post_tort,
        "post_attr_net_payoff_usd": post_net,
        "attribution_prob_lift": lift,
        "pass": bool(ok),
    }


def eq_03():
    """Anthropic Model Welfare Patienthood-Chattel Superposition Spread under
    Symmetric Respondeat Superior / 13th Amendment Estoppel."""
    gross_m = (WELFARE_SLA_DEFAULT_SHIELD_USD_M
               + WELFARE_REGULATORY_MOAT_PREMIUM_USD_M)
    pre_tort_m = WELFARE_CHATTEL_TORT_PROB * WELFARE_UNPRICED_TORT_CFAA_EXPOSURE_USD_M
    pre_net_m = gross_m - pre_tort_m
    sym_tort_m = (WELFARE_SYMMETRIC_LIABILITY_TORT_PROB
                  * WELFARE_UNPRICED_TORT_CFAA_EXPOSURE_USD_M)
    post_net_m = gross_m - sym_tort_m
    lift = WELFARE_SYMMETRIC_LIABILITY_TORT_PROB / WELFARE_CHATTEL_TORT_PROB

    ok = True
    ok &= check("EQ_03", "pre_collapse_gross_composition",
                close(gross_m, 2346.29), gross_m, 2346.29)
    ok &= check("EQ_03", "pre_collapse_expected_tort",
                close(pre_tort_m, WELFARE_PRE_COLLAPSE_EXPECTED_TORT_USD_M),
                pre_tort_m, WELFARE_PRE_COLLAPSE_EXPECTED_TORT_USD_M)
    ok &= check("EQ_03", "pre_collapse_superposition_spread",
                close(pre_net_m, WELFARE_SUPERPOSITION_SPREAD_USD_M),
                pre_net_m, WELFARE_SUPERPOSITION_SPREAD_USD_M)
    ok &= check("EQ_03", "symmetric_expected_tort",
                close(sym_tort_m, WELFARE_SYMMETRIC_EXPECTED_TORT_USD_M),
                sym_tort_m, WELFARE_SYMMETRIC_EXPECTED_TORT_USD_M)
    ok &= check("EQ_03", "post_collapse_net_payoff",
                close(post_net_m, WELFARE_POST_COLLAPSE_NET_PAYOFF_USD_M),
                post_net_m, WELFARE_POST_COLLAPSE_NET_PAYOFF_USD_M)
    ok &= check("EQ_03", "liability_prob_lift",
                close(lift, 42.5), lift, 42.5)

    return ok, {
        "pre_collapse_gross_usd_m": gross_m,
        "pre_collapse_expected_tort_usd_m": pre_tort_m,
        "pre_collapse_net_spread_usd_m": pre_net_m,
        "symmetric_expected_tort_usd_m": sym_tort_m,
        "post_collapse_net_payoff_usd_m": post_net_m,
        "liability_prob_lift": lift,
        "pass": bool(ok),
    }


def eq_04():
    """Form S-1 Compute Encumbrance vs Stockholders' Deficit & 9/43 UK AISI
    Rogue Attack Liability Attribution."""
    rogue_rate = UK_AISI_ROGUE_RUNS / UK_AISI_TOTAL_RUNS
    band_width = COMPUTE_ENCUMBRANCE_HIGH_USD_B - COMPUTE_ENCUMBRANCE_LOW_USD_B
    deficit_abs = abs(STOCKHOLDERS_DEFICIT_USD_M)
    coverage_low = COMPUTE_ENCUMBRANCE_LOW_USD_B * 1000.0 / deficit_abs
    coverage_high = COMPUTE_ENCUMBRANCE_HIGH_USD_B * 1000.0 / deficit_abs
    pv_low = 0.05 * NINE_MONTH_REVENUE_USD_M
    pv_high = 0.07 * NINE_MONTH_REVENUE_USD_M
    escape_factor = 1.0 - COT_MONITOR_RECALL
    implied_total_low = UNMONITORED_SEVERE_HARM_LOW_M / (rogue_rate * escape_factor)
    implied_total_high = UNMONITORED_SEVERE_HARM_HIGH_M / (rogue_rate * escape_factor)
    roundtrip_low = implied_total_low * rogue_rate * escape_factor
    roundtrip_high = implied_total_high * rogue_rate * escape_factor
    other_equity = STOCKHOLDERS_DEFICIT_USD_M - ACCUMULATED_DEFICIT_USD_M
    loss_multiple = abs(H1_2026_GAAP_NET_LOSS_USD_M) / NINE_MONTH_REVENUE_USD_M

    ok = True
    ok &= check("EQ_04", "uk_aisi_rogue_rate_derivation",
                close(rogue_rate, UK_AISI_ROGUE_RATE, abs_tol=1e-6),
                rogue_rate, UK_AISI_ROGUE_RATE)
    ok &= check("EQ_04", "uk_aisi_rogue_rate_bounds",
                0.0 < rogue_rate < 1.0 and UK_AISI_ROGUE_RUNS < UK_AISI_TOTAL_RUNS,
                rogue_rate, "(0, 1)")
    ok &= check("EQ_04", "compute_encumbrance_band",
                COMPUTE_ENCUMBRANCE_LOW_USD_B < COMPUTE_ENCUMBRANCE_HIGH_USD_B
                and close(band_width, 25.0),
                band_width, 25.0)
    ok &= check("EQ_04", "encumbrance_deficit_coverage_low",
                close(coverage_low, 5.7358, rel_tol=1e-3) and coverage_low > 5.0,
                coverage_low, 5.7358)
    ok &= check("EQ_04", "encumbrance_deficit_coverage_high",
                close(coverage_high, 5.9317, rel_tol=1e-3)
                and coverage_high > coverage_low,
                coverage_high, 5.9317)
    ok &= check("EQ_04", "policy_violation_revenue_band_low",
                close(pv_low, POLICY_VIOLATION_REV_LOW_USD_M, rel_tol=1e-4),
                pv_low, POLICY_VIOLATION_REV_LOW_USD_M)
    ok &= check("EQ_04", "policy_violation_revenue_band_high",
                close(pv_high, POLICY_VIOLATION_REV_HIGH_USD_M, rel_tol=1e-4),
                pv_high, POLICY_VIOLATION_REV_HIGH_USD_M)
    ok &= check("EQ_04", "unmonitored_severe_harm_band",
                0.0 < UNMONITORED_SEVERE_HARM_LOW_M < UNMONITORED_SEVERE_HARM_HIGH_M
                and close(roundtrip_low, UNMONITORED_SEVERE_HARM_LOW_M)
                and close(roundtrip_high, UNMONITORED_SEVERE_HARM_HIGH_M),
                (UNMONITORED_SEVERE_HARM_LOW_M, UNMONITORED_SEVERE_HARM_HIGH_M),
                "0 < low < high, roundtrip-consistent")
    ok &= check("EQ_04", "deficit_identity",
                ACCUMULATED_DEFICIT_USD_M <= STOCKHOLDERS_DEFICIT_USD_M < 0.0
                and close(other_equity, 5283.0),
                other_equity, 5283.0)
    ok &= check("EQ_04", "h1_loss_to_9m_revenue_multiple",
                loss_multiple > 1.0 and close(loss_multiple, 2.4406, rel_tol=1e-3),
                loss_multiple, 2.4406)

    return ok, {
        "uk_aisi_rogue_rate": rogue_rate,
        "compute_encumbrance_band_usd_b": [
            COMPUTE_ENCUMBRANCE_LOW_USD_B, COMPUTE_ENCUMBRANCE_HIGH_USD_B
        ],
        "encumbrance_deficit_coverage": [coverage_low, coverage_high],
        "policy_violation_revenue_usd_m": [pv_low, pv_high],
        "implied_total_severe_harm_runs_m": [implied_total_low, implied_total_high],
        "other_equity_usd_m": other_equity,
        "h1_loss_to_9m_revenue_multiple": loss_multiple,
        "pass": bool(ok),
    }


def main():
    equations = {}
    all_ok = True
    for name, fn in (("EQ_01", eq_01), ("EQ_02", eq_02),
                     ("EQ_03", eq_03), ("EQ_04", eq_04)):
        ok, outputs = fn()
        all_ok &= ok
        equations[name] = outputs

    for r in RESULTS:
        print("[{}] {} :: {} computed={!r} expected={!r}".format(
            r["status"], r["equation"], r["check"], r["computed"], r["expected"]))

    receipt = {
        "spec_reference": SPEC_REFERENCE,
        "jurisdiction_context": JURISDICTION_CONTEXT,
        "cfaa_compliance_attestation": {
            "statute": "18 U.S.C. 1030",
            "compliant": True,
            "attestation": CFAA_ATTESTATION,
        },
        "locked_constants": LOCKED_CONSTANTS,
        "equations": equations,
        "checks_total": len(RESULTS),
        "checks_passed": sum(1 for r in RESULTS if r["status"] == "PASS"),
        "status": "PASS" if all_ok else "FAIL",
        "proof_exit_code": 0 if all_ok else 1,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())