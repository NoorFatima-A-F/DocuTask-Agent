"""
Nested Workflow Executor.
Coordinates execution of nested workflows with depth checking and variable passing.
"""

from typing import Any, Callable, Coroutine, Dict, List, Optional
from uuid import UUID
from app.agents.workflow.exceptions import WorkflowException
from app.agents.workflow.workflow_instance import WorkflowInstance


class NestedWorkflowExecutor:
    """Executes workflows within nested scopes, guarding against infinite recursion."""

    def __init__(self, max_depth: int = 5) -> None:
        self.max_depth = max_depth

    def validate_nesting_depth(self, current_depth: int) -> None:
        """Ensures nesting depth does not exceed configured maximum."""
        if current_depth >= self.max_depth:
            raise WorkflowException(
                f"Maximum workflow nesting depth exceeded: {current_depth} >= {self.max_depth}"
            )

    async def execute_nested(
        self,
        caller_instance: WorkflowInstance,
        nested_request: Any,
        executor_func: Callable[[Any], Coroutine[Any, Any, Any]],
        current_depth: int = 1,
    ) -> Any:
        """Executes a nested workflow and returns result."""
        self.validate_nesting_depth(current_depth)
        return await executor_func(nested_request)
