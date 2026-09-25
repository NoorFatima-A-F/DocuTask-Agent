"""
Decision Adapter for Recovery Subsystem.
Queries DecisionEngine to clear recovery strategies against governance, cost, and compliance policies.
"""

from app.agents.decision.context import DecisionContext
from app.agents.decision.engine import DecisionEngine, DecisionResult


class RecoveryDecisionAdapter:
    """Decoupled adapter evaluating recovery policy compliance with DecisionEngine."""

    def __init__(self, decision_engine: DecisionEngine | None = None):
        self.decision_engine = decision_engine or DecisionEngine()

    async def evaluate_recovery_authorization(self, strategy_name: str, estimated_cost_usd: float) -> DecisionResult:
        ctx = DecisionContext(
            action_type="RECOVERY_EVALUATION",
            estimated_cost_usd=estimated_cost_usd
        )
        return await self.decision_engine.evaluate(ctx)
