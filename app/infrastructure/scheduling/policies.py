"""Scheduling Policy Engine for Governance, Security, and Compliance Bounds."""

from typing import List, Tuple
from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.workers.models import Worker


class SchedulingPolicyEngine:
    """Evaluates high-level governance, security, and tenant compliance policies."""

    def evaluate_placement_policy(
        self, worker: Worker, workload: WorkloadRequest
    ) -> Tuple[bool, List[str]]:
        """Evaluate if placing workload onto worker violates any organizational policy."""
        violations = []

        # 1. Compliance check (e.g. HIPAA requires compliant worker capability)
        if "HIPAA" in workload.compliance_context:
            if "compliance.hipaa" not in worker.capabilities and "HIPAA" not in worker.labels.values():
                violations.append(f"Policy violation: Workload requires HIPAA compliance, worker '{worker.worker_id}' is non-compliant.")

        # 2. Air-Gapped / Isolated cluster policy
        if workload.security_context.get("air_gapped") == "true":
            if worker.labels.get("isolated") != "true":
                violations.append(f"Policy violation: Workload demands air-gapped isolation, worker '{worker.worker_id}' is not isolated.")

        return len(violations) == 0, violations
