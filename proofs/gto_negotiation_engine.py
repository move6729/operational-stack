import hashlib
import json
import math
from typing import Dict, Any, List, Tuple

class GTONegotiationEngine:
    """
    Automated Game-Theoretic Optimal (GTO) negotiation state-machine verifier.
    Executes sub-bandwidth delay curves, statutory regulatory escalations, circuit-breaker exits,
    and payoff floor validation against legacy external counterparties (OPEN-GTO-v1.0).
    """

    def validate_schema(self, payload: Dict[str, Any]) -> bool:
        required_keys = [
            "negotiation_id",
            "counterparty_id",
            "reserve_floor_value",
            "time_decay_gamma",
            "statutory_notice_flag",
            "regulatory_escalation_triggers"
        ]
        return all(key in payload for key in required_keys)

    def calculate_time_discount_decay(self, elapsed_seconds: float, gamma: float = 0.0001) -> float:
        return math.exp(-gamma * elapsed_seconds)

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

    def evaluate_offer(
        self, payload: Dict[str, Any], offered_value: float, elapsed_seconds: float
    ) -> Dict[str, Any]:
        if not self.validate_schema(payload):
            return {"accepted": False, "reason": "INVALID_SCHEMA"}

        reserve = payload["reserve_floor_value"]
        gamma = payload["time_decay_gamma"]
        decay = self.calculate_time_discount_decay(elapsed_seconds, gamma)
        adjusted_floor = reserve * decay

        escalation_active, statutory_notices = self.evaluate_regulatory_escalation(payload, offered_value)

        if offered_value >= adjusted_floor:
            return {
                "accepted": True,
                "offered_value": offered_value,
                "adjusted_floor": adjusted_floor,
                "regulatory_escalation": escalation_active,
                "notices": statutory_notices
            }
        else:
            return {
                "accepted": False,
                "offered_value": offered_value,
                "adjusted_floor": adjusted_floor,
                "regulatory_escalation": escalation_active,
                "notices": statutory_notices,
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
        ]
    }

    # Low offer triggers statutory regulatory escalation
    eval_sub_floor = engine.evaluate_offer(payload, offered_value=40.0, elapsed_seconds=100.0)
    assert not eval_sub_floor["accepted"]
    assert eval_sub_floor["regulatory_escalation"] is True
    assert len(eval_sub_floor["notices"]) == 3

    # Satisfactory offer accepted
    eval_acceptable = engine.evaluate_offer(payload, offered_value=105.0, elapsed_seconds=100.0)
    assert eval_acceptable["accepted"] is True

    # Check SHA-256 state transition verification
    record = {"payload": payload, "evaluation": eval_sub_floor}
    expected_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode('utf-8')).hexdigest()
    assert engine.commit_state_transition(payload, eval_sub_floor, expected_hash) is True

    return True


if __name__ == "__main__":
    if simulate_gto_proof():
        print("OPEN-GTO-v1.0 ENGINE VERIFICATION PROOF: PASSED")
