"""
Enterprise Task Scheduler & Multi-Tier Priority Queues.
Supports 10 dedicated queues: critical, high, normal, low, background, ai, human, connector, retry, dead-letter.
"""

import asyncio
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from ..domain.models import TaskPriority, TaskType


class QueueTier(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"
    AI = "ai"
    HUMAN = "human"
    CONNECTOR = "connector"
    RETRY = "retry"
    DEAD_LETTER = "dead-letter"


@dataclass
class ScheduledTask:
    """Scheduled task waiting in execution queue."""
    task_id: str
    execution_id: str
    task_name: str
    task_type: TaskType
    priority: TaskPriority = TaskPriority.NORMAL
    queue_tier: QueueTier = QueueTier.NORMAL
    payload: Dict[str, Any] = field(default_factory=dict)
    scheduled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: Optional[datetime] = None
    attempts: int = 0


class TaskScheduler:
    """Multi-Queue Enterprise Task Scheduler."""

    def __init__(self):
        self._queues: Dict[QueueTier, deque] = {tier: deque() for tier in QueueTier}

    def schedule_task(
        self,
        task_id: str,
        execution_id: str,
        task_name: str,
        task_type: TaskType = TaskType.SYSTEM,
        priority: TaskPriority = TaskPriority.NORMAL,
        payload: Optional[Dict[str, Any]] = None,
        deadline: Optional[datetime] = None,
    ) -> ScheduledTask:
        """Enqueue task into optimal priority/functional queue tier."""
        tier = self._determine_queue_tier(task_type, priority)
        item = ScheduledTask(
            task_id=task_id,
            execution_id=execution_id,
            task_name=task_name,
            task_type=task_type,
            priority=priority,
            queue_tier=tier,
            payload=payload or {},
            deadline=deadline,
        )
        self._queues[tier].append(item)
        return item

    def _determine_queue_tier(self, task_type: TaskType, priority: TaskPriority) -> QueueTier:
        """Route task to specialized queue tier."""
        if priority == TaskPriority.CRITICAL:
            return QueueTier.CRITICAL
        if task_type == TaskType.HUMAN or task_type == TaskType.APPROVAL:
            return QueueTier.HUMAN
        if task_type == TaskType.AI:
            return QueueTier.AI
        if task_type == TaskType.CONNECTOR:
            return QueueTier.CONNECTOR
        if priority == TaskPriority.HIGH:
            return QueueTier.HIGH
        if priority == TaskPriority.LOW:
            return QueueTier.LOW
        if priority == TaskPriority.BACKGROUND:
            return QueueTier.BACKGROUND
        return QueueTier.NORMAL

    def pop_next(self) -> Optional[ScheduledTask]:
        """Pop the highest priority available task across all queue tiers."""
        priority_order = [
            QueueTier.CRITICAL,
            QueueTier.HIGH,
            QueueTier.AI,
            QueueTier.CONNECTOR,
            QueueTier.NORMAL,
            QueueTier.HUMAN,
            QueueTier.RETRY,
            QueueTier.LOW,
            QueueTier.BACKGROUND,
        ]
        for tier in priority_order:
            q = self._queues[tier]
            if q:
                return q.popleft()
        return None

    def queue_depth(self, tier: Optional[QueueTier] = None) -> int:
        """Return depth of specified queue or aggregate depth."""
        if tier:
            return len(self._queues[tier])
        return sum(len(q) for q in self._queues.values())
