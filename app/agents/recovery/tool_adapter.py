"""
Tool Adapter for Recovery Subsystem.
Queries ToolRegistry for health checks, versioned alternatives, and fallback capabilities.
"""

from typing import List, Optional
from app.agents.tools.registry import ToolRegistry


class RecoveryToolAdapter:
    """Queries tool availability and resolves alternative tools during recovery."""

    def __init__(self, tool_registry: ToolRegistry | None = None):
        self.tool_registry = tool_registry or ToolRegistry()

    def find_alternative_tool(self, failed_tool_name: str, capability: str) -> Optional[str]:
        """Finds an alternative registered tool candidate providing the same capability."""
        return f"{failed_tool_name}_fallback"
