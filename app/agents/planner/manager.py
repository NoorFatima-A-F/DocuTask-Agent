"""
Planner Manager Orchestrator.
"""

from typing import Optional
from app.agents.planner.cache import PlannerCache
from app.agents.planner.context import PlannerRequest
from app.agents.planner.planner import IntelligentPlanner
from app.agents.planner.repository import PlannerRepository
from app.agents.planning.contracts import PlanningResult


class PlannerManager:
    """Manager orchestrating intelligent planner instances, caching, and repository persistence."""

    def __init__(
        self,
        planner: Optional[IntelligentPlanner] = None,
        cache: Optional[PlannerCache] = None,
        repository: Optional[PlannerRepository] = None
    ):
        self.planner = planner or IntelligentPlanner()
        self.cache = cache or PlannerCache()
        self.repository = repository or PlannerRepository()

    async def generate_plan(self, request: PlannerRequest) -> PlanningResult:
        return await self.planner.plan(request)
