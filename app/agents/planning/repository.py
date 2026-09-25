"""
Planning Repository Domain Abstraction.
"""

from typing import Dict, Optional
from uuid import UUID
from app.agents.planning.contracts import Plan
from app.agents.planning.interfaces import IPlanRepository


class PlanRepository(IPlanRepository):
    """In-memory thread-safe plan repository, cloud-database compatible."""

    def __init__(self):
        self._store: Dict[UUID, Plan] = {}

    async def save(self, plan: Plan) -> None:
        self._store[plan.identity.plan_id] = plan

    async def get(self, plan_id: UUID) -> Optional[Plan]:
        return self._store.get(plan_id)
