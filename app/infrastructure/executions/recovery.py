"""Lost Worker Detection and Safe Recovery Coordinator."""

from datetime import datetime, timezone
from enum import Enum
import threading
from typing import Dict, List, Optional, Tuple

from app.infrastructure.executions.workload import WorkloadRequest, WorkloadState
from app.infrastructure.executions.assignment import AssignmentManager, AssignmentStatus
from app.infrastructure.executions.leases import ExecutionLeaseManager
from app.infrastructure.workers.models import Worker, WorkerStatus
from app.infrastructure.workers.registry import WorkerRegistry


class RecoveryClassification(str, Enum):
    SAFE_TO_RETRY = "SAFE_TO_RETRY"
    REQUIRES_COMPENSATION = "REQUIRES_COMPENSATION"
    REQUIRES_MANUAL_REVIEW = "REQUIRES_MANUAL_REVIEW"
    NON_RETRYABLE = "NON_RETRYABLE"
    UNKNOWN = "UNKNOWN"


class LostWorkerRecoveryCoordinator:
    """Detects unresponsive or crashed workers and coordinates safe workload recovery."""

    def __init__(
        self,
        worker_registry: WorkerRegistry,
        assignment_manager: AssignmentManager,
        lease_manager: ExecutionLeaseManager,
    ) -> None:
        self.worker_registry = worker_registry
        self.assignment_manager = assignment_manager
        self.lease_manager = lease_manager
        self._recovered_workloads: List[str] = []
        self._lock = threading.RLock()

    def classify_workload_recovery(self, workload: WorkloadRequest) -> RecoveryClassification:
        """Classify retry safety according to retry policy and attempt counts."""
        if workload.retry_count >= workload.max_retries:
            return RecoveryClassification.NON_RETRYABLE

        # Idempotent or read-only tasks are safe to retry
        if workload.idempotency_key or workload.workload_type.value in ("OCR_JOB", "EMBEDDING_JOB", "EVALUATION_JOB"):
            return RecoveryClassification.SAFE_TO_RETRY

        # Non-idempotent custom or connector mutations require review
        if workload.workload_type.value in ("CONNECTOR_TASK", "CUSTOM"):
            return RecoveryClassification.REQUIRES_MANUAL_REVIEW

        return RecoveryClassification.SAFE_TO_RETRY

    def scan_and_recover_lost_workers(
        self, active_workloads: Dict[str, WorkloadRequest]
    ) -> List[Tuple[str, RecoveryClassification]]:
        """Scan for workers with expired leases and evaluate recovery for their in-flight assignments."""
        with self._lock:
            recovered = []
            expired_workers = self.worker_registry.heartbeat_manager.scan_dead_workers()

            for worker_id in expired_workers:
                worker = self.worker_registry.get_worker(worker_id)
                if not worker:
                    continue

                # Mark worker UNAVAILABLE
                if worker.status != WorkerStatus.UNAVAILABLE and worker.status != WorkerStatus.TERMINATED:
                    self.worker_registry.transition_worker_state(
                        worker_id, WorkerStatus.UNAVAILABLE, reason="Heartbeat lease expired"
                    )

                # Process all in-flight assignments on this worker
                for asg_id in list(worker.active_assignments):
                    asg = self.assignment_manager.get_assignment(asg_id)
                    if not asg or asg.status not in (AssignmentStatus.PENDING_ACK, AssignmentStatus.RUNNING):
                        continue

                    workload = active_workloads.get(asg.workload_id)
                    if not workload:
                        continue

                    classification = self.classify_workload_recovery(workload)

                    # Fail the stale assignment
                    self.assignment_manager.fail_assignment(
                        asg_id, error_message=f"Worker '{worker_id}' lost connectivity (lease expired)."
                    )

                    # Release execution lease
                    self.lease_manager.release_lease(asg.execution_lease_id)

                    if classification == RecoveryClassification.SAFE_TO_RETRY:
                        workload.retry_count += 1
                        workload.state = WorkloadState.RETRY_PENDING
                    elif classification == RecoveryClassification.NON_RETRYABLE:
                        workload.state = WorkloadState.FAILED
                    else:
                        workload.state = WorkloadState.BLOCKED

                    recovered.append((workload.workload_id, classification))
                    self._recovered_workloads.append(workload.workload_id)

            return recovered
