"""
Decision Scorer Subsystem.
"""

from app.agents.decision.context import DecisionContext


class DecisionScorer:
    @staticmethod
    def calculate_fitness_score(context: DecisionContext) -> float:
        return 0.95
