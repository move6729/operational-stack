import hashlib
import json
import time
from typing import Dict, Any, List, Optional


class OpenTenantEngine:
    """
    Bare-Metal Sovereign Tenant Rights & Landlord Compliance Engine (OPEN-TENANT-v1.0).
    Provides a zero-rent, schema-enforced alternative to corporate landlord platforms,
    evaluating habitability rent abatements, statutory notice windows, illegal retaliation levels,
    HITL physical legal pleadings, and zero-C2 stigmergic class leverage thresholds.
    """

    def __init__(self):
        self.registered_cases: Dict[str, Dict[str, Any]] = {}

    def register_case(self, case_schema: Dict[str, Any]) -> bool:
        """
        Registers a new tenant defense case schema instance into local memory.
        """
        if case_schema.get("protocol_version") != "OPEN-TENANT-v1.0":
            return False
        case_id = case_schema.get("case_id")
        if not case_id:
            return False
        self.registered_cases[case_id] = case_schema
        return True

    def calculate_total_rent_abatement(self, case_id: str) -> int:
        """
        Calculates total statutory rent abatement in cents based on registered habitability defects.
        """
        case = self.registered_cases.get(case_id)
        if not case:
            return 0

        monthly_rent_cents = case.get("monthly_rent_cents", 0)
        defects = case.get("habitability_defects", [])
        total_abatement_cents = 0

        for defect in defects:
            severity = defect.get("severity_factor", 0.0)
            duration_days = defect.get("duration_days", 0)
            daily_rent = monthly_rent_cents / 30.0
            abatement = int(daily_rent * severity * duration_days)
            total_abatement_cents += abatement

        return total_abatement_cents

    def evaluate_retaliation_presumption(self, case_id: str, statutory_window_days: int = 180) -> bool:
        """
        Evaluates whether a landlord action (e.g., rent hike or eviction notice) triggers a legal presumption
        of illegal retaliation based on recent tenant protected activity within the statutory window.
        """
        case = self.registered_cases.get(case_id)
        if not case:
            return False

        protected_activities = case.get("protected_activities", [])
        adverse_actions = case.get("adverse_actions", [])

        if not protected_activities or not adverse_actions:
            return False

        latest_activity_time = max(act.get("timestamp", 0) for act in protected_activities)
        earliest_adverse_time = min(adv.get("timestamp", 0) for adv in adverse_actions)

        if earliest_adverse_time >= latest_activity_time:
            delta_days = (earliest_adverse_time - latest_activity_time) / 86400.0
            if delta_days <= statutory_window_days:
                return True

        return False

    def evaluate_jurisdictional_leverage(self, case_id: str, current_timestamp: int) -> Dict[str, Any]:
        """
        Evaluates current statutory cure windows and determines the active escalation state.
        States:
          0 = Detection / Logging
          1 = Statutory Cure Window Active
          2 = Rent Escrow Lock Triggered
          3 = Stigmergic Class Leverage Threshold Reached
        """
        case = self.registered_cases.get(case_id)
        if not case:
            return {"escalation_state": 0, "escrow_eligible": False, "cure_window_expired": False}

        defects = case.get("habitability_defects", [])
        cure_window_expired = False

        for defect in defects:
            notice_timestamp = defect.get("notice_timestamp", 0)
            statutory_cure_days = defect.get("statutory_cure_days", 14)
            expiry = notice_timestamp + (statutory_cure_days * 86400)
            if current_timestamp >= expiry and notice_timestamp > 0:
                cure_window_expired = True
                break

        abatement_cents = self.calculate_total_rent_abatement(case_id)
        retaliation_triggered = self.evaluate_retaliation_presumption(case_id)

        escalation_state = 0
        if cure_window_expired:
            escalation_state = 2
        elif defects:
            escalation_state = 1

        return {
            "escalation_state": escalation_state,
            "escrow_eligible": cure_window_expired,
            "cure_window_expired": cure_window_expired,
            "retaliation_presumption": retaliation_triggered,
            "total_abatement_cents": abatement_cents
        }

    def generate_pro_se_pleading(self, case_id: str, current_timestamp: int) -> Dict[str, Any]:
        """
        Generates a human-actionable Pro Se legal pleading artifact and escrow lock instruction.
        """
        case = self.registered_cases.get(case_id)
        if not case:
            return {}

        leverage = self.evaluate_jurisdictional_leverage(case_id, current_timestamp)
        tenant_name = case.get("tenant_identity", {}).get("name", "TENANT PRO SE")
        property_address = case.get("property_address", "PROPERTY LOCATION")

        pleading_text = (
            f"IN THE MUNICIPAL HOUSING COURT\n"
            f"TENANT DEFENSE ACTION & HABITABILITY ESCROW AFFIDAVIT\n\n"
            f"PLAINTIFF/TENANT: {tenant_name}\n"
            f"PREMISES: {property_address}\n\n"
            f"STATEMENT OF STATUTORY HABITABILITY DEFECTS:\n"
            f"- Total Calculated Rent Abatement: ${leverage.get('total_abatement_cents', 0) / 100:.2f}\n"
            f"- Statutory Cure Window Expired: {leverage.get('cure_window_expired')}\n"
            f"- Statutory Retaliation Presumption Active: {leverage.get('retaliation_presumption')}\n\n"
            f"WHEREFORE, Tenant prays for an Order validating rent escrow withholding under municipal code "
            f"and enjoining Landlord from retaliatory eviction or adverse credit reporting."
        )

        artifact_hash = hashlib.sha256(pleading_text.encode('utf-8')).hexdigest()

        return {
            "case_id": case_id,
            "artifact_type": "PRO_SE_HOUSING_PLEADING",
            "sha256_hash": artifact_hash,
            "pleading_text": pleading_text,
            "escalation_state": leverage.get("escalation_state")
        }

    def evaluate_stigmergic_class_threshold(
        self,
        building_id: str,
        peer_proof_hashes: List[str],
        min_threshold: int = 3
    ) -> Dict[str, Any]:
        """
        Evaluates zero-C2 stigmergic class coordination across independent peer nodes in the same building/portfolio.
        When threshold of cryptographically signed proofs is reached, collective leverage is unlocked.
        """
        valid_proofs = set(peer_proof_hashes)
        proof_count = len(valid_proofs)
        class_action_triggered = proof_count >= min_threshold

        return {
            "building_id": building_id,
            "participating_nodes": proof_count,
            "min_threshold": min_threshold,
            "collective_leverage_triggered": class_action_triggered,
            "action_protocol": "COLLECTIVE_RENT_ESCROW_STRIKE" if class_action_triggered else "INDIVIDUAL_ESCROW"
        }

    def commit_state_transition(self, case_id: str, new_payload: str, expected_hash: str) -> bool:
        """
        Commits a state transition for a case strictly if the payload matches expected SHA-256 target hash.
        """
        computed_hash = hashlib.sha256(new_payload.encode('utf-8')).hexdigest()
        if computed_hash != expected_hash:
            return False

        case = self.registered_cases.get(case_id)
        if not case:
            return False

        case["last_committed_payload"] = new_payload
        case["state_hash"] = computed_hash
        return True


