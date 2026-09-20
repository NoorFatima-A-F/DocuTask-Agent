"""
Enterprise Saga Compensation Engine.
Coordinates backward rollback of distributed transactions when a forward workflow step fails.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from ..domain.models import TaskDefinition
from ..domain.exceptions import CompensationException


@dataclass
class CompensationRecord:
    task_id: str
    compensation_action: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"  # PENDING, COMPLETED, FAILED
    error_message: Optional[str] = None
    executed_at: Optional[datetime] = None


class CompensationEngine:
    """Manages Saga compensation registration and reverse execution."""

    def __init__(self):
        # Key: execution_id -> List of completed tasks with compensations in forward order
        self._completed_compensations: Dict[str, List[CompensationRecord]] = {}
        self._handlers: Dict[str, Callable[[CompensationRecord], Any]] = {}

    def register_handler(self, action_name: str, handler: Callable[[CompensationRecord], Any]) -> None:
        """Register handler for specific compensation action."""
        self._handlers[action_name] = handler

    def record_completed_task(self, execution_id: str, task_def: TaskDefinition, inputs: Dict[str, Any]) -> None:
        """Record completed task if it has a declared compensation action."""
        if not task_def.compensation_action:
            return

        if execution_id not in self._completed_compensations:
            self._completed_compensations[execution_id] = []

        rec = CompensationRecord(
            task_id=task_def.id,
            compensation_action=task_def.compensation_action,
            inputs=inputs,
        )
        self._completed_compensations[execution_id].append(rec)

    async def execute_rollback(self, execution_id: str) -> List[CompensationRecord]:
        """Execute compensation actions in strict REVERSE order of forward completion."""
        records = self._completed_compensations.get(execution_id, [])
        if not records:
            return []

        executed_records = []
        # Reverse execution for Saga rollback
        for rec in reversed(records):
            rec.status = "IN_PROGRESS"
            handler = self._handlers.get(rec.compensation_action)
            try:
                if handler:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(rec)
                    else:
                        handler(rec)
                rec.status = "COMPLETED"
                rec.executed_at = datetime.now(timezone.utc)
            except Exception as e:
                rec.status = "FAILED"
                rec.error_message = str(e)
                raise CompensationException(
                    f"Saga compensation '{rec.compensation_action}' failed for task '{rec.task_id}': {str(e)}",
                    execution_id=execution_id,
                    task_id=rec.task_id,
                ) from e

            executed_records.append(rec)

        return executed_records
