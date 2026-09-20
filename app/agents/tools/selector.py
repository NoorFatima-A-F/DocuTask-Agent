"""
Tool Selector Component.
Selects optimal tool candidate based on SelectionPolicy strategies (Highest Confidence, Lowest Cost, Lowest Latency, Hybrid Weighted).
"""

from typing import Optional
from app.agents.tools.base import BaseTool
from app.agents.tools.capabilities import CapabilityRequirement
from app.agents.tools.interfaces import ICapabilityResolver, IToolRegistry, IToolSelector
from app.agents.tools.policies import SelectionPolicy, SelectionStrategyEnum


class ToolSelector(IToolSelector):
    """Engine executing tool selection strategies for planners and executors."""

    def __init__(self, resolver: ICapabilityResolver, registry: IToolRegistry):
        self.resolver = resolver
        self.registry = registry

    async def select(
        self,
        requirement: CapabilityRequirement,
        policy: Optional[SelectionPolicy] = None
    ) -> Optional[BaseTool]:
        """Resolves capability matches and selects optimal tool using active selection policy."""
        matches = await self.resolver.resolve(requirement)
        if not matches:
            return None

        pol = policy or SelectionPolicy()

        if pol.strategy == SelectionStrategyEnum.HIGHEST_CONFIDENCE:
            selected_match = max(matches, key=lambda m: m.score.confidence_score)
        elif pol.strategy == SelectionStrategyEnum.LOWEST_COST:
            selected_match = max(matches, key=lambda m: m.score.cost_score)
        elif pol.strategy == SelectionStrategyEnum.LOWEST_LATENCY:
            selected_match = max(matches, key=lambda m: m.score.latency_score)
        else:  # HYBRID_WEIGHTED or default
            selected_match = matches[0]  # Resolver already ranks by overall hybrid score

        return await self.registry.get_tool(selected_match.tool_id)
