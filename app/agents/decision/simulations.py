"""
Decision Simulator Subsystem for Dry-Run Evaluations.
"""

from app.agents.decision.context import DecisionContext
from app.agents.decision.engine import DecisionEngine, DecisionResult


class DecisionSimulator:
    """Simulator running dry-run policy and decision evaluations."""

    def __init__(self, engine: DecisionEngine):
        self.engine = engine

    async def simulate_evaluation(self, context: DecisionContext) -> DecisionResult:
        return await self.engine.evaluate(context)
