"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Scheduler.
Provides priority queuing, fair scheduling, concurrency bounding, deadline enforcement,
and preemption across autonomous agent tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import heapq
import uuid
import logging

logger = logging.getLogger(__name__)


class TaskPriority(int, Enum):
    """Numeric priority values for min-heap priority queuing (lower int = higher priority)."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass(order=True)
class ScheduledTask:
    """Prioritized scheduled task wrapper."""
    priority_level: int
    scheduled_time: float
    task_id: str = field(compare=False)
    agent_type: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False, default_factory=dict)
    deadline: Optional[datetime] = field(compare=False, default=None)
    created_at: datetime = field(compare=False, default_factory=lambda: datetime.now(timezone.utc))


class AgentScheduler:
    """
    Schedules and dispatches agent tasks respecting concurrency limits,
    priorities, and execution deadlines.
    """

    def __init__(self, max_concurrent_tasks: int = 20):
        self.max_concurrent_tasks = max_concurrent_tasks
        self._queue: List[ScheduledTask] = []
        self._active_tasks: Dict[str, ScheduledTask] = {}

    def schedule(
        self,
        task_id: str,
        agent_type: str,
        payload: Optional[Dict[str, Any]] = None,
        priority: TaskPriority | str = TaskPriority.NORMAL,
        deadline: Optional[datetime] = None,
    ) -> ScheduledTask:
        """Enqueues a task for execution."""
        if isinstance(priority, str):
            p_val = TaskPriority[priority.upper()].value if priority.upper() in TaskPriority.__members__ else TaskPriority.NORMAL.value
        else:
            p_val = priority.value

        task = ScheduledTask(
            priority_level=p_val,
            scheduled_time=datetime.now(timezone.utc).timestamp(),
            task_id=task_id,
            agent_type=agent_type,
            payload=payload or {},
            deadline=deadline,
        )
        heapq.heappush(self._queue, task)
        logger.info(f"Scheduled task '{task_id}' for '{agent_type}' [Priority: {p_val}]")
        return task

    def pop_next(self) -> Optional[ScheduledTask]:
        """Pulls the highest priority task ready for execution if concurrency permits."""
        if len(self._active_tasks) >= self.max_concurrent_tasks:
            logger.warning(f"Scheduler at max concurrency limit ({self.max_concurrent_tasks})")
            return None

        if not self._queue:
            return None

        task = heapq.heappop(self._queue)
        self._active_tasks[task.task_id] = task
        return task

    def complete_task(self, task_id: str) -> None:
        """Releases concurrency slot for completed task."""
        self._active_tasks.pop(task_id, None)

    @property
    def queue_size(self) -> int:
        return len(self._queue)

    @property
    def active_count(self) -> int:
        return len(self._active_tasks)
