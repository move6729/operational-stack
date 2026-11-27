import hashlib
import json
import time
from typing import Any, Dict


class OpenCRMEngine:
    """
    Bare-Metal Sovereign CRM Engine (OPEN-CRM-v1.0).
    Provides a zero-rent alternative to proprietary cloud CRM platforms.
    """

    PROTOCOL_VERSION = "OPEN-CRM-v1.0"

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
    engine = OpenCRMEngine(node_id="edge-node-01")

    test_obj_id = "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    initial_payload = json.dumps({"pipeline_stage": "QUALIFIED_LEAD", "value": 150000})
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-CRM-v1.0",
        "object_id": test_obj_id,
        "entity_type": "opportunity",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "relations_graph": {
            "associated_contacts": ["contact-uuid-001"],
            "associated_account": ["account-uuid-002"],
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_object(schema_payload)
    print(f"Object Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    updated_payload = json.dumps({"pipeline_stage": "CLOSED_WON", "value": 150000})
    expected_transition_hash = hashlib.sha256(updated_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        obj_id=test_obj_id,
        new_payload=updated_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_obj_id]['local_state_vector']['state_hash']}")
