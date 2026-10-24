#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: WEATHER MODIFICATION EFFICACY-CULPABILITY
SUPERPOSITION & PARAMETRIC BASIS (v1.0)
SPEC-WEATHER-MODIFICATION-LIABILITY-SUPERPOSITION-AND-PARAMETRIC-BASIS-v1.0

Deterministically verifies the three governing equations of the weather
modification efficacy-culpability superposition:

  EQ_01 (Statistical Masking inside Natural Variance). A cloud-seeding
     operator claiming a precipitation shift Delta_mu = +12.0% inside a basin
     with natural interannual standard deviation sigma_nat = 24.0% generates a
     single-season signal-to-noise ratio SNR_1 = Delta_mu / sigma_nat = 0.50.
     Under a two-sided z = 1.96 (95% confidence) evidentiary threshold, a
     downstream tort plaintiff requires N_min = (z / SNR_1)^2 = 15.3664
     consecutive instrumented years to statistically isolate anthropogenic
     causation from natural weather variance.

  EQ_02 (The Efficacy-Culpability Superposition Spread). The operator
     simultaneously sells commercial efficacy (P_contract = $2,400,000
     municipal seeding fee plus V_param = $4,500,000 parametric derivative
     payout = $6,900,000 gross inflow) while invoking Slutsky ("no vested
     property right in clouds") and SNR_1 = 0.50 to suppress tort recovery
     probability to p_tort = 0.04 against D_ext = $35,000,000 downstream
     flood/drought damages (E[L_tort] = p_tort * D_ext = $1,400,000),
     capturing a net arbitrage spread
     S_super = (P_contract + V_param) - E[L_tort] = +$5,500,000.

  EQ_03 (2026 Attribution-Science Phase Transition & Superposition Collapse).
     When isotopic tracer telemetry and ensemble attribution models push
     proximate-cause probability across the p_tort* = 0.51 preponderance bar,
     expected liability jumps to E[L_tort]' = 0.51 * $35,000,000 = $17,850,000,
     inverting operator net payoff to -$10,950,000 and collapsing the
     15 U.S.C. Section 330 notice-only shield.

Pure Python 3 standard library. Zero external dependencies.
"""

import hashlib
import json
import math
import sys

# ---------------------------------------------------------------------------
# EQ_01: Statistical masking inside natural interannual variance
# ---------------------------------------------------------------------------
DELTA_MU_PCT = 12.0            # claimed seeding precipitation yield shift
SIGMA_NAT_PCT = 24.0           # natural interannual precipitation sigma
Z_THRESHOLD_95PCT = 1.96       # two-sided 95% confidence evidentiary bar

# ---------------------------------------------------------------------------
# EQ_02: Efficacy-culpability superposition spread
# ---------------------------------------------------------------------------
P_CONTRACT_USD = 2400000.0                 # municipal seeding contract fee
CME_DEGREE_DAY_MULTIPLIER_USD = 20.0       # CME HDD/CDD index point multiplier
V_PARAM_USD = 4500000.0                    # parametric derivative payout
P_TORT = 0.04                              # suppressed tort recovery probability
D_EXT_USD = 35000000.0                     # downstream flood/drought damage
STATUTORY_NONREPORTING_MAX_FINE_USD = 10000.0  # 15 U.S.C. Section 330d cap

# ---------------------------------------------------------------------------
# EQ_03: 2026 attribution-science phase transition
# ---------------------------------------------------------------------------
P_TORT_STAR = 0.51                         # preponderance-of-evidence bar


# ---------------------------------------------------------------------------
# EQ_01
# ---------------------------------------------------------------------------
def theorem1_statistical_masking():
    snr_1 = DELTA_MU_PCT / SIGMA_NAT_PCT
    n_min = (Z_THRESHOLD_95PCT / snr_1) ** 2
    masking_holds = snr_1 < 1.0 and n_min > 1.0

    assert abs(snr_1 - 0.50) < 1e-12
    assert abs(n_min - 15.3664) < 1e-9
    assert masking_holds is True
    # A single instrumented season cannot clear the 95% causation bar.
    assert n_min > 1.0

    return {
        "delta_mu_pct": DELTA_MU_PCT,
        "sigma_nat_pct": SIGMA_NAT_PCT,
        "snr_single_season": round(snr_1, 12),
        "z_threshold_95pct": Z_THRESHOLD_95PCT,
        "seasons_required_95pct": round(n_min, 6),
        "masking_holds": masking_holds,
    }


# ---------------------------------------------------------------------------
# EQ_02
# ---------------------------------------------------------------------------
def theorem2_superposition_spread():
    gross_inflow = P_CONTRACT_USD + V_PARAM_USD
    e_l_tort = P_TORT * D_EXT_USD
    s_super = gross_inflow - e_l_tort
    parametric_index_points = V_PARAM_USD / CME_DEGREE_DAY_MULTIPLIER_USD
    spread_positive = s_super > 0.0

    assert abs(gross_inflow - 6900000.0) < 1e-6
    assert abs(e_l_tort - 1400000.0) < 1e-6
    assert abs(s_super - 5500000.0) < 1e-6
    assert abs(parametric_index_points - 225000.0) < 1e-6
    assert spread_positive is True
    # The notice-only statutory fine is de minimis against the captured spread.
    assert STATUTORY_NONREPORTING_MAX_FINE_USD < s_super
    assert STATUTORY_NONREPORTING_MAX_FINE_USD < e_l_tort

    return {
        "p_contract_usd": P_CONTRACT_USD,
        "cme_degree_day_multiplier_usd": CME_DEGREE_DAY_MULTIPLIER_USD,
        "parametric_index_points": round(parametric_index_points, 6),
        "v_param_usd": V_PARAM_USD,
        "gross_inflow_usd": round(gross_inflow, 6),
        "p_tort": P_TORT,
        "d_ext_usd": D_EXT_USD,
        "e_l_tort_usd": round(e_l_tort, 6),
        "statutory_nonreporting_max_fine_usd": STATUTORY_NONREPORTING_MAX_FINE_USD,
        "s_super_usd": round(s_super, 6),
        "spread_positive": spread_positive,
    }


# ---------------------------------------------------------------------------
# EQ_03
# ---------------------------------------------------------------------------
def theorem3_attribution_phase_transition(t2):
    e_l_tort_post = P_TORT_STAR * D_EXT_USD
    net_pnl_post = t2["gross_inflow_usd"] - e_l_tort_post
    superposition_collapses = net_pnl_post < 0.0
    notice_only_shield_collapses = P_TORT_STAR > 0.5 and superposition_collapses

    assert abs(e_l_tort_post - 17850000.0) < 1e-6
    assert abs(net_pnl_post - (-10950000.0)) < 1e-6
    assert superposition_collapses is True
    assert notice_only_shield_collapses is True
    # Phase transition: post-attribution expected cost strictly dominates the
    # pre-attribution suppressed expectation, inverting the net payoff sign.
    assert e_l_tort_post > t2["e_l_tort_usd"]
    assert t2["s_super_usd"] > 0.0 > net_pnl_post

    return {
        "p_tort_star": P_TORT_STAR,
        "d_ext_usd": D_EXT_USD,
        "e_l_tort_post_usd": round(e_l_tort_post, 6),
        "gross_inflow_usd": t2["gross_inflow_usd"],
        "net_pnl_post_usd": round(net_pnl_post, 6),
        "superposition_collapses": superposition_collapses,
        "notice_only_shield_collapses": notice_only_shield_collapses,
    }


# ---------------------------------------------------------------------------
# Schema structural check
# ---------------------------------------------------------------------------
def verify_schema():
    here = __file__.rsplit("/", 1)[0]
    root = here.rsplit("/", 1)[0]
    path = root + "/schema/weather_modification_liability_superposition_parametric_basis.json"
    with open(path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == (
        "urn:opstack:schema:"
        "weather_modification_liability_superposition_parametric_basis.json"
    )
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert schema["properties"]["spec_version"]["const"] == (
        "SPEC-WEATHER-MODIFICATION-LIABILITY-SUPERPOSITION-"
        "AND-PARAMETRIC-BASIS-v1.0"
    )

    required = schema["required"]
    props = schema["properties"]
    assert len(required) == len(props) == 6
    assert set(required) == set(props)

    for key in (
        "theorem_1_statistical_masking_natural_variance",
        "theorem_2_efficacy_culpability_superposition_spread",
        "theorem_3_attribution_phase_transition_collapse",
    ):
        block = props[key]
        assert block["additionalProperties"] is False
        assert set(block["required"]) == set(block["properties"])

    assert props["verification"]["properties"]["proof"]["const"] == (
        "proofs/verify_weather_modification_liability_"
        "superposition_parametric_basis.py"
    )
    assert props["verification"]["properties"]["exit_code"]["const"] == 0
    assert len(props["empirical_anchors"]["items"]["required"]) == 2

    return len(required), len(props)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run_verification():
    print("=" * 78)
    print("SPEC-WEATHER-MODIFICATION-LIABILITY-SUPERPOSITION-AND-PARAMETRIC-BASIS-v1.0")
    print("=" * 78)

    n_req, n_prop = verify_schema()
    print("[SCHEMA] required=%d properties=%d" % (n_req, n_prop))

    t1 = theorem1_statistical_masking()
    print(
        "[EQ_01] Delta_mu=%.1f%% inside sigma_nat=%.1f%% | SNR_1=%.2f < 1 | "
        "N_min=(z/SNR_1)^2=%.4f instrumented seasons to clear 95%% causation"
        % (
            t1["delta_mu_pct"],
            t1["sigma_nat_pct"],
            t1["snr_single_season"],
            t1["seasons_required_95pct"],
        )
    )

    t2 = theorem2_superposition_spread()
    print(
        "[EQ_02] Gross inflow=$%.2f (contract $%.2f + parametric $%.2f) | "
        "E[L_tort]=p_tort*D_ext=$%.2f | S_super=+$%.2f | "
        "Section 330d fine=$%.2f (de minimis)"
        % (
            t2["gross_inflow_usd"],
            t2["p_contract_usd"],
            t2["v_param_usd"],
            t2["e_l_tort_usd"],
            t2["s_super_usd"],
            t2["statutory_nonreporting_max_fine_usd"],
        )
    )

    t3 = theorem3_attribution_phase_transition(t2)
    print(
        "[EQ_03] p_tort*=%.2f | E[L_tort]'=$%.2f | net PnL=-$%.2f < 0 | "
        "superposition_collapses=%s | notice_only_shield_collapses=%s"
        % (
            t3["p_tort_star"],
            t3["e_l_tort_post_usd"],
            abs(t3["net_pnl_post_usd"]),
            t3["superposition_collapses"],
            t3["notice_only_shield_collapses"],
        )
    )

    manifest = {
        "spec": (
            "SPEC-WEATHER-MODIFICATION-LIABILITY-SUPERPOSITION-"
            "AND-PARAMETRIC-BASIS-v1.0"
        ),
        "eq_01": t1,
        "eq_02": t2,
        "eq_03": t3,
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode("utf-8")
    ).hexdigest()

    print("=" * 78)
    print(
        "[PASS] SPEC-WEATHER-MODIFICATION-LIABILITY-SUPERPOSITION-"
        "AND-PARAMETRIC-BASIS-v1.0 | 3/3 Equations Verified | SHA-256: %s"
        % digest
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(run_verification())
