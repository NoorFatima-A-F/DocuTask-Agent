"""
Scientific Constraints - Constraint Validator
Enforces pre-dispatch assertions preventing any non-compliant candidate plan from executing.
"""

from typing import Dict
from app.runtime.constraints.feasibility_engine import FeasibilityEngine


class ConstraintViolationError(ValueError):
    """Raised when a selected plan violates hard operational boundaries."""
    pass


class ConstraintValidator:
    """Validates candidate plans against operational and business rules."""

    @staticmethod
    def assert_feasible(candidate_metrics: Dict[str, float], constraints: Dict[str, float]) -> None:
        eval_res = FeasibilityEngine.evaluate(candidate_metrics, constraints)
        if not eval_res.is_feasible:
            raise ConstraintViolationError(
                f"Candidate plan violates hard constraints: {'; '.join(eval_res.violated_constraints)}"
            )
