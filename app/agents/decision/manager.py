"""
Decision Manager Orchestrator.
"""

from typing import Optional
from app.agents.decision.context import DecisionContext
from app.agents.decision.engine import DecisionEngine, DecisionResult


class DecisionManager:
    """Manager orchestrating decision evaluations and caching."""

    def __init__(self, engine: Optional[DecisionEngine] = None):
        self.engine = engine or DecisionEngine()

    async def evaluate_decision(self, context: DecisionContext) -> DecisionResult:
        return await self.engine.evaluate(context)
