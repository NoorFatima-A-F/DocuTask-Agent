"""
Worker & Queue Subsystem Dependency Injector.
Provides singleton instances of JobQueueProvider, AsyncWorkerEngine, and JobDispatcher.
"""

from app.workers.base import JobQueueProvider
from app.workers.queue import AsyncInMemoryJobQueue
from app.workers.worker import AsyncWorkerEngine

_queue_provider_instance: JobQueueProvider = AsyncInMemoryJobQueue()
_worker_engine_instance: AsyncWorkerEngine = AsyncWorkerEngine(queue_provider=_queue_provider_instance)


def get_queue_provider() -> JobQueueProvider:
    """Provides active JobQueueProvider instance."""
    return _queue_provider_instance


def get_worker_engine() -> AsyncWorkerEngine:
    """Provides active AsyncWorkerEngine instance."""
    return _worker_engine_instance
