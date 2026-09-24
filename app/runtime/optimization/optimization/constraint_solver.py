"""
Constraint Solver for Phase 13.6 (ARIA-EOP).
Validates operational constraints (budget, deadline, confidence floors, concurrency ceilings) for candidate strategies.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class ConstraintCheckResult(BaseModel):
    is_satisfied: bool = True
    violations: List[str] = Field(default_factory=list)
    constraint_margins: Dict[str, float] = Field(default_factory=dict)


class ConstraintSolver:
    """
    Solves and validates multidimensional operational constraints for plan execution candidates.
    """

    @classmethod
    def solve(
        cls,
        candidate_cost: float,
        candidate_latency_ms: float,
        candidate_confidence: float,
        candidate_concurrency: int,
        max_budget_usd: float = 0.50,
        max_latency_ms: float = 5000.0,
        min_confidence: float = 0.85,
        max_concurrency: int = 16,
    ) -> ConstraintCheckResult:
        violations = []
        margins = {}

        # Budget Check
        budget_margin = round(max_budget_usd - candidate_cost, 4)
        margins["budget_margin_usd"] = budget_margin
        if candidate_cost > max_budget_usd:
            violations.append(f"Cost ${candidate_cost:.4f} exceeds max budget ${max_budget_usd:.4f}")

        # Latency / Deadline Check
        latency_margin = round(max_latency_ms - candidate_latency_ms, 1)
        margins["latency_margin_ms"] = latency_margin
        if candidate_latency_ms > max_latency_ms:
            violations.append(f"Latency {candidate_latency_ms:.1f}ms exceeds max deadline {max_latency_ms:.1f}ms")

        # Confidence Floor Check
        conf_margin = round(candidate_confidence - min_confidence, 4)
        margins["confidence_margin"] = conf_margin
        if candidate_confidence < min_confidence:
            violations.append(f"Confidence {candidate_confidence:.3f} below floor {min_confidence:.3f}")

        # Concurrency Ceiling Check
        margins["concurrency_headroom"] = float(max_concurrency - candidate_concurrency)
        if candidate_concurrency > max_concurrency:
            violations.append(f"Concurrency {candidate_concurrency} exceeds limit {max_concurrency}")

        return ConstraintCheckResult(
            is_satisfied=len(violations) == 0,
            violations=violations,
            constraint_margins=margins,
        )
