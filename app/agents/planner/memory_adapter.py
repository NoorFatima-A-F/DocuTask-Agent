"""
Read-Only Memory Adapter for Planning Subsystem.
Planner queries historical plans, performance statistics, and reflections without mutating memory.
"""

from typing import Any, Dict, List, Optional
from app.agents.memory.manager import MemoryManager


class PlannerMemoryAdapter:
    """Read-only memory adapter retrieving execution history and historical successful plans."""

    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        self.memory_manager = memory_manager

    async def get_historical_workflows(self, goal_topic: str) -> List[Dict[str, Any]]:
        if not self.memory_manager:
            return []
        items = await self.memory_manager.search(goal_topic, top_k=3)
        return [{"key": item.key, "value": item.value} for item in items]
