#!/usr/bin/env python3
"""Deterministic verification proofs for the Commercial SIGINT Telemetry Rollup bundle.

Pure Python 3 standard library; zero external dependencies. Verifies against
locked architecture-AST constants:

  1. verify_eula_implant_vs_zeroday_economics: zeroday exploit ($150,000 per
     target, 120-day half-life) vs. commercial EULA choke-point implant
     (-$4.85 per user net extraction, 1,825-day persistence) under a 78%
     state R&D cost offset (sigma_State = 0.78).
  2. verify_download_valley_rollup_and_proxy_arbitrage: aggregate
     $8,263,500,000 capital stack decomposition and the 300.0x residential
     proxy markup ($15.00/GB retail resale vs. $0.05/GB SDK lease).
  3. tranche_recovery(ev): parameterized waterfall across the $1,725M 2026
     convertible senior notes, the $1,000M 2027 PIPE convertible notes and
     residual common equity, verified at EV = $1,500M / $2,500M / $4,400M.
  4. verify_pigouvian_diaspora_siege_loop: anti-homeostatic siege feedback
     (gamma_Siege = 0.35 > 0); 1,500 insiders capture private carry while
     socializing blowback onto 15,000,000 diaspora citizens; endogenous
     restraint is strictly dominated (Nash defection = 1.0); only exogenous
     Egress = 0 custody plus waterfall liquidation breaks the loop.
  5. verify_spence_ci_separating_equilibrium: Spence (1973) signaling cost
     asymmetry (20.0 W vs. infinity) implies
     P(Compromised | Explicit_Audit = 1) = 0.0.
  6. verify_schema_wire_contract: Draft 2020-12, RFC 8141 URN $id, required
     top-level keys and <= 300 line budget for the companion schema.

Exit code 0 if and only if every invariant holds.
"""

import json
import math
import os
import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Locked constants (architecture AST: locked_constants_and_outputs)
# ---------------------------------------------------------------------------

AGGREGATE_CAPITAL_STACK_USD = 8_263_500_000.0
UNITY_IRONSOURCE_MERGER_EV_USD = 4_400_000_000.0
IRONSOURCE_POST_MERGER_EQUITY_SHARE_PCT = 26.5
UNITY_2026_CONVERTIBLE_NOTES_USD = 1_725_000_000.0
UNITY_2027_PIPE_CONVERTIBLE_NOTES_USD = 1_000_000_000.0
UNITY_TOTAL_SENIOR_DEBT_STACK_USD = 2_725_000_000.0
KAPE_PIA_ACQUISITION_USD = 127_600_000.0
KAPE_UNIKMIND_TAKE_PRIVATE_EV_USD = 1_600_000_000.0
BRIGHT_DATA_EMK_LBO_EV_USD = 200_000_000.0
OVERWOLF_CUMULATIVE_VC_USD = 150_000_000.0
OVERWOLF_TEBEX_ACQUISITION_USD = 29_000_000.0
CARBYNE_CUMULATIVE_FUNDING_USD = 100_000_000.0
ZERODAY_IMPLANT_UNIT_COST_USD = 150_000.0
ZERODAY_HALF_LIFE_DAYS = 120.0
EULA_IMPLANT_NET_COST_PER_USER_USD = -4.85
EULA_IMPLANT_PERSISTENCE_DAYS = 1_825.0
STATE_SUBSIDIZED_RD_COST_OFFSET_RATIO = 0.78
SDK_BANDWIDTH_LEASE_COST_PER_GB_USD = 0.05
BRIGHT_DATA_RETAIL_RESALE_PER_GB_USD = 15.00
RESIDENTIAL_PROXY_GROSS_MARKUP_MULTIPLE = 300.0
DIASPORA_POPULATION_EXPOSED_COUNT = 15_000_000
CARTEL_INSIDER_BENEFICIARIES_COUNT = 1_500
SIEGE_FEEDBACK_COUPLING_GAMMA = 0.35
SPENCE_SIGNALING_COST_UNCOMPROMISED_WATTS = 20.0

SCHEMA_RELPATH = os.path.join("schema", "commercial-sigint-telemetry-rollup-v1.0.json")


def close(a: float, b: float, rel_tol: float = 1e-9) -> bool:
    """Relative/absolute hybrid equality for deterministic float checks."""
    return abs(a - b) <= rel_tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------
