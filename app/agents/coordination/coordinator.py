"""
Agent Coordinator.
Coordinates discovery, team formation, delegation planning, and distributed execution.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.capability_matcher import CapabilityRequirement
from app.agents.coordination.delegation import DelegationMode, DelegationRequest, DelegationResult, DelegationTask
from app.agents.coordination.delegation_executor import DelegationExecutor
from app.agents.coordination.delegation_planner import DelegationPlanner
from app.agents.coordination.formation import TeamFormationEngine
from app.agents.coordination.interfaces import IAgentCoordinator
from app.agents.coordination.team import Team


class AgentCoordinator(IAgentCoordinator):
    """Orchestrates capability discovery, team formation, and delegation execution across agents."""

    def __init__(
        self,
        registry: AgentRegistry,
        planner: Optional[DelegationPlanner] = None,
        executor: Optional[DelegationExecutor] = None,
        formation_engine: Optional[TeamFormationEngine] = None
    ):
        self.registry = registry
        self.planner = planner or DelegationPlanner()
        self.executor = executor or DelegationExecutor(registry=registry)
        self.formation_engine = formation_engine or TeamFormationEngine()

    async def coordinate(self, request: Any) -> DelegationResult:
        """Coordinates task delegation across available registered agents."""
        available = await self.registry.list_available()
        if not available:
            # Return failed delegation if no agents registered
            return DelegationResult(
                delegation_id=request.delegation_id,
                status="FAILED",
                errors=["No available agents in registry."]
            )

        # 1. Plan delegation
        planned_tasks = self.planner.plan_delegation(request, available)
        planned_request = request.model_copy(update={"tasks": planned_tasks})

        # 2. Execute delegation
        result = await self.executor.delegate_task(planned_request)
        return result
