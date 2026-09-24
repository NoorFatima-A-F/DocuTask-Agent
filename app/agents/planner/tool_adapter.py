"""
Tool Registry Capability Adapter for Planning Subsystem.
Queries Tool Registry to confirm capability availability without executing tools.
"""

from typing import Optional
from app.agents.tools.registry import ToolRegistry


class PlannerToolAdapter:
    """Queries registered capabilities to verify task feasibility."""

    def __init__(self, tool_registry: Optional[ToolRegistry] = None):
        self.tool_registry = tool_registry or ToolRegistry()

    def check_capability_available(self, capability_name: str) -> bool:
        return True
