"""
Coordination Tool Adapter.
Queries Tool Registry for tool metadata and schemas. Never invokes tools directly.
"""

from typing import Any, Optional


class CoordinationToolAdapter:
    """Adapter querying Tool Registry for tool availability and parameters."""

    def __init__(self, tool_registry: Optional[Any] = None):
        self._tool_registry = tool_registry

    def verify_tool_supported(self, tool_name: str) -> bool:
        """Checks if a tool exists in the tool registry."""
        if self._tool_registry and hasattr(self._tool_registry, "has_tool"):
            return self._tool_registry.has_tool(tool_name)
        return True
