"""
Test Suite: Heterogeneous Resource Scheduler & Fair Priority Queue
Validates worker allocation/release, priority ranking (CRITICAL > HIGH > NORMAL > LOW), and backpressure limits.
"""
from app.runtime.resource_scheduler.worker_pool import WorkerPoolManager
from app.runtime.resource_scheduler.priority_scheduler import PriorityScheduler


def test_worker_pool_allocation_and_release():
    pool_mgr = WorkerPoolManager()
    
    w1 = pool_mgr.allocate_worker("OCR_POOL")
    assert w1 is not None
    assert w1.pool_type == "OCR_POOL"
    assert w1.active_jobs > 0

    pool_mgr.release_worker(w1.worker_id)
    status = pool_mgr.get_pool_status()
    assert "OCR_POOL" in status
    assert status["OCR_POOL"]["worker_count"] >= 2


def test_priority_scheduler_queue_ordering_and_dispatch():
    scheduler = PriorityScheduler()
    # Clear seed queue
    scheduler.task_queue.clear()

    # Enqueue in reverse priority
    scheduler.enqueue_task("task_low", "m1", "LLM_POOL", priority="LOW")
    scheduler.enqueue_task("task_crit", "m1", "LLM_POOL", priority="CRITICAL")
    scheduler.enqueue_task("task_high", "m1", "LLM_POOL", priority="HIGH")

    # Critical should be dispatched first
    d1 = scheduler.dispatch_next()
    assert d1 is not None
    assert d1["task_id"] == "task_crit"
    assert d1["assigned_worker_id"] is not None

    # High should be dispatched next
    d2 = scheduler.dispatch_next()
    assert d2 is not None
    assert d2["task_id"] == "task_high"


def test_priority_scheduler_backpressure():
    scheduler = PriorityScheduler()
    scheduler._max_queue_depth = 2
    scheduler.task_queue.clear()

    assert scheduler.enqueue_task("t1", "m1", "OCR_POOL") is True
    assert scheduler.enqueue_task("t2", "m1", "OCR_POOL") is True
    # Exceeds max queue depth -> rejected
    assert scheduler.enqueue_task("t3", "m1", "OCR_POOL") is False
