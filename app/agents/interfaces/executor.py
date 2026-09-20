"""
Agent Executor Interface.
Defines contract for executing planned steps.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.context import AgentContext


class AgentExecutor(ABC):
    """Abstract interface for agent task execution engine."""

    @abstractmethod
    async def execute_steps(self, plan: List[Dict[str, Any]], context: AgentContext) -> Dict[str, Any]:
        """Executes a list of planned steps within the agent context."""
        pass
