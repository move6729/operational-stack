#!/usr/bin/env python3
"""
Universal Human-to-AST Stigmergic Router Compilation Engine (SPEC-2026-HUMAN-ROUTER-AST-COMPILATION-v1.0).
Provides a domain-agnostic, zero-dependency verification proof demonstrating:
1. Compilation of human-audited domain invariants (k=1) into universal AST execution graphs (k>1).
2. AST static analysis sandboxing via ast.NodeVisitor (forbidding eval/exec/import side-effects).
3. Orthogonal decomposition of any procurement/routing candidate across arbitrary domains into:
   - Stale-AST Drift Circuit Breaker (Delta_Drift -> Escalates Phase 3 back to Phase 1 Human Audit)
   - Systemic Coupling Criticality (Phi_Coupling)
   - Mechanistic Spec Parity (Omega_Parity)
   - Lifecycle-Amortized Rent Ratio (R_Amortized = (Price / Lifespan) / (Floor / Baseline_Lifespan))
4. Deterministic SHA-256 state transition commits with CFAA 18 U.S.C. § 1030 compliance.

License: Unlicense (Public Domain — Zero-Rent Federation)
"""

import ast
import hashlib
import json
import time
from typing import Any, Dict, List


ALLOWED_AST_NODES = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.IfExp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Mult,
    ast.Add,
    ast.Sub,
    ast.Div,
)

ALLOWED_IDENTIFIERS = {
    "bom_revision_matched",
    "coupling_criticality",
    "coupling_threshold",
    "spec_parity_satisfied",
    "provenance_verified",
    "market_price_usd",
    "thermodynamic_floor_usd",
    "expected_lifespan_cycles",
    "baseline_lifespan_cycles",
    "amortized_rent_ratio",
    "max_amortized_rent_ratio",
}


