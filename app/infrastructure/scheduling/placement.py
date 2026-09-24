"""End-to-End Placement Engine Orchestrating Global and Regional Placement."""

from typing import Dict, Optional, Tuple

from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.executions.assignment import AssignmentManager, WorkloadAssignment
from app.infrastructure.executions.leases import ExecutionLeaseManager
from app.infrastructure.executions.workload import WorkloadRequest, WorkloadState
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.scheduling.concurrency import ConcurrencyController
from app.infrastructure.scheduling.diagnostics import (
    SchedulerDiagnosticsService,
    SchedulingDecision,
)
from app.infrastructure.scheduling.global_scheduler import GlobalScheduler
from app.infrastructure.scheduling.regional_scheduler import RegionalScheduler
from app.infrastructure.scheduling.reservations import ResourceReservationManager
from app.infrastructure.workers.registry import WorkerRegistry


class PlacementEngine:
    """Master Placement Engine coordinating multi-region execution placement."""

    def __init__(
        self,
        region_registry: RegionRegistry,
        cluster_registry: ClusterRegistry,
        worker_registry: WorkerRegistry,
        assignment_manager: AssignmentManager,
        lease_manager: ExecutionLeaseManager,
        reservation_manager: ResourceReservationManager,
        concurrency_controller: ConcurrencyController,
        diagnostics_service: SchedulerDiagnosticsService,
    ) -> None:
        self.region_registry = region_registry
        self.cluster_registry = cluster_registry
        self.worker_registry = worker_registry
        self.assignment_manager = assignment_manager
        self.lease_manager = lease_manager
        self.reservation_manager = reservation_manager
        self.concurrency_controller = concurrency_controller
        self.diagnostics_service = diagnostics_service

        self.global_scheduler = GlobalScheduler(region_registry)
        self._regional_schedulers: Dict[str, RegionalScheduler] = {}

    def get_or_create_regional_scheduler(self, region_id: str) -> RegionalScheduler:
        if region_id not in self._regional_schedulers:
            self._regional_schedulers[region_id] = RegionalScheduler(
                region_id=region_id,
                cluster_registry=self.cluster_registry,
                worker_registry=self.worker_registry,
                assignment_manager=self.assignment_manager,
                lease_manager=self.lease_manager,
                reservation_manager=self.reservation_manager,
                concurrency_controller=self.concurrency_controller,
                diagnostics_service=self.diagnostics_service,
            )
        return self._regional_schedulers[region_id]

    def place_workload(
        self, workload: WorkloadRequest, attempt: int = 1
    ) -> Tuple[bool, Optional[WorkloadAssignment], SchedulingDecision]:
        """Orchestrate coarse global placement and fine-grained regional placement."""
        workload.state = WorkloadState.VALIDATING

        # 1. Global Scheduler: select & rank regions
        eligible_regions = self.global_scheduler.select_eligible_regions(workload)
        if not eligible_regions:
            workload.state = WorkloadState.BLOCKED
            decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                candidate_count=0,
                rejection_reasons=[
                    f"No eligible regions satisfy data residency/jurisdiction '{workload.required_jurisdiction}' "
                    f"and tenant constraints for '{workload.tenant_id}'."
                ],
            )
            self.diagnostics_service.record_decision(decision)
            return False, None, decision

        ranked_regions = self.global_scheduler.rank_eligible_regions(eligible_regions, workload)

        # 2. Regional Scheduler: try placement across ranked regions
        last_decision: Optional[SchedulingDecision] = None
        for region in ranked_regions:
            reg_scheduler = self.get_or_create_regional_scheduler(region.region_id)
            success, assignment, decision = reg_scheduler.schedule_workload(workload, attempt=attempt)
            last_decision = decision
            if success and assignment:
                return True, assignment, decision

        # If all candidate regions failed placement
        workload.state = WorkloadState.WAITING
        if not last_decision:
            last_decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                rejection_reasons=["All regional schedulers failed placement."],
            )
        return False, None, last_decision
