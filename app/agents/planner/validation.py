"""
Planner Plan Validation Engine.
"""

from typing import List
from app.agents.planning.contracts import Plan
from app.agents.planning.validation import GraphValidationResult, PlanValidator


class PlannerPlanValidator:
    """Validates plan candidates before final presentation."""

    def __init__(self):
        self.validator = PlanValidator()

    def validate_plan_candidate(self, plan: Plan) -> GraphValidationResult:
        return self.validator.validate_and_report(plan)
