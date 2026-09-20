"""
Enterprise Distributed Scheduler Test Suite.
Validates:
- Strict priority queueing (CRITICAL > HIGH > NORMAL > LOW > BACKGROUND)
- Worker assignment & load accounting
- Failure handling & exponential retry re-queueing
- Terminal failure state when retry threshold exceeded
- Job listing and status inspection
"""

from uuid import uuid4
import pytest
from app.agents.runtime.enterprise.distributed_scheduler import DistributedScheduler
from app.agents.runtime.enterprise.scheduler_state import (
    JobPriority,
    JobStatus,
    ScheduledJob,
)


def test_job_submission_and_priority_dispatch():
    scheduler = DistributedScheduler()

    job_low = ScheduledJob(name="low_task", priority=JobPriority.LOW)
    job_critical = ScheduledJob(name="critical_task", priority=JobPriority.CRITICAL)
    job_normal = ScheduledJob(name="normal_task", priority=JobPriority.NORMAL)

    scheduler.submit_job(job_low)
    scheduler.submit_job(job_critical)
    scheduler.submit_job(job_normal)

    # First polled job must be CRITICAL
    first = scheduler.poll_next_job(worker_id="worker-1")
    assert first is not None
    assert first.name == "critical_task"
    assert first.priority == JobPriority.CRITICAL
    assert first.assigned_worker == "worker-1"
    assert first.status == JobStatus.RUNNING

    # Second polled job must be NORMAL
    second = scheduler.poll_next_job(worker_id="worker-2")
    assert second is not None
    assert second.name == "normal_task"

    # Third polled job must be LOW
    third = scheduler.poll_next_job(worker_id="worker-1")
    assert third is not None
    assert third.name == "low_task"

    # No more jobs
    empty = scheduler.poll_next_job(worker_id="worker-1")
    assert empty is None


def test_worker_load_tracking():
    scheduler = DistributedScheduler()
    job = ScheduledJob(name="load_test_job")
    scheduler.submit_job(job)

    assert scheduler._worker_loads.get("worker-A", 0) == 0

    polled = scheduler.poll_next_job(worker_id="worker-A")
    assert scheduler._worker_loads.get("worker-A", 0) == 1

    completed = scheduler.complete_job(polled.job_id)
    assert completed.status == JobStatus.COMPLETED
    assert scheduler._worker_loads.get("worker-A", 0) == 0


def test_job_retry_requeue_and_terminal_failure():
    scheduler = DistributedScheduler()
    job = ScheduledJob(name="retryable_job", max_retries=3)
    scheduler.submit_job(job)

    # 1st attempt
    j1 = scheduler.poll_next_job("worker-1")
    assert j1.retry_count == 0

    # Fail 1st attempt -> should re-queue (retry_count becomes 1)
    f1 = scheduler.fail_job(j1.job_id)
    assert f1.status == JobStatus.PENDING
    assert f1.retry_count == 1

    # 2nd attempt
    j2 = scheduler.poll_next_job("worker-2")
    assert j2.retry_count == 1

    # Fail 2nd attempt -> should re-queue (retry_count becomes 2)
    f2 = scheduler.fail_job(j2.job_id)
    assert f2.status == JobStatus.PENDING
    assert f2.retry_count == 2

    # 3rd attempt
    j3 = scheduler.poll_next_job("worker-3")
    assert j3.retry_count == 2

    # Fail 3rd attempt -> exceeds max_retries (3) -> terminal FAILED
    f3 = scheduler.fail_job(j3.job_id)
    assert f3.status == JobStatus.FAILED
    assert f3.retry_count == 3

    # No more jobs in queue
    assert scheduler.poll_next_job("worker-1") is None


def test_list_and_get_job():
    scheduler = DistributedScheduler()
    j1 = ScheduledJob(name="j1")
    j2 = ScheduledJob(name="j2")
    scheduler.submit_job(j1)
    scheduler.submit_job(j2)

    assert len(scheduler.list_jobs()) == 2
    assert scheduler.get_job(j1.job_id).name == "j1"
    assert scheduler.get_job(uuid4()) is None
