"""
Agent Goal Manager Interface.
Defines contract for setting, decomposing, and tracking agent execution goals.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.context import AgentContext


class AgentGoalManager(ABC):
    """Abstract interface for agent goal management."""

    @abstractmethod
    async def set_goal(self, goal_statement: str, context: AgentContext) -> Dict[str, Any]:
        """Sets and validates the primary agent execution goal."""
        pass

    @abstractmethod
    async def decompose_goal(self, goal_statement: str, context: AgentContext) -> List[str]:
        """Decomposes goal into sub-goals."""
        pass
