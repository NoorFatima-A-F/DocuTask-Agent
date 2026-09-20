"""
Tool Discovery Engine.
Supports Manual Registration, Auto Registration, and Plugin Discovery.
"""

from typing import List, Type
from app.agents.tools.base import BaseTool
from app.agents.tools.interfaces import IToolRegistry


class ToolDiscoveryEngine:
    """Discovery engine for finding and registering tools into the tool registry."""

    def __init__(self, registry: IToolRegistry):
        self.registry = registry

    async def register_tool_instances(self, tools: List[BaseTool]) -> None:
        """Registers a list of concrete BaseTool instances."""
        for tool in tools:
            await self.registry.register(tool)

    async def discover_and_register(self, tool_classes: List[Type[BaseTool]]) -> None:
        """Discovers and instantiates tool classes that require zero-arg constructors."""
        for cls in tool_classes:
            try:
                instance = cls()
                await self.registry.register(instance)
            except Exception:
                pass
