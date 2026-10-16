import datetime
import hashlib
import json
import os
from typing import Any, Dict, List


class TemporalCommitShieldEngine:
    """
    Bare-Metal Sovereign Temporal Commit Shield & Monotonic Past-Jitter Engine.
    Implements OPSTACK-KERNEL-v2.2 Invariants 4, 6, 20, 21, 22, 24, 25.
    Prevents cadence fingerprinting and timezone leakage while maintaining
    strict DAG order (T_{n-1} <= T_n <= T_now <= T_push).
    """

    def __init__(self, config: Dict[str, Any]):
        self.jurisdiction_context = config.get("jurisdiction_context", "US")
        self.cfaa_compliant = config.get("cfaa_compliance_attestation", False)
        if not self.cfaa_compliant:
            raise ValueError("CFAA compliance attestation required (18 U.S.C. § 1030).")

        self.fuzz_mode = config.get("fuzz_mode", "MONOTONIC_CADENCE_JITTER")
        self.max_lookback_s = int(config.get("max_lookback_window_seconds", 1800))
        self.force_utc = config.get("force_utc_zero_offset", True)
        if not self.force_utc:
            raise ValueError("UTC zero-offset normalization is mandatory (Invariant 4).")

    @staticmethod
    def _draw_uint16_entropy() -> int:
        """Draws 16 bits of local CSPRNG/hardware entropy without external network calls."""
        return int.from_bytes(os.urandom(2), byteorder="big")

    def compute_fuzzed_timestamp(self, now_epoch: int, parent_epoch: int = 0) -> Dict[str, Any]:
        """
        Computes a fuzzed UTC timestamp guaranteed to satisfy:
        parent_epoch <= fuzzed_epoch <= now_epoch
        """
        if now_epoch < parent_epoch:
            raise ValueError("Clock skew violation: now_epoch < parent_epoch")

        if self.fuzz_mode == "CIRCADIAN_UTC_MIDNIGHT_CLAMP":
            utc_midnight = (now_epoch // 86400) * 86400
            fuzzed_ts = max(utc_midnight, parent_epoch + 1)
            fuzzed_ts = min(fuzzed_ts, now_epoch)
        else:
            min_ts = max(now_epoch - self.max_lookback_s, parent_epoch)
            span = now_epoch - min_ts
            if span > 1:
                rand_val = self._draw_uint16_entropy()
                fuzzed_ts = min_ts + 1 + (rand_val % (span - 1))
            else:
                fuzzed_ts = now_epoch

        iso_utc = datetime.datetime.fromtimestamp(
            fuzzed_ts, tz=datetime.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "parent_epoch": parent_epoch,
            "fuzzed_epoch": fuzzed_ts,
            "now_epoch": now_epoch,
            "iso_8601_utc": iso_utc,
            "monotonic_valid": parent_epoch <= fuzzed_ts <= now_epoch,
            "timezone_stripped": iso_utc.endswith("Z"),
        }

    def simulate_commit_sequence(self, raw_commit_epochs: List[int]) -> List[Dict[str, Any]]:
        """Simulates a sequence of commits to verify DAG monotonicity."""
        history: List[Dict[str, Any]] = []
        last_fuzzed = 0
        for now_ts in raw_commit_epochs:
            res = self.compute_fuzzed_timestamp(now_epoch=now_ts, parent_epoch=last_fuzzed)
            history.append(res)
            last_fuzzed = res["fuzzed_epoch"]
        return history

    def commit_state_transition(
        self, event_id: str, execution_payload: Dict[str, Any], expected_hash: str
    ) -> bool:
        """Cryptographically verifies state transition via SHA-256."""
        payload_bytes = json.dumps(execution_payload, sort_keys=True).encode("utf-8")
        computed_hash = hashlib.sha256(payload_bytes).hexdigest()
        return computed_hash == expected_hash


def run_temporal_commit_shield_proof() -> bool:
    """Executable standalone proof verifying temporal fuzzing bounds."""
    config = {
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "fuzz_mode": "MONOTONIC_CADENCE_JITTER",
        "max_lookback_window_seconds": 1800,
        "force_utc_zero_offset": True,
    }
    engine = TemporalCommitShieldEngine(config)

    raw_epochs = [1792166400, 1792166402, 1792166402, 1792167000, 1792169000]
    seq = engine.simulate_commit_sequence(raw_epochs)
    prev_ts = 0
    for item in seq:
        assert item["monotonic_valid"] is True
        assert item["timezone_stripped"] is True
        assert prev_ts <= item["fuzzed_epoch"] <= item["now_epoch"]
        prev_ts = item["fuzzed_epoch"]

    payload = {"event_id": "commit_fuzz_001", "verified": True}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    assert engine.commit_state_transition("commit_fuzz_001", payload, digest) is True

    return True


if __name__ == "__main__":
    passed = run_temporal_commit_shield_proof()
    print(f"TEMPORAL_COMMIT_SHIELD_PROOF: {'PASSED' if passed else 'FAILED'}")
    assert passed
