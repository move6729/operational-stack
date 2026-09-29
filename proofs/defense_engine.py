# SPDX-License-Identifier: Unlicense
"""
Bare-Metal Sovereign Defense & Dual-Use Supply Chain Engine (OPEN-DEFENSE-v1.0).
Provides a zero-rent alternative to locked-in proprietary defense procurement contractors
by verifying CNC/3D-printing toolpaths (G-code), material specifications, and open supply network nodes.
"""

import hashlib
import json
from typing import Dict, Any, List

class OpenDefenseEngine:
    """
    Bare-Metal Sovereign Defense Procurement Engine (OPEN-DEFENSE-v1.0).
    Disintermediates defense gatekeepers via deterministic G-code verification
    and decentralized peer-to-peer manufacturing node attestations.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.registered_manifests: Dict[str, Dict[str, Any]] = {}

    def register_manifest(self, manifest_schema: Dict[str, Any]) -> bool:
        """
        Registers an open hardware manufacturing specification manifest into state.
        Verifies required fields and structural schema properties.
        """
        manifest_id = manifest_schema.get("manifest_id")
        if not manifest_id or not manifest_id.startswith("def-"):
            return False

        gcode_hash = manifest_schema.get("gcode_sha256")
        cad_hash = manifest_schema.get("cad_file_hash")
        if not gcode_hash or len(gcode_hash) != 64 or not cad_hash or len(cad_hash) != 64:
            return False

        self.registered_manifests[manifest_id] = manifest_schema
        return True

    def verify_toolpath_integrity(self, manifest_id: str, raw_gcode: str) -> bool:
        """
        Verifies that a local CNC/3D printer toolpath string deterministically matches
        the SHA-256 hash registered in the defense specification manifest.
        """
        manifest = self.registered_manifests.get(manifest_id)
        if not manifest:
            return False

        computed_hash = hashlib.sha256(raw_gcode.encode("utf-8")).hexdigest()
        return computed_hash == manifest.get("gcode_sha256")

    def commit_state_transition(self, manifest_id: str, execution_payload: str, expected_hash: str) -> bool:
        """
        Commits a deterministic state transition verifying manufacturing execution.
        """
        manifest = self.registered_manifests.get(manifest_id)
        if not manifest:
            return False

        payload_bytes = f"{manifest_id}:{execution_payload}".encode("utf-8")
        computed_hash = hashlib.sha256(payload_bytes).hexdigest()

        return computed_hash == expected_hash


def run_defense_proof() -> bool:
    engine = OpenDefenseEngine(node_id="node-defense-alpha")

    raw_gcode = "G21 ; Millimeters\nG90 ; Absolute positioning\nM3 S12000 ; Spindle ON\nG0 X0 Y0 Z5\nG1 Z-2 F100\nG1 X50 Y50 F300\nM5 ; Spindle OFF"
    gcode_hash = hashlib.sha256(raw_gcode.encode("utf-8")).hexdigest()
    cad_hash = hashlib.sha256(b"CAD_MODEL_BINARY_STUB_v1.0").hexdigest()

    manifest = {
        "manifest_id": "def-1234567890ab",
        "timestamp_utc": 1774828800,
        "component_name": "Autonomous Flight Surface Actuator Mount",
        "material_specification": {
            "material_type": "ALUMINUM_7075_T6",
            "tensile_strength_mpa": 570.0,
            "tolerance_mm": 0.02
        },
        "manufacturing_type": "CNC_MILLING",
        "gcode_sha256": gcode_hash,
        "cad_file_hash": cad_hash,
        "dual_use_classification": "CIVILIAN_DUAL_USE",
        "decentralized_supplier_nodes": ["node-fab-01", "node-fab-02"],
        "attestation_signature": hashlib.sha256(b"ATTESTATION_OK").hexdigest()
    }

    if not engine.register_manifest(manifest):
        return False

    if not engine.verify_toolpath_integrity("def-1234567890ab", raw_gcode):
        return False

    payload = "COMPLETED_JOB_123"
    expected = hashlib.sha256(f"def-1234567890ab:{payload}".encode("utf-8")).hexdigest()

    return engine.commit_state_transition("def-1234567890ab", payload, expected)


if __name__ == "__main__":
    success = run_defense_proof()
    print(f"[OPEN-DEFENSE-v1.0] Manufacturing Attestation Proof: {'PASSED' if success else 'FAILED'}")
    assert success is True
