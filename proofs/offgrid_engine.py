import hashlib
import json
from typing import Dict, Any


class SelfSovereignOffGridEngine:
    """
    Self-Sovereign Physical Infrastructure & Off-Grid Energy Engine (OPEN-INFRA-v1.0).
    Directly pairs local compute task execution with bare-metal solar, battery, and power actuators,
    optimizing thermodynamic compute yield during peak renewable generation windows.
    """

    def __init__(self):
        self.actuator_states: Dict[str, Dict[str, Any]] = {}

    def register_node_telemetry(self, telemetry_schema: Dict[str, Any]) -> bool:
        if "node_id" not in telemetry_schema:
            return False
        self.actuator_states[telemetry_schema["node_id"]] = telemetry_schema
        return True

    def evaluate_optimal_execution_mode(self, node_id: str) -> str:
        if node_id not in self.actuator_states:
            return "IDLE"

        state = self.actuator_states[node_id]
        solar_w = state.get("solar_input_watts", 0.0)
        battery_pct = state.get("battery_charge_percent", 0.0)

        if solar_w > 150.0 or battery_pct > 80.0:
            return "FULL_COMPUTE_MAX_YIELD"
        elif battery_pct < 20.0 and solar_w < 20.0:
            return "BATTERY_CONSERVATION"
        else:
            return "IDLE"

    def commit_actuator_transition(self, node_id: str, payload_str: str, expected_hash: str) -> bool:
        calculated = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        if calculated == expected_hash:
            if node_id in self.actuator_states:
                self.actuator_states[node_id]["actuator_state"] = self.evaluate_optimal_execution_mode(node_id)
                self.actuator_states[node_id]["commit_hash"] = calculated
            return True
        return False


def run_offgrid_proof() -> bool:
    engine = SelfSovereignOffGridEngine()
    node_telemetry = {
        "node_id": "SOLAR-EDGE-NODE-01",
        "solar_input_watts": 350.5,
        "battery_charge_percent": 95.0,
        "grid_connected": False,
        "actuator_state": "IDLE",
        "timestamp": 1774000000
    }

    assert engine.register_node_telemetry(node_telemetry) is True
    mode = engine.evaluate_optimal_execution_mode("SOLAR-EDGE-NODE-01")
    assert mode == "FULL_COMPUTE_MAX_YIELD"

    payload = "ACTUATOR_DISPATCH_FULL_POWER_0x01"
    target_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    committed = engine.commit_actuator_transition("SOLAR-EDGE-NODE-01", payload, target_hash)
    assert committed is True
    assert engine.actuator_states["SOLAR-EDGE-NODE-01"]["actuator_state"] == "FULL_COMPUTE_MAX_YIELD"
    return True


if __name__ == "__main__":
    assert run_offgrid_proof() is True
    print("OPEN-INFRA-v1.0 Proof Executed Successfully.")
