"""Unified High-Level Scheduling and Worker Management SDK."""

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerLease,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.registry import WorkerRegistry
from app.infrastructure.workers.heartbeat import WorkerHeartbeatPayload
from app.infrastructure.executions.workload import (
    ResourceRequirements,
    WorkloadPriority,
    WorkloadRequest,
    WorkloadState,
    WorkloadType,
)
from app.infrastructure.executions.assignment import (
    AssignmentManager,
    WorkloadAssignment,
)
from app.infrastructure.executions.leases import ExecutionLeaseManager
from app.infrastructure.executions.recovery import (
    LostWorkerRecoveryCoordinator,
    RecoveryClassification,
)
from app.infrastructure.scheduling.concurrency import ConcurrencyController
from app.infrastructure.scheduling.reservations import ResourceReservationManager
from app.infrastructure.scheduling.diagnostics import (
    SchedulerDiagnosticsReport,
    SchedulerDiagnosticsService,
    SchedulingDecision,
)
from app.infrastructure.scheduling.placement import PlacementEngine


class WorkerSDK:
    """Unified SDK interface for Worker management and heartbeat reporting."""

    def __init__(self, worker_registry: Optional[WorkerRegistry] = None) -> None:
        self.worker_registry = worker_registry or WorkerRegistry()

    def register_worker(
        self,
        worker_id: str,
        region_id: str,
        cluster_id: str,
        worker_type: WorkerType = WorkerType.CUSTOM,
        service_name: str = "docutask-worker",
        version: str = "3.1.0",
        capabilities: Optional[Set[str]] = None,
        labels: Optional[Dict[str, str]] = None,
        resource_capacity: Optional[ResourceCapacity] = None,
        concurrency_limit: int = 10,
        supported_workloads: Optional[List[str]] = None,
    ) -> Worker:
        worker = Worker(
            worker_id=worker_id,
            region_id=region_id,
            cluster_id=cluster_id,
            worker_type=worker_type,
            service_name=service_name,
            version=version,
            capabilities=capabilities or set(),
            labels=labels or {},
            resource_capacity=resource_capacity or ResourceCapacity(),
            concurrency_limit=concurrency_limit,
            supported_workloads=supported_workloads or ["workflow", "agent", "ocr"],
        )
        return self.worker_registry.register_worker(worker)

    def heartbeat(self, payload: WorkerHeartbeatPayload) -> Optional[WorkerLease]:
        return self.worker_registry.heartbeat(payload)

    def drain(self, worker_id: str, reason: str = "Graceful drain") -> Optional[Worker]:
        return self.worker_registry.drain_worker(worker_id, reason=reason)

    def get_worker(self, worker_id: str) -> Optional[Worker]:
        return self.worker_registry.get_worker(worker_id)

    def list_workers(
        self,
        region_id: Optional[str] = None,
        cluster_id: Optional[str] = None,
        status: Optional[WorkerStatus] = None,
    ) -> List[Worker]:
        return self.worker_registry.list_workers(region_id=region_id, cluster_id=cluster_id, status=status)


class SchedulingSDK:
    """Unified SDK interface for Workload Scheduling, Placement, and Diagnostics."""

    def __init__(
        self,
        region_registry: Optional[RegionRegistry] = None,
        cluster_registry: Optional[ClusterRegistry] = None,
        worker_registry: Optional[WorkerRegistry] = None,
    ) -> None:
        self.region_registry = region_registry or RegionRegistry()
        self.cluster_registry = cluster_registry or ClusterRegistry()
        self.worker_registry = worker_registry or WorkerRegistry()

        self.lease_manager = ExecutionLeaseManager()
        self.assignment_manager = AssignmentManager(self.worker_registry)
        self.reservation_manager = ResourceReservationManager(self.worker_registry)
        self.concurrency_controller = ConcurrencyController()
        self.diagnostics_service = SchedulerDiagnosticsService()

        self.placement_engine = PlacementEngine(
            region_registry=self.region_registry,
            cluster_registry=self.cluster_registry,
            worker_registry=self.worker_registry,
            assignment_manager=self.assignment_manager,
            lease_manager=self.lease_manager,
            reservation_manager=self.reservation_manager,
            concurrency_controller=self.concurrency_controller,
            diagnostics_service=self.diagnostics_service,
        )

        self.recovery_coordinator = LostWorkerRecoveryCoordinator(
            worker_registry=self.worker_registry,
            assignment_manager=self.assignment_manager,
            lease_manager=self.lease_manager,
        )

        self._workloads: Dict[str, WorkloadRequest] = {}

    def submit(
        self, workload: WorkloadRequest
    ) -> Tuple[bool, Optional[WorkloadAssignment], SchedulingDecision]:
        """Submit and place a workload request across the multi-region topology."""
        self._workloads[workload.workload_id] = workload
        success, assignment, decision = self.placement_engine.place_workload(workload)
        return success, assignment, decision

    def status(self, workload_id: str) -> Optional[WorkloadState]:
        """Get lifecycle state of a submitted workload."""
        workload = self._workloads.get(workload_id)
        return workload.state if workload else None

    def cancel(self, workload_id: str) -> bool:
        """Cancel an in-flight or waiting workload."""
        workload = self._workloads.get(workload_id)
        if not workload:
            return False

        workload.state = WorkloadState.CANCELLED

        # Release any active assignment & lease
        assignment = self.assignment_manager.get_active_assignment(workload_id)
        if assignment:
            self.assignment_manager.fail_assignment(assignment.assignment_id, "Cancelled by user")
            self.lease_manager.release_lease(assignment.execution_lease_id)
            self.reservation_manager.release_reservation(assignment.reservation_id)

        return True

    def reschedule(
        self, workload_id: str
    ) -> Tuple[bool, Optional[WorkloadAssignment], Optional[SchedulingDecision]]:
        """Attempt rescheduling of a waiting or failed workload."""
        workload = self._workloads.get(workload_id)
        if not workload:
            return False, None, None
        workload.retry_count += 1
        return self.submit(workload)

    def diagnostics(self, workload_id: str) -> Optional[SchedulerDiagnosticsReport]:
        """Generate comprehensive diagnostic report for a workload."""
        workload = self._workloads.get(workload_id)
        if not workload:
            return None

        eligible_regions = self.placement_engine.global_scheduler.select_eligible_regions(workload)
        return self.diagnostics_service.generate_diagnostics_report(
            workload_id=workload_id,
            state=workload.state.value,
            eligible_regions_count=len(eligible_regions),
        )

    def recover_lost_workers(self) -> List[Tuple[str, RecoveryClassification]]:
        """Run lost worker recovery loop across active workloads."""
        return self.recovery_coordinator.scan_and_recover_lost_workers(self._workloads)
