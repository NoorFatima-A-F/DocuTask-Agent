"""
Planner Candidate Plan Repository Abstraction.
"""

from typing import Dict, List, Optional
from app.agents.planner.metadata import CandidatePlan


class PlannerRepository:
    """Repository storing generated candidate plans and planning traces."""

    def __init__(self):
        self._store: Dict[str, List[CandidatePlan]] = {}

    async def save_candidates(self, goal_id: str, candidates: List[CandidatePlan]) -> None:
        self._store[goal_id] = candidates

    async def get_candidates(self, goal_id: str) -> Optional[List[CandidatePlan]]:
        return self._store.get(goal_id)
