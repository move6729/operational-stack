import hashlib
import json
import time
from typing import Any, Dict


class OpenFinEngine:
    """
    Bare-Metal Sovereign FinTech Engine (OPEN-FIN-v1.0).
    Provides a zero-rent alternative to proprietary payment and open-banking tollbooths like Stripe and Plaid.
    """

    PROTOCOL_VERSION = "OPEN-FIN-v1.0"

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
    engine = OpenFinEngine(node_id="edge-fin-settlement-01")

    test_obj_id = "a9b8c7d6-e5f4-3a2b-1c0d-9e8f7a6b5c4d"
    initial_payload = json.dumps({
        "sender": "did:mesh:ledger-pubkey-0x8192a",
        "recipient": "did:mesh:ledger-pubkey-0x4018f",
        "amount_micro_units": 1500000000,
        "currency": "USDC_CANONICAL",
        "status": "INTENT_PROPOSED"
    })
    initial_hash = hashlib.sha256(initial_payload.encode("utf-8")).hexdigest()

    schema_payload = {
        "protocol_version": "OPEN-FIN-v1.0",
        "object_id": test_obj_id,
        "entity_type": "payment_intent",
        "local_state_vector": {
            "state_hash": initial_hash,
            "timestamp_epoch": int(time.time()),
        },
        "relations_graph": {
            "associated_escrow": ["escrow-lock-node-09"],
            "settlement_batch": ["batch-epoch-8491"],
        },
        "security_invariants": {
            "isolated_sandbox_required": True,
            "statutory_compliance_verified": True,
        },
    }

    registered = engine.register_object(schema_payload)
    print(f"Payment Intent Registration Status: {'SUCCESS' if registered else 'FAILED'}")

    settled_payload = json.dumps({
        "sender": "did:mesh:ledger-pubkey-0x8192a",
        "recipient": "did:mesh:ledger-pubkey-0x4018f",
        "amount_micro_units": 1500000000,
        "currency": "USDC_CANONICAL",
        "status": "SETTLED_IRREVOCABLE"
    })
    expected_transition_hash = hashlib.sha256(settled_payload.encode("utf-8")).hexdigest()

    committed = engine.commit_state_transition(
        obj_id=test_obj_id,
        new_payload=settled_payload,
        expected_hash=expected_transition_hash,
    )
    print(f"State Transition Status: {'SUCCESS' if committed else 'FAILED'}")
    print(f"Verified State Hash: {engine.registry[test_obj_id]['local_state_vector']['state_hash']}")
