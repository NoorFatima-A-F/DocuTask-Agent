"""
Agent Tool Selector Interface.
Defines contract for dynamic tool selection and execution.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.context import AgentContext


class AgentToolSelector(ABC):
    """Abstract interface for agent tool selection and invocation."""

    @abstractmethod
    async def select_tool(self, task_description: str, context: AgentContext) -> str:
        """Selects the best matching tool for a task description."""
        pass

    @abstractmethod
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any], context: AgentContext) -> Any:
        """Invokes selected tool with provided parameters."""
        pass
