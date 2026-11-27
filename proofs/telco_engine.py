import hashlib
import json
import time
from typing import Any, Dict


class OpenTelcoEngine:
    """
    Bare-Metal Sovereign Telco Engine (OPEN-TELCO-v1.0).
    Provides a zero-rent alternative to proprietary telecom API aggregators like Twilio and Infobip.
    """

    PROTOCOL_VERSION = "OPEN-TELCO-v1.0"

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_dispatch(self, obj_schema: Dict[str, Any]) -> bool:
        if obj_schema.get("protocol_version") != self.PROTOCOL_VERSION:
            raise ValueError(f"Invalid protocol version. Expected {self.PROTOCOL_VERSION}")

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required") or not sec_invariants.get("statutory_compliance_verified"):
            raise PermissionError("Security invariants failed.")

        dispatch_id = obj_schema.get("dispatch_id")
        if not dispatch_id:
            raise ValueError("Missing dispatch_id in schema payload.")

        self.registry[dispatch_id] = obj_schema
        return True

    def commit_state_transition(self, dispatch_id: str, new_payload: str, expected_hash: str) -> bool:
        if dispatch_id not in self.registry:
            raise KeyError(f"Dispatch {dispatch_id} not registered in engine.")

        computed_hash = hashlib.sha256(new_payload.encode("utf-8")).hexdigest()
        if computed_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Computed: {computed_hash}, Expected: {expected_hash}")

        self.registry[dispatch_id]["local_state_vector"] = {
            "state_hash": computed_hash,
            "timestamp_epoch": int(time.time()),
        }
        return True


if __name__ == "__main__":
    engine = OpenTelcoEngine(node_id="edge-node-telco-01")

    test_id = "e1b2c3a4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    initial_payload = json.dumps({"status": "ROUTING_INITIATED", "channel": "WEBRTC_MESH"})
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-TELCO-v1.0",
        "dispatch_id": test_id,
        "origin_peer": "peer-node-alpha",
        "target_peer": "peer-node-beta",
        "payload_type": "WEBRTC_SDP",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_dispatch(schema_payload)
    print(f"Telco Dispatch Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    delivered_payload = json.dumps({"status": "DELIVERED_P2P", "channel": "WEBRTC_MESH", "ack_sig": "sig-ack-99"})
    expected_transition_hash = hashlib.sha256(delivered_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        dispatch_id=test_id,
        new_payload=delivered_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"Telco Dispatch Delivery Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_id]['local_state_vector']['state_hash']}")
