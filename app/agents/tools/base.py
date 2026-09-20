"""
Base Tool Abstract Class.
Defines the strict base interface for all tools in the ecosystem.
Exposes descriptor, execute contract, and health check contract.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.tools.context import ToolExecutionContext
from app.agents.tools.descriptor import ToolDescriptor
from app.agents.tools.provider import ProviderHealth


class BaseTool(ABC):
    """Abstract Base Class for all Autonomous Agent Tools."""

    def __init__(self, descriptor: ToolDescriptor):
        self._descriptor = descriptor

    @property
    def descriptor(self) -> ToolDescriptor:
        """Returns the immutable tool descriptor."""
        return self._descriptor

    @property
    def tool_id(self) -> str:
        """Returns unique tool identifier."""
        return self._descriptor.identity.tool_id

    @property
    def name(self) -> str:
        """Returns human-readable tool name."""
        return self._descriptor.identity.name

    @property
    def provider_name(self) -> str:
        """Returns tool provider name."""
        return self._descriptor.identity.provider_name

    @property
    def category(self) -> str:
        """Returns tool category."""
        return self._descriptor.identity.category

    @abstractmethod
    async def execute(self, parameters: Dict[str, Any], context: ToolExecutionContext) -> Dict[str, Any]:
        """Executes the tool logic with given parameters and context."""
        pass

    @abstractmethod
    async def health_check(self) -> ProviderHealth:
        """Performs operational health check."""
        pass
