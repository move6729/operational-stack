# SPDX-License-Identifier: Unlicense
"""
Bare-Metal Sovereign Tenant Rights & Landlord Compliance Engine (OPEN-TENANT-v1.0).
Provides a zero-rent alternative to locked-in proprietary tenant portals and property managers
by evaluating habitability rent abatements, statutory notice windows, and illegal retaliation levers.
"""

import hashlib
import json
import time
from typing import Dict, Any, List

class OpenTenantEngine:
    """
    Bare-Metal Sovereign Tenant Rights & Landlord Compliance Engine (OPEN-TENANT-v1.0).
    Provides a zero-rent, schema-enforced alternative to corporate landlord platforms,
    evaluating habitability rent abatements, statutory notice windows, and illegal retaliation levers.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.cases: Dict[str, Dict[str, Any]] = {}

    def register_case(self, case_schema: Dict[str, Any]) -> bool:
        """
        Registers a tenant case schema into local state and validates structural fields.
        """
        case_id = case_schema.get("case_id")
        if not case_id or not case_id.startswith("tenant-"):
            return False

        state_hash = case_schema.get("state_hash")
        if not state_hash or len(state_hash) != 64:
            return False

        self.cases[case_id] = case_schema
        return True

    def calculate_total_rent_abatement(self, case_id: str) -> int:
        """
        Calculates monthly rent abatement in cents based on uncured habitability defects.
        """
        if case_id not in self.cases:
            return 0

        case = self.cases[case_id]
        monthly_rent = case.get("monthly_rent_cents", 0)
        defects: List[Dict[str, Any]] = case.get("habitability_defects", [])

        total_abatement_percent = 0.0
        for defect in defects:
            if not defect.get("landlord_cured", True):
                total_abatement_percent += defect.get("estimated_rent_abatement_percent", 0.0)

        # Cap maximum rent abatement at 100%
        total_abatement_percent = min(100.0, total_abatement_percent)
        abatement_cents = int((total_abatement_percent / 100.0) * monthly_rent)
        return abatement_cents

    def evaluate_retaliation_presumption(self, case_id: str, statutory_window_days: int = 180) -> bool:
        """
        Evaluates whether an adverse landlord action falls within the statutory timeline
        following a tenant protected activity (complaint/repair notice), triggering legal presumption of retaliation.
        """
        if case_id not in self.cases:
            return False

        case = self.cases[case_id]
        action_type = case.get("landlord_action_type", "none")
        if action_type == "none":
            return False

        action_ts = case.get("landlord_action_timestamp", 0)
        protected_ts = case.get("protected_activity_timestamp", 0)

        if protected_ts == 0 or action_ts < protected_ts:
            return False

        elapsed_sec = action_ts - protected_ts
        elapsed_days = elapsed_sec / 86400.0

        return elapsed_days <= statutory_window_days

    def evaluate_jurisdictional_leverage(self, case_id: str, current_timestamp: int) -> Dict[str, Any]:
        """
        Evaluates local state and municipal statutory laws to calculate accumulated statutory fines,
        identify landlord breaches, and determine rent withholding eligibility.
        """
        if case_id not in self.cases:
            return {"statutory_breach_detected": False, "accumulated_fines_cents": 0, "rent_withholding_eligible": False}

        case = self.cases[case_id]
        matrix = case.get("statutory_remedy_matrix", {})
        cure_days = matrix.get("max_statutory_cure_days", 14)
        daily_fine_cents = matrix.get("daily_statutory_fine_cents", 0)
        withholding_permitted = matrix.get("rent_withholding_permitted", False)

        defects = case.get("habitability_defects", [])
        total_accumulated_fines = 0
        statutory_breach_detected = False

        for defect in defects:
            if not defect.get("landlord_cured", True):
                reported_ts = defect.get("date_reported_timestamp", 0)
                if reported_ts > 0 and current_timestamp > reported_ts:
                    elapsed_days = (current_timestamp - reported_ts) / 86400.0
                    if elapsed_days > cure_days:
                        statutory_breach_detected = True
                        uncured_days_over_limit = int(elapsed_days - cure_days)
                        total_accumulated_fines += uncured_days_over_limit * daily_fine_cents

        return {
            "statutory_breach_detected": statutory_breach_detected,
            "accumulated_fines_cents": total_accumulated_fines,
            "rent_withholding_eligible": statutory_breach_detected and withholding_permitted
        }

    def commit_state_transition(self, case_id: str, new_payload: str, expected_hash: str) -> bool:
        """
        Commits a deterministic state transition verified via SHA-256 target state hashing.
        """
        if case_id not in self.cases:
            return False

        payload_bytes = f"{case_id}:{new_payload}".encode("utf-8")
        computed_hash = hashlib.sha256(payload_bytes).hexdigest()

        if computed_hash == expected_hash:
            self.cases[case_id]["state_hash"] = expected_hash
            return True
        return False


def run_tenant_proof() -> bool:
    """
    Executes a deterministic verification proof for OPEN-TENANT-v1.0.
    """
    engine = OpenTenantEngine(node_id="node-tenant-edge-01")

    base_ts = int(time.time())

    case_data = {
        "case_id": "tenant-a1b2c3d4e5f6",
        "timestamp_utc": base_ts,
        "tenant_node_id": "node-tenant-edge-01",
        "jurisdiction_code": "CA-SAN_FRANCISCO",
        "lease_start_timestamp": base_ts - (180 * 86400),
        "monthly_rent_cents": 250000,
        "habitability_defects": [
            {
                "defect_type": "heating_hvac",
                "date_reported_timestamp": base_ts,
                "notice_method": "written_letter",
                "landlord_cured": False,
                "estimated_rent_abatement_percent": 30.0
            },
            {
                "defect_type": "plumbing_sanitation",
                "date_reported_timestamp": base_ts,
                "notice_method": "certified_mail",
                "landlord_cured": False,
                "estimated_rent_abatement_percent": 25.0
            }
        ],
        "landlord_action_timestamp": base_ts + (10 * 86400),
        "landlord_action_type": "rent_increase",
        "protected_activity_timestamp": base_ts,
        "statutory_retaliation_suspected": True,
        "statutory_remedy_matrix": {
            "statute_reference": "SF Civ. Code § 1942.4 / SFHCO Sec. 37.10B",
            "max_statutory_cure_days": 14,
            "daily_statutory_fine_cents": 10000,
            "rent_withholding_permitted": True,
            "statutory_retaliation_window_days": 180
        },
        "state_hash": hashlib.sha256(b"INITIAL_TENANT_CASE_STATE").hexdigest()
    }

    if not engine.register_case(case_data):
        return False

    # Verify calculated rent abatement (30% + 25% = 55% of $2,500 = $1,375.00 / 137,500 cents)
    abatement = engine.calculate_total_rent_abatement("tenant-a1b2c3d4e5f6")
    if abatement != 137500:
        return False

    # Verify statutory retaliation presumption within 180-day window
    is_retaliatory = engine.evaluate_retaliation_presumption("tenant-a1b2c3d4e5f6", statutory_window_days=180)
    if not is_retaliatory:
        return False

    # Verify jurisdictional statutory leverage (30 days past report, 14-day cure window = 16 uncured days @ $100/day = $1,600 / 160,000 cents)
    current_eval_ts = base_ts + (30 * 86400)
    leverage = engine.evaluate_jurisdictional_leverage("tenant-a1b2c3d4e5f6", current_timestamp=current_eval_ts)
    if not leverage["statutory_breach_detected"] or leverage["accumulated_fines_cents"] != 160000 or not leverage["rent_withholding_eligible"]:
        return False

    # Test state transition verification
    payload = "FILE_TENANT_REMEDY_NOTICE_SERVED"
    expected_hash = hashlib.sha256(f"tenant-a1b2c3d4e5f6:{payload}".encode("utf-8")).hexdigest()
    return engine.commit_state_transition("tenant-a1b2c3d4e5f6", payload, expected_hash)


if __name__ == "__main__":
    result = run_tenant_proof()
    print(f"[OPEN-TENANT-v1.0] Tenant Defense Proof: {'PASSED' if result else 'FAILED'}")
    assert result is True
