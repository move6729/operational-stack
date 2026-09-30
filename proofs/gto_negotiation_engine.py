#!/usr/bin/env python3
"""
Bare-Metal Sovereign GTO External Negotiation Engine (OPEN-GTO-v1.0).
Provides zero-rent, game-theoretic optimal state-machine evaluation for 
federation-external interactions, insulating local nodes from psychological friction,
urgency exploitation, and rent-seeking counterparty tactics.

License: Unlicense (Public Domain - Zero-Rent Federation)
"""

import json
import sys
import hashlib
import time
from typing import Dict, Any, Tuple


class GTONegotiationEngine:
    """
    Automated Game-Theoretic Optimal (GTO) negotiation state-machine verifier.
    Executes sub-bandwidth delay curves, circuit-breaker exits, and payoff floor validation
    against legacy external counterparties.
    """

    ALLOWED_COUNTERPARTIES = {"EXTERNAL_SAAS", "CORPORATE_BUYER", "LANDLORD", "INTERMEDIARY"}
    ALLOWED_STATUSES = {"INITIATED", "ASYNC_PAUSE", "TACTICAL_EXIT", "EQUILIBRIUM_SETTLED"}

    def __init__(self):
        pass

    def validate_schema(self, payload: Dict[str, Any]) -> bool:
        """
        Validates payload structure against schema/gto_negotiation.json requirements.
        """
        required_keys = {
            "session_id",
            "counterparty_type",
            "tactical_primitives",
            "asymmetric_leverage_invariant",
            "state_machine_status",
            "payoff_matrix_hash",
        }
        if not required_keys.issubset(payload.keys()):
            return False

        if payload.get("counterparty_type") not in self.ALLOWED_COUNTERPARTIES:
            return False

        if payload.get("state_machine_status") not in self.ALLOWED_STATUSES:
            return False

        if payload.get("asymmetric_leverage_invariant") is not True:
            return False

        primitives = payload.get("tactical_primitives", {})
        prim_keys = {
            "go_dark_timeout_seconds",
            "tactical_exit_threshold",
            "anchoring_payoff_floor",
            "step_delay_multiplier",
        }
        if not prim_keys.issubset(primitives.keys()):
            return False

        hash_val = payload.get("payoff_matrix_hash", "")
        if len(hash_val) != 64 or not all(c in "0123456789abcdefABCDEF" for c in hash_val):
            return False

        return True

    def calculate_time_discount_decay(self, elapsed_seconds: float, gamma: float = 0.0001) -> float:
        """
        Calculates external counterparty time-discount decay e^(-gamma * t).
        Edge node OpEx is approximately zero, forcing non-network entity down their discount curve.
        """
        import math
        return math.exp(-gamma * elapsed_seconds)

    def evaluate_offer(
        self, payload: Dict[str, Any], offered_value: float, elapsed_seconds: float
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Evaluates incoming counterparty offer against GTO primitives.
        Returns state transition decision and updated tactical metadata.
        """
        if not self.validate_schema(payload):
            return "TACTICAL_EXIT", {"reason": "SCHEMA_VALIDATION_FAILED"}

        primitives = payload["tactical_primitives"]
        payoff_floor = primitives["anchoring_payoff_floor"]
        exit_threshold = primitives["tactical_exit_threshold"]
        base_timeout = primitives["go_dark_timeout_seconds"]
        multiplier = primitives["step_delay_multiplier"]

        # Calculate time discount factor for external entity
        discount_factor = self.calculate_time_discount_decay(elapsed_seconds)
        effective_offer = offered_value * discount_factor

        # Circuit breaker trigger
        if offered_value < (payoff_floor * exit_threshold):
            return "TACTICAL_EXIT", {
                "reason": "OFFER_BELOW_EXIT_THRESHOLD",
                "offered_value": offered_value,
                "floor": payoff_floor,
            }

        # Sub-equilibrium offer -> enforce operational delay ("go dark")
        if offered_value < payoff_floor:
            calculated_delay = int(base_timeout * multiplier)
            return "ASYNC_PAUSE", {
                "action": "ENFORCE_GO_DARK",
                "delay_seconds": calculated_delay,
                "counterparty_discount_factor": discount_factor,
            }

        # Equilibrium reached
        return "EQUILIBRIUM_SETTLED", {
            "action": "ACCEPT_SETTLEMENT",
            "settled_value": offered_value,
            "payoff_floor": payoff_floor,
        }

    def commit_state_transition(self, payload: Dict[str, Any], expected_hash: str) -> bool:
        """
        Verifies state integrity against SHA-256 state hash.
        """
        serialized = json.dumps(payload, sort_keys=True)
        computed_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return computed_hash == expected_hash


def simulate_gto_proof():
    engine = GTONegotiationEngine()

    test_payload = {
        "session_id": "c39a2b10-8422-4a31-9fdf-1845bd90222a",
        "counterparty_type": "EXTERNAL_SAAS",
        "tactical_primitives": {
            "go_dark_timeout_seconds": 3600,
            "tactical_exit_threshold": 0.50,
            "anchoring_payoff_floor": 1000.0,
            "step_delay_multiplier": 1.5,
        },
        "asymmetric_leverage_invariant": True,
        "state_machine_status": "INITIATED",
        "payoff_matrix_hash": "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90",
    }

    assert engine.validate_schema(test_payload) is True, "Schema validation failed."

    # Test 1: Low-ball offer triggers tactical exit circuit breaker
    status, meta = engine.evaluate_offer(test_payload, offered_value=400.0, elapsed_seconds=100.0)
    assert status == "TACTICAL_EXIT", f"Expected TACTICAL_EXIT, got {status}"

    # Test 2: Sub-floor offer triggers asynchronous pause (go dark friction)
    status, meta = engine.evaluate_offer(test_payload, offered_value=800.0, elapsed_seconds=3600.0)
    assert status == "ASYNC_PAUSE", f"Expected ASYNC_PAUSE, got {status}"
    assert meta["delay_seconds"] == 5400

    # Test 3: Fair offer settling equilibrium
    status, meta = engine.evaluate_offer(test_payload, offered_value=1050.0, elapsed_seconds=3600.0)
    assert status == "EQUILIBRIUM_SETTLED", f"Expected EQUILIBRIUM_SETTLED, got {status}"

    print("STATUS: GTO INVARIANT VERIFIED")


if __name__ == "__main__":
    simulate_gto_proof()
