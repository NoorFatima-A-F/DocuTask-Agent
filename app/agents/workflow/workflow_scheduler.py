"""
Workflow Scheduler.
Schedules delayed, recurring, and cron-triggered workflows with priority queuing.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.interfaces import IWorkflowScheduler


class ScheduledWorkflowItem(BaseModel):
    """Specification of a scheduled workflow run."""
    schedule_id: UUID = Field(default_factory=uuid4)
    definition_id: UUID
    cron_expression: Optional[str] = None
    execute_after_timestamp: float = 0.0
    priority: int = Field(default=1, ge=1, le=10)
    is_recurring: bool = False

    model_config = {"frozen": True}


class WorkflowScheduler(IWorkflowScheduler):
    """Schedules workflows for immediate or deferred activation."""

    def __init__(self):
        self._schedules: Dict[UUID, ScheduledWorkflowItem] = {}

    async def schedule(self, scheduled_item: ScheduledWorkflowItem) -> None:
        """Enqueues a workflow schedule."""
        self._schedules[scheduled_item.schedule_id] = scheduled_item

    def get_ready_items(self) -> List[ScheduledWorkflowItem]:
        """Returns schedules whose delay threshold has elapsed, sorted by priority."""
        now = datetime.now(timezone.utc).timestamp()
        ready = [
            item for item in self._schedules.values()
            if item.execute_after_timestamp <= now
        ]
        return sorted(ready, key=lambda x: x.priority, reverse=True)
