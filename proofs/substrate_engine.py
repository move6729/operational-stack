"""
Bare-Metal Sovereign Off-Grid Substrate Resilience Engine (OPEN-SUBSTRATE-v1.0).
Secures physical survival (power, water, hardware salvage) against utility blackouts or supply blockades.
"""

import hashlib
import json
from typing import Dict, Any


class OpenSubstrateEngine:
    """
    Bare-Metal Sovereign Off-Grid Substrate Resilience Engine (OPEN-SUBSTRATE-v1.0).
    Enforces local power and water autonomy invariants without external grid dependencies.
    """

    def calculate_autonomy_days(self, payload: Dict[str, Any]) -> Dict[str, float]:
        daily_power = payload.get("daily_power_draw_wh", 0.0)
        daily_water = payload.get("daily_water_draw_liters", 0.0)

        power_days = payload.get("offgrid_power_capacity_wh", 0.0) / daily_power if daily_power > 0 else float("inf")
        water_days = payload.get("water_storage_liters", 0.0) / daily_water if daily_water > 0 else float("inf")

        effective_autonomy = min(power_days, water_days)
        return {
            "power_autonomy_days": power_days,
            "water_autonomy_days": water_days,
            "effective_autonomy_days": effective_autonomy,
        }

    def evaluate_resilience_status(self, payload: Dict[str, Any]) -> bool:
        if not payload.get("cfaa_compliant", False):
            return False

        expected_days = payload.get("expected_blackout_days", 0.0)
        metrics = self.calculate_autonomy_days(payload)
        return metrics["effective_autonomy_days"] >= expected_days

    def commit_state_transition(self, node_id: str, new_payload: Dict[str, Any], expected_hash: str) -> bool:
        if not self.evaluate_resilience_status(new_payload):
            return False

        payload_copy = {k: v for k, v in new_payload.items() if k != "expected_hash"}
        raw_bytes = json.dumps(payload_copy, sort_keys=True).encode("utf-8")
        computed_hash = hashlib.sha256(raw_bytes).hexdigest()
        return computed_hash == expected_hash


def simulate_substrate_engine_proof() -> bool:
    engine = OpenSubstrateEngine()
    payload = {
        "node_id": "node-alpha-1",
        "jurisdiction_context": "US",
        "cfaa_compliant": True,
        "offgrid_power_capacity_wh": 50000.0,
        "water_storage_liters": 1000.0,
        "salvaged_hardware_count": 5,
        "expected_blackout_days": 14.0,
        "daily_power_draw_wh": 2500.0,
        "daily_water_draw_liters": 50.0,
    }

    raw_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    expected_hash = hashlib.sha256(raw_bytes).hexdigest()
    payload["expected_hash"] = expected_hash

    return engine.commit_state_transition("node-alpha-1", payload, expected_hash)


if __name__ == "__main__":
    success = simulate_substrate_engine_proof()
    print(f"OPEN-SUBSTRATE-v1.0 Verification: {success}")
