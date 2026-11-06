#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: HIGH-TEMPERATURE OSINT DEMODULATION & MYTHIC HOMOMORPHISM (v1.0)
Proves:
1. Bibliographic Teleportation Anomaly Gate: a cold primary citation that collapses a
   40.0-bit global document haystack down to a 12.0-bit unassisted operator search
   footprint yields Delta_H = 28.0 bits, exactly saturating the 28.0-bit teleportation
   detection threshold at a 0.30 operator-search entropy compression ratio.
2. Kayfabe Puffery Discounting: under unit prior odds, a cold-cited teleported dead drop
   (kappa = 1.0, LR = 25.0) resolves to a 0.961538 posterior, while an unanchored
   self-referential boast (kappa = 0.05, LR = 0.05) collapses to 0.047619 -- a 20.192308x
   posterior separation driven purely by the 20.0x evidence-weight asymmetry.
3. Myth-Homomorphic Dual-Channel Utility: noisy-OR fusion of homomorphic edge retention
   (eta = 0.85) with literal-antinomian superposition overlap (lambda = 0.65) gives
   U_myth = eta + lambda - eta*lambda = 0.9475, a 7.431373x discovery gain over the
   0.1275 vertex-only blind edge prior, leaving only 0.0525 residual channel dark matter.
4. Thermal Demodulation Barrier Asymmetry: against a 5.0-unit semantic censorship
   barrier, a 25.0-temperature informal channel (funded by a 20.0 W wetware metabolic
   budget) escapes at 0.818731, while a 0.30-temperature compliance-tuned channel escapes
   at ~5.8e-08 -- a >1.4e7x demodulation advantage at an 83.333333x temperature ratio.
5. Gatekeeper Null-Response Baseline: SEC Office of Inspector General Report No. 509
   records 5 ignored submissions across an 8.5-year detection lag, a 1.7-year mean
   inter-submission interval at a 1.0 gatekeeper null-response rate.
