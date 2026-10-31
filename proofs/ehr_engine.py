import hashlib
import json
import time
from typing import Any, Dict


class OpenEHREngine:
    """
    Bare-Metal Sovereign EHR Engine (OPEN-EHR-v1.0).
    Provides a zero-rent alternative to proprietary cloud health record monopolies like Epic Systems.
    """

    PROTOCOL_VERSION = "OPEN-EHR-v1.0"

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
    engine = OpenEHREngine(node_id="edge-clinic-node-01")

    test_obj_id = "c3b934b1-e23a-4e2b-bb4c-6d2f3c7a8b9e"
    initial_payload = json.dumps({
        "patient_identifier": "LOCAL-ENC-PATIENT-9921",
        "encounter_type": "AMBULATORY",
        "vitals": {"bp_systolic": 118, "bp_diastolic": 76, "spo2": 99}
    })
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-EHR-v1.0",
        "object_id": test_obj_id,
        "entity_type": "clinical_encounter",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "relations_graph": {
            "associated_patient": ["patient-local-uuid-441"],
            "attending_clinician": ["provider-local-uuid-108"],
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_object(schema_payload)
    print(f"Health Record Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    updated_clinical_payload = json.dumps({
        "patient_identifier": "LOCAL-ENC-PATIENT-9921",
        "encounter_type": "AMBULATORY",
        "diagnostic_disposition": "DISCHARGED_STABLE",
        "vitals": {"bp_systolic": 118, "bp_diastolic": 76, "spo2": 99}
    })
    expected_transition_hash = hashlib.sha256(updated_clinical_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        obj_id=test_obj_id,
        new_payload=updated_clinical_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_obj_id]['local_state_vector']['state_hash']}")
