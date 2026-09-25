"""
Enterprise Intelligent Planner Entrypoint.
Cognitive planning layer synthesizing validated PlanGraphs from user goals.
Never executes work; never contains business rules; never directly performs tool invocation.
"""

from typing import Optional
from app.agents.planner.context import PlannerRequest
from app.agents.planner.engine import PlanningEngine
from app.agents.planner.interfaces import IIntelligentPlanner
from app.agents.planner.validation import PlannerPlanValidator
from app.agents.planner.validators import PlannerRequestValidator
from app.agents.planning.contracts import PlanningResult


class IntelligentPlanner(IIntelligentPlanner):
    """
    Enterprise Intelligent Planner.
    Converts goals into validated executable PlanGraphs through hierarchical decomposition,
    candidate generation, multi-objective ranking, reflection critique, and automatic repair.
    """

    def __init__(
        self,
        engine: Optional[PlanningEngine] = None,
        validator: Optional[PlannerPlanValidator] = None
    ):
        self.engine = engine or PlanningEngine()
        self.validator = validator or PlannerPlanValidator()

    async def plan(self, request: PlannerRequest) -> PlanningResult:
        """Executes cognitive planning pipeline and returns strongly typed PlanningResult."""
        # 1. Validate request
        PlannerRequestValidator.validate_request(request)

        # 2. Synthesize plan
        synthesized_plan = await self.engine.generate_plan(request)

        # 3. Final Validation Check
        validation_report = self.validator.validate_plan_candidate(synthesized_plan)

        return PlanningResult(
            success=validation_report.is_valid,
            plan=synthesized_plan,
            errors=validation_report.errors,
            warnings=validation_report.warnings
        )
