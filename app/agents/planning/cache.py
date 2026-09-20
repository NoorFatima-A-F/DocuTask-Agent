"""
Planning Cache Subsystem.
"""

from typing import Dict, Optional
from uuid import UUID
from app.agents.planning.contracts import Plan


class PlanCache:
    """In-memory cache for fast Plan retrieval."""

    def __init__(self):
        self._cache: Dict[UUID, Plan] = {}

    def get(self, plan_id: UUID) -> Optional[Plan]:
        return self._cache.get(plan_id)

    def set(self, plan_id: UUID, plan: Plan) -> None:
        self._cache[plan_id] = plan

    def clear(self) -> None:
        self._cache.clear()
