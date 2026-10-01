import hashlib
import json
import math
from typing import Dict, Any, List, Tuple

class GTONegotiationEngine:
    """
    Automated Game-Theoretic Optimal (GTO) negotiation state-machine verifier.
    Executes sub-bandwidth delay curves, statutory regulatory escalations, circuit-breaker exits,
    payoff floor validation, trembling-hand noise filtering, grim-trigger lockouts, peer settlement
    transparency, and collective subrogation/litigation aggregation against legacy external counterparties (OPEN-GTO-v1.0).
    """

    def validate_schema(self, payload: Dict[str, Any]) -> bool:
        required_keys = [
            "negotiation_id",
            "counterparty_id",
            "reserve_floor_value",
            "time_decay_gamma",
            "statutory_notice_flag",
            "regulatory_escalation_triggers",
            "trembling_hand_epsilon",
            "grim_trigger_active",
            "separating_signal_proof",
            "shared_peer_settlements",
            "collective_subrogation_claims"
        ]
        return all(key in payload for key in required_keys)

    def calculate_time_discount_decay(self, elapsed_seconds: float, gamma: float = 0.0001) -> float:
        return math.exp(-gamma * elapsed_seconds)

    def evaluate_shared_peer_reserve_floor(self, base_reserve: float, shared_peer_settlements: List[float]) -> float:
        """
        Informs local reserve floor using peer settlement transparency graphs.
        Inverts information asymmetry by anchoring reserve floors to the max/high-percentile peer outcome.
        """
        if not shared_peer_settlements:
            return base_reserve
        peer_max = max(shared_peer_settlements)
        return max(base_reserve, peer_max)

    def evaluate_regulatory_escalation(self, payload: Dict[str, Any], offered_value: float) -> Tuple[bool, List[str]]:
        """
        Evaluates whether statutory regulatory escalation is triggered based on counterparty offer defect.
        Returns a tuple of (escalation_triggered, generated_statutory_notices).
        """
        reserve = payload.get("reserve_floor_value", 0.0)
        triggers = payload.get("regulatory_escalation_triggers", [])
        statutory_flag = payload.get("statutory_notice_flag", False)

        if offered_value < reserve and statutory_flag and triggers:
            notices = [
                f"STATUTORY ESCALATION: Offer {offered_value} below reserve threshold {reserve}. Invoking trigger [{trigger}]."
                for trigger in triggers
            ]
            return True, notices
        return False, []

    def evaluate_collective_subrogation(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Evaluates whether pooled peer dispute marks trigger a collective subrogation/litigation claim.
        """
        claims = payload.get("collective_subrogation_claims", [])
        if len(claims) >= 3:
            aggregated_hash = hashlib.sha256(json.dumps(claims, sort_keys=True).encode('utf-8')).hexdigest()
            return True, f"COLLECTIVE_SUBROGATION_TRIGGERED: {len(claims)} proof marks pooled. Class-Action Claim Hash: {aggregated_hash}"
        return False, "INSUFFICIENT_SUBROGATION_QUORUM"

    def evaluate_offer(
        self, payload: Dict[str, Any], offered_value: float, elapsed_seconds: float
    ) -> Dict[str, Any]:
        if not self.validate_schema(payload):
            return {"accepted": False, "reason": "INVALID_SCHEMA"}

        # Grim-Trigger lock check: zero-egress state transition if counterparty previously defaulted
        if payload.get("grim_trigger_active", False):
            return {
                "accepted": False,
                "reason": "GRIM_TRIGGER_LOCKED",
                "action": "PERMANENT_COUNTERPARTY_BLACKOUT"
            }

        base_reserve = payload["reserve_floor_value"]
        gamma = payload["time_decay_gamma"]
        epsilon = payload.get("trembling_hand_epsilon", 0.0)
        shared_settlements = payload.get("shared_peer_settlements", [])

        # Dynamic reserve calculation taking into account peer transparency
        effective_base = self.evaluate_shared_peer_reserve_floor(base_reserve, shared_settlements)
        decay = self.calculate_time_discount_decay(elapsed_seconds, gamma)
        
        # Trembling-hand noise filtering: floor adjustment bound under noise epsilon
        adjusted_floor = (effective_base * decay) * (1.0 - epsilon)

        escalation_active, statutory_notices = self.evaluate_regulatory_escalation(payload, offered_value)
        subrogation_triggered, subrogation_notice = self.evaluate_collective_subrogation(payload)

        if offered_value >= adjusted_floor:
            return {
                "accepted": True,
                "offered_value": offered_value,
                "adjusted_floor": adjusted_floor,
                "regulatory_escalation": escalation_active,
                "notices": statutory_notices,
                "subrogation_triggered": subrogation_triggered,
                "subrogation_notice": subrogation_notice
            }
        else:
            return {
                "accepted": False,
                "offered_value": offered_value,
                "adjusted_floor": adjusted_floor,
                "regulatory_escalation": escalation_active,
                "notices": statutory_notices,
                "subrogation_triggered": subrogation_triggered,
                "subrogation_notice": subrogation_notice,
                "action": "GO_DARK_OR_REGULATORY_FILING"
            }

    def commit_state_transition(
        self, payload: Dict[str, Any], evaluation: Dict[str, Any], expected_hash: str
    ) -> bool:
        record = {
            "payload": payload,
            "evaluation": evaluation
        }
        serialized = json.dumps(record, sort_keys=True)
        computed_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        return computed_hash == expected_hash


def simulate_gto_proof() -> bool:
    engine = GTONegotiationEngine()
    payload = {
        "negotiation_id": "GTO-2026-0001",
        "counterparty_id": "LEGACY-SAAS-RENTIER",
        "reserve_floor_value": 100.0,
        "time_decay_gamma": 0.00005,
        "statutory_notice_flag": True,
        "regulatory_escalation_triggers": [
            "CFPB_UNFAIR_DECEPTIVE_PRACTICES",
            "FTC_SECTION_5_NOTICE",
            "STATE_AG_CONSUMER_PROTECTION"
        ],
        "trembling_hand_epsilon": 0.02,
        "grim_trigger_active": False,
        "separating_signal_proof": "0xDKIM_AGE_PROOF_60_DAYS",
        "shared_peer_settlements": [105.0, 110.0, 108.0],
        "collective_subrogation_claims": [
            "STATUTORY_VIOLATION_NODE_01",
            "STATUTORY_VIOLATION_NODE_02",
            "STATUTORY_VIOLATION_NODE_03"
        ]
    }

    # Low offer triggers statutory regulatory escalation and collective subrogation
    eval_sub_floor = engine.evaluate_offer(payload, offered_value=40.0, elapsed_seconds=100.0)
    assert not eval_sub_floor["accepted"]
    assert eval_sub_floor["regulatory_escalation"] is True
    assert len(eval_sub_floor["notices"]) == 3
    assert eval_sub_floor["subrogation_triggered"] is True

    # Satisfactory offer accepted with dynamic peer-informed reserve floor
    eval_acceptable = engine.evaluate_offer(payload, offered_value=112.0, elapsed_seconds=100.0)
    assert eval_acceptable["accepted"] is True

    # Grim-Trigger lock verification
    payload_grim = dict(payload)
    payload_grim["grim_trigger_active"] = True
    eval_grim = engine.evaluate_offer(payload_grim, offered_value=200.0, elapsed_seconds=0.0)
    assert eval_grim["accepted"] is False
    assert eval_grim["reason"] == "GRIM_TRIGGER_LOCKED"

    # Check SHA-256 state transition verification
    record = {"payload": payload, "evaluation": eval_sub_floor}
    expected_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode('utf-8')).hexdigest()
    assert engine.commit_state_transition(payload, eval_sub_floor, expected_hash) is True

    return True


if __name__ == "__main__":
    if simulate_gto_proof():
        print("OPEN-GTO-v1.0 ENGINE VERIFICATION PROOF: PASSED")
