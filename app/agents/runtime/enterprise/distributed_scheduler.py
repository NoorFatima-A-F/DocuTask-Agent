"""
Distributed Scheduler.
Coordinates priority-ordered job queueing, worker load distribution, and retry policy execution.
"""

import heapq
import logging
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.runtime.enterprise.scheduler_state import (
    JobStatus,
    ScheduledJob,
)

logger = logging.getLogger(__name__)


class DistributedScheduler:
    """Enterprise distributed priority job scheduler."""

    def __init__(self) -> None:
        self._jobs: Dict[UUID, ScheduledJob] = {}
        # Priority heap entries: (priority_int, timestamp, job_id)
        self._priority_queue: List[tuple] = []
        self._worker_loads: Dict[str, int] = {}

    def submit_job(self, job: ScheduledJob) -> ScheduledJob:
        """Enrolls a job into the persistent scheduler queue."""
        self._jobs[job.job_id] = job
        heapq.heappush(
            self._priority_queue,
            (job.priority.value, job.run_at.timestamp(), job.job_id),
        )
        logger.info(f"DistributedScheduler: Enqueued job '{job.name}' (priority={job.priority.name})")
        return job

    def poll_next_job(self, worker_id: str) -> Optional[ScheduledJob]:
        """Dequeues highest priority job and assigns to worker with least load."""
        while self._priority_queue:
            priority, ts, job_id = heapq.heappop(self._priority_queue)
            job = self._jobs.get(job_id)
            if job and job.status in (JobStatus.PENDING, JobStatus.SCHEDULED):
                scheduled = job.mark_scheduled(worker_id).mark_running()
                self._jobs[job_id] = scheduled
                self._worker_loads[worker_id] = self._worker_loads.get(worker_id, 0) + 1
                return scheduled
        return None

    def complete_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        """Marks a job as completed and updates worker load."""
        job = self._jobs.get(job_id)
        if not job:
            return None
        completed = job.mark_completed()
        self._jobs[job_id] = completed
        if job.assigned_worker and job.assigned_worker in self._worker_loads:
            self._worker_loads[job.assigned_worker] = max(0, self._worker_loads[job.assigned_worker] - 1)
        return completed

    def fail_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        """Handles job failure with retry re-queueing."""
        job = self._jobs.get(job_id)
        if not job:
            return None
        failed = job.mark_failed()
        self._jobs[job_id] = failed
        if failed.status == JobStatus.PENDING:
            # Re-queue for retry
            heapq.heappush(
                self._priority_queue,
                (failed.priority.value, failed.run_at.timestamp(), failed.job_id),
            )
            logger.warning(
                f"DistributedScheduler: Re-queued failed job '{failed.name}' (retry {failed.retry_count}/{failed.max_retries})"
            )
        return failed

    def get_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        return self._jobs.get(job_id)

    def list_jobs(self) -> List[ScheduledJob]:
        return list(self._jobs.values())