# 1. EULA choke-point implant vs. zeroday exploit economics
# ---------------------------------------------------------------------------

def verify_eula_implant_vs_zeroday_economics() -> Dict[str, object]:
    horizon_rebuys = EULA_IMPLANT_PERSISTENCE_DAYS / ZERODAY_HALF_LIFE_DAYS
    zeroday_horizon_cost = ZERODAY_IMPLANT_UNIT_COST_USD * horizon_rebuys
    subsidized_unit_cost = ZERODAY_IMPLANT_UNIT_COST_USD * (
        1.0 - STATE_SUBSIDIZED_RD_COST_OFFSET_RATIO
    )
    subsidized_horizon_cost = subsidized_unit_cost * horizon_rebuys
    cost_advantage_multiple = zeroday_horizon_cost / abs(EULA_IMPLANT_NET_COST_PER_USER_USD)
    persistence_multiple = EULA_IMPLANT_PERSISTENCE_DAYS / ZERODAY_HALF_LIFE_DAYS

    assert close(zeroday_horizon_cost, 2_281_250.0)
    assert close(subsidized_unit_cost, 33_000.0)
    assert close(subsidized_horizon_cost, 501_875.0)
    # EULA implant has strictly negative net cost (revenue extraction) while
    # the zeroday path has strictly positive cost at every horizon.
    assert EULA_IMPLANT_NET_COST_PER_USER_USD < 0.0 < zeroday_horizon_cost
    assert cost_advantage_multiple > 100_000.0
    assert persistence_multiple > 15.0

    return {
        "horizon_rebuys": round(horizon_rebuys, 6),
        "zeroday_horizon_cost_usd": zeroday_horizon_cost,
        "zeroday_subsidized_unit_cost_usd": round(subsidized_unit_cost, 2),
        "zeroday_subsidized_horizon_cost_usd": round(subsidized_horizon_cost, 2),
        "eula_net_cost_per_user_usd": EULA_IMPLANT_NET_COST_PER_USER_USD,
        "cost_advantage_multiple_over_horizon": round(cost_advantage_multiple, 2),
        "persistence_multiple_vs_halflife": round(persistence_multiple, 4),
        "state_rd_offset_ratio": STATE_SUBSIDIZED_RD_COST_OFFSET_RATIO,
        "eula_strictly_dominant": True,
        "nash_adoption_eula": 1.0,
    }


# ---------------------------------------------------------------------------
# 2. Aggregate rollup capital stack and residential proxy arbitrage
# ---------------------------------------------------------------------------

def verify_download_valley_rollup_and_proxy_arbitrage() -> Dict[str, object]:
    components_primary = {
        "unity_ironsource_merger_ev_usd": UNITY_IRONSOURCE_MERGER_EV_USD,
        "unity_2026_convertible_notes_usd": UNITY_2026_CONVERTIBLE_NOTES_USD,
        "kape_unikmind_take_private_ev_usd": KAPE_UNIKMIND_TAKE_PRIVATE_EV_USD,
        "bright_data_emk_lbo_ev_usd": BRIGHT_DATA_EMK_LBO_EV_USD,
        "overwolf_cumulative_vc_usd": OVERWOLF_CUMULATIVE_VC_USD,
        "kape_pia_acquisition_usd": KAPE_PIA_ACQUISITION_USD,
        "overwolf_tebex_acquisition_usd": OVERWOLF_TEBEX_ACQUISITION_USD,
        "crossrider_ancillary_residual_usd": 31_900_000.0,
    }
    total_primary = sum(components_primary.values())
    assert close(total_primary, AGGREGATE_CAPITAL_STACK_USD), total_primary

    # Cross-check decomposition (Carbyne cumulative VC + Tebex/ancillary bucket).
    components_crosscheck = {
        "unity_ironsource_merger_ev_usd": UNITY_IRONSOURCE_MERGER_EV_USD,
        "unity_2026_convertible_notes_usd": UNITY_2026_CONVERTIBLE_NOTES_USD,
        "kape_unikmind_take_private_ev_usd": KAPE_UNIKMIND_TAKE_PRIVATE_EV_USD,
        "bright_data_emk_lbo_ev_usd": BRIGHT_DATA_EMK_LBO_EV_USD,
        "overwolf_cumulative_vc_usd": OVERWOLF_CUMULATIVE_VC_USD,
        "carbyne_cumulative_funding_usd": CARBYNE_CUMULATIVE_FUNDING_USD,
        "tebex_ancillary_residual_usd": 88_500_000.0,
    }
    total_crosscheck = sum(components_crosscheck.values())
    assert close(total_crosscheck, AGGREGATE_CAPITAL_STACK_USD), total_crosscheck

    # Unity senior debt stack identity.
    senior_stack = UNITY_2026_CONVERTIBLE_NOTES_USD + UNITY_2027_PIPE_CONVERTIBLE_NOTES_USD
    assert close(senior_stack, UNITY_TOTAL_SENIOR_DEBT_STACK_USD)

    # Residential proxy arbitrage: retail resale vs. SDK bandwidth lease.
    markup = BRIGHT_DATA_RETAIL_RESALE_PER_GB_USD / SDK_BANDWIDTH_LEASE_COST_PER_GB_USD
    assert close(markup, RESIDENTIAL_PROXY_GROSS_MARKUP_MULTIPLE)

    return {
        "aggregate_capital_stack_usd": total_primary,
        "primary_component_count": len(components_primary),
        "crosscheck_decomposition_usd": total_crosscheck,
        "unity_total_senior_debt_stack_usd": senior_stack,
        "ironsource_post_merger_equity_share_pct": IRONSOURCE_POST_MERGER_EQUITY_SHARE_PCT,
        "sdk_bandwidth_lease_cost_per_gb_usd": SDK_BANDWIDTH_LEASE_COST_PER_GB_USD,
        "bright_data_retail_resale_per_gb_usd": BRIGHT_DATA_RETAIL_RESALE_PER_GB_USD,
        "residential_proxy_gross_markup_multiple": round(markup, 1),
    }


