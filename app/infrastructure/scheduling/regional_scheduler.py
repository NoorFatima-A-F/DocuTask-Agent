"""Regional Scheduler for Cluster Selection and Fine-Grained Worker Placement."""

import time
from typing import Dict, List, Optional, Tuple

from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.executions.assignment import AssignmentManager, WorkloadAssignment
from app.infrastructure.executions.leases import ExecutionLeaseManager
from app.infrastructure.executions.workload import WorkloadRequest, WorkloadState
from app.infrastructure.scheduling.concurrency import ConcurrencyController
from app.infrastructure.scheduling.constraints import ConstraintEvaluator
from app.infrastructure.scheduling.diagnostics import (
    SchedulerDiagnosticsService,
    SchedulingDecision,
)
from app.infrastructure.scheduling.policies import SchedulingPolicyEngine
from app.infrastructure.scheduling.reservations import ResourceReservationManager
from app.infrastructure.scheduling.scoring import PlacementScoringEngine
from app.infrastructure.topology.selectors import ClusterSelector
from app.infrastructure.workers.models import Worker
from app.infrastructure.workers.registry import WorkerRegistry


class RegionalScheduler:
    """Performs cluster selection, worker candidate filtering, scoring, reservation, and assignment."""

    def __init__(
        self,
        region_id: str,
        cluster_registry: ClusterRegistry,
        worker_registry: WorkerRegistry,
        assignment_manager: AssignmentManager,
        lease_manager: ExecutionLeaseManager,
        reservation_manager: ResourceReservationManager,
        concurrency_controller: ConcurrencyController,
        diagnostics_service: SchedulerDiagnosticsService,
        scoring_engine: Optional[PlacementScoringEngine] = None,
        policy_engine: Optional[SchedulingPolicyEngine] = None,
    ) -> None:
        self.region_id = region_id
        self.cluster_registry = cluster_registry
        self.worker_registry = worker_registry
        self.assignment_manager = assignment_manager
        self.lease_manager = lease_manager
        self.reservation_manager = reservation_manager
        self.concurrency_controller = concurrency_controller
        self.diagnostics_service = diagnostics_service
        self.scoring_engine = scoring_engine or PlacementScoringEngine(
            capability_registry=worker_registry.capability_registry
        )
        self.policy_engine = policy_engine or SchedulingPolicyEngine()
        self.cluster_selector = ClusterSelector(cluster_registry)
        self.constraint_evaluator = ConstraintEvaluator(
            capability_registry=worker_registry.capability_registry,
            lease_manager=worker_registry.lease_manager,
        )

    def schedule_workload(
        self, workload: WorkloadRequest, attempt: int = 1
    ) -> Tuple[bool, Optional[WorkloadAssignment], SchedulingDecision]:
        """Execute fine-grained placement within this region."""
        start_time = time.time()
        rejected_candidates: Dict[str, List[str]] = {}
        high_level_reasons: List[str] = []

        # 1. Select eligible clusters in this region
        eligible_clusters = self.cluster_selector.select_eligible_clusters(workload, self.region_id)
        if not eligible_clusters:
            high_level_reasons.append(f"No eligible healthy clusters found in region '{self.region_id}'.")
            decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                selected_region=self.region_id,
                candidate_count=0,
                rejection_reasons=high_level_reasons,
                decision_latency_ms=(time.time() - start_time) * 1000.0,
            )
            self.diagnostics_service.record_decision(decision)
            return False, None, decision

        # 2. Collect candidate workers from eligible clusters
        valid_workers: List[Worker] = []
        for cluster in eligible_clusters:
            cluster_workers = self.worker_registry.list_workers(
                region_id=self.region_id, cluster_id=cluster.cluster_id
            )

            for worker in cluster_workers:
                # Evaluate hard constraints
                passed_constraints, errs = self.constraint_evaluator.evaluate_worker(worker, workload)
                if not passed_constraints:
                    rejected_candidates[worker.worker_id] = errs
                    continue

                # Evaluate policies
                passed_policy, pol_errs = self.policy_engine.evaluate_placement_policy(worker, workload)
                if not passed_policy:
                    rejected_candidates[worker.worker_id] = pol_errs
                    continue

                # Evaluate concurrency limits
                can_admit, conc_errs = self.concurrency_controller.can_admit_workload(
                    workload, self.region_id, cluster.cluster_id
                )
                if not can_admit:
                    rejected_candidates[worker.worker_id] = conc_errs
                    continue

                valid_workers.append(worker)

        if not valid_workers:
            high_level_reasons.append(f"No viable workers found satisfying constraints in region '{self.region_id}'.")
            decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                selected_region=self.region_id,
                candidate_count=len(rejected_candidates),
                rejected_candidates=rejected_candidates,
                rejection_reasons=high_level_reasons,
                decision_latency_ms=(time.time() - start_time) * 1000.0,
            )
            self.diagnostics_service.record_decision(decision)
            return False, None, decision

        # 3. Score & rank candidate workers
        ranked_scores = self.scoring_engine.rank_candidates(valid_workers, workload)
        best_score = ranked_scores[0]
        selected_worker = self.worker_registry.get_worker(best_score.worker_id)
        if not selected_worker:
            high_level_reasons.append("Selected worker candidate became unavailable.")
            decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                selected_region=self.region_id,
                rejection_reasons=high_level_reasons,
                decision_latency_ms=(time.time() - start_time) * 1000.0,
            )
            self.diagnostics_service.record_decision(decision)
            return False, None, decision

        # 4. Reserve capacity
        reservation = self.reservation_manager.create_reservation(
            workload_id=workload.workload_id,
            worker=selected_worker,
            resources=workload.resource_requirements,
        )
        if not reservation:
            high_level_reasons.append(f"Capacity reservation failed on worker '{selected_worker.worker_id}'.")
            decision = SchedulingDecision(
                workload_id=workload.workload_id,
                is_scheduled=False,
                selected_region=self.region_id,
                rejection_reasons=high_level_reasons,
                decision_latency_ms=(time.time() - start_time) * 1000.0,
            )
            self.diagnostics_service.record_decision(decision)
            return False, None, decision

        # 5. Issue execution lease
        lease = self.lease_manager.issue_execution_lease(
            workload_id=workload.workload_id,
            worker_id=selected_worker.worker_id,
            attempt=attempt,
        )

        # 6. Create assignment
        assignment = self.assignment_manager.create_assignment(
            workload=workload,
            worker=selected_worker,
            reservation_id=reservation.reservation_id,
            execution_lease_id=lease.lease_id,
            attempt=attempt,
        )

        # 7. Track concurrency admission
        self.concurrency_controller.track_admission(
            workload, self.region_id, selected_worker.cluster_id
        )

        # 8. Update workload state
        workload.state = WorkloadState.ASSIGNED

        decision = SchedulingDecision(
            workload_id=workload.workload_id,
            is_scheduled=True,
            selected_region=self.region_id,
            selected_cluster=selected_worker.cluster_id,
            selected_worker=selected_worker.worker_id,
            candidate_count=len(valid_workers),
            rejected_candidates=rejected_candidates,
            score_breakdown=best_score,
            reservation_id=reservation.reservation_id,
            execution_lease_id=lease.lease_id,
            decision_latency_ms=(time.time() - start_time) * 1000.0,
        )
        self.diagnostics_service.record_decision(decision)

        return True, assignment, decision
