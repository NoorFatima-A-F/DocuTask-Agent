"""
Intelligent Planner Core Interfaces.
Defines IIntelligentPlanner, IPlanningPipeline, and IPlanningEngine.
"""

from abc import ABC, abstractmethod
from app.agents.planner.context import PlannerRequest
from app.agents.planning.contracts import Plan, PlanningResult


class IIntelligentPlanner(ABC):
    """Abstract Cognitive Intelligent Planner Interface."""

    @abstractmethod
    async def plan(self, request: PlannerRequest) -> PlanningResult:
        """Decomposes goal and synthesizes an optimized, validated PlanGraph."""
        pass


class IPlanningPipeline(ABC):
    """Abstract Planning Multi-Stage Pipeline Interface."""

    @abstractmethod
    async def execute_pipeline(self, request: PlannerRequest) -> Plan:
        """Executes full planning pipeline through analysis, decomposition, ranking, and reflection."""
        pass
