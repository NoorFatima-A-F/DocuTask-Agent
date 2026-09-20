"""
Agent State Manager Interface.
Defines contract for persisting and transitioning agent state.
"""

from abc import ABC, abstractmethod
from app.agents.context import AgentContext
from app.agents.state import AgentState


class AgentStateManager(ABC):
    """Abstract interface for agent state persistence and management."""

    @abstractmethod
    async def get_state(self, context: AgentContext) -> AgentState:
        """Retrieves current agent state."""
        pass

    @abstractmethod
    async def transition(self, target_state: AgentState, context: AgentContext) -> None:
        """Transitions agent state and persists change."""
        pass
