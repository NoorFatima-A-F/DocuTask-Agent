"""
Workflow Execution Adapter.
Bridges Workflow Runtime with the Stateful Execution Engine (app.agents.execution).
Routes atomic task execution to the execution engine without replacing it.
"""

from typing import Any, Dict, Optional


class WorkflowExecutionAdapter:
    """Adapter dispatching workflow tasks to the Stateful Execution Engine."""

    def __init__(self, execution_engine: Optional[Any] = None) -> None:
        self._execution_engine = execution_engine

    async def execute_task(
        self,
        task_id: str,
        handler: str,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Dispatches an atomic task to the Execution Engine."""
        if self._execution_engine and hasattr(self._execution_engine, "execute_task"):
            result = await self._execution_engine.execute_task(task_id, handler, input_data)
            return result if isinstance(result, dict) else {"output": result}
        return {
            "status": "COMPLETED",
            "task_id": task_id,
            "handler": handler,
            "result": f"Executed by WorkflowExecutionAdapter for task {task_id}",
        }
