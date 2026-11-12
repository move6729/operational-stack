import hashlib
import json
import math
from typing import Dict, Any, List, Tuple


class SubCentMicroSettlementEngine:
    """
    Sub-Cent Thermodynamic Micro-Settlement Ledger (OPEN-SETTLEMENT-v1.0).
    Provides a zero-chain-bloat, lightweight state ledger for micro-yield task clearing
    between local edge compute nodes without gas fees, platform commissions, or third-party rent.

    Enforces Hardware Silicon Amortization & Thermodynamic Energy Cost Floor:
    TaskPrice_Subcents >= EnergyCost(Watts, duration) + HardwareDepreciation(CapEx, LifespanHours, duration)
    """

    SUBCENTS_PER_USD = 100000  # 1 USD = 100,000 subcents (1 subcent = 1/1000th cent)

    def __init__(self, ledger_id: str):
        self.ledger_id = ledger_id
        self.balances: Dict[str, int] = {}  # Balance in sub-cents (1/1000th cent)
        self.transactions: List[Dict[str, Any]] = []

    def set_balance(self, pubkey: str, subcents: int):
        self.balances[pubkey] = subcents

    def calculate_compute_cost_floor_subcents(
        self,
        execution_duration_sec: float,
        power_draw_watts: float,
        electricity_rate_kwh_usd: float,
        hardware_capex_usd: float,
        hardware_lifespan_hours: float
    ) -> Tuple[int, Dict[str, float]]:
        """
        Calculates minimum cost floor in subcents accounting for:
        1. Direct Energy Cost (Watts * Hours * Rate_per_kWh)
        2. Hardware Silicon Amortization / Depreciation (CapEx / Total_Lifespan_Hours * Task_Hours)
        """
        duration_hours = execution_duration_sec / 3600.0

        # 1. Energy Cost in USD
        energy_kwh = (power_draw_watts / 1000.0) * duration_hours
        energy_cost_usd = energy_kwh * electricity_rate_kwh_usd

        # 2. Hardware Amortization in USD
        depreciation_rate_per_hour = hardware_capex_usd / max(1.0, hardware_lifespan_hours)
        hardware_depreciation_usd = depreciation_rate_per_hour * duration_hours

        total_cost_usd = energy_cost_usd + hardware_depreciation_usd
        total_cost_subcents = math.ceil(total_cost_usd * self.SUBCENTS_PER_USD)

        metrics = {
            "energy_cost_usd": round(energy_cost_usd, 6),
            "hardware_depreciation_usd": round(hardware_depreciation_usd, 6),
            "total_cost_usd": round(total_cost_usd, 6),
            "min_subcents_floor": total_cost_subcents
        }

        return total_cost_subcents, metrics

    def process_settlement(
        self,
        sender_pubkey: str,
        receiver_pubkey: str,
        amount_subcents: int,
        task_proof_hash: str,
        execution_metrics: Dict[str, Any]
    ) -> Tuple[bool, str]:
        if amount_subcents <= 0:
            return False, "INVALID_AMOUNT_SUB_ZERO"

        sender_balance = self.balances.get(sender_pubkey, 0)
        if sender_balance < amount_subcents:
            return False, "INSUFFICIENT_SENDER_BALANCE"

        # Hardware Depreciation & Energy Pricing Floor Validation
        duration_sec = execution_metrics.get("execution_duration_sec", 1.0)
        power_watts = execution_metrics.get("power_draw_watts", 100.0)
        elec_rate = execution_metrics.get("electricity_rate_kwh_usd", 0.12)
        capex = execution_metrics.get("hardware_capex_usd", 1200.0)
        lifespan_h = execution_metrics.get("hardware_lifespan_hours", 20000.0)

        min_floor_subcents, metrics = self.calculate_compute_cost_floor_subcents(
            execution_duration_sec=duration_sec,
            power_draw_watts=power_watts,
            electricity_rate_kwh_usd=elec_rate,
            hardware_capex_usd=capex,
            hardware_lifespan_hours=lifespan_h
        )

        if amount_subcents < min_floor_subcents:
            return False, f"BOUNTY_BELOW_DEPRECIATION_AND_ENERGY_FLOOR_MIN_{min_floor_subcents}_SUBCENTS"

        # Execute zero-fee settlement
        self.balances[sender_pubkey] = sender_balance - amount_subcents
        self.balances[receiver_pubkey] = self.balances.get(receiver_pubkey, 0) + amount_subcents

        tx_entry = {
            "sender": sender_pubkey,
            "receiver": receiver_pubkey,
            "amount_subcents": amount_subcents,
            "task_proof_hash": task_proof_hash,
            "execution_metrics": execution_metrics,
            "cost_floor_metrics": metrics,
            "prev_tx_hash": self.transactions[-1]["tx_hash"] if self.transactions else "0" * 64
        }

        tx_bytes = json.dumps(tx_entry, sort_keys=True).encode('utf-8')
        tx_entry["tx_hash"] = hashlib.sha256(tx_bytes).hexdigest()
        self.transactions.append(tx_entry)
        return True, "SETTLEMENT_SUCCESSFUL"

    def verify_ledger_integrity(self) -> bool:
        """Verifies hash-chain integrity of settlement ledger."""
        for i, tx in enumerate(self.transactions):
            expected_prev = self.transactions[i - 1]["tx_hash"] if i > 0 else "0" * 64
            if tx["prev_tx_hash"] != expected_prev:
                return False
        return True


