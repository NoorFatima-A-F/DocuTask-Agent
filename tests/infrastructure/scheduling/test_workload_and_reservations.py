"""Tests for Workload Requests, Resource Reservations, and Concurrency Controls."""

from datetime import datetime, timezone, timedelta
from app.infrastructure.executions.workload import (
    ResourceRequirements,
    WorkloadPriority,
    WorkloadRequest,
    WorkloadState,
    WorkloadType,
)
from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.registry import WorkerRegistry
from app.infrastructure.scheduling.reservations import (
    ReservationStatus,
    ResourceReservationManager,
)
from app.infrastructure.scheduling.concurrency import ConcurrencyController


def test_workload_request_instantiation():
    req = WorkloadRequest(
        workload_id="wkl-test-1",
        workload_type=WorkloadType.OCR_JOB,
        tenant_id="tenant-alpha",
        priority=WorkloadPriority.HIGH,
        required_capabilities={"document.ocr", "gpu.cuda"},
        resource_requirements=ResourceRequirements(cpu_cores=2.0, memory_gb=8.0, gpu_count=1),
        region_preferences=["us-east-1", "us-west-2"],
        data_locality_uri="s3://docutask-us-east-1-data/invoice.pdf",
    )
    assert req.workload_id == "wkl-test-1"
    assert req.priority == WorkloadPriority.HIGH
    assert req.state == WorkloadState.SUBMITTED
    assert req.resource_requirements.gpu_count == 1


def test_resource_reservation_manager():
    registry = WorkerRegistry()
    worker = Worker(
        worker_id="wrk-res-1",
        resource_capacity=ResourceCapacity(cpu_cores=8.0, memory_gb=32.0, gpu_count=2, worker_slots=10),
    )
    registry.register_worker(worker)

    res_mgr = ResourceReservationManager(registry)

    # 1. Successful reservation
    req = ResourceRequirements(cpu_cores=4.0, memory_gb=16.0, gpu_count=1, worker_slots=2)
    reservation = res_mgr.create_reservation("wkl-1", worker, req)
    assert reservation is not None
    assert reservation.status == ReservationStatus.PENDING
    assert worker.resource_available.cpu_cores == 4.0
    assert worker.resource_available.gpu_count == 1
    assert worker.resource_available.worker_slots == 8

    # 2. Activate reservation
    assert res_mgr.activate_reservation(reservation.reservation_id) is True

    # 3. Release reservation
    assert res_mgr.release_reservation(reservation.reservation_id) is True
    assert worker.resource_available.cpu_cores == 8.0
    assert worker.resource_available.gpu_count == 2
    assert worker.resource_available.worker_slots == 10

    # 4. Expired reservation cleanup
    pending_res = res_mgr.create_reservation("wkl-2", worker, req, ttl_seconds=1)
    # Manually expire
    pending_res.expires_at = datetime.now(timezone.utc) - timedelta(seconds=10)
    cleaned = res_mgr.clean_expired_reservations()
    assert pending_res.reservation_id in cleaned
    assert worker.resource_available.cpu_cores == 8.0


def test_concurrency_controller():
    controller = ConcurrencyController(
        platform_limit=10,
        tenant_default_limit=2,
        region_default_limit=5,
        cluster_default_limit=3,
    )

    workload_a1 = WorkloadRequest(workload_id="w1", tenant_id="tenant-a")
    workload_a2 = WorkloadRequest(workload_id="w2", tenant_id="tenant-a")
    workload_a3 = WorkloadRequest(workload_id="w3", tenant_id="tenant-a")

    # Admit first 2 for tenant-a
    assert controller.can_admit_workload(workload_a1, "us-east-1", "cls-1")[0] is True
    controller.track_admission(workload_a1, "us-east-1", "cls-1")

    assert controller.can_admit_workload(workload_a2, "us-east-1", "cls-1")[0] is True
    controller.track_admission(workload_a2, "us-east-1", "cls-1")

    # 3rd should breach tenant concurrency limit of 2
    can_admit, reasons = controller.can_admit_workload(workload_a3, "us-east-1", "cls-1")
    assert can_admit is False
    assert any("tenant" in r.lower() for r in reasons)

    # Release one job
    controller.track_release(workload_a1, "us-east-1", "cls-1")
    assert controller.can_admit_workload(workload_a3, "us-east-1", "cls-1")[0] is True
