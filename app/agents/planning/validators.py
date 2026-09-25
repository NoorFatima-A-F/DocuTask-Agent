"""
Plan Fail-Fast Structural Validators.
"""

from app.agents.planning.contracts import Plan
from app.agents.planning.exceptions import PlanValidationException


class PlanStructuralValidator:
    """Fail-fast validator for Plan aggregates."""

    @staticmethod
    def validate_plan_structure(plan: Plan) -> None:
        if not plan.name or not plan.name.strip():
            raise PlanValidationException("Plan name cannot be empty.")
        if plan.statistics.estimated_cost_usd < 0:
            raise PlanValidationException("Plan estimated cost cannot be negative.")