def run_settlement_proof() -> bool:
    ledger = SubCentMicroSettlementEngine(ledger_id="SETTLE-LOCAL-01")
    node_a = "pubkey_client_0x1111"
    node_b = "pubkey_worker_node_0x2222"

    ledger.set_balance(node_a, 100000)  # 100 cents = $1.00 USD
    ledger.set_balance(node_b, 0)

    task_hash = hashlib.sha256(b"TASK_EXECUTION_PROOF_101").hexdigest()

    # 1. Test Execution Metrics (10 seconds of 250W compute on $1200 GPU over 20,000hr lifespan @ $0.15/kWh)
    exec_metrics = {
        "execution_duration_sec": 10.0,
        "power_draw_watts": 250.0,
        "electricity_rate_kwh_usd": 0.15,
        "hardware_capex_usd": 1200.0,
        "hardware_lifespan_hours": 20000.0
    }

    # Minimum floor calculation:
    # Energy: (250W / 1000) * (10s / 3600) * $0.15 = $0.000010416
    # Depreciation: ($1200 / 20000hr) * (10s / 3600) = $0.000166666
    # Total Floor = $0.000177083 USD -> ~18 subcents.

    min_floor, details = ledger.calculate_compute_cost_floor_subcents(
        execution_duration_sec=10.0,
        power_draw_watts=250.0,
        electricity_rate_kwh_usd=0.15,
        hardware_capex_usd=1200.0,
        hardware_lifespan_hours=20000.0
    )
    assert min_floor > 0

    # Test rejecting settlement below floor
    failed_success, fail_reason = ledger.process_settlement(
        sender_pubkey=node_a,
        receiver_pubkey=node_b,
        amount_subcents=5,  # 5 subcents is below floor (~18 subcents)
        task_proof_hash=task_hash,
        execution_metrics=exec_metrics
    )
    assert failed_success is False
    assert "BELOW_DEPRECIATION_AND_ENERGY_FLOOR" in fail_reason

    # Test valid settlement above cost floor
    success, msg = ledger.process_settlement(
        sender_pubkey=node_a,
        receiver_pubkey=node_b,
        amount_subcents=500,  # 500 subcents (0.5 cents USD)
        task_proof_hash=task_hash,
        execution_metrics=exec_metrics
    )
    assert success is True
    assert ledger.balances[node_a] == 99500
    assert ledger.balances[node_b] == 500
    assert len(ledger.transactions) == 1
    assert ledger.verify_ledger_integrity() is True

    print("OPEN-SETTLEMENT-v1.0 Hardware Amortization & Thermodynamic Proof Executed Successfully.")
    return True


if __name__ == "__main__":
    assert run_settlement_proof() is True
    print("OPEN-SETTLEMENT-v1.0 Proof Executed Successfully.")
