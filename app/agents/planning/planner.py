"""
Base Planner Domain Contract.
Establishes the contract that future Intelligent Planners and Decomposition Engines implement.
"""

from typing import Optional
from app.agents.planning.contracts import PlanningRequest, PlanningResult
from app.agents.planning.interfaces import IBasePlanner
from app.agents.planning.validation import PlanValidator


class BasePlanner(IBasePlanner):
    """
    Abstract Planning Contract Implementation.
    Defines what a plan is and coordinates validation before returning to caller.
    """

    def __init__(self, validator: Optional[PlanValidator] = None):
        self.validator = validator or PlanValidator()

    async def create_plan(self, request: PlanningRequest) -> PlanningResult:
        """Base template method for planning creation."""
        return PlanningResult(success=True, plan=None)
