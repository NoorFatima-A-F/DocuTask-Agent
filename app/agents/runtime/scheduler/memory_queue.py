"""
In-Memory Priority Task Queue Backend with Distributed Lease Emulation.
Thread-safe and async-safe implementation with heartbeat renewal, lease timeouts, and DLQ.
"""

import asyncio
import heapq
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.runtime.enterprise.scheduler_state import JobPriority, JobStatus, ScheduledJob
from app.agents.runtime.scheduler.task_queue import TaskLease, TaskQueueBackend

logger = logging.getLogger(__name__)


class MemoryTaskQueue(TaskQueueBackend):
    """In-memory task queue implementation with full lease management and DLQ."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._jobs: Dict[UUID, ScheduledJob] = {}
        # Entry: (priority_value, run_at_timestamp, job_id)
        self._heap: List[tuple] = []
        self._active_leases: Dict[UUID, TaskLease] = {}
        self._dlq: List[ScheduledJob] = []

    async def enqueue(self, job: ScheduledJob) -> None:
        async with self._lock:
            self._jobs[job.job_id] = job
            heapq.heappush(
                self._heap,
                (job.priority.value, job.run_at.timestamp(), job.job_id),
            )
            logger.debug(f"MemoryTaskQueue: Enqueued job {job.job_id} ({job.name})")

    async def dequeue_with_lease(
        self,
        worker_id: str,
        lease_duration_seconds: float = 30.0,
    ) -> Optional[ScheduledJob]:
        async with self._lock:
            now = datetime.now(timezone.utc)
            now_ts = now.timestamp()
            skipped: List[tuple] = []
            selected_job: Optional[ScheduledJob] = None

            while self._heap:
                entry = heapq.heappop(self._heap)
                priority, run_at_ts, job_id = entry
                job = self._jobs.get(job_id)

                if not job:
                    continue

                if job.status not in (JobStatus.PENDING, JobStatus.SCHEDULED):
                    continue

                if run_at_ts > now_ts:
                    # Not yet eligible to run
                    skipped.append(entry)
                    continue

                # Eligible!
                selected_job = job
                break

            # Restore skipped jobs
            for item in skipped:
                heapq.heappush(self._heap, item)

            if not selected_job:
                return None

            expires_at = now + timedelta(seconds=lease_duration_seconds)
            lease = TaskLease(
                job_id=selected_job.job_id,
                worker_id=worker_id,
                acquired_at=now,
                expires_at=expires_at,
            )
            self._active_leases[selected_job.job_id] = lease

            running_job = selected_job.mark_scheduled(worker_id).mark_running()
            self._jobs[selected_job.job_id] = running_job
            logger.info(f"MemoryTaskQueue: Leased job {selected_job.job_id} to worker {worker_id} until {expires_at.isoformat()}")
            return running_job

    async def renew_lease(
        self,
        job_id: UUID,
        worker_id: str,
        extension_seconds: float = 30.0,
    ) -> bool:
        async with self._lock:
            lease = self._active_leases.get(job_id)
            if not lease:
                return False
            if lease.worker_id != worker_id:
                return False

            now = datetime.now(timezone.utc)
            if now > lease.expires_at:
                # Already expired!
                del self._active_leases[job_id]
                return False

            new_expires = now + timedelta(seconds=extension_seconds)
            self._active_leases[job_id] = lease.model_copy(
                update={"expires_at": new_expires, "renewal_count": lease.renewal_count + 1}
            )
            logger.debug(f"MemoryTaskQueue: Renewed lease for job {job_id} by worker {worker_id}")
            return True

    async def complete_job(self, job_id: UUID, worker_id: str) -> bool:
        async with self._lock:
            lease = self._active_leases.get(job_id)
            if lease and lease.worker_id != worker_id:
                return False

            self._active_leases.pop(job_id, None)
            job = self._jobs.get(job_id)
            if not job:
                return False

            self._jobs[job_id] = job.mark_completed()
            logger.info(f"MemoryTaskQueue: Completed job {job_id} by worker {worker_id}")
            return True

    async def fail_job(self, job_id: UUID, worker_id: str, error_message: str) -> bool:
        async with self._lock:
            lease = self._active_leases.get(job_id)
            if lease and lease.worker_id != worker_id:
                return False

            self._active_leases.pop(job_id, None)
            job = self._jobs.get(job_id)
            if not job:
                return False

            failed_job = job.mark_failed()
            self._jobs[job_id] = failed_job

            if failed_job.status == JobStatus.PENDING:
                # Retries remain: re-enqueue
                heapq.heappush(
                    self._heap,
                    (failed_job.priority.value, failed_job.run_at.timestamp(), failed_job.job_id),
                )
                logger.warning(
                    f"MemoryTaskQueue: Re-enqueued failed job {job_id} (retry {failed_job.retry_count}/{failed_job.max_retries})"
                )
            else:
                # Exhausted: Move to DLQ
                self._dlq.append(failed_job)
                logger.error(f"MemoryTaskQueue: Job {job_id} permanently failed; routed to DLQ. Reason: {error_message}")
            return True

    async def reclaim_expired_leases(self) -> int:
        async with self._lock:
            now = datetime.now(timezone.utc)
            expired_ids = [
                jid for jid, lease in self._active_leases.items()
                if now > lease.expires_at
            ]

            reclaimed_count = 0
            for jid in expired_ids:
                del self._active_leases[jid]
                job = self._jobs.get(jid)
                if job and job.status == JobStatus.RUNNING:
                    # Mark as failed / re-queue for recovery
                    reclaimed_job = job.mark_failed()
                    self._jobs[jid] = reclaimed_job
                    if reclaimed_job.status == JobStatus.PENDING:
                        heapq.heappush(
                            self._heap,
                            (reclaimed_job.priority.value, reclaimed_job.run_at.timestamp(), reclaimed_job.job_id),
                        )
                    else:
                        self._dlq.append(reclaimed_job)
                    reclaimed_count += 1
                    logger.warning(f"MemoryTaskQueue: Reclaimed expired lease for job {jid}")

            return reclaimed_count

    async def get_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        async with self._lock:
            return self._jobs.get(job_id)

    async def get_dlq_jobs(self) -> List[ScheduledJob]:
        async with self._lock:
            return list(self._dlq)
