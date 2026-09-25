"""
Agent Planner Interface.
Defines contract for generating execution plans from goals.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.context import AgentContext


class AgentPlanner(ABC):
    """Abstract interface for agent goal planning engine."""

    @abstractmethod
    async def create_plan(self, goal: str, context: AgentContext) -> List[Dict[str, Any]]:
        """Generates a structured execution plan from a goal statement."""
        pass
