"""
Tool Catalog Subsystem.
Provides searchable directory index for tool descriptors, categories, and capability matrices.
"""

from typing import Dict, List, Optional
from app.agents.tools.descriptor import ToolDescriptor
from app.agents.tools.interfaces import IToolRegistry


class ToolCatalog:
    """Catalog directory index providing search and filter utilities over registered tools."""

    def __init__(self, registry: IToolRegistry):
        self.registry = registry

    async def search_by_category(self, category: str) -> List[ToolDescriptor]:
        """Searches tool descriptors by category name."""
        tools = await self.registry.list_tools()
        return [t for t in tools if t.identity.category.upper() == category.upper()]

    async def search_by_provider(self, provider_name: str) -> List[ToolDescriptor]:
        """Searches tool descriptors by provider name."""
        tools = await self.registry.list_tools()
        return [t for t in tools if t.identity.provider_name.upper() == provider_name.upper()]
