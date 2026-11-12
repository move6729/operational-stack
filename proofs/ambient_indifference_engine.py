import hashlib
import json
import time
import os
from typing import Dict, Any, List, Optional


class AmbientIndifferenceEngine:
    """
    Bare-Metal Sovereign Biological Entropy & Ambient Indifference Proxy (AMBIENT-INDIFFERENCE-v1.0).
    Implements OPSTACK-KERNEL-v2.1 Invariants 24-27.
    Resolves option sets during operator utility indifference via local hardware entropy,
    neutralizing predictive behavioral profiling without compromising human agency.
    """

    def __init__(self, config: Dict[str, Any]):
        self.jurisdiction_context = config.get("jurisdiction_context", "US")
        self.cfaa_compliant = config.get("cfaa_compliance_attestation", False)
        if not self.cfaa_compliant:
            raise ValueError("CFAA compliance attestation required (18 U.S.C. § 1030).")

        self.utility_epsilon = config.get("utility_epsilon_threshold", 0.02)
        self.entropy_source = config.get("entropy_source", "CHAOTIC_COUNTER_FALLBACK")
        self.latency_threshold_ms = config.get("fallback_input_latency_threshold_ms", 1200)
        self.high_impact_override = config.get("high_impact_domain_override", False)

        if self.high_impact_override:
            self.utility_epsilon = 0.0

    def get_hardware_entropy_byte(self) -> int:
        """
        Harvests 1 byte of local hardware entropy without cloud dependencies.
        Uses /dev/urandom or high-resolution CPU timing jitter as chaotic fallback.
        """
        try:
            return os.urandom(1)[0]
        except Exception:
            jitter = time.perf_counter_ns() ^ (time.time_ns() & 0xFFFF)
            return jitter % 256

    def evaluate_option_set(
        self,
        options: List[Dict[str, Any]],
        utility_scores: List[float],
        input_latency_ms: Optional[int] = None,
        is_high_impact: bool = False,
    ) -> Dict[str, Any]:
        """
        Evaluates option sets. If utility delta <= epsilon, injects local hardware entropy to select
        the execution path, rendering external profiling loss-functions divergent.
        """
        if len(options) != len(utility_scores) or len(options) < 1:
            return {"status": "ERROR", "selected_index": -1, "reason": "Invalid option matrix"}

        if is_high_impact or self.high_impact_override:
            return {
                "status": "OPERATOR_ESCROW_REQUIRED",
                "selected_index": -1,
                "reason": "High-impact domain bounds hard-lock epsilon to 0.0. Operator choice required.",
                "entropy_injected": False,
            }

        sorted_scores = sorted(utility_scores, reverse=True)
        utility_delta = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else 1.0

        hesitation_detected = (
            input_latency_ms is not None and input_latency_ms >= self.latency_threshold_ms
        )

        indifference_triggered = (utility_delta <= self.utility_epsilon) or hesitation_detected

        if indifference_triggered and len(options) > 1:
            raw_entropy = self.get_hardware_entropy_byte()
            top_candidates = [
                i
                for i, score in enumerate(utility_scores)
                if (sorted_scores[0] - score) <= self.utility_epsilon
            ]
            if not top_candidates:
                top_candidates = list(range(len(options)))

            selected_idx = top_candidates[raw_entropy % len(top_candidates)]
            return {
                "status": "ENTROPY_RESOLVED",
                "selected_index": selected_idx,
                "selected_option": options[selected_idx],
                "utility_delta": utility_delta,
                "entropy_injected": True,
                "entropy_val": raw_entropy,
            }

        max_idx = utility_scores.index(max(utility_scores))
        return {
            "status": "DETERMINISTIC_SELECTION",
            "selected_index": max_idx,
            "selected_option": options[max_idx],
            "utility_delta": utility_delta,
            "entropy_injected": False,
        }

    def commit_state_transition(
        self, event_id: str, execution_payload: Dict[str, Any], expected_hash: str
    ) -> bool:
        """
        Cryptographically commits state transition via SHA-256 validation.
        """
        payload_bytes = json.dumps(execution_payload, sort_keys=True).encode("utf-8")
        computed_hash = hashlib.sha256(payload_bytes).hexdigest()
        return computed_hash == expected_hash


def run_ambient_indifference_proof() -> bool:
    """
    Executable standalone proof function verifying the Biological Entropy Engine.
    """
    config = {
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "utility_epsilon_threshold": 0.02,
        "entropy_source": "CHAOTIC_COUNTER_FALLBACK",
        "fallback_input_latency_threshold_ms": 1200,
        "high_impact_domain_override": False,
    }

    engine = AmbientIndifferenceEngine(config)

    options = [
        {"route_id": "route_alpha", "cost_watts": 12.5},
        {"route_id": "route_beta", "cost_watts": 12.6},
    ]
    scores = [0.95, 0.94]

    res = engine.evaluate_option_set(options, scores, input_latency_ms=1500)
    assert res["status"] == "ENTROPY_RESOLVED"
    assert res["entropy_injected"] is True

    high_impact_options = [
        {"action": "TRANSFER_CAPITAL", "amount": 10000},
        {"action": "HOLD_CAPITAL", "amount": 10000},
    ]
    high_impact_scores = [0.99, 0.99]
    res_hi = engine.evaluate_option_set(
        high_impact_options, high_impact_scores, is_high_impact=True
    )
    assert res_hi["status"] == "OPERATOR_ESCROW_REQUIRED"
    assert res_hi["entropy_injected"] is False

    payload = {"event": "INFERENCE_COMPLETED", "selected_route": "route_alpha"}
    payload_str = json.dumps(payload, sort_keys=True)
    target_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

    assert engine.commit_state_transition("evt_001", payload, target_hash) is True
    assert engine.commit_state_transition("evt_001", payload, "invalid_hash") is False

    return True


if __name__ == "__main__":
    success = run_ambient_indifference_proof()
    print(f"AMBIENT_INDIFFERENCE_ENGINE_PROOF: {'PASSED' if success else 'FAILED'}")
    assert success
