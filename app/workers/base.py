"""
Abstract Job Queue Provider Base Class.
Defines common interface for queue backends (AsyncInMemory, Redis, RabbitMQ, Celery).
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.workers.jobs import JobTask


class JobQueueProvider(ABC):
    """Abstract job queue interface."""

    @abstractmethod
    async def enqueue(self, task: JobTask) -> None:
        """Enqueues job task into queue."""
        pass

    @abstractmethod
    async def dequeue(self, timeout: float = 1.0) -> Optional[JobTask]:
        """Dequeues next available job task."""
        pass

    @abstractmethod
    async def cancel(self, job_id: UUID) -> bool:
        """Cancels job if currently in queue."""
        pass

    @abstractmethod
    async def get_queue_size(self) -> int:
        """Returns total pending tasks count in queue."""
        pass
