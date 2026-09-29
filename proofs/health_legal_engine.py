import hashlib
import json
from typing import Dict, Any, List


class OpenHealthLegalEngine:
    """
    Bare-Metal Sovereign Healthcare & Medical Billing Defense Engine (OPEN-HEALTH-LEGAL-v1.0).
    Parses medical bills/chargemasters, enforces statutory protections (e.g., No Surprises Act),
    calculates overcharge deltas against standard benchmark medians, and auto-generates
    binding pro se dispute pleadings without middleman legal fees or bill-advocate tollbooths.
    """

    def __init__(self):
        self.cases: Dict[str, Dict[str, Any]] = {}

    def register_case(self, case_schema: Dict[str, Any]) -> bool:
        if "case_id" not in case_schema or "claim_items" not in case_schema:
            return False
        case_id = case_schema["case_id"]
        self.cases[case_id] = case_schema
        return True

    def calculate_statutory_overcharge_cents(self, case_id: str) -> int:
        if case_id not in self.cases:
            return 0
        case = self.cases[case_id]
        total_overcharge = 0

        for item in case.get("claim_items", []):
            billed = item.get("billed_cents", 0)
            benchmark = item.get("benchmark_median_cents", 0)
            is_emergency = item.get("emergency_service", False)

            # Under the No Surprises Act, out-of-network emergency billing above in-network median is illegal
            if is_emergency and billed > benchmark:
                total_overcharge += (billed - benchmark)
            elif billed > benchmark * 3:
                # Excessive unconscionable chargemaster markup (>300% median benchmark)
                total_overcharge += (billed - benchmark)

        return total_overcharge

    def generate_pro_se_dispute_pleading(self, case_id: str, timestamp: int) -> Dict[str, Any]:
        if case_id not in self.cases:
            return {}

        case = self.cases[case_id]
        overcharge_cents = self.calculate_statutory_overcharge_cents(case_id)

        pleading_text = (
            f"NOTICE OF STATUTORY MEDICAL BILLING DISPUTE & DEMAND FOR ADJUSTMENT\n"
            f"Case ID: {case_id}\n"
            f"Provider NPI: {case.get('provider_npi')}\n"
            f"Statutory Notice under No Surprises Act (45 C.F.R. § 149) and State Consumer Protection Law.\n"
            f"Identified Excessive Statutory Delta: {overcharge_cents / 100:.2f} USD.\n"
            f"Demand: Adjust total billed amount to benchmark median. Formal response required within 30 days."
        )

        pleading_hash = hashlib.sha256(pleading_text.encode('utf-8')).hexdigest()

        return {
            "case_id": case_id,
            "timestamp": timestamp,
            "statutory_overcharge_cents": overcharge_cents,
            "pleading_hash": pleading_hash,
            "pleading_body": pleading_text
        }

    def commit_state_transition(self, case_id: str, execution_payload: str, expected_hash: str) -> bool:
        calculated_hash = hashlib.sha256(execution_payload.encode('utf-8')).hexdigest()
        if calculated_hash == expected_hash:
            if case_id in self.cases:
                self.cases[case_id]["status"] = "DISPUTE_DISPATCHED"
                self.cases[case_id]["committed_hash"] = calculated_hash
            return True
        return False


def run_health_legal_proof() -> bool:
    engine = OpenHealthLegalEngine()
    case_data = {
        "case_id": "HLTH-1234abcd",
        "patient_pubkey": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "provider_npi": "1234567890",
        "claim_items": [
            {
                "cpt_code": "99285",
                "billed_cents": 550000,
                "benchmark_median_cents": 120000,
                "emergency_service": True
            }
        ],
        "statutory_violations": ["NO_SURPRISES_ACT_OUT_OF_NETWORK"],
        "dispute_timestamp": 1774000000
    }

    assert engine.register_case(case_data) is True
    overcharge = engine.calculate_statutory_overcharge_cents("HLTH-1234abcd")
    assert overcharge == 430000  # 550000 - 120000

    pleading = engine.generate_pro_se_dispute_pleading("HLTH-1234abcd", 1774000000)
    target_hash = pleading["pleading_hash"]

    committed = engine.commit_state_transition("HLTH-1234abcd", pleading["pleading_body"], target_hash)
    assert committed is True
    return True


if __name__ == "__main__":
    assert run_health_legal_proof() is True
    print("OPEN-HEALTH-LEGAL-v1.0 Proof Executed Successfully.")
