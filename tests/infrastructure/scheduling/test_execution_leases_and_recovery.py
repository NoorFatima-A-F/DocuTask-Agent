"""Tests for Execution Leases, Assignments, and Lost Worker Recovery."""

from datetime import datetime, timezone, timedelta
from app.infrastructure.executions.workload import (
    WorkloadRequest,
    WorkloadState,
    WorkloadType,
)
from app.infrastructure.executions.leases import (
    ExecutionLeaseManager,
    ExecutionLeaseStatus,
)
from app.infrastructure.executions.assignment import (
    AssignmentManager,
    AssignmentStatus,
)
from app.infrastructure.executions.recovery import (
    LostWorkerRecoveryCoordinator,
    RecoveryClassification,
)
from app.infrastructure.workers.models import (
    Worker,
    WorkerLease,
    WorkerStatus,
)
from app.infrastructure.workers.registry import WorkerRegistry


def test_execution_lease_manager():
    lease_mgr = ExecutionLeaseManager()

    # Issue lease for attempt 1
    lease1 = lease_mgr.issue_execution_lease("wkl-100", "wrk-1", attempt=1, ttl_seconds=10)
    assert lease1.status == ExecutionLeaseStatus.ACTIVE
    assert lease_mgr.is_lease_valid(lease1.lease_id) is True

    # Issuing lease for attempt 2 should revoke lease 1
    lease2 = lease_mgr.issue_execution_lease("wkl-100", "wrk-2", attempt=2, ttl_seconds=10)
    assert lease2.status == ExecutionLeaseStatus.ACTIVE
    assert lease_mgr.is_lease_valid(lease1.lease_id) is False
    assert lease_mgr.is_lease_valid(lease2.lease_id) is True


def test_assignment_manager_lifecycle():
    worker_reg = WorkerRegistry()
    worker = Worker(worker_id="wrk-asg-1", status=WorkerStatus.AVAILABLE)
    worker_reg.register_worker(worker)

    asg_mgr = AssignmentManager(worker_reg)
    workload = WorkloadRequest(workload_id="wkl-asg-1", tenant_id="tenant-1")

    # 1. Create assignment
    asg = asg_mgr.create_assignment(workload, worker, "res-1", "lease-1")
    assert asg.status == AssignmentStatus.PENDING_ACK
    assert asg.assignment_id in worker.active_assignments

    # 2. Worker ACK
    ack_asg = asg_mgr.acknowledge_assignment(asg.assignment_id)
    assert ack_asg.status == AssignmentStatus.RUNNING

    # 3. Complete assignment
    comp_asg = asg_mgr.complete_assignment(asg.assignment_id)
    assert comp_asg.status == AssignmentStatus.COMPLETED
    assert asg.assignment_id not in worker.active_assignments


def test_lost_worker_recovery_coordinator():
    worker_reg = WorkerRegistry()
    worker = Worker(
        worker_id="wrk-lost-1",
        status=WorkerStatus.AVAILABLE,
        cluster_id="cls-1",
    )
    worker_reg.register_worker(worker)

    asg_mgr = AssignmentManager(worker_reg)
    lease_mgr = ExecutionLeaseManager()
    recovery = LostWorkerRecoveryCoordinator(worker_reg, asg_mgr, lease_mgr)

    workload = WorkloadRequest(
        workload_id="wkl-lost-1",
        workload_type=WorkloadType.OCR_JOB,
        tenant_id="tenant-1",
        idempotency_key="idem-123",
    )
    lease = lease_mgr.issue_execution_lease("wkl-lost-1", "wrk-lost-1")
    asg = asg_mgr.create_assignment(workload, worker, "res-1", lease.lease_id)
    asg_mgr.acknowledge_assignment(asg.assignment_id)

    # Simulate worker lease expiration
    worker_reg.lease_manager._leases["wrk-lost-1"] = WorkerLease(
        worker_id="wrk-lost-1",
        cluster_id="cls-1",
        ttl_seconds=5,
        last_renewed=datetime.now(timezone.utc) - timedelta(seconds=20),
    )

    # Run recovery
    active_workloads = {"wkl-lost-1": workload}
    recovered = recovery.scan_and_recover_lost_workers(active_workloads)

    assert len(recovered) == 1
    assert recovered[0] == ("wkl-lost-1", RecoveryClassification.SAFE_TO_RETRY)
    assert workload.state == WorkloadState.RETRY_PENDING
    assert workload.retry_count == 1
    assert asg_mgr.get_assignment(asg.assignment_id).status == AssignmentStatus.FAILED