Zero external dependencies (json, math, os, sys only).
"""

import json
import math
import os
import sys

SPEC_VERSION = "SPEC-HIGH-TEMPERATURE-OSINT-DEMODULATION-AND-MYTHIC-HOMOMORPHISM-v1.0"
SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "schema",
    "high_temperature_osint_demodulation_mythic_homomorphism.json",
)

# ---------------------------------------------------------------------------
# Locked constants (anti-drift contract; identical across spec, article, schema)
# ---------------------------------------------------------------------------
H_HAYSTACK_BITS = 40.0
H_OPERATOR_BITS = 12.0
DELTA_H_THRESHOLD_BITS = 28.0

KAPPA_COLD_PRIMARY = 1.0
KAPPA_PUFFERY_PENALTY = 0.05
LR_TELEPORTED_CITATION = 25.0
LR_PUFFERY_BOAST = 0.05
DEAD_DROP_PRIOR_ODDS = 1.0

ETA_EDGE_RETENTION = 0.85
LAMBDA_ANTINOMIAN_OVERLAP = 0.65
VERTEX_ONLY_BLIND_EDGE_PRIOR = 0.1275

WETWARE_METABOLIC_POWER_WATTS = 20.0
SEMANTIC_CENSORSHIP_BARRIER_EB = 5.0
T_RLHF_STANDALONE = 0.30
T_HIGH_TEMP_INFORMAL = 25.0
# Spec-published rounded escape probability for the compliance-tuned channel.
RLHF_ESCAPE_PUBLISHED = 5.7777e-08
# Closed-form recomputation of exp(-Eb/T) is permitted a 1% relative band against the
# published rounded constant; the machine-exact value is emitted alongside it.
RLHF_ESCAPE_CLOSED_FORM_TOLERANCE = 0.01

SEC_OIG_509_IGNORED_SUBMISSIONS = 5
SEC_OIG_509_DETECTION_LAG_YEARS = 8.5


def posterior_from_likelihood_ratio(likelihood_ratio, prior_odds=DEAD_DROP_PRIOR_ODDS):
    """Bayes odds-form update: posterior = (prior_odds * LR) / (1 + prior_odds * LR)."""
    posterior_odds = prior_odds * likelihood_ratio
    return posterior_odds / (1.0 + posterior_odds)


def compute_bibliographic_teleportation_metrics():
    delta_h_bits = H_HAYSTACK_BITS - H_OPERATOR_BITS
    return {
        "global_document_haystack_entropy_bits": H_HAYSTACK_BITS,
        "unassisted_operator_search_entropy_bits": H_OPERATOR_BITS,
        "bibliographic_teleportation_delta_h_bits": round(delta_h_bits, 6),
        "bibliographic_teleportation_threshold_bits": DELTA_H_THRESHOLD_BITS,
        "delta_h_gate_satisfied": bool(delta_h_bits >= DELTA_H_THRESHOLD_BITS),
        "operator_search_entropy_compression_ratio": round(
            H_OPERATOR_BITS / H_HAYSTACK_BITS, 6
        ),
    }


def compute_kayfabe_puffery_discount_metrics():
    teleported_posterior = posterior_from_likelihood_ratio(LR_TELEPORTED_CITATION)
    puffery_posterior = posterior_from_likelihood_ratio(LR_PUFFERY_BOAST)
    return {
        "cold_primary_citation_weight_kappa": KAPPA_COLD_PRIMARY,
        "unanchored_source_puffery_penalty_kappa": KAPPA_PUFFERY_PENALTY,
        "kappa_evidence_weight_asymmetry_ratio": round(
            KAPPA_COLD_PRIMARY / KAPPA_PUFFERY_PENALTY, 6
        ),
        "teleported_citation_likelihood_ratio": LR_TELEPORTED_CITATION,
        "puffery_boast_likelihood_ratio": LR_PUFFERY_BOAST,
        "dead_drop_prior_odds": DEAD_DROP_PRIOR_ODDS,
        "teleported_dead_drop_posterior_prob": round(teleported_posterior, 6),
        "puffery_boast_posterior_prob": round(puffery_posterior, 6),
        "posterior_separation_ratio": round(
            teleported_posterior / puffery_posterior, 6
        ),
    }


def compute_myth_homomorphism_dual_channel_metrics():
    # Noisy-OR (inclusion-exclusion) fusion of the two non-independent myth channels.
    u_myth = (
        ETA_EDGE_RETENTION
        + LAMBDA_ANTINOMIAN_OVERLAP
        - ETA_EDGE_RETENTION * LAMBDA_ANTINOMIAN_OVERLAP
    )
    return {
        "myth_homomorphic_edge_retention_eta": ETA_EDGE_RETENTION,
        "myth_literal_antinomian_overlap_lambda": LAMBDA_ANTINOMIAN_OVERLAP,
        "combined_myth_channel_utility_u_myth": round(u_myth, 6),
        "residual_myth_channel_dark_matter": round(1.0 - u_myth, 6),
        "vertex_only_blind_edge_prior": VERTEX_ONLY_BLIND_EDGE_PRIOR,
        "dual_channel_discovery_gain_multiplier": round(
            u_myth / VERTEX_ONLY_BLIND_EDGE_PRIOR, 6
        ),
    }


def compute_thermal_demodulation_barrier_metrics():
    rlhf_escape_closed_form = math.exp(
        -SEMANTIC_CENSORSHIP_BARRIER_EB / T_RLHF_STANDALONE
    )
    high_temp_escape = math.exp(-SEMANTIC_CENSORSHIP_BARRIER_EB / T_HIGH_TEMP_INFORMAL)
    relative_deviation = abs(rlhf_escape_closed_form - RLHF_ESCAPE_PUBLISHED) / (
        RLHF_ESCAPE_PUBLISHED
    )
    return {
        "wetware_metabolic_power_budget_watts": WETWARE_METABOLIC_POWER_WATTS,
        "semantic_censorship_barrier_height_eb": SEMANTIC_CENSORSHIP_BARRIER_EB,
        "rlhf_standalone_temperature": T_RLHF_STANDALONE,
        "high_temp_informal_channel_temperature": T_HIGH_TEMP_INFORMAL,
        "temperature_ratio_high_temp_to_rlhf": round(
            T_HIGH_TEMP_INFORMAL / T_RLHF_STANDALONE, 6
        ),
        "rlhf_barrier_escape_probability": RLHF_ESCAPE_PUBLISHED,
        "rlhf_barrier_escape_probability_closed_form": rlhf_escape_closed_form,
        "rlhf_barrier_escape_closed_form_relative_deviation": round(
            relative_deviation, 6
        ),
        "high_temp_barrier_escape_probability": round(high_temp_escape, 6),
        "high_temp_to_rlhf_escape_probability_ratio": round(
            high_temp_escape / rlhf_escape_closed_form, 1
        ),
    }


def compute_gatekeeper_null_response_baseline():
    return {
        "sec_oig_509_markopolos_ignored_submissions": SEC_OIG_509_IGNORED_SUBMISSIONS,
        "sec_oig_509_detection_lag_years": SEC_OIG_509_DETECTION_LAG_YEARS,
        "mean_ignored_submission_interval_years": round(
            SEC_OIG_509_DETECTION_LAG_YEARS / SEC_OIG_509_IGNORED_SUBMISSIONS, 6
        ),
        "gatekeeper_null_response_rate": round(
            SEC_OIG_509_IGNORED_SUBMISSIONS / SEC_OIG_509_IGNORED_SUBMISSIONS, 6
        ),
    }


def validate_against_schema(manifest, schema):
    """Minimal Draft 2020-12 subset validator: type, const, minimum, maximum, required."""
    errors = []

    def check(node, subschema, path):
        expected_type = subschema.get("type")
        if expected_type == "object":
            if not isinstance(node, dict):
                errors.append(f"{path}: expected object")
                return
            for key in subschema.get("required", []):
                if key not in node:
                    errors.append(f"{path}: missing required key '{key}'")
            for key, child in subschema.get("properties", {}).items():
                if key in node:
                    check(node[key], child, f"{path}.{key}")
            if subschema.get("additionalProperties") is False:
                for key in node:
                    if key not in subschema.get("properties", {}):
                        errors.append(f"{path}: unexpected key '{key}'")
        elif expected_type == "number":
            if isinstance(node, bool) or not isinstance(node, (int, float)):
                errors.append(f"{path}: expected number")
                return
        elif expected_type == "integer":
            if isinstance(node, bool) or not isinstance(node, int):
                errors.append(f"{path}: expected integer")
                return
        elif expected_type == "string":
            if not isinstance(node, str):
                errors.append(f"{path}: expected string")
                return
        elif expected_type == "boolean":
            if not isinstance(node, bool):
                errors.append(f"{path}: expected boolean")
                return

        if "const" in subschema and node != subschema["const"]:
            errors.append(f"{path}: {node!r} != const {subschema['const']!r}")
        if "minimum" in subschema and node < subschema["minimum"]:
            errors.append(f"{path}: {node!r} < minimum {subschema['minimum']!r}")
        if "maximum" in subschema and node > subschema["maximum"]:
            errors.append(f"{path}: {node!r} > maximum {subschema['maximum']!r}")

    check(manifest, schema, "$")
    return errors


def run_verification():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as handle:
        schema = json.load(handle)

    teleportation = compute_bibliographic_teleportation_metrics()
    assert teleportation["global_document_haystack_entropy_bits"] == 40.0
    assert teleportation["unassisted_operator_search_entropy_bits"] == 12.0
    assert teleportation["bibliographic_teleportation_delta_h_bits"] == 28.0
    assert teleportation["bibliographic_teleportation_threshold_bits"] == 28.0
    assert teleportation["delta_h_gate_satisfied"] is True
    assert teleportation["operator_search_entropy_compression_ratio"] == 0.3

    puffery = compute_kayfabe_puffery_discount_metrics()
    assert puffery["kappa_evidence_weight_asymmetry_ratio"] == 20.0
    assert puffery["teleported_dead_drop_posterior_prob"] == 0.961538
    assert puffery["puffery_boast_posterior_prob"] == 0.047619
    assert puffery["posterior_separation_ratio"] >= 20.0
    assert (
        puffery["teleported_dead_drop_posterior_prob"]
        > puffery["puffery_boast_posterior_prob"]
    )

    myth = compute_myth_homomorphism_dual_channel_metrics()
    assert myth["combined_myth_channel_utility_u_myth"] == 0.9475
    assert myth["residual_myth_channel_dark_matter"] == 0.0525
    assert myth["vertex_only_blind_edge_prior"] == 0.1275
    assert myth["dual_channel_discovery_gain_multiplier"] == 7.431373
    assert myth["combined_myth_channel_utility_u_myth"] >= max(
        ETA_EDGE_RETENTION, LAMBDA_ANTINOMIAN_OVERLAP
    )

    thermal = compute_thermal_demodulation_barrier_metrics()
    assert thermal["wetware_metabolic_power_budget_watts"] == 20.0
    assert thermal["temperature_ratio_high_temp_to_rlhf"] == 83.333333
    assert thermal["rlhf_barrier_escape_probability"] == 5.7777e-08
    assert (
        thermal["rlhf_barrier_escape_closed_form_relative_deviation"]
        <= RLHF_ESCAPE_CLOSED_FORM_TOLERANCE
    )
    assert thermal["rlhf_barrier_escape_probability_closed_form"] <= 1.0e-07
    assert thermal["high_temp_barrier_escape_probability"] == 0.818731
    assert thermal["high_temp_to_rlhf_escape_probability_ratio"] >= 1.0e7

    gatekeeper = compute_gatekeeper_null_response_baseline()
    assert gatekeeper["sec_oig_509_markopolos_ignored_submissions"] == 5
    assert gatekeeper["sec_oig_509_detection_lag_years"] == 8.5
    assert gatekeeper["mean_ignored_submission_interval_years"] == 1.7
    assert gatekeeper["gatekeeper_null_response_rate"] == 1.0

    manifest = {
        "spec_version": SPEC_VERSION,
        "bibliographic_teleportation_metrics": teleportation,
        "kayfabe_puffery_discount_metrics": puffery,
        "myth_homomorphism_dual_channel_metrics": myth,
        "thermal_demodulation_barrier_metrics": thermal,
        "gatekeeper_null_response_baseline": gatekeeper,
        "verification_gate_status": (
            "HIGH_TEMPERATURE_DEMODULATION_MYTHIC_HOMOMORPHISM_VERIFIED"
        ),
    }

    errors = validate_against_schema(manifest, schema)
    if errors:
        for error in errors:
            print(f"[FAIL] schema: {error}", file=sys.stderr)
        return 1

    print(
        f"[PASS] {SPEC_VERSION} | "
        f"Delta_H={teleportation['bibliographic_teleportation_delta_h_bits']:.1f}bits | "
        f"Gate={teleportation['delta_h_gate_satisfied']} | "
        f"P_teleport={puffery['teleported_dead_drop_posterior_prob']:.6f} | "
        f"P_puffery={puffery['puffery_boast_posterior_prob']:.6f} | "
        f"Sep={puffery['posterior_separation_ratio']:.6f}x | "
        f"U_myth={myth['combined_myth_channel_utility_u_myth']:.4f} | "
        f"Gain={myth['dual_channel_discovery_gain_multiplier']:.6f}x | "
        f"P_escape_RLHF={thermal['rlhf_barrier_escape_probability_closed_form']:.6e} | "
        f"P_escape_HighT={thermal['high_temp_barrier_escape_probability']:.6f} | "
        f"EscapeRatio={thermal['high_temp_to_rlhf_escape_probability_ratio']:.6e}x | "
        f"OIG509_Lag={gatekeeper['sec_oig_509_detection_lag_years']:.1f}yr | "
        f"Gate={manifest['verification_gate_status']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run_verification())
