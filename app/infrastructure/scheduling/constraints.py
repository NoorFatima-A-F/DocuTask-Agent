"""Hard Constraint Evaluation for Worker Candidate Filtering."""

from typing import List, Tuple
from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.workers.models import Worker, WorkerStatus
from app.infrastructure.workers.lifecycle import WorkerLifecycleStateMachine
from app.infrastructure.workers.leases import WorkerLeaseManager
from app.infrastructure.workers.capabilities import WorkerCapabilityRegistry


class ConstraintEvaluator:
    """Evaluates mandatory hard constraints before candidate scoring."""

    def __init__(
        self,
        capability_registry: WorkerCapabilityRegistry,
        lease_manager: WorkerLeaseManager,
    ) -> None:
        self.capability_registry = capability_registry
        self.lease_manager = lease_manager

    def evaluate_worker(self, worker: Worker, workload: WorkloadRequest) -> Tuple[bool, List[str]]:
        """Validate if worker satisfies all hard non-negotiable constraints."""
        reasons = []

        # 1. State & Schedulability
        if not WorkerLifecycleStateMachine.is_schedulable(worker.status):
            reasons.append(f"Worker '{worker.worker_id}' is in non-schedulable state '{worker.status.value}'.")

        # 2. Worker Lease Validity
        if not self.lease_manager.is_lease_valid(worker.worker_id):
            reasons.append(f"Worker '{worker.worker_id}' heartbeat lease is expired or invalid.")

        # 3. Worker Constraints
        if workload.worker_constraints and worker.worker_id not in workload.worker_constraints:
            reasons.append(f"Worker '{worker.worker_id}' is not in requested worker constraints.")

        # 4. Tenant Restrictions
        if worker.tenant_restrictions and workload.tenant_id not in worker.tenant_restrictions:
            reasons.append(f"Worker '{worker.worker_id}' is restricted, excluding tenant '{workload.tenant_id}'.")

        # 5. Mandatory Capabilities
        if workload.required_capabilities:
            if not self.capability_registry.satisfies_capabilities(
                worker.worker_id, workload.required_capabilities
            ):
                missing = workload.required_capabilities - worker.capabilities
                reasons.append(f"Worker '{worker.worker_id}' missing mandatory capabilities: {list(missing)}.")

        # 6. Resource Capacity Check
        avail = worker.resource_available
        req = workload.resource_requirements
        if avail.cpu_cores < req.cpu_cores:
            reasons.append(f"Insufficient CPU on worker '{worker.worker_id}': free={avail.cpu_cores}, req={req.cpu_cores}.")
        if avail.memory_gb < req.memory_gb:
            reasons.append(f"Insufficient Memory on worker '{worker.worker_id}': free={avail.memory_gb}GB, req={req.memory_gb}GB.")
        if req.gpu_count > 0 and avail.gpu_count < req.gpu_count:
            reasons.append(f"Insufficient GPU on worker '{worker.worker_id}': free={avail.gpu_count}, req={req.gpu_count}.")
        if avail.worker_slots < req.worker_slots:
            reasons.append(f"Insufficient Slots on worker '{worker.worker_id}': free={avail.worker_slots}, req={req.worker_slots}.")

        # 7. Worker Concurrency Limit
        if len(worker.active_assignments) >= worker.concurrency_limit:
            reasons.append(f"Worker '{worker.worker_id}' reached concurrency limit ({worker.concurrency_limit}).")

        return len(reasons) == 0, reasons