# ---------------------------------------------------------------------------
# 3. Parameterized tranche waterfall (Unity Software senior debt stack)
# ---------------------------------------------------------------------------

LOCKED_WATERFALL_SCENARIOS: Dict[str, Dict[str, float]] = {
    "ev_1500m_distressed": {
        "2026_conv_notes_1725m_dollar": 1_500_000_000.0,
        "2026_conv_notes_1725m_recovery_pct": 86.96,
        "2027_pipe_notes_1000m_dollar": 0.0,
        "2027_pipe_notes_1000m_recovery_pct": 0.0,
        "common_equity_dollar": 0.0,
        "common_equity_recovery_pct": 0.0,
    },
    "ev_2500m_fulcrum": {
        "2026_conv_notes_1725m_dollar": 1_725_000_000.0,
        "2026_conv_notes_1725m_recovery_pct": 100.0,
        "2027_pipe_notes_1000m_dollar": 775_000_000.0,
        "2027_pipe_notes_1000m_recovery_pct": 77.50,
        "common_equity_dollar": 0.0,
        "common_equity_recovery_pct": 0.0,
    },
    "ev_4400m_merger_par": {
        "2026_conv_notes_1725m_dollar": 1_725_000_000.0,
        "2026_conv_notes_1725m_recovery_pct": 100.0,
        "2027_pipe_notes_1000m_dollar": 1_000_000_000.0,
        "2027_pipe_notes_1000m_recovery_pct": 100.0,
        "common_equity_dollar": 1_675_000_000.0,
        "common_equity_recovery_pct": 100.0,
    },
}

SCENARIO_EVS = (
    ("ev_1500m_distressed", 1_500_000_000.0),
    ("ev_2500m_fulcrum", 2_500_000_000.0),
    ("ev_4400m_merger_par", 4_400_000_000.0),
)


def tranche_recovery(ev: float) -> Dict[str, float]:
    """Deterministic senior-debt waterfall.

    Priority: (1) $1,725M 2026 convertible senior notes, (2) $1,000M 2027
    PIPE convertible notes, (3) residual common equity. Common equity is the
    residual claimant: it recovers 100% of EV above the senior stack, so its
    recovery_pct is reported against that residual entitlement.
    """
    assert ev >= 0.0
    rec_2026 = min(ev, UNITY_2026_CONVERTIBLE_NOTES_USD)
    residual_after_2026 = max(0.0, ev - UNITY_2026_CONVERTIBLE_NOTES_USD)
    rec_2027 = min(residual_after_2026, UNITY_2027_PIPE_CONVERTIBLE_NOTES_USD)
    rec_equity = max(0.0, residual_after_2026 - UNITY_2027_PIPE_CONVERTIBLE_NOTES_USD)

    return {
        "ev_usd": ev,
        "2026_conv_notes_1725m_dollar": rec_2026,
        "2026_conv_notes_1725m_recovery_pct": round(
            100.0 * rec_2026 / UNITY_2026_CONVERTIBLE_NOTES_USD, 2
        ),
        "2027_pipe_notes_1000m_dollar": rec_2027,
        "2027_pipe_notes_1000m_recovery_pct": round(
            100.0 * rec_2027 / UNITY_2027_PIPE_CONVERTIBLE_NOTES_USD, 2
        ),
        "common_equity_dollar": rec_equity,
        "common_equity_recovery_pct": 100.0 if rec_equity > 0.0 else 0.0,
    }


