"""
Agent Observer Interface.
Defines contract for inspecting execution results and environmental feedback.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.context import AgentContext


class AgentObserver(ABC):
    """Abstract interface for agent environment observation engine."""

    @abstractmethod
    async def observe(self, execution_output: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Observes execution results and collects environmental feedback."""
        pass
