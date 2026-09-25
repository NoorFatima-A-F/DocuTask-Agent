"""
Planning Subsystem Core Interfaces.
Defines IPlanManager, IPlanValidator, IPlanRepository, and IBasePlanner.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.agents.planning.contracts import Plan, PlanningRequest, PlanningResult


class IPlanValidator(ABC):
    """Abstract interface for Plan and DAG validation."""
    @abstractmethod
    def validate_plan(self, plan: Plan) -> List[str]:
        pass


class IPlanRepository(ABC):
    """Abstract interface for Plan persistence."""
    @abstractmethod
    async def save(self, plan: Plan) -> None:
        pass

    @abstractmethod
    async def get(self, plan_id: UUID) -> Optional[Plan]:
        pass


class IBasePlanner(ABC):
    """Abstract Base Planner defining planning generation contracts."""
    @abstractmethod
    async def create_plan(self, request: PlanningRequest) -> PlanningResult:
        pass


class IPlanManager(ABC):
    """Abstract interface for Plan Lifecycle Management."""
    @abstractmethod
    async def register_plan(self, plan: Plan) -> Plan:
        pass

    @abstractmethod
    async def get_plan(self, plan_id: UUID) -> Optional[Plan]:
        pass