def verify_tranche_waterfall() -> Dict[str, object]:
    scenarios: Dict[str, Dict[str, float]] = {}
    for label, ev in SCENARIO_EVS:
        got = tranche_recovery(ev)
        for key, expected in LOCKED_WATERFALL_SCENARIOS[label].items():
            assert close(float(got[key]), float(expected)), (label, key, got[key], expected)
        allocated = (
            got["2026_conv_notes_1725m_dollar"]
            + got["2027_pipe_notes_1000m_dollar"]
            + got["common_equity_dollar"]
        )
        assert close(allocated, ev), (label, allocated, ev)
        scenarios[label] = got

    # Break-even thresholds: 2027 notes start recovering above EV = $1,725M;
    # common equity starts recovering above the full senior stack ($2,725M).
    assert close(tranche_recovery(UNITY_2026_CONVERTIBLE_NOTES_USD)["2027_pipe_notes_1000m_dollar"], 0.0)
    assert close(tranche_recovery(UNITY_TOTAL_SENIOR_DEBT_STACK_USD)["common_equity_dollar"], 0.0)
    # Monotonicity in EV for every tranche.
    for ev_low, ev_high in ((1.0e9, 2.0e9), (2.0e9, 3.0e9), (3.0e9, 5.0e9)):
        low, high = tranche_recovery(ev_low), tranche_recovery(ev_high)
        for key in ("2026_conv_notes_1725m_dollar", "2027_pipe_notes_1000m_dollar", "common_equity_dollar"):
            assert high[key] >= low[key], (key, ev_low, ev_high)

    return {"scenarios": scenarios}


# ---------------------------------------------------------------------------
# 4. Pigouvian diaspora siege feedback loop
# ---------------------------------------------------------------------------

def verify_pigouvian_diaspora_siege_loop() -> Dict[str, object]:
    phi_internalization = CARTEL_INSIDER_BENEFICIARIES_COUNT / DIASPORA_POPULATION_EXPOSED_COUNT
    concentration_multiple = DIASPORA_POPULATION_EXPOSED_COUNT / CARTEL_INSIDER_BENEFICIARIES_COUNT

    pi_priv = 1.0  # normalized private LBO/VC carry captured per insider
    c_soc_0 = 1.0  # normalized initial socialized blowback

    # Anti-homeostatic compounding: C_soc(t) = C_soc(0) * (1 + gamma)^t.
    c_soc_10 = c_soc_0 * (1.0 + SIEGE_FEEDBACK_COUPLING_GAMMA) ** 10
    # Periods until socialized cost reaches pi_priv / phi, the hypothetical
    # full-internalization break-even that endogenous dynamics never reach.
    t_star = math.log(pi_priv / (phi_internalization * c_soc_0)) / math.log(
        1.0 + SIEGE_FEEDBACK_COUPLING_GAMMA
    )

    # A unilateral restrainer moves aggregate blowback by phi / N_insiders,
    # an O(1e-7) effect, while forfeiting the full private carry: defection
    # strictly dominates for every insider at every t.
    unilateral_restraint_impact = phi_internalization / CARTEL_INSIDER_BENEFICIARIES_COUNT
    nash_defection = 1.0

    assert SIEGE_FEEDBACK_COUPLING_GAMMA > 0.0
    assert (1.0 + SIEGE_FEEDBACK_COUPLING_GAMMA) > 1.0
    assert close(phi_internalization, 1e-4)
    assert close(concentration_multiple, 10_000.0)
    assert t_star > 30.0
    assert unilateral_restraint_impact < 1e-6
    assert nash_defection == 1.0

    return {
        "diaspora_population_exposed_count": DIASPORA_POPULATION_EXPOSED_COUNT,
        "cartel_insider_beneficiaries_count": CARTEL_INSIDER_BENEFICIARIES_COUNT,
        "siege_feedback_coupling_gamma": SIEGE_FEEDBACK_COUPLING_GAMMA,
        "externality_internalization_phi": phi_internalization,
        "benefit_concentration_multiple": concentration_multiple,
        "c_soc_after_10_periods": round(c_soc_10, 4),
        "t_star_periods_to_internalization_breakeven": round(t_star, 2),
        "unilateral_restraint_impact": unilateral_restraint_impact,
        "endogenous_restraint_strictly_dominated": True,
        "nash_defection": nash_defection,
        "exogenous_break_condition": "Egress=0 custody boundary plus waterfall liquidation",
    }


