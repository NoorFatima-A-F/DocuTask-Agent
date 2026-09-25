"""
Budget Evaluator Subsystem.
"""

from app.agents.decision.costing import CostEstimate
from app.agents.decision.policies import CostPolicy


class CostBudgetEvaluator:
    """Evaluates cost estimates against budget policies."""

    @staticmethod
    def evaluate_budget(estimate: CostEstimate, policy: CostPolicy) -> bool:
        return estimate.estimated_cost_usd <= policy.max_cost_per_execution_usd
