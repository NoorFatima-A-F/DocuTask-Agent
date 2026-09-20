"""
Planning Manager Subsystem Orchestrator.
Orchestrates plan validation, repository persistence, caching, and lifecycle state management.
"""

from typing import Optional
from uuid import UUID
from app.agents.planning.cache import PlanCache
from app.agents.planning.contracts import Plan
from app.agents.planning.interfaces import IPlanManager, IPlanRepository, IPlanValidator
from app.agents.planning.repository import PlanRepository
from app.agents.planning.validation import PlanValidator


class PlanManager(IPlanManager):
    """
    Enterprise Plan Manager.
    Unified orchestrator managing plan registration, caching, persistence, and validation.
    """

    def __init__(
        self,
        repository: Optional[IPlanRepository] = None,
        validator: Optional[IPlanValidator] = None,
        cache: Optional[PlanCache] = None
    ):
        self.repository = repository or PlanRepository()
        self.validator = validator or PlanValidator()
        self.cache = cache or PlanCache()

    async def register_plan(self, plan: Plan) -> Plan:
        """Validates and persists a plan instance."""
        errors = self.validator.validate_plan(plan)
        if errors:
            raise ValueError(f"Plan validation failed: {'; '.join(errors)}")

        await self.repository.save(plan)
        self.cache.set(plan.identity.plan_id, plan)
        return plan

    async def get_plan(self, plan_id: UUID) -> Optional[Plan]:
        """Retrieves plan from cache or persistent repository."""
        cached = self.cache.get(plan_id)
        if cached:
            return cached
        plan = await self.repository.get(plan_id)
        if plan:
            self.cache.set(plan_id, plan)
        return plan
