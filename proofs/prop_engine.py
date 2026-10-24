import hashlib
import json
import time
from typing import Any, Dict


class OpenPropEngine:
    """
    Bare-Metal Sovereign Property Engine (OPEN-PROP-v1.0).
    Provides a zero-rent alternative to proprietary real estate platforms like Yardi, RealPage, and AppFolio.
    """

    PROTOCOL_VERSION = "OPEN-PROP-v1.0"

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_lease(self, obj_schema: Dict[str, Any]) -> bool:
        if obj_schema.get("protocol_version") != self.PROTOCOL_VERSION:
            raise ValueError(f"Invalid protocol version. Expected {self.PROTOCOL_VERSION}")

        sec_invariants = obj_schema.get("security_invariants", {})
        if not sec_invariants.get("isolated_sandbox_required") or not sec_invariants.get("statutory_compliance_verified"):
            raise PermissionError("Security invariants failed.")

        lease_id = obj_schema.get("lease_id")
        if not lease_id:
            raise ValueError("Missing lease_id in schema payload.")

        self.registry[lease_id] = obj_schema
        return True

    def commit_state_transition(self, lease_id: str, new_payload: str, expected_hash: str) -> bool:
        if lease_id not in self.registry:
            raise KeyError(f"Lease {lease_id} not registered in engine.")

        computed_hash = hashlib.sha256(new_payload.encode("utf-8")).hexdigest()
        if computed_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Computed: {computed_hash}, Expected: {expected_hash}")

        self.registry[lease_id]["local_state_vector"] = {
            "state_hash": computed_hash,
            "timestamp_epoch": int(time.time()),
        }
        return True


if __name__ == "__main__":
    engine = OpenPropEngine(node_id="edge-node-prop-01")

    test_id = "f1b2c3a4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    initial_payload = json.dumps({"status": "LEASE_EXECUTED", "monthly_rent_cents": 250000})
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-PROP-v1.0",
        "lease_id": test_id,
        "property_id": "prop-bldg-001",
        "unit_id": "unit-4b",
        "tenant_did": "did:key:z6MkpTHR8VNsBxYAAWHu321",
        "monthly_rent_cents": 250000,
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_lease(schema_payload)
    print(f"Prop Lease Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    updated_payload = json.dumps({"status": "RENT_PAID_SETTLED", "monthly_rent_cents": 250000, "tx_ref": "tx-hash-777"})
    expected_transition_hash = hashlib.sha256(updated_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        lease_id=test_id,
        new_payload=updated_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"Prop Lease State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_id]['local_state_vector']['state_hash']}")
