"""
Redis-backed Task Queue Backend with Distributed Leases and Dead-Letter Queue.
Provides horizontally scalable priority scheduling across multiple runtime worker nodes.
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional
from uuid import UUID
from app.agents.runtime.enterprise.scheduler_state import JobStatus, ScheduledJob
from app.agents.runtime.scheduler.task_queue import TaskQueueBackend

logger = logging.getLogger(__name__)


class RedisTaskQueue(TaskQueueBackend):
    """Production distributed Redis-backed task queue with lease fencing and DLQ."""

    def __init__(self, redis_client: Any, prefix: str = "runtime:scheduler") -> None:
        self.client = redis_client
        self.prefix = prefix

    def _jobs_hash(self) -> str:
        return f"{self.prefix}:jobs"

    def _queue_zset(self) -> str:
        return f"{self.prefix}:queue"

    def _leases_hash(self) -> str:
        return f"{self.prefix}:leases"

    def _dlq_list(self) -> str:
        return f"{self.prefix}:dlq"

    def _calculate_score(self, priority: int, run_at_ts: float) -> float:
        # Lower score dequeues first: priority 0 (CRITICAL) before 3 (LOW)
        return (priority * 1_000_000_000.0) + run_at_ts

    async def enqueue(self, job: ScheduledJob) -> None:
        job_data = job.model_dump_json()
        score = self._calculate_score(job.priority.value, job.run_at.timestamp())
        job_id_str = str(job.job_id)

        await self.client.hset(self._jobs_hash(), job_id_str, job_data)
        await self.client.zadd(self._queue_zset(), {job_id_str: score})
        logger.debug(f"RedisTaskQueue: Enqueued job {job.job_id}")

    async def dequeue_with_lease(
        self,
        worker_id: str,
        lease_duration_seconds: float = 30.0,
    ) -> Optional[ScheduledJob]:
        # Peek candidate from sorted set
        candidates = await self.client.zrange(self._queue_zset(), 0, 10)
        if not candidates:
            return None

        now = datetime.now(timezone.utc)
        now_ts = now.timestamp()
        selected_job: Optional[ScheduledJob] = None

        for cand_id in candidates:
            cand_id_str = cand_id if isinstance(cand_id, str) else cand_id.decode("utf-8")
            raw_job = await self.client.hget(self._jobs_hash(), cand_id_str)
            if not raw_job:
                await self.client.zrem(self._queue_zset(), cand_id_str)
                continue

            if isinstance(raw_job, bytes):
                raw_job = raw_job.decode("utf-8")
            job_dict = json.loads(raw_job)
            job = ScheduledJob(**job_dict)

            if job.run_at.timestamp() > now_ts:
                continue

            # Atomically claim by removing from queue
            removed = await self.client.zrem(self._queue_zset(), cand_id_str)
            if removed:
                selected_job = job
                break

        if not selected_job:
            return None

        expires_at = now + timedelta(seconds=lease_duration_seconds)
        lease_data = json.dumps({
            "worker_id": worker_id,
            "expires_at": expires_at.isoformat(),
            "acquired_at": now.isoformat(),
        })
        await self.client.hset(self._leases_hash(), str(selected_job.job_id), lease_data)

        running_job = selected_job.mark_scheduled(worker_id).mark_running()
        await self.client.hset(self._jobs_hash(), str(selected_job.job_id), running_job.model_dump_json())
        return running_job

    async def renew_lease(
        self,
        job_id: UUID,
        worker_id: str,
        extension_seconds: float = 30.0,
    ) -> bool:
        job_id_str = str(job_id)
        raw_lease = await self.client.hget(self._leases_hash(), job_id_str)
        if not raw_lease:
            return False

        if isinstance(raw_lease, bytes):
            raw_lease = raw_lease.decode("utf-8")
        lease_info = json.loads(raw_lease)
        if lease_info.get("worker_id") != worker_id:
            return False

        now = datetime.now(timezone.utc)
        expires_at = datetime.fromisoformat(lease_info["expires_at"])
        if now > expires_at:
            await self.client.hdel(self._leases_hash(), job_id_str)
            return False

        new_expires = now + timedelta(seconds=extension_seconds)
        lease_info["expires_at"] = new_expires.isoformat()
        await self.client.hset(self._leases_hash(), job_id_str, json.dumps(lease_info))
        return True

    async def complete_job(self, job_id: UUID, worker_id: str) -> bool:
        job_id_str = str(job_id)
        raw_lease = await self.client.hget(self._leases_hash(), job_id_str)
        if raw_lease:
            if isinstance(raw_lease, bytes):
                raw_lease = raw_lease.decode("utf-8")
            lease_info = json.loads(raw_lease)
            if lease_info.get("worker_id") != worker_id:
                return False

        await self.client.hdel(self._leases_hash(), job_id_str)
        raw_job = await self.client.hget(self._jobs_hash(), job_id_str)
        if not raw_job:
            return False

        if isinstance(raw_job, bytes):
            raw_job = raw_job.decode("utf-8")
        job = ScheduledJob(**json.loads(raw_job))
        completed = job.mark_completed()
        await self.client.hset(self._jobs_hash(), job_id_str, completed.model_dump_json())
        return True

    async def fail_job(self, job_id: UUID, worker_id: str, error_message: str) -> bool:
        job_id_str = str(job_id)
        await self.client.hdel(self._leases_hash(), job_id_str)
        raw_job = await self.client.hget(self._jobs_hash(), job_id_str)
        if not raw_job:
            return False

        if isinstance(raw_job, bytes):
            raw_job = raw_job.decode("utf-8")
        job = ScheduledJob(**json.loads(raw_job))
        failed_job = job.mark_failed()
        await self.client.hset(self._jobs_hash(), job_id_str, failed_job.model_dump_json())

        if failed_job.status == JobStatus.PENDING:
            score = self._calculate_score(failed_job.priority.value, failed_job.run_at.timestamp())
            await self.client.zadd(self._queue_zset(), {job_id_str: score})
        else:
            await self.client.rpush(self._dlq_list(), failed_job.model_dump_json())
        return True

    async def reclaim_expired_leases(self) -> int:
        all_leases = await self.client.hgetall(self._leases_hash())
        now = datetime.now(timezone.utc)
        reclaimed_count = 0

        for raw_jid, raw_lease in all_leases.items():
            jid_str = raw_jid if isinstance(raw_jid, str) else raw_jid.decode("utf-8")
            if isinstance(raw_lease, bytes):
                raw_lease = raw_lease.decode("utf-8")
            lease_info = json.loads(raw_lease)
            expires_at = datetime.fromisoformat(lease_info["expires_at"])

            if now > expires_at:
                await self.client.hdel(self._leases_hash(), jid_str)
                raw_job = await self.client.hget(self._jobs_hash(), jid_str)
                if raw_job:
                    if isinstance(raw_job, bytes):
                        raw_job = raw_job.decode("utf-8")
                    job = ScheduledJob(**json.loads(raw_job))
                    if job.status == JobStatus.RUNNING:
                        reclaimed = job.mark_failed()
                        await self.client.hset(self._jobs_hash(), jid_str, reclaimed.model_dump_json())
                        if reclaimed.status == JobStatus.PENDING:
                            score = self._calculate_score(reclaimed.priority.value, reclaimed.run_at.timestamp())
                            await self.client.zadd(self._queue_zset(), {jid_str: score})
                        else:
                            await self.client.rpush(self._dlq_list(), reclaimed.model_dump_json())
                        reclaimed_count += 1

        return reclaimed_count

    async def get_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        raw = await self.client.hget(self._jobs_hash(), str(job_id))
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return ScheduledJob(**json.loads(raw))

    async def get_dlq_jobs(self) -> List[ScheduledJob]:
        items = await self.client.lrange(self._dlq_list(), 0, -1)
        res = []
        for item in items:
            if isinstance(item, bytes):
                item = item.decode("utf-8")
            res.append(ScheduledJob(**json.loads(item)))
        return res
