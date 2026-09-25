"""
Tool Ecosystem Injectable Factory.
Instantiates and wires ToolRegistry, CapabilityResolver, ToolSelector, and ToolHealthMonitor.
"""

from app.agents.tools.health import ToolHealthMonitor
from app.agents.tools.registry import ToolRegistry
from app.agents.tools.resolver import CapabilityResolver
from app.agents.tools.selector import ToolSelector


class ToolFactory:
    """Factory container wiring tool ecosystem components."""

    @staticmethod
    def create_tool_ecosystem():
        """Creates and wires a complete tool ecosystem tuple (registry, resolver, selector, health_monitor)."""
        registry = ToolRegistry()
        resolver = CapabilityResolver(registry=registry)
        selector = ToolSelector(resolver=resolver, registry=registry)
        health_monitor = ToolHealthMonitor()
        return registry, resolver, selector, health_monitor
