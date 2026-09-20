"""
Planner Candidate Cache Subsystem.
"""

from typing import Dict, List, Optional
from app.agents.planner.metadata import CandidatePlan


class PlannerCache:
    """In-memory cache for plan candidates and evaluation results."""

    def __init__(self):
        self._cache: Dict[str, List[CandidatePlan]] = {}

    def get_candidates(self, goal_id: str) -> Optional[List[CandidatePlan]]:
        return self._cache.get(goal_id)

    def set_candidates(self, goal_id: str, candidates: List[CandidatePlan]) -> None:
        self._cache[goal_id] = candidates

    def clear(self) -> None:
        self._cache.clear()
