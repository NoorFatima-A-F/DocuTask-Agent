"""
Plan Candidate Scorer.
Computes multi-dimensional fitness scores across cost, duration, confidence, and complexity.
"""

from app.agents.planner.metadata import CandidatePlan


class PlanCandidateScorer:
    """Evaluates candidate plan quality."""

    def score_candidate(self, candidate: CandidatePlan) -> float:
        cost_weight = 0.3
        duration_weight = 0.3
        confidence_weight = 0.4

        cost_score = max(0.0, 1.0 - (candidate.estimated_cost_usd / 10.0))
        duration_score = max(0.0, 1.0 - (candidate.estimated_duration_seconds / 60.0))
        confidence_score = candidate.confidence

        return (cost_score * cost_weight) + (duration_score * duration_weight) + (confidence_score * confidence_weight)
