"""
Agent Registry.
Thread-safe catalog managing active, registered, and retired agents in the platform.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.exceptions import AgentNotFoundError, DuplicateAgentIdError
from app.agents.coordination.interfaces import IAgentRegistry
from app.agents.coordination.lifecycle import AgentLifecycleState


class AgentRegistry(IAgentRegistry):
    """Registry maintaining active agent instances with fail-fast duplicate checks."""

    def __init__(self):
        self._agents: Dict[UUID, Agent] = {}

    async def register(self, agent: Agent) -> None:
        """Registers a new agent instance, failing fast on duplicate IDs."""
        if agent.agent_id in self._agents:
            raise DuplicateAgentIdError(f"Agent with ID {agent.agent_id} is already registered.", agent.agent_id)
        registered_agent = agent.transition_to(AgentLifecycleState.AVAILABLE)
        self._agents[agent.agent_id] = registered_agent

    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Retrieves an agent by its UUID."""
        return self._agents.get(agent_id)

    async def list_available(self) -> List[Agent]:
        """Returns all agents currently in the AVAILABLE lifecycle state."""
        return [
            a for a in self._agents.values()
            if a.state == AgentLifecycleState.AVAILABLE
        ]

    async def update_agent(self, agent: Agent) -> None:
        """Updates agent record in registry."""
        if agent.agent_id not in self._agents:
            raise AgentNotFoundError(f"Agent {agent.agent_id} not found in registry.", agent.agent_id)
        self._agents[agent.agent_id] = agent

    async def unregister(self, agent_id: UUID) -> None:
        """Retires and unregisters an agent."""
        if agent_id in self._agents:
            self._agents[agent_id] = self._agents[agent_id].transition_to(AgentLifecycleState.RETIRED)

    def size(self) -> int:
        """Returns count of registered agents."""
        return len(self._agents)
