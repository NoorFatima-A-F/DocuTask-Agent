"""
Workflow Planner Adapter.
Bridges Workflow Runtime with Intelligent Planner (app.agents.planner / app.agents.planning).
Enables dynamic on-demand plan generation within workflow stages.
"""

from typing import Any, Dict, Optional


class WorkflowPlannerAdapter:
    """Adapter delegating goal decomposition to the Intelligent Planner."""

    def __init__(self, planner: Optional[Any] = None) -> None:
        self._planner = planner

    async def plan_goal(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Requests the Intelligent Planner to generate a plan for a workflow step."""
        if self._planner and hasattr(self._planner, "create_plan"):
            plan_result = await self._planner.create_plan(goal, context or {})
            return {"status": "SUCCESS", "plan": plan_result}
        return {
            "status": "SUCCESS",
            "adapter": "WorkflowPlannerAdapter",
            "goal": goal,
            "tasks": ["step-1", "step-2"],
        }
