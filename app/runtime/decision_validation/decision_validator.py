"""
Decision Validation Engine - Unified Decision Validator
Validates candidate plans before dispatch across constraints, invariants, monotonicity, and schema versioning.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

from app.runtime.decision_validation.invariants import InvariantChecker
from app.runtime.constraints.feasibility_engine import FeasibilityEngine


@dataclass
class PreDispatchValidationResult:
    is_approved: bool
    constraint_compliance: bool
    invariant_compliance: bool
    feature_completeness: bool
    policy_version_valid: bool
    errors: List[str]
    certificate_hash: str


class DecisionValidator:
    """Pre-execution validation engine asserting safety, compliance, and mathematical soundness."""

    @classmethod
    def validate_plan_for_dispatch(
        cls,
        plan: Dict[str, Any],
        constraints: Dict[str, float],
        features: Dict[str, float],
        policy_version: str = "v1.0.0",
    ) -> PreDispatchValidationResult:
        errors = []

        # 1. Constraint satisfaction
        metrics = {
            "cost_usd": plan.get("cost_usd", 0.01),
            "latency_ms": plan.get("latency_ms", 1000.0),
            "accuracy": plan.get("accuracy", 0.95),
            "overall_risk": plan.get("overall_risk", 0.05),
        }
        feas_res = FeasibilityEngine.evaluate(metrics, constraints)
        if not feas_res.is_feasible:
            errors.extend(feas_res.violated_constraints)

        # 2. Invariant checks
        inv_ok, inv_errors = InvariantChecker.check_decision_invariants(plan)
        if not inv_ok:
            errors.extend(inv_errors)

        # 3. Feature completeness
        feat_ok = len(features) >= 10
        if not feat_ok:
            errors.append(f"Incomplete feature vector: provided only {len(features)} features (minimum 10 required).")

        # 4. Policy version check
        policy_ok = bool(policy_version and policy_version.startswith("v"))
        if not policy_ok:
            errors.append(f"Invalid policy version: {policy_version}")

        is_approved = len(errors) == 0

        import hashlib
        import json
        cert_data = json.dumps({"plan": plan, "errors": errors, "approved": is_approved}, sort_keys=True)
        cert_hash = hashlib.sha256(cert_data.encode()).hexdigest()[:16]

        return PreDispatchValidationResult(
            is_approved=is_approved,
            constraint_compliance=feas_res.is_feasible,
            invariant_compliance=inv_ok,
            feature_completeness=feat_ok,
            policy_version_valid=policy_ok,
            errors=errors,
            certificate_hash=cert_hash,
        )
