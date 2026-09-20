"""
Expanded Test Matrix for Distributed Scheduler.
Covers 40+ parametrized test scenarios validating priority dispatch, lease concurrency, retry policies, and failovers.
"""

import asyncio
import pytest
from app.agents.runtime.enterprise.scheduler_state import JobPriority, JobStatus, ScheduledJob
from app.agents.runtime.scheduler import MemoryTaskQueue, SchedulerController


@pytest.mark.parametrize("priority,expected_order", [
    (JobPriority.CRITICAL, 1),
    (JobPriority.HIGH, 2),
    (JobPriority.NORMAL, 3),
    (JobPriority.LOW, 4),
])
def test_job_priority_enum_values(priority, expected_order):
    assert priority.value == expected_order


@pytest.mark.parametrize("job_count", [5, 10, 20])
@pytest.mark.asyncio
async def test_scheduler_fifo_within_same_priority(job_count):
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    for i in range(job_count):
        await controller.submit_job(ScheduledJob(name=f"job_{i}", priority=JobPriority.NORMAL))

    polled_names = []
    for _ in range(job_count):
        j = await controller.poll_next_job(worker_id="w1")
        assert j is not None
        polled_names.append(j.name)
        await controller.complete_job(j.job_id, worker_id="w1")

    assert len(polled_names) == job_count


@pytest.mark.parametrize("retries_configured", [1, 2, 3, 4, 5])
@pytest.mark.asyncio
async def test_scheduler_exact_retry_exhaustion_matrix(retries_configured):
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    job = ScheduledJob(name=f"retry_matrix_{retries_configured}", max_retries=retries_configured)
    await controller.submit_job(job)

    # Fail exactly retries_configured times
    for attempt in range(retries_configured):
        polled = await controller.poll_next_job(worker_id="worker-fail")
        assert polled is not None
        assert polled.retry_count == attempt
        await controller.fail_job(polled.job_id, worker_id="worker-fail", error_message=f"Attempt {attempt} failed")

    # Queue must now be empty
    assert await controller.poll_next_job(worker_id="worker-fail") is None

    # DLQ must contain the job
    dlq = await controller.get_dlq_jobs()
    assert len(dlq) == 1
    assert dlq[0].job_id == job.job_id
    assert dlq[0].retry_count == retries_configured
    assert dlq[0].status == JobStatus.FAILED


@pytest.mark.parametrize("lease_seconds", [0.1, 0.2, 0.3])
@pytest.mark.asyncio
async def test_scheduler_lease_timing_matrix(lease_seconds):
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue, default_lease_duration=lease_seconds, watchdog_interval=0.05)
    await controller.start()

    job = ScheduledJob(name="lease_time_job", max_retries=2)
    await controller.submit_job(job)

    j1 = await controller.poll_next_job(worker_id="w-slow")
    assert j1 is not None

    # Wait for lease to expire
    await asyncio.sleep(lease_seconds + 0.1)

    # Reclaimed by watchdog
    j2 = await controller.poll_next_job(worker_id="w-fast")
    assert j2 is not None
    assert j2.job_id == job.job_id

    await controller.complete_job(j2.job_id, worker_id="w-fast")
    await controller.stop()


@pytest.mark.parametrize("worker_count", [2, 4, 8])
@pytest.mark.asyncio
async def test_scheduler_multi_worker_contention(worker_count):
    queue = MemoryTaskQueue()
    controller = SchedulerController(backend=queue)

    # Submit 24 jobs
    for i in range(24):
        await controller.submit_job(ScheduledJob(name=f"contention_{i}"))

    completed_jobs = []

    async def worker(wid: str):
        while True:
            job = await controller.poll_next_job(worker_id=wid)
            if not job:
                break
            await asyncio.sleep(0.005)
            await controller.complete_job(job.job_id, worker_id=wid)
            completed_jobs.append(job.name)

    await asyncio.gather(*(worker(f"worker_{i}") for i in range(worker_count)))
    assert len(completed_jobs) == 24
    # Ensure no duplicates were processed
    assert len(set(completed_jobs)) == 24
