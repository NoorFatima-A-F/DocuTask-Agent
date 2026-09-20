"""
Enterprise Distributed Scheduler Controller.
Coordinates distributed task queue backends, lease watchdog, worker load balancing, and deduplication.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set
from uuid import UUID
from app.agents.runtime.enterprise.scheduler_state import ScheduledJob
from app.agents.runtime.scheduler.task_queue import TaskQueueBackend

logger = logging.getLogger(__name__)


class SchedulerController:
    """
    Central Controller for the Distributed Agent Runtime Scheduler.
    Manages task queues, heartbeat renewals, automatic expired lease reclamation, and deduplication tokens.
    """

    def __init__(
        self,
        backend: TaskQueueBackend,
        default_lease_duration: float = 30.0,
        watchdog_interval: float = 5.0,
    ) -> None:
        self.backend = backend
        self.default_lease_duration = default_lease_duration
        self.watchdog_interval = watchdog_interval
        self._processed_dedup_keys: Set[str] = set()
        self._worker_loads: Dict[str, int] = {}
        self._watchdog_task: Optional[asyncio.Task] = None
        self._is_running = False

    async def start(self) -> None:
        """Starts the scheduler controller and background lease reclamation watchdog."""
        if self._is_running:
            return
        self._is_running = True
        self._watchdog_task = asyncio.create_task(self._watchdog_loop())
        logger.info("SchedulerController started with active watchdog.")

    async def stop(self) -> None:
        """Stops the scheduler controller and cancels the watchdog."""
        self._is_running = False
        if self._watchdog_task and not self._watchdog_task.done():
            self._watchdog_task.cancel()
            try:
                await self._watchdog_task
            except asyncio.CancelledError:
                pass
        logger.info("SchedulerController stopped.")

    async def submit_job(self, job: ScheduledJob, dedup_key: Optional[str] = None) -> Optional[ScheduledJob]:
        """
        Submits a job to the distributed queue.
        If dedup_key is supplied and already submitted, returns None to guarantee idempotency.
        """
        if dedup_key:
            if dedup_key in self._processed_dedup_keys:
                logger.warning(f"SchedulerController: Dropped duplicate job submission with dedup_key='{dedup_key}'")
                return None
            self._processed_dedup_keys.add(dedup_key)

        await self.backend.enqueue(job)
        return job

    async def poll_next_job(self, worker_id: str, lease_duration: Optional[float] = None) -> Optional[ScheduledJob]:
        """Polls for the highest priority job eligible to execute and assigns a lease to worker_id."""
        duration = lease_duration or self.default_lease_duration
        job = await self.backend.dequeue_with_lease(worker_id=worker_id, lease_duration_seconds=duration)
        if job:
            self._worker_loads[worker_id] = self._worker_loads.get(worker_id, 0) + 1
        return job

    async def renew_job_lease(self, job_id: UUID, worker_id: str, extension_seconds: Optional[float] = None) -> bool:
        """Renews an active lease during long-running execution."""
        duration = extension_seconds or self.default_lease_duration
        return await self.backend.renew_lease(job_id=job_id, worker_id=worker_id, extension_seconds=duration)

    async def complete_job(self, job_id: UUID, worker_id: str) -> bool:
        """Marks job completed and decrements worker active load."""
        success = await self.backend.complete_job(job_id=job_id, worker_id=worker_id)
        if success and worker_id in self._worker_loads:
            self._worker_loads[worker_id] = max(0, self._worker_loads[worker_id] - 1)
        return success

    async def fail_job(self, job_id: UUID, worker_id: str, error_message: str) -> bool:
        """Marks job failed and decrements worker active load."""
        success = await self.backend.fail_job(job_id=job_id, worker_id=worker_id, error_message=error_message)
        if success and worker_id in self._worker_loads:
            self._worker_loads[worker_id] = max(0, self._worker_loads[worker_id] - 1)
        return success

    async def get_worker_load(self, worker_id: str) -> int:
        return self._worker_loads.get(worker_id, 0)

    async def get_dlq_jobs(self) -> List[ScheduledJob]:
        return await self.backend.get_dlq_jobs()

    async def _watchdog_loop(self) -> None:
        """Periodically reclaims expired leases for dead or unresponsive workers."""
        while self._is_running:
            try:
                await asyncio.sleep(self.watchdog_interval)
                reclaimed = await self.backend.reclaim_expired_leases()
                if reclaimed > 0:
                    logger.warning(f"SchedulerController Watchdog: Reclaimed {reclaimed} expired leases.")
            except asyncio.CancelledError:
                break
            except Exception as ex:
                logger.error(f"SchedulerController Watchdog error: {ex}", exc_info=True)
