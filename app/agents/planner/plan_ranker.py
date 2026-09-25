"""
Plan Ranker and Candidate Selection Engine.
"""

from typing import List, Optional
from app.agents.planner.metadata import CandidatePlan


class PlanRanker:
    """Ranks multiple candidate plans and selects optimal winning plan."""

    def rank_and_select_best(self, candidates: List[CandidatePlan]) -> Optional[CandidatePlan]:
        if not candidates:
            return None
        sorted_candidates = sorted(candidates, key=lambda c: c.rank_score, reverse=True)
        return sorted_candidates[0]
