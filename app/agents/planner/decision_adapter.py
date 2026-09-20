"""
Decision Engine Adapter for Planning Subsystem.
Delegates policy compliance, risk checks, and budget evaluations to DecisionEngine.
"""

from typing import Optional
from app.agents.decision.context import DecisionContext
from app.agents.decision.engine import DecisionEngine, DecisionResult


class PlannerDecisionAdapter:
    """Adapts DecisionEngine evaluations for plan constraint satisfaction."""

    def __init__(self, decision_engine: Optional[DecisionEngine] = None):
        self.decision_engine = decision_engine or DecisionEngine()

    async def evaluate_plan_feasibility(self, estimated_cost_usd: float) -> DecisionResult:
        ctx = DecisionContext(action_type="PLAN_EVALUATION", estimated_cost_usd=estimated_cost_usd)
        return await self.decision_engine.evaluate(ctx)
