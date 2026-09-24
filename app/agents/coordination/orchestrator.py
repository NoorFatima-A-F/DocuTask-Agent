"""
Coordination Orchestrator.
Coordinates teams, swarms, consensus evaluations, and multi-agent workflows.
"""

from typing import Any, Optional
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.coordinator import AgentCoordinator
from app.agents.coordination.swarm import SwarmEngine


class CoordinationOrchestrator:
    """High-level orchestrator coordinating team workflows, swarms, and distributed allocations."""

    def __init__(
        self,
        registry: AgentRegistry,
        coordinator: Optional[AgentCoordinator] = None,
        swarm_engine: Optional[SwarmEngine] = None
    ):
        self.registry = registry
        self.coordinator = coordinator or AgentCoordinator(registry=registry)
        self.swarm_engine = swarm_engine or SwarmEngine()

    async def execute_coordinated_workflow(self, request: Any) -> Any:
        """Executes a coordinated multi-agent workflow."""
        return await self.coordinator.coordinate(request)
