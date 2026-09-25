"""
Coordination Planner Adapter.
Bridges multi-agent coordination layer with the Intelligent Planner.
Requests hierarchical task decompositions without containing planning logic.
"""

from typing import Any, Dict, List, Optional


class CoordinationPlannerAdapter:
    """Adapter requesting task graphs and decompositions from the Intelligent Planner."""

    def __init__(self, planner: Optional[Any] = None):
        self._planner = planner

    async def request_plan_decomposition(self, goal: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Requests goal decomposition into subtasks."""
        if self._planner and hasattr(self._planner, "plan"):
            res = await self._planner.plan(goal)
            return getattr(res, "tasks", [])
        return [{"task_id": "subtask_1", "task_name": f"Execute: {goal[:30]}"}]
