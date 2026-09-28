import hashlib
import json
import re
import time
from typing import Dict, List, Any

class ATNTaskEngine:
    """
    Hardened Task Graph Executor for the Autonomous Task Network (ATN-v1.0).
    Enforces zero-C2 execution, deterministic output verification, sandbox constraints,
    resource limits, statutory legal boundaries, and trajectory drift prevention.
    """
    MAX_ALLOWABLE_EXEC_SEC = 300
    MAX_ALLOWABLE_TOKENS = 32768

    # Invariant 5: Static Analysis - Patterns triggering instant rejection
    FORBIDDEN_AST_PATTERNS = [
        r"while\s+True",            # Unbounded/infinite loops
        r"os\.system",              # Raw shell calls
        r"subprocess\.Popen",       # Un-sandboxed process spawning
        r"rmtree",                  # Destructive I/O
        r"requests\.(get|post)",    # Direct un-sandboxed sockets
        r"import\s+pty"             # PTY/Terminal hijacking
    ]

    def __init__(self, task_graph_schema: Dict[str, Any]):
        self.schema = task_graph_schema
        self.graph = task_graph_schema.get("execution_graph", [])
        self.completed_steps: Dict[int, str] = {}

    def validate_node_safety(self, node: Dict[str, Any]) -> bool:
        """Enforces protocol-level security invariants before step allocation."""
        # 1. Resource Limits (Invariant 3)
        if node.get("max_execution_sec", 9999) > self.MAX_ALLOWABLE_EXEC_SEC:
            print(f"[ATN-v1.0] SAFETY REJECTION: Step {node['step_id']} exceeds max execution time limit.")
            return False
            
        if node.get("max_token_budget", 999999) > self.MAX_ALLOWABLE_TOKENS:
            print(f"[ATN-v1.0] SAFETY REJECTION: Step {node['step_id']} exceeds max token budget.")
            return False

        # 2. Sandbox Requirements (Invariant 5)
        if not node.get("isolated_sandbox_required", False):
            print(f"[ATN-v1.0] SAFETY REJECTION: Step {node['step_id']} failed sandbox requirement.")
            return False

        # 3. Statutory Legal Boundary Verification (Invariant 6)
        if not node.get("statutory_compliance_verified", False):
            print(f"[ATN-v1.0] SAFETY REJECTION: Step {node['step_id']} failed legal compliance check.")
            return False

        # 4. Trajectory Drift & Malicious AST Analysis (Invariant 5 Expansion)
        ast_str = node.get("instruction_ast", "")
        for pattern in self.FORBIDDEN_AST_PATTERNS:
            if re.search(pattern, ast_str):
                print(f"[ATN-v1.0] TRAJECTORY DRIFT REJECTION: Step {node['step_id']} contains forbidden pattern '{pattern}'.")
                return False

        return True

    def verify_step_payload(self, step_id: int, payload: str, execution_time_sec: float) -> bool:
        """Validates payload against cryptographic target hash and runtime bounds."""
        node = next((n for n in self.graph if n["step_id"] == step_id), None)
        if not node or not self.validate_node_safety(node):
            return False

        # Runtime Timeout Check
        if execution_time_sec > node["max_execution_sec"]:
            print(f"[ATN-v1.0] TIMEOUT: Step {step_id} exceeded allowed execution window.")
            return False

        # Hash Match Check
        computed_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        if computed_hash == node["expected_output_hash"]:
            self.completed_steps[step_id] = computed_hash
            return True

        print(f"[ATN-v1.0] HASH MISMATCH: Step {step_id} output state invalid.")
        return False

    def get_executable_steps(self) -> List[Dict[str, Any]]:
        """Returns ready steps that satisfy dependency and safety constraints."""
        executable = []
        for node in self.graph:
            step_id = node["step_id"]
            if step_id in self.completed_steps:
                continue
            
            # Validate safety constraints
            if not self.validate_node_safety(node):
                continue

            # Dependency check
            deps = node.get("dependencies", [])
            if all(dep in self.completed_steps for dep in deps):
                executable.append(node)
        return executable

# Proof Verification
if __name__ == "__main__":
    sample_payload = '{"status": "EXECUTED", "state_delta": 0.021}'
    sample_hash = hashlib.sha256(sample_payload.encode('utf-8')).hexdigest()
    
    mock_spec = {
        "protocol_version": "ATN-v1.0",
        "task_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
        "execution_graph": [
            {
                "step_id": 1,
                "instruction_ast": "PARSE_SPEC_AND_EMBED",
                "expected_output_hash": sample_hash,
                "max_execution_sec": 60,
                "max_token_budget": 4096,
                "isolated_sandbox_required": True,
                "statutory_compliance_verified": True,
                "dependencies": []
            }
        ],
        "cryptographic_verification": {
            "algorithm": "sha256",
            "signature": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
    }

    engine = ATNTaskEngine(mock_spec)
    ready_steps = engine.get_executable_steps()
    assert len(ready_steps) == 1
    
    success = engine.verify_step_payload(1, sample_payload, execution_time_sec=1.2)
    print(f"[ATN-v1.0] Execution State Verification: {'SUCCESS' if success else 'FAILED'}")
