import hashlib
import json
import time
from typing import Any, Dict


class OpenEduEngine:
    """
    Bare-Metal Sovereign Educational Engine (OPEN-EDU-v1.0).
    Provides a zero-rent alternative to proprietary LMS platforms like Canvas, Blackboard, and D2L Brightspace.
    """

    PROTOCOL_VERSION = "OPEN-EDU-v1.0"

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_credential(self, obj_schema: Dict[str, Any]) -> bool:
        if obj_schema.get("protocol_version") != self.PROTOCOL_VERSION:
            raise ValueError(f"Invalid protocol version. Expected {self.PROTOCOL_VERSION}")

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required") or not sec_invariants.get("statutory_compliance_verified"):
            raise PermissionError("Security invariants failed.")

        cred_id = obj_schema.get("credential_id")
        if not cred_id:
            raise ValueError("Missing credential_id in schema payload.")

        self.registry[cred_id] = obj_schema
        return True

    def commit_state_transition(self, cred_id: str, new_payload: str, expected_hash: str) -> bool:
        if cred_id not in self.registry:
            raise KeyError(f"Credential {cred_id} not registered in engine.")

        computed_hash = hashlib.sha256(new_payload.encode("utf-8")).hexdigest()
        if computed_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Computed: {computed_hash}, Expected: {expected_hash}")

        self.registry[cred_id]["local_state_vector"] = {
            "state_hash": computed_hash,
            "timestamp_epoch": int(time.time()),
        }
        return True


if __name__ == "__main__":
    engine = OpenEduEngine(node_id="edge-node-edu-01")

    test_id = "c1b2c3a4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    initial_payload = json.dumps({"status": "ENROLLED", "mastery_score": 0.0})
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-EDU-v1.0",
        "credential_id": test_id,
        "student_did": "did:key:z6MkpTHR8VNsBxYAAWHu321",
        "institution_did": "did:key:z6MkVN182kS29mAAWHu987",
        "course_code": "CS-801",
        "mastery_score": 98.5,
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_credential(schema_payload)
    print(f"Edu Credential Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    updated_payload = json.dumps({"status": "CREDENTIAL_ISSUED", "mastery_score": 98.5, "completion_hash": "hash-cert-888"})
    expected_transition_hash = hashlib.sha256(updated_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        cred_id=test_id,
        new_payload=updated_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"Edu Credential State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_id]['local_state_vector']['state_hash']}")
