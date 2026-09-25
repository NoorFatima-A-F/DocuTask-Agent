"""
Priority Evaluator Subsystem.
"""

from app.agents.decision.context import DecisionContext


class PriorityEvaluator:
    @staticmethod
    def resolve_priority(context: DecisionContext) -> str:
        return "MEDIUM"
