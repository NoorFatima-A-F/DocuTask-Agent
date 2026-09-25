"""
Worker Pool Runtime.
Manages bounded pool of execution workers with concurrency limiting and lease tracking.
"""

import asyncio
from typing import Optional
from uuid import uuid4
from app.agents.execution.exceptions import WorkerExhaustionException
from app.agents.execution.lease_manager import WorkerLease, WorkerLeaseManager
from app.agents.execution.worker import Worker, WorkerStatus
from app.agents.execution.worker_registry import WorkerRegistry
from app.agents.execution.worker_selector import WorkerSelector


class WorkerPool:
    """Pool maintaining bounded active workers and managing worker leases."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.registry = WorkerRegistry()
        self.lease_manager = WorkerLeaseManager()
        self.selector = WorkerSelector()
        self._lock = asyncio.Lock()

        # Initialize default workers
        for i in range(max_workers):
            worker = Worker(
                worker_id=f"worker_{i+1}",
                capabilities=["DEFAULT", "OCR", "LLM", "DECISION", "TOOL", "ALL"],
                status=WorkerStatus.IDLE
            )
            self.registry.register(worker)

    async def acquire_worker(self, node_id: str, capability: Optional[str] = None) -> WorkerLease:
        """Acquires an idle worker for the given node and grants a lease."""
        async with self._lock:
            idle_workers = self.registry.list_idle()
            selected = self.selector.select_worker(idle_workers, capability)
            if not selected:
                raise WorkerExhaustionException(f"No worker available to execute node '{node_id}'.")

            # Mark busy
            busy_worker = selected.model_copy(
                update={"status": WorkerStatus.BUSY, "assigned_node_id": node_id}
            )
            self.registry.register(busy_worker)

            lease_id = f"lease_{uuid4().hex[:8]}"
            lease = self.lease_manager.grant_lease(lease_id, selected.worker_id, node_id)
            return lease

    async def release_worker(self, lease: WorkerLease) -> None:
        """Releases the worker back to the idle pool and closes the lease."""
        async with self._lock:
            self.lease_manager.release_lease(lease.lease_id)
            worker = self.registry.get(lease.worker_id)
            if worker:
                idle_worker = worker.model_copy(
                    update={"status": WorkerStatus.IDLE, "assigned_node_id": None}
                )
                self.registry.register(idle_worker)
