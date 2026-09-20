"""Tests for Worker Domain Models, Resource Capacities, and Lifecycle State Machine."""

import pytest
from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerLease,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.lifecycle import (
    WorkerLifecycleStateMachine,
    InvalidWorkerStateTransitionError,
)


def test_worker_model_instantiation():
    capacity = ResourceCapacity(
        cpu_cores=16.0,
        memory_gb=64.0,
        gpu_count=2,
        gpu_type="nvidia-t4",
        worker_slots=20,
    )
    worker = Worker(
        worker_id="wrk-ocr-01",
        worker_type=WorkerType.OCR,
        region_id="us-east-1",
        cluster_id="cls-us-1",
        capabilities={"document.ocr", "gpu.t4"},
        resource_capacity=capacity,
        concurrency_limit=15,
    )

    assert worker.worker_id == "wrk-ocr-01"
    assert worker.worker_type == WorkerType.OCR
    assert worker.status == WorkerStatus.DISCOVERED
    assert worker.resource_available.cpu_cores == 16.0
    assert worker.resource_available.gpu_count == 2
    assert worker.resource_available.worker_slots == 20


def test_worker_lifecycle_valid_transitions():
    sm = WorkerLifecycleStateMachine()

    # DISCOVERED -> REGISTERING -> REGISTERED -> AVAILABLE
    assert sm.transition(WorkerStatus.DISCOVERED, WorkerStatus.REGISTERING) == WorkerStatus.REGISTERING
    assert sm.transition(WorkerStatus.REGISTERING, WorkerStatus.REGISTERED) == WorkerStatus.REGISTERED
    assert sm.transition(WorkerStatus.REGISTERED, WorkerStatus.AVAILABLE) == WorkerStatus.AVAILABLE

    # AVAILABLE -> RESERVED -> ASSIGNED -> RUNNING -> AVAILABLE
    assert sm.transition(WorkerStatus.AVAILABLE, WorkerStatus.RESERVED) == WorkerStatus.RESERVED
    assert sm.transition(WorkerStatus.RESERVED, WorkerStatus.ASSIGNED) == WorkerStatus.ASSIGNED
    assert sm.transition(WorkerStatus.ASSIGNED, WorkerStatus.RUNNING) == WorkerStatus.RUNNING
    assert sm.transition(WorkerStatus.RUNNING, WorkerStatus.AVAILABLE) == WorkerStatus.AVAILABLE

    # AVAILABLE -> DRAINING -> UNAVAILABLE -> RECOVERING -> REGISTERED
    assert sm.transition(WorkerStatus.AVAILABLE, WorkerStatus.DRAINING) == WorkerStatus.DRAINING
    assert sm.transition(WorkerStatus.DRAINING, WorkerStatus.UNAVAILABLE) == WorkerStatus.UNAVAILABLE
    assert sm.transition(WorkerStatus.UNAVAILABLE, WorkerStatus.RECOVERING) == WorkerStatus.RECOVERING
    assert sm.transition(WorkerStatus.RECOVERING, WorkerStatus.REGISTERED) == WorkerStatus.REGISTERED

    # UNAVAILABLE -> TERMINATED
    assert sm.transition(WorkerStatus.UNAVAILABLE, WorkerStatus.TERMINATED) == WorkerStatus.TERMINATED


def test_worker_lifecycle_invalid_transitions():
    sm = WorkerLifecycleStateMachine()

    # DISCOVERED cannot jump directly to RUNNING
    with pytest.raises(InvalidWorkerStateTransitionError):
        sm.transition(WorkerStatus.DISCOVERED, WorkerStatus.RUNNING)

    # TERMINATED cannot transition to any state
    with pytest.raises(InvalidWorkerStateTransitionError):
        sm.transition(WorkerStatus.TERMINATED, WorkerStatus.AVAILABLE)


def test_worker_schedulability():
    sm = WorkerLifecycleStateMachine()
    assert sm.is_schedulable(WorkerStatus.AVAILABLE) is True
    assert sm.is_schedulable(WorkerStatus.RESERVED) is True
    assert sm.is_schedulable(WorkerStatus.RUNNING) is True
    assert sm.is_schedulable(WorkerStatus.DRAINING) is False
    assert sm.is_schedulable(WorkerStatus.UNAVAILABLE) is False
    assert sm.is_schedulable(WorkerStatus.TERMINATED) is False
