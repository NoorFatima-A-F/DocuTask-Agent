"""
Candidate Plan Evaluator.
"""

from typing import List
from app.agents.planner.context import PlannerContext
from app.agents.planner.metadata import CandidatePlan
from app.agents.planner.scoring import PlanCandidateScorer


class CandidateEvaluator:
    """Evaluates multiple candidate plans against user budget and context requirements."""

    def __init__(self):
        self.scorer = PlanCandidateScorer()

    def evaluate_candidates(self, candidates: List[CandidatePlan], context: PlannerContext) -> List[CandidatePlan]:
        evaluated = []
        for cand in candidates:
            score = self.scorer.score_candidate(cand)
            # Budget check
            if cand.estimated_cost_usd <= context.planning_budget_usd:
                evaluated.append(
                    CandidatePlan(
                        candidate_id=cand.candidate_id,
                        plan=cand.plan,
                        strategy_used=cand.strategy_used,
                        rank_score=round(score, 3),
                        estimated_cost_usd=cand.estimated_cost_usd,
                        estimated_duration_seconds=cand.estimated_duration_seconds,
                        confidence=cand.confidence
                    )
                )
        return evaluated