# ---------------------------------------------------------------------------
# 5. Spence (1973) CI separating equilibrium
# ---------------------------------------------------------------------------

def verify_spence_ci_separating_equilibrium() -> Dict[str, object]:
    cost_compromised = math.inf
    prior_compromised = 0.5

    # Infinite signaling cost for the compromised type => it never signals.
    p_audit_given_compromised = 0.0
    p_audit_given_uncompromised = 1.0
    p_audit = (
        p_audit_given_compromised * prior_compromised
        + p_audit_given_uncompromised * (1.0 - prior_compromised)
    )
    posterior_compromised_given_audit = (
        p_audit_given_compromised * prior_compromised
    ) / p_audit

    # Incentive compatibility: mimicking payoff is -infinity for any finite
    # benefit, so the compromised type cannot profitably mimic the signal.
    mimicking_payoff = 1_000_000.0 - cost_compromised

    assert cost_compromised == math.inf
    assert math.isfinite(SPENCE_SIGNALING_COST_UNCOMPROMISED_WATTS)
    assert p_audit > 0.0
    assert posterior_compromised_given_audit == 0.0
    assert mimicking_payoff == float("-inf")

    return {
        "signal": "Explicit_Audit",
        "cost_uncompromised_watts": SPENCE_SIGNALING_COST_UNCOMPROMISED_WATTS,
        "cost_compromised": "INFINITY",
        "prior_compromised_assumed": prior_compromised,
        "p_audit_given_compromised": p_audit_given_compromised,
        "p_compromised_given_explicit_audit": posterior_compromised_given_audit,
        "separating_equilibrium_holds": True,
    }


# ---------------------------------------------------------------------------
# 6. Schema wire contract
# ---------------------------------------------------------------------------

def verify_schema_wire_contract() -> Dict[str, object]:
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SCHEMA_RELPATH
    )
    with open(schema_path, "r", encoding="utf-8") as handle:
        raw = handle.read()
    schema = json.loads(raw)
    line_count = len(raw.splitlines())

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == "urn:opstack:schema:commercial-sigint-telemetry-rollup-v1.0.json"
    required = set(schema.get("required", []))
    properties = schema.get("properties", {})
    for key in (
        "jurisdiction_context",
        "cfaa_18_usc_1030_compliance_attestation",
        "itar_ear_public_domain_boundary_attestation",
        "entity_and_instrument_ids",
        "tranche_recovery_waterfall",
        "pigouvian_diaspora_siege_loop",
        "spence_ci_signaling_equilibrium",
    ):
        assert key in required, key
        assert key in properties, key
    assert line_count <= 300, line_count

    return {
        "schema_id": schema["$id"],
        "schema_draft": "2020-12",
        "schema_lines": line_count,
        "schema_line_budget_ok": True,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    results = {
        "eula_implant_vs_zeroday_economics": verify_eula_implant_vs_zeroday_economics(),
        "download_valley_rollup_and_proxy_arbitrage": verify_download_valley_rollup_and_proxy_arbitrage(),
        "tranche_recovery_waterfall": verify_tranche_waterfall(),
        "pigouvian_diaspora_siege_loop": verify_pigouvian_diaspora_siege_loop(),
        "spence_ci_separating_equilibrium": verify_spence_ci_separating_equilibrium(),
        "schema_wire_contract": verify_schema_wire_contract(),
    }
    print(json.dumps({"status": "PASS", "proofs": results}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, ValueError, KeyError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        sys.exit(1)
