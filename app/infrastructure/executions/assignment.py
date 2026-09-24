"""Workload Assignment Tracking and Worker Dispatch."""

from datetime import datetime, timezone
from enum import Enum
import secrets
import threading
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.executions.workload import ResourceRequirements, WorkloadRequest
from app.infrastructure.workers.models import Worker
from app.infrastructure.workers.registry import WorkerRegistry


class AssignmentStatus(str, Enum):
    PENDING_ACK = "PENDING_ACK"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    RECOVERY_PENDING = "RECOVERY_PENDING"


class WorkloadAssignment(BaseModel):
    """Record linking a workload to a specific worker execution attempt."""

    assignment_id: str = Field(default_factory=lambda: f"asg_{secrets.token_hex(8)}")
    workload_id: str
    worker_id: str
    reservation_id: str
    execution_lease_id: str
    attempt: int = 1
    status: AssignmentStatus = AssignmentStatus.PENDING_ACK
    allocated_resources: ResourceRequirements = Field(default_factory=ResourceRequirements)
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class AssignmentManager:
    """Manages assignment state, worker ACKs, and resource accounting updates."""

    def __init__(self, worker_registry: WorkerRegistry) -> None:
        self.worker_registry = worker_registry
        self._assignments: Dict[str, WorkloadAssignment] = {}
        self._workload_assignments: Dict[str, List[str]] = {}  # workload_id -> list of assignment_ids
        self._lock = threading.RLock()

    def create_assignment(
        self,
        workload: WorkloadRequest,
        worker: Worker,
        reservation_id: str,
        execution_lease_id: str,
        attempt: int = 1,
    ) -> WorkloadAssignment:
        """Create and record an assignment for a selected worker."""
        with self._lock:
            assignment = WorkloadAssignment(
                workload_id=workload.workload_id,
                worker_id=worker.worker_id,
                reservation_id=reservation_id,
                execution_lease_id=execution_lease_id,
                attempt=attempt,
                allocated_resources=workload.resource_requirements,
                status=AssignmentStatus.PENDING_ACK,
            )
            self._assignments[assignment.assignment_id] = assignment
            if workload.workload_id not in self._workload_assignments:
                self._workload_assignments[workload.workload_id] = []
            self._workload_assignments[workload.workload_id].append(assignment.assignment_id)

            # Update worker active assignments
            if assignment.assignment_id not in worker.active_assignments:
                worker.active_assignments.append(assignment.assignment_id)

            return assignment

    def acknowledge_assignment(self, assignment_id: str) -> Optional[WorkloadAssignment]:
        """Worker ACKs assignment reception and begins execution."""
        with self._lock:
            asg = self._assignments.get(assignment_id)
            if not asg:
                return None
            asg.status = AssignmentStatus.RUNNING
            asg.started_at = datetime.now(timezone.utc)
            return asg

    def complete_assignment(self, assignment_id: str) -> Optional[WorkloadAssignment]:
        """Mark assignment as successfully completed."""
        with self._lock:
            asg = self._assignments.get(assignment_id)
            if not asg:
                return None
            asg.status = AssignmentStatus.COMPLETED
            asg.completed_at = datetime.now(timezone.utc)

            # Free worker slot
            worker = self.worker_registry.get_worker(asg.worker_id)
            if worker and assignment_id in worker.active_assignments:
                worker.active_assignments.remove(assignment_id)

            return asg

    def fail_assignment(self, assignment_id: str, error_message: str = "") -> Optional[WorkloadAssignment]:
        """Mark assignment as failed."""
        with self._lock:
            asg = self._assignments.get(assignment_id)
            if not asg:
                return None
            asg.status = AssignmentStatus.FAILED
            asg.completed_at = datetime.now(timezone.utc)
            asg.error_message = error_message

            worker = self.worker_registry.get_worker(asg.worker_id)
            if worker and assignment_id in worker.active_assignments:
                worker.active_assignments.remove(assignment_id)

            return asg

    def get_assignment(self, assignment_id: str) -> Optional[WorkloadAssignment]:
        with self._lock:
            return self._assignments.get(assignment_id)

    def get_assignments_for_workload(self, workload_id: str) -> List[WorkloadAssignment]:
        with self._lock:
            ids = self._workload_assignments.get(workload_id, [])
            return [self._assignments[aid] for aid in ids if aid in self._assignments]

    def get_active_assignment(self, workload_id: str) -> Optional[WorkloadAssignment]:
        with self._lock:
            assignments = self.get_assignments_for_workload(workload_id)
            for asg in reversed(assignments):
                if asg.status in (AssignmentStatus.PENDING_ACK, AssignmentStatus.RUNNING):
                    return asg
            return None
