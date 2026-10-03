"""
Unit and Concurrency Tests for Production Distributed Scheduler.
Verifies distributed leasing, worker failover, lease expiration, DLQ routing, and deduplication.
"""

import asyncio
import pytest
from app.agents.runtime.enterprise.scheduler_state import JobPriority, JobStatus, ScheduledJob
from app.agents.runtime.scheduler import (
    MemoryTaskQueue,
    RedisTaskQueue,
    SchedulerController,
)


@pytest.mark.asyncio
async def test_task_leasing_and_completion():
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue, default_lease_duration=10.0)
    await controller.start()

    job = ScheduledJob(name="lease_task", priority=JobPriority.HIGH)
    await controller.submit_job(job)

    polled = await controller.poll_next_job(worker_id="worker-node-1")
    assert polled is not None
    assert polled.assigned_worker == "worker-node-1"
    assert polled.status == JobStatus.RUNNING
    assert await controller.get_worker_load("worker-node-1") == 1

    # Complete
    completed = await controller.complete_job(job.job_id, worker_id="worker-node-1")
    assert completed is True
    assert await controller.get_worker_load("worker-node-1") == 0

    await controller.stop()


@pytest.mark.asyncio
async def test_lease_renewal():
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue, default_lease_duration=2.0)
    await controller.start()

    job = ScheduledJob(name="long_task", priority=JobPriority.NORMAL)
    await controller.submit_job(job)

    polled = await controller.poll_next_job(worker_id="worker-node-1")
    assert polled is not None

    # Renew lease
    renewed = await controller.renew_job_lease(polled.job_id, worker_id="worker-node-1", extension_seconds=5.0)
    assert renewed is True

    # Attempt renewal by wrong worker
    renewed_wrong = await controller.renew_job_lease(polled.job_id, worker_id="worker-intruder")
    assert renewed_wrong is False

    await controller.stop()


@pytest.mark.asyncio
async def test_worker_failover_on_lease_expiry():
    queue = MemoryTaskQueue()
    # Fast lease duration (0.2s)
    controller = SchedulerController(backend=queue, default_lease_duration=0.2, watchdog_interval=0.1)
    await controller.start()

    job = ScheduledJob(name="crash_task", priority=JobPriority.CRITICAL, max_retries=2)
    await controller.submit_job(job)

    polled = await controller.poll_next_job(worker_id="crashed-worker")
    assert polled is not None
    assert polled.retry_count == 0

    # Wait for lease to expire and watchdog to reclaim
    await asyncio.sleep(0.4)

    # Job should now be reclaimed and available for a healthy worker
    failover_job = await controller.poll_next_job(worker_id="healthy-worker")
    assert failover_job is not None
    assert failover_job.job_id == job.job_id
    assert failover_job.assigned_worker == "healthy-worker"
    assert failover_job.retry_count == 1

    await controller.stop()


@pytest.mark.asyncio
async def test_duplicate_execution_prevention_dedup():
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    job1 = ScheduledJob(name="dedup_task_1")
    job2 = ScheduledJob(name="dedup_task_2")

    res1 = await controller.submit_job(job1, dedup_key="invoice-100293")
    assert res1 is not None

    # Submitting another job with identical dedup key is rejected
    res2 = await controller.submit_job(job2, dedup_key="invoice-100293")
    assert res2 is None


@pytest.mark.asyncio
async def test_dlq_routing():
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    job = ScheduledJob(name="failing_task", max_retries=2)
    await controller.submit_job(job)

    # Attempt 1
    j1 = await controller.poll_next_job(worker_id="w-1")
    assert j1 is not None
    await controller.fail_job(j1.job_id, worker_id="w-1", error_message="First failure")

    # Attempt 2 (exhausts max_retries=2)
    j2 = await controller.poll_next_job(worker_id="w-1")
    assert j2 is not None
    await controller.fail_job(j2.job_id, worker_id="w-1", error_message="Second terminal failure")

    dlq = await controller.get_dlq_jobs()
    assert len(dlq) == 1
    assert dlq[0].job_id == job.job_id
    assert dlq[0].status == JobStatus.FAILED


class FakeRedisQueueClient:
    def __init__(self):
        self.hashes = {}
        self.zsets = {}
        self.lists = {}

    async def hset(self, key, field, value):
        if key not in self.hashes:
            self.hashes[key] = {}
        self.hashes[key][field] = value

    async def hget(self, key, field):
        return self.hashes.get(key, {}).get(field)

    async def hdel(self, key, field):
        if key in self.hashes:
            self.hashes[key].pop(field, None)

    async def hgetall(self, key):
        return self.hashes.get(key, {})

    async def zadd(self, key, mapping):
        if key not in self.zsets:
            self.zsets[key] = {}
        for k, score in mapping.items():
            self.zsets[key][k] = score

    async def zrange(self, key, start, stop):
        z = self.zsets.get(key, {})
        sorted_members = sorted(z.keys(), key=lambda m: z[m])
        return sorted_members

    async def zrem(self, key, member):
        if key in self.zsets and member in self.zsets[key]:
            del self.zsets[key][member]
            return 1
        return 0

    async def rpush(self, key, val):
        if key not in self.lists:
            self.lists[key] = []
        self.lists[key].append(val)

    async def lrange(self, key, start, stop):
        return self.lists.get(key, [])


@pytest.mark.asyncio
async def test_redis_task_queue_operations():
    fake_redis = FakeRedisQueueClient()
    queue = RedisTaskQueue(redis_client=fake_redis, prefix="test:scheduler")

    job = ScheduledJob(name="redis_job", priority=JobPriority.HIGH, max_retries=1)
    await queue.enqueue(job)

    polled = await queue.dequeue_with_lease(worker_id="worker-red-1", lease_duration_seconds=5.0)
    assert polled is not None
    assert polled.assigned_worker == "worker-red-1"

    renewed = await queue.renew_lease(job.job_id, worker_id="worker-red-1", extension_seconds=10.0)
    assert renewed is True

    completed = await queue.complete_job(job.job_id, worker_id="worker-red-1")
    assert completed is True

    fetched = await queue.get_job(job.job_id)
    assert fetched.status == JobStatus.COMPLETED


@pytest.mark.asyncio
async def test_scheduler_high_concurrency():
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    # Enqueue 50 concurrent jobs
    for i in range(50):
        priority = JobPriority.CRITICAL if i % 5 == 0 else JobPriority.NORMAL
        await controller.submit_job(ScheduledJob(name=f"job_{i}", priority=priority))

    processed = []

    async def worker_loop(wid: str):
        while True:
            job = await controller.poll_next_job(worker_id=wid)
            if not job:
                break
            await asyncio.sleep(0.005)
            await controller.complete_job(job.job_id, worker_id=wid)
            processed.append(job.name)

    workers = [worker_loop(f"w_{w}") for w in range(5)]
    await asyncio.gather(*workers)

    assert len(processed) == 50
    # The first jobs dequeued should be the critical ones (multiples of 5)
    first_five = processed[:5]
    critical_in_first_five = [n for n in first_five if int(n.split("_")[1]) % 5 == 0]
    assert len(critical_in_first_five) >= 3
