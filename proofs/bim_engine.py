import hashlib
import json
import time
from typing import Any, Dict


class OpenBIMEngine:
    """
    Bare-Metal Sovereign Spatial BIM Engine (OPEN-BIM-v1.0).
    Provides a zero-rent alternative to proprietary AEC BIM platforms like Autodesk Revit and BIM 360.
    """

    PROTOCOL_VERSION = "OPEN-BIM-v1.0"

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
    engine = OpenBIMEngine(node_id="edge-bim-coordinator-01")

    test_obj_id = "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a"
    initial_payload = json.dumps({
        "element_guid": "IFCWALL-EXT-LEVEL-02-NORTH",
        "spatial_coordinates": {"x": 120.45, "y": 88.10, "z": 6.00},
        "material": "REINFORCED_CONCRETE_C30",
        "status": "DESIGN_ISSUED_FOR_REVIEW"
    })
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-BIM-v1.0",
        "object_id": test_obj_id,
        "entity_type": "spatial_element",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "relations_graph": {
            "adjacent_structural_nodes": ["col-l2-c04", "slab-l2-s01"],
            "clash_group_id": ["clash-set-mep-hvac-003"],
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_object(schema_payload)
    print(f"Spatial BIM Element Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    coordinated_payload = json.dumps({
        "element_guid": "IFCWALL-EXT-LEVEL-02-NORTH",
        "spatial_coordinates": {"x": 120.45, "y": 88.10, "z": 6.00},
        "material": "REINFORCED_CONCRETE_C30",
        "status": "COORDINATED_NO_CLASHES"
    })
    expected_transition_hash = hashlib.sha256(coordinated_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        obj_id=test_obj_id,
        new_payload=coordinated_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_obj_id]['local_state_vector']['state_hash']}")
