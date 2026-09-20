"""
In-Memory Async Job Queue Implementation.
Uses Python asyncio.Queue with cancellation tracking.
Prepared for seamless replacement with Redis/Celery/RabbitMQ.
"""

import asyncio
from typing import Dict, Optional, Set
from uuid import UUID

from app.core.logging import logger
from app.workers.base import JobQueueProvider
from app.workers.jobs import JobTask


class AsyncInMemoryJobQueue(JobQueueProvider):
    """In-memory asyncio-backed job queue provider."""

    def __init__(self, maxsize: int = 1000):
        self._queue: asyncio.Queue[JobTask] = asyncio.Queue(maxsize=maxsize)
        self._cancelled_jobs: Set[UUID] = set()

    async def enqueue(self, task: JobTask) -> None:
        """Pushes job task onto queue."""
        await self._queue.put(task)
        logger.info(f"Enqueued job '{task.job_id}' (Type={task.job_type}, Document={task.document_id})")

    async def dequeue(self, timeout: float = 1.0) -> Optional[JobTask]:
        """Dequeues next task from queue within timeout."""
        try:
            task = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            
            # Check if task was cancelled while sitting in queue
            if task.job_id in self._cancelled_jobs:
                self._cancelled_jobs.remove(task.job_id)
                self._queue.task_done()
                logger.info(f"Skipping cancelled job '{task.job_id}' during dequeue")
                return None

            return task
        except asyncio.TimeoutError:
            return None

    async def cancel(self, job_id: UUID) -> bool:
        """Flags job ID as cancelled."""
        self._cancelled_jobs.add(job_id)
        logger.info(f"Job '{job_id}' marked as cancelled in queue")
        return True

    async def get_queue_size(self) -> int:
        """Returns pending tasks count."""
        return self._queue.qsize()

    def task_done(self) -> None:
        """Marks current task as completed in queue."""
        self._queue.task_done()

