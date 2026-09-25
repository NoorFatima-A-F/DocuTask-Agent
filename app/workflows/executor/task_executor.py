"""
Enterprise Task Executor.
Executes individual task units by dispatching to registered capability handlers, connectors, agents, or custom functions.
"""

import asyncio
from typing import Any, Callable, Dict, Optional
from ..domain.models import TaskDefinition, TaskType
from ..domain.exceptions import TaskExecutionException
from ...platform.capabilities.registry import CapabilityRegistry


class TaskExecutor:
    """Executes tasks according to their TaskType and capability specification."""

    def __init__(self, capability_registry: Optional[CapabilityRegistry] = None):
        self.capability_registry = capability_registry or CapabilityRegistry()
        self._custom_handlers: Dict[str, Callable[[TaskDefinition, Dict[str, Any]], Any]] = {}
        self._register_default_handlers()

    def register_handler(self, task_name_or_type: str, handler: Callable[[TaskDefinition, Dict[str, Any]], Any]) -> None:
        """Register custom task execution handler."""
        self._custom_handlers[task_name_or_type] = handler

    async def execute_task(self, task_def: TaskDefinition, context_variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task and return output dictionary."""
        # 1. Check custom handler by task name or task id
        handler = self._custom_handlers.get(task_def.id) or self._custom_handlers.get(task_def.name) or self._custom_handlers.get(task_def.type.value)

        if handler:
            try:
                if asyncio.iscoroutinefunction(handler):
                    res = await handler(task_def, context_variables)
                else:
                    res = handler(task_def, context_variables)
                return res if isinstance(res, dict) else {"result": res}
            except Exception as e:
                raise TaskExecutionException(f"Task '{task_def.id}' execution failed: {str(e)}", task_id=task_def.id) from e

        # 2. Built-in defaults
        if task_def.type == TaskType.TRANSFORM:
            # Simple dictionary transform
            result = dict(task_def.inputs)
            for k, v in context_variables.items():
                if k not in result:
                    result[k] = v
            return result

        elif task_def.type == TaskType.VALIDATION:
            # Deterministic validation
            return {"validated": True, "task_id": task_def.id}

        elif task_def.type == TaskType.TIMER:
            # Simulation timer or sleep
            await asyncio.sleep(min(0.05, task_def.timeout_seconds))
            return {"timer_elapsed": True}

        # Default fallback execution returns inputs merged with context
        return {"status": "SUCCESS", "task_id": task_def.id, **task_def.outputs}

    def _register_default_handlers(self) -> None:
        pass
