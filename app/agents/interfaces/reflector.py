"""
Agent Reflector Interface.
Defines contract for self-reflection, accuracy evaluation, and strategy adjustment.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.context import AgentContext


class AgentReflector(ABC):
    """Abstract interface for agent self-reflection engine."""

    @abstractmethod
    async def reflect(self, observation: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Evaluates execution quality, accuracy, and determines next actions or replanning."""
        pass
