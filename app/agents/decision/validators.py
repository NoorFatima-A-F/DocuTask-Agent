"""
Decision Validator Guards.
"""

from app.agents.decision.context import DecisionContext
from app.agents.decision.exceptions import DecisionEvaluationException


class DecisionValidator:
    @staticmethod
    def validate_context(context: DecisionContext) -> None:
        if context.estimated_cost_usd < 0:
            raise DecisionEvaluationException("Estimated cost cannot be negative.")