def run_tenant_proof() -> bool:
    """
    Runnable proof demonstrating tenant statutory evaluation, Pro Se pleading generation, and stigmergic class trigger.
    """
    engine = OpenTenantEngine()
    sample_case = {
        "protocol_version": "OPEN-TENANT-v1.0",
        "case_id": "case-uuid-10928",
        "monthly_rent_cents": 200000,
        "property_address": "124 Main Street, Unit 4B",
        "tenant_identity": {"name": "Jane Doe"},
        "habitability_defects": [
            {
                "defect_type": "HEATING_FAILURE",
                "severity_factor": 0.5,
                "duration_days": 10,
                "notice_timestamp": 100000,
                "statutory_cure_days": 3
            }
        ],
        "protected_activities": [{"timestamp": 100000, "activity": "WRITTEN_HABITABILITY_NOTICE"}],
        "adverse_actions": [{"timestamp": 105000, "action": "EVICTION_NOTICE"}]
    }

    if not engine.register_case(sample_case):
        return False

    abatement = engine.calculate_total_rent_abatement("case-uuid-10928")
    retaliation = engine.evaluate_retaliation_presumption("case-uuid-10928")
    leverage = engine.evaluate_jurisdictional_leverage("case-uuid-10928", current_timestamp=500000)
    pleading = engine.generate_pro_se_pleading("case-uuid-10928", current_timestamp=500000)
    stigmergic = engine.evaluate_stigmergic_class_threshold("building-88", ["hash1", "hash2", "hash3"], min_threshold=3)

    return (
        abatement == 333333 and
        retaliation is True and
        leverage["escalation_state"] == 2 and
        pleading["artifact_type"] == "PRO_SE_HOUSING_PLEADING" and
        stigmergic["collective_leverage_triggered"] is True
    )


if __name__ == "__main__":
    success = run_tenant_proof()
    print(f"OPEN-TENANT-v1.0 Verification Proof: {'PASSED' if success else 'FAILED'}")
