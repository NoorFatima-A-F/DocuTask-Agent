"""
Workflow Coordination Adapter.
Bridges Workflow Runtime with the Multi-Agent Coordination layer (app.agents.coordination).
Enables orchestrating multi-agent collaboration sessions, swarms, and team executions within workflow stages.
"""

from typing import Any, Dict, Optional


class WorkflowCoordinationAdapter:
    """Adapter delegating multi-agent coordination steps to the Coordination Engine."""

    def __init__(self, coordination_engine: Optional[Any] = None) -> None:
        self._engine = coordination_engine

    async def coordinate_agents(
        self,
        goal: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Dispatches a multi-agent goal to the coordination engine."""
        if self._engine and hasattr(self._engine, "coordinate"):
            result = await self._engine.coordinate(goal, parameters or {})
            return result if isinstance(result, dict) else {"result": str(result)}
        return {
            "status": "COMPLETED",
            "adapter": "WorkflowCoordinationAdapter",
            "goal": goal,
        }