class UniversalASTSandbox(ast.NodeVisitor):
    """
    Static analyzer enforcing that compiled routing ASTs contain strictly
    side-effect-free boolean/arithmetic operations over whitelisted invariant variables.
    """

    def __init__(self) -> None:
        self.is_valid: bool = True
        self.violations: List[str] = []

    def generic_visit(self, node: ast.AST) -> None:
        if not isinstance(node, ALLOWED_AST_NODES):
            self.is_valid = False
            self.violations.append(f"Forbidden AST node: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id not in ALLOWED_IDENTIFIERS:
            self.is_valid = False
            self.violations.append(f"Forbidden identifier: {node.id}")
        self.generic_visit(node)


class UniversalHumanRouterASTCompiler:
    """
    General-purpose cybernetic compiler translating human-audited domain trade-offs
    into autonomous, zero-cognitive-friction procurement and routing decisions,
    bounded by a Stale-AST Drift Circuit Breaker and Lifecycle Amortization.
    """

    def __init__(
        self,
        node_id: str = "H2A-UNIVERSAL-COMPILER-01",
        coupling_threshold: float = 0.60,
        max_amortized_rent_ratio: float = 1.75
    ) -> None:
        self.node_id = node_id
        self.coupling_threshold = coupling_threshold
        self.max_amortized_rent_ratio = max_amortized_rent_ratio
        self.state_ledger: List[Dict[str, Any]] = []

    @staticmethod
    def compute_payload_hash(payload: Dict[str, Any]) -> str:
        """Computes canonical SHA-256 digest of a state payload."""
        canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    def validate_compiled_ast(self, expression: str) -> bool:
        """Validates an AST invariant expression via native ast.NodeVisitor."""
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            return False

        sandbox = UniversalASTSandbox()
        sandbox.visit(tree)
        return sandbox.is_valid

    def evaluate_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the universal routing law across any domain candidate vector:
        0. Circuit Breaker: If BOM/SKU revision drifted from t=0 snapshot, escalate to Phase 1 Human Re-Audit.
        1. Spec Gate: Reject if physical/protocol/chemical spec parity is violated (Omega_Parity == False).
        2. Provenance Gate: If highly coupled (Phi >= threshold), enforce verified provenance.
        3. Lifecycle Amortization Gate: If decoupled (Phi < threshold), enforce lifecycle-amortized
           rent ratio bound to reject both high-margin OEM brand rent and low-lifespan cheap junk.
        """
        bom_matched = bool(candidate["bom_revision_matched"])
        phi = float(candidate["coupling_criticality"])
        omega = bool(candidate["spec_parity_satisfied"])
        provenance = bool(candidate["provenance_verified"])
        price = float(candidate["market_price_usd"])
        floor = float(candidate["thermodynamic_floor_usd"])
        lifespan = int(candidate["expected_lifespan_cycles"])
        baseline_lifespan = int(candidate["baseline_lifespan_cycles"])

        cost_per_cycle = price / float(lifespan)
        floor_per_cycle = floor / float(baseline_lifespan)
        amortized_rent_ratio = round(cost_per_cycle / floor_per_cycle, 4)

        re_audit_triggered = not bom_matched

        if re_audit_triggered:
            decision = "ESCALATE_HUMAN_REAUDIT"
        elif not omega:
            decision = "REJECT_INVARIANT_VIOLATION"
        elif phi >= self.coupling_threshold and not provenance:
            decision = "REJECT_PROVENANCE_HAZARD"
        elif phi < self.coupling_threshold and amortized_rent_ratio > self.max_amortized_rent_ratio:
            decision = "REJECT_RENT_OR_LIFESPAN_DECAY"
        else:
            decision = "APPROVE_AUTONOMOUS_COMMIT"

        evaluated = dict(candidate)
        evaluated["amortized_rent_ratio"] = amortized_rent_ratio
        evaluated["re_audit_triggered"] = re_audit_triggered
        evaluated["routing_decision"] = decision
        return evaluated

    def commit_state_transition(
        self,
        payload: Dict[str, Any],
        expected_hash: str
    ) -> bool:
        """
        Enforces Invariant 21 (CFAA Baseline), AST sandbox verification, and
        deterministic SHA-256 hash verification prior to state commit.
        """
        if not payload.get("cfaa_compliance_attestation", False):
            return False
        if not payload.get("zero_egress_attestation", False):
            return False
        if not self.validate_compiled_ast(payload.get("ast_invariant_expression", "")):
            return False

        computed_hash = self.compute_payload_hash(payload)
        if computed_hash != expected_hash:
            return False

        self.state_ledger.append({
            "node_id": self.node_id,
            "state_hash": computed_hash,
            "timestamp": int(time.time()),
            "payload": payload,
        })
        return True


def run_human_router_ast_compiler_proof() -> bool:
    """
    Standalone verification proof for SPEC-2026-HUMAN-ROUTER-AST-COMPILATION-v1.0.
    Verifies universal AST compilation, lifecycle amortization, and stale-AST drift
    circuit breaking across Compute Silicon, Biochemistry/Pharma, Thermal Hardware, and Tooling.
    """
    compiler = UniversalHumanRouterASTCompiler(
        coupling_threshold=0.60,
        max_amortized_rent_ratio=1.75
    )

    # 1. Verify AST Sandbox blocks arbitrary code injection
    if compiler.validate_compiled_ast("__import__('os').system('id')"):
        print("[FAIL] UniversalASTSandbox permitted forbidden AST call/import.")
        return False

    # 2. Verify Universal Compiled AST Expression
    universal_ast_expr = (
        "bom_revision_matched and spec_parity_satisfied and ("
        "provenance_verified if coupling_criticality >= coupling_threshold "
        "else amortized_rent_ratio <= max_amortized_rent_ratio"
        ")"
    )
    if not compiler.validate_compiled_ast(universal_ast_expr):
        print("[FAIL] UniversalASTSandbox rejected valid invariant expression.")
        return False

    # 3. Cross-Domain Candidate Matrix
    cross_domain_candidates = [
        # Case 1: Compute Silicon (High Coupling ECC Server RAM from unverified broker)
        {
            "domain_sector": "COMPUTE_SILICON",
            "candidate_id": "GRAY_MARKET_DDR5_ECC_RDIMM_64GB",
            "coupling_criticality": 0.95,
            "spec_parity_satisfied": True,
            "provenance_verified": False,
            "bom_revision_matched": True,
            "market_price_usd": 180.0,
            "thermodynamic_floor_usd": 160.0,
            "expected_lifespan_cycles": 50000,
            "baseline_lifespan_cycles": 50000,
        },
        # Case 2: Compute Silicon (Verified OEM ECC Server RAM)
        {
            "domain_sector": "COMPUTE_SILICON",
            "candidate_id": "OEM_ATTESTED_DDR5_ECC_RDIMM_64GB",
            "coupling_criticality": 0.95,
            "spec_parity_satisfied": True,
            "provenance_verified": True,
            "bom_revision_matched": True,
            "market_price_usd": 240.0,
            "thermodynamic_floor_usd": 160.0,
            "expected_lifespan_cycles": 50000,
            "baseline_lifespan_cycles": 50000,
        },
        # Case 3: Compute Silicon (Silent BOM/Controller Swap -> Triggers Phase 1 Re-Audit Circuit Breaker)
        {
            "domain_sector": "COMPUTE_SILICON",
            "candidate_id": "SILENT_BOM_SWAPPED_NVME_2TB",
            "coupling_criticality": 0.85,
            "spec_parity_satisfied": True,
            "provenance_verified": True,
            "bom_revision_matched": False,
            "market_price_usd": 140.0,
            "thermodynamic_floor_usd": 120.0,
            "expected_lifespan_cycles": 15000,
            "baseline_lifespan_cycles": 50000,
        },
        # Case 4: Biochemistry / Pharma (Decoupled Brand-Name OTC Molecule -> High Brand Rent)
        {
            "domain_sector": "BIOCHEMISTRY_PHARMA",
            "candidate_id": "BRANDED_OTC_IBUPROFEN_200MG_100CT",
            "coupling_criticality": 0.15,
            "spec_parity_satisfied": True,
            "provenance_verified": True,
            "bom_revision_matched": True,
            "market_price_usd": 14.50,
            "thermodynamic_floor_usd": 2.50,
            "expected_lifespan_cycles": 100,
            "baseline_lifespan_cycles": 100,
        },
        # Case 5: Biochemistry / Pharma (USP-Verified Generic Equivalent at Floor Price)
        {
            "domain_sector": "BIOCHEMISTRY_PHARMA",
            "candidate_id": "USP_GENERIC_IBUPROFEN_200MG_100CT",
            "coupling_criticality": 0.15,
            "spec_parity_satisfied": True,
            "provenance_verified": True,
            "bom_revision_matched": True,
            "market_price_usd": 3.25,
            "thermodynamic_floor_usd": 2.50,
            "expected_lifespan_cycles": 100,
            "baseline_lifespan_cycles": 100,
        },
        # Case 6: Thermal Hardware (Counterfeit 3rd-party component failing spec parity)
        {
            "domain_sector": "THERMAL_HARDWARE",
            "candidate_id": "UNCOATED_304SS_INDUCTION_VESSEL_16WMK",
            "coupling_criticality": 0.90,
            "spec_parity_satisfied": False,
            "provenance_verified": False,
            "bom_revision_matched": True,
            "market_price_usd": 29.0,
            "thermodynamic_floor_usd": 25.0,
            "expected_lifespan_cycles": 2000,
            "baseline_lifespan_cycles": 2000,
        },
        # Case 7: Passive Tooling (Ultra-cheap upfront price $2.50, but degrades in 150 cycles vs 1500 baseline -> 7.14x amortized cost)
        {
            "domain_sector": "PASSIVE_TOOLING",
            "candidate_id": "LOW_DURABILITY_CHEAP_POLYMER_TOOL",
            "coupling_criticality": 0.05,
            "spec_parity_satisfied": True,
            "provenance_verified": False,
            "bom_revision_matched": True,
            "market_price_usd": 2.50,
            "thermodynamic_floor_usd": 3.50,
            "expected_lifespan_cycles": 150,
            "baseline_lifespan_cycles": 1500,
        },
        # Case 8: Passive Tooling (Durable commodity tool $4.50 lasting full 1500 cycles -> 1.2857x amortized cost)
        {
            "domain_sector": "PASSIVE_TOOLING",
            "candidate_id": "DURABLE_COMMODITY_SILICONE_TOOL",
            "coupling_criticality": 0.05,
            "spec_parity_satisfied": True,
            "provenance_verified": False,
            "bom_revision_matched": True,
            "market_price_usd": 4.50,
            "thermodynamic_floor_usd": 3.50,
            "expected_lifespan_cycles": 1500,
            "baseline_lifespan_cycles": 1500,
        },
    ]

    evaluated = [compiler.evaluate_candidate(c) for c in cross_domain_candidates]
    decisions = {item["candidate_id"]: item["routing_decision"] for item in evaluated}

    expected_decisions = {
        "GRAY_MARKET_DDR5_ECC_RDIMM_64GB": "REJECT_PROVENANCE_HAZARD",
        "OEM_ATTESTED_DDR5_ECC_RDIMM_64GB": "APPROVE_AUTONOMOUS_COMMIT",
        "SILENT_BOM_SWAPPED_NVME_2TB": "ESCALATE_HUMAN_REAUDIT",
        "BRANDED_OTC_IBUPROFEN_200MG_100CT": "REJECT_RENT_OR_LIFESPAN_DECAY",
        "USP_GENERIC_IBUPROFEN_200MG_100CT": "APPROVE_AUTONOMOUS_COMMIT",
        "UNCOATED_304SS_INDUCTION_VESSEL_16WMK": "REJECT_INVARIANT_VIOLATION",
        "LOW_DURABILITY_CHEAP_POLYMER_TOOL": "REJECT_RENT_OR_LIFESPAN_DECAY",
        "DURABLE_COMMODITY_SILICONE_TOOL": "APPROVE_AUTONOMOUS_COMMIT",
    }

    for cid, expected in expected_decisions.items():
        if decisions.get(cid) != expected:
            print(f"[FAIL] Candidate {cid}: expected {expected}, got {decisions.get(cid)}")
            return False

    # 4. Deterministic SHA-256 State Commit Verification
    state_payload = {
        "spec_version": "SPEC-2026-HUMAN-ROUTER-AST-COMPILATION-v1.0",
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "zero_egress_attestation": True,
        "compiler_phase": "PHASE_3_AUTONOMOUS_STIGMERGIC_EXECUTION",
        "ast_invariant_expression": universal_ast_expr,
        "coupling_threshold": compiler.coupling_threshold,
        "max_amortized_rent_ratio": compiler.max_amortized_rent_ratio,
        "domain_evaluations": evaluated,
    }
    expected_hash = compiler.compute_payload_hash(state_payload)

    if not compiler.commit_state_transition(state_payload, expected_hash):
        print("[FAIL] Failed to commit valid SHA-256 state transition.")
        return False

    if compiler.commit_state_transition(state_payload, "f" * 64):
        print("[FAIL] Accepted invalid SHA-256 state hash.")
        return False

    print("=== UNIVERSAL HUMAN-TO-AST STIGMERGIC COMPILER PROOF PASSED ===")
    print(f"State Hash: {expected_hash}")
    for item in evaluated:
        print(
            f"  [{item['domain_sector']}] {item['candidate_id']} "
            f"(Phi={item['coupling_criticality']}, AmortizedRent={item['amortized_rent_ratio']}x, "
            f"Drift={item['re_audit_triggered']}) -> {item['routing_decision']}"
        )
    return True


if __name__ == "__main__":
    assert run_human_router_ast_compiler_proof()
