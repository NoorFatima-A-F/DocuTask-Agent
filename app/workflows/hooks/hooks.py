"""
Workflow Execution Lifecycle Hooks.
"""

from typing import Any, Callable, Dict, List, Optional
from ..domain.models import ExecutionRecord, TaskDefinition, TaskExecutionRecord


class WorkflowHooks:
    """Registry for workflow execution lifecycle interceptors."""

    def __init__(self):
        self._before_start: List[Callable[[ExecutionRecord], Any]] = []
        self._before_task: List[Callable[[str, TaskDefinition, Dict[str, Any]], Any]] = []
        self._after_task: List[Callable[[str, TaskExecutionRecord], Any]] = []
        self._on_failure: List[Callable[[ExecutionRecord, Exception], Any]] = []
        self._on_completion: List[Callable[[ExecutionRecord], Any]] = []
        self._on_compensation: List[Callable[[str, str], Any]] = []

    def on_before_start(self, fn: Callable[[ExecutionRecord], Any]) -> None:
        self._before_start.append(fn)

    def on_before_task(self, fn: Callable[[str, TaskDefinition, Dict[str, Any]], Any]) -> None:
        self._before_task.append(fn)

    def on_after_task(self, fn: Callable[[str, TaskExecutionRecord], Any]) -> None:
        self._after_task.append(fn)

    def on_failure_hook(self, fn: Callable[[ExecutionRecord, Exception], Any]) -> None:
        self._on_failure.append(fn)

    def on_completion_hook(self, fn: Callable[[ExecutionRecord], Any]) -> None:
        self._on_completion.append(fn)

    def trigger_before_start(self, execution: ExecutionRecord) -> None:
        for fn in self._before_start:
            fn(execution)

    def trigger_after_task(self, execution_id: str, task_rec: TaskExecutionRecord) -> None:
        for fn in self._after_task:
            fn(execution_id, task_rec)

    def trigger_completion(self, execution: ExecutionRecord) -> None:
        for fn in self._on_completion:
            fn(execution)
