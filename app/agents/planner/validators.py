"""
Planner Fail-Fast Request Validators.
"""

from app.agents.planner.context import PlannerRequest
from app.agents.planner.exceptions import GoalAnalysisException


class PlannerRequestValidator:
    """Fail-fast validator for PlannerRequest models."""

    @staticmethod
    def validate_request(request: PlannerRequest) -> None:
        if not request.goal.name or not request.goal.name.strip():
            raise GoalAnalysisException("Goal name cannot be empty.")
        if request.context.planning_budget_usd < 0:
            raise GoalAnalysisException("Planning budget cannot be negative.")
