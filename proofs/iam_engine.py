import hashlib
import json
import time
from typing import Any, Dict


class OpenIAMEngine:
    """
    Bare-Metal Sovereign IAM Engine (OPEN-IAM-v1.0).
    Provides a zero-rent alternative to proprietary cloud identity vendors like Okta and Ping Identity.
    """

    PROTOCOL_VERSION = "OPEN-IAM-v1.0"

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_identity(self, obj_schema: Dict[str, Any]) -> bool:
        if obj_schema.get("protocol_version") != self.PROTOCOL_VERSION:
            raise ValueError(f"Invalid protocol version. Expected {self.PROTOCOL_VERSION}")

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required") or not sec_invariants.get("statutory_compliance_verified"):
            raise PermissionError("Security invariants failed.")

        identity_id = obj_schema.get("identity_id")
        if not identity_id:
            raise ValueError("Missing identity_id in schema payload.")

        self.registry[identity_id] = obj_schema
        return True

    def commit_state_transition(self, identity_id: str, new_payload: str, expected_hash: str) -> bool:
        if identity_id not in self.registry:
            raise KeyError(f"Identity {identity_id} not registered in engine.")

        computed_hash = hashlib.sha256(new_payload.encode("utf-8")).hexdigest()
        if computed_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Computed: {computed_hash}, Expected: {expected_hash}")

        self.registry[identity_id]["local_state_vector"] = {
            "state_hash": computed_hash,
            "timestamp_epoch": int(time.time()),
        }
        return True


if __name__ == "__main__":
    engine = OpenIAMEngine(node_id="edge-node-iam-01")

    test_id = "d1b2c3a4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    initial_payload = json.dumps({"status": "ACTIVE", "roles": ["ADMIN", "AUDITOR"]})
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-IAM-v1.0",
        "identity_id": test_id,
        "did_identifier": "did:key:z6MkpTHR8VNsBxYAAWHu321",
        "public_keys": [
            {
                "key_id": "key-1",
                "key_type": "Ed25519VerificationKey2020",
                "public_key_hex": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            }
        ],
        "role_claims": ["ADMIN", "AUDITOR"],
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_identity(schema_payload)
    print(f"Identity Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    updated_payload = json.dumps({"status": "ACTIVE", "roles": ["ADMIN", "AUDITOR", "SYSTEM_OPERATOR"]})
    expected_transition_hash = hashlib.sha256(updated_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        identity_id=test_id,
        new_payload=updated_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"Identity State Update Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_id]['local_state_vector']['state_hash']}")
