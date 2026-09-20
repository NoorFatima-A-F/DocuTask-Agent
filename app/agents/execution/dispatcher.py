"""
Task Dispatcher.
Assigns scheduled task nodes to available workers in the WorkerPool.
"""

from typing import Optional
from app.agents.execution.lease_manager import WorkerLease
from app.agents.execution.worker_pool import WorkerPool


class TaskDispatcher:
    """Dispatches scheduled tasks to worker pool instances."""

    def __init__(self, worker_pool: WorkerPool):
        self.worker_pool = worker_pool

    async def dispatch_task(self, node_id: str, capability: Optional[str] = None) -> WorkerLease:
        """Acquires a worker lease for the task."""
        return await self.worker_pool.acquire_worker(node_id, capability)

    async def complete_task(self, lease: WorkerLease) -> None:
        """Releases the worker lease upon task completion."""
        await self.worker_pool.release_worker(lease)
