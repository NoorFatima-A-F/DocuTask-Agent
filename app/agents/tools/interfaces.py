"""
Tool Subsystem Interfaces.
Defines contracts for ToolRegistry, CapabilityResolver, ToolSelector, and ToolDiscoveryEngine.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.agents.tools.base import BaseTool
from app.agents.tools.capabilities import CapabilityMatch, CapabilityRequirement
from app.agents.tools.descriptor import ToolDescriptor
from app.agents.tools.policies import SelectionPolicy


class IToolRegistry(ABC):
    """Abstract interface for Tool Registry."""

    @abstractmethod
    async def register(self, tool: BaseTool) -> None:
        """Registers a tool in the registry."""
        pass

    @abstractmethod
    async def deregister(self, tool_id: str) -> None:
        """Deregisters a tool from the registry."""
        pass

    @abstractmethod
    async def get_tool(self, tool_id: str) -> Optional[BaseTool]:
        """Retrieves a registered tool by tool ID."""
        pass

    @abstractmethod
    async def list_tools(self) -> List[ToolDescriptor]:
        """Lists all registered tool descriptors."""
        pass


class ICapabilityResolver(ABC):
    """Abstract interface for Capability Resolver."""

    @abstractmethod
    async def resolve(self, requirement: CapabilityRequirement) -> List[CapabilityMatch]:
        """Resolves capability requirements against registered tools and returns ranked candidates."""
        pass


class IToolSelector(ABC):
    """Abstract interface for Tool Selector."""

    @abstractmethod
    async def select(
        self,
        requirement: CapabilityRequirement,
        policy: Optional[SelectionPolicy] = None
    ) -> Optional[BaseTool]:
        """Selects the best matching tool for a capability requirement using selection policies."""
        pass
