import hashlib
import json
import time
from typing import Dict, List, Any

class AshbyOntologyEngine:
    """
    Bare-Metal Sovereign Ontology Engine (ASHBY-v1.0).
    Provides a zero-rent, Ashby's Law-compliant alternative to centralized surveillance ontologies.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.local_objects: Dict[str, Dict[str, Any]] = {}
        self.state_history: List[str] = []

    def register_object(self, obj_schema: Dict[str, Any]) -> bool:
        """Validates and registers a sovereign object into the local ontology graph."""
        if obj_schema.get("protocol_version") != "ASHBY-v1.0":
            print(f"[ASHBY-v1.0] REJECTION: Invalid protocol version.")
            return False

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required", False) or not sec_invariants.get("statutory_compliance_verified", False):
            print(f"[ASHBY-v1.0] REJECTION: Object failed security/statutory invariants.")
            return False

        obj_id = obj_schema["object_id"]
        self.local_objects[obj_id] = obj_schema
        print(f"[ASHBY-v1.0] SUCCESS: Object {obj_id} ({obj_schema['entity_type']}) registered locally.")
        return True

    def commit_state_transition(self, obj_id: str, new_payload: str, expected_hash: str) -> bool:
        """Commits a deterministic state transition verified via cryptographic hash."""
        if obj_id not in self.local_objects:
            print(f"[ASHBY-v1.0] ERROR: Object {obj_id} not found in local state graph.")
            return False

        computed_hash = hashlib.sha256(new_payload.encode('utf-8')).hexdigest()
        if computed_hash != expected_hash:
            print(f"[ASHBY-v1.0] STATE REJECTION: Hash mismatch for Object {obj_id}.")
            return False

        self.local_objects[obj_id]["local_state_vector"]["state_hash"] = computed_hash
        self.local_objects[obj_id]["local_state_vector"]["timestamp_epoch"] = int(time.time())
        self.state_history.append(computed_hash)
        
        print(f"[ASHBY-v1.0] STATE COMMIT: Object {obj_id} updated to hash {computed_hash[:16]}...")
        return True

if __name__ == "__main__":
    payload = '{"physical_asset": "LOCAL_SOLAR_ARRAY_01", "watts_output": 4200}'
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    mock_obj = {
        "protocol_version": "ASHBY-v1.0",
        "object_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "entity_type": "EnergyGridAsset",
        "local_state_vector": {
            "state_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "timestamp_epoch": 1700000000
        },
        "relations_graph": [
            {
                "target_object_id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
                "relation_type": "SUPPLIES_COMPUTE_NODE",
                "cryptographic_proof": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        ],
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True
        }
    }

    engine = AshbyOntologyEngine("node_local_ring0")
    if engine.register_object(mock_obj):
        engine.commit_state_transition(mock_obj["object_id"], payload, payload_hash)
