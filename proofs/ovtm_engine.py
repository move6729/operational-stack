import hashlib
import json
import time
from typing import Any, Dict


class OpenOVTMEngine:
    """
    Bare-Metal Sovereign Vehicle Telemetry & Kinetic Mobility Engine (OVTM-S v1.1).
    Provides a zero-rent alternative to proprietary connected car platforms like Tesla Fleet API.
    """

    PROTOCOL_VERSION = "OVTM-S v1.1"

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_object(self, obj_schema: Dict[str, Any]) -> bool:
        if obj_schema.get("protocol_version") != self.PROTOCOL_VERSION:
            raise ValueError(f"Invalid protocol version. Expected {self.PROTOCOL_VERSION}")

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required") or not sec_invariants.get("statutory_compliance_verified"):
            raise PermissionError("Security invariants failed.")

        obj_id = obj_schema.get("object_id")
        if not obj_id:
            raise ValueError("Missing object_id in schema payload.")

        self.registry[obj_id] = obj_schema
        return True

    def commit_state_transition(self, obj_id: str, new_payload: str, expected_hash: str) -> bool:
        if obj_id not in self.registry:
            raise KeyError(f"Object {obj_id} not registered in engine.")

        computed_hash = hashlib.sha256(new_payload.encode("utf-8")).hexdigest()
        if computed_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Computed: {computed_hash}, Expected: {expected_hash}")

        self.registry[obj_id]["local_state_vector"] = {
            "state_hash": computed_hash,
            "timestamp_epoch": int(time.time()),
        }
        return True


if __name__ == "__main__":
    engine = OpenOVTMEngine(node_id="edge-vehicle-ecu-01")

    test_obj_id = "c0d1e2f3-a4b5-6c7d-8e9f-0a1b2c3d4e5f"
    initial_payload = json.dumps({
        "vehicle_vin_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "battery_soc_pct": 82.5,
        "kinetic_airgap_status": "HARDWARE_INTERLOCK_LOCKED",
        "telemetry_state": "INGRESS_STREAMING"
    })
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OVTM-S v1.1",
        "object_id": test_obj_id,
        "entity_type": "telematics_frame",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "relations_graph": {
            "can_bus_nodes": ["ecu-drive-by-wire", "ecu-battery-management"],
            "gateway_interlock": ["hardware-relay-airgap-01"],
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_object(schema_payload)
    print(f"Vehicle Telemetry Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    verified_payload = json.dumps({
        "vehicle_vin_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "battery_soc_pct": 82.5,
        "kinetic_airgap_status": "HARDWARE_INTERLOCK_LOCKED",
        "telemetry_state": "VERIFIED_HARDWARE_AIRGAP"
    })
    expected_transition_hash = hashlib.sha256(verified_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        obj_id=test_obj_id,
        new_payload=verified_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_obj_id]['local_state_vector']['state_hash']}")
