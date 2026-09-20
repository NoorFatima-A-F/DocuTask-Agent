"""
Agent Recovery Engine Interface.
Defines contract for exception recovery, state rollback, and exponential backoff retry handling.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.context import AgentContext


class AgentRecoveryEngine(ABC):
    """Abstract interface for agent failure recovery engine."""

    @abstractmethod
    async def recover(self, exception: Exception, context: AgentContext) -> Dict[str, Any]:
        """Attempts recovery strategy for an execution exception."""
        pass
