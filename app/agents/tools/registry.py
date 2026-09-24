"""
Thread-Safe & Async-Safe Tool Registry Implementation.
Indexes tools by Tool ID, Capability, Provider, and Category.
"""

import asyncio
from typing import Dict, List, Optional, Set
from app.agents.tools.base import BaseTool
from app.agents.tools.descriptor import ToolDescriptor
from app.agents.tools.exceptions import ToolValidationException
from app.agents.tools.interfaces import IToolRegistry


class ToolRegistry(IToolRegistry):
    """
    Production-grade Thread-Safe Tool Registry.
    Maintains primary tool dictionary and indexes for fast capability/category/provider lookup.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._capability_index: Dict[str, Set[str]] = {}
        self._category_index: Dict[str, Set[str]] = {}
        self._provider_index: Dict[str, Set[str]] = {}
        self._lock = asyncio.Lock()

    async def register(self, tool: BaseTool) -> None:
        """Registers tool and updates indexes thread-safely."""
        if not tool or not tool.tool_id:
            raise ToolValidationException("Cannot register tool with missing or empty tool_id.")

        async with self._lock:
            self._tools[tool.tool_id] = tool

            # Index by category
            category = tool.category.upper()
            if category not in self._category_index:
                self._category_index[category] = set()
            self._category_index[category].add(tool.tool_id)

            # Index by provider
            provider = tool.provider_name.upper()
            if provider not in self._provider_index:
                self._provider_index[provider] = set()
            self._provider_index[provider].add(tool.tool_id)

            # Index by capabilities
            for cap in tool.descriptor.metadata.supported_capabilities:
                cap_upper = cap.upper()
                if cap_upper not in self._capability_index:
                    self._capability_index[cap_upper] = set()
                self._capability_index[cap_upper].add(tool.tool_id)

    async def deregister(self, tool_id: str) -> None:
        """Deregisters tool and cleans up index entries thread-safely."""
        async with self._lock:
            tool = self._tools.pop(tool_id, None)
            if not tool:
                return

            # Clean category index
            category = tool.category.upper()
            if category in self._category_index:
                self._category_index[category].discard(tool_id)

            # Clean provider index
            provider = tool.provider_name.upper()
            if provider in self._provider_index:
                self._provider_index[provider].discard(tool_id)

            # Clean capability index
            for cap in tool.descriptor.metadata.supported_capabilities:
                cap_upper = cap.upper()
                if cap_upper in self._capability_index:
                    self._capability_index[cap_upper].discard(tool_id)

    async def get_tool(self, tool_id: str) -> Optional[BaseTool]:
        """Retrieves registered tool instance by ID."""
        async with self._lock:
            return self._tools.get(tool_id)

    async def list_tools(self) -> List[ToolDescriptor]:
        """Lists all registered tool descriptors."""
        async with self._lock:
            return [tool.descriptor for tool in self._tools.values()]

    async def find_by_capability(self, capability_name: str) -> List[BaseTool]:
        """Fast lookup of registered tools matching a capability name."""
        cap_upper = capability_name.upper()
        async with self._lock:
            tool_ids = self._capability_index.get(cap_upper, set())
            return [self._tools[tid] for tid in tool_ids if tid in self._tools]
