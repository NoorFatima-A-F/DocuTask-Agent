"""
Distributed Transaction & State Consistency Verifier.
"""
from typing import List, Dict, Any
from app.platform_verification.service_communication.domain.models import DistributedConsistencyReport
from app.platform_verification.service_communication.domain.interfaces import IDistributedConsistencyVerifier


class DistributedConsistencyVerifier(IDistributedConsistencyVerifier):
    """Verifies idempotency keys, compensation actions, and orphan state prevention."""

    def verify_consistency(self, workflows: List[Dict[str, Any]]) -> DistributedConsistencyReport:
        idempotent_ok = True
        orphan_prevented = True
        no_duplicate_queue = True
        compensation_ok = True

        for wf in workflows:
            if not wf.get("uses_idempotency_key", True):
                idempotent_ok = False

            if wf.get("orphan_records_created_on_crash", False):
                orphan_prevented = False

            if wf.get("duplicate_queue_task_on_retry", False):
                no_duplicate_queue = False

            if not wf.get("has_compensation_rollback", True):
                compensation_ok = False

        all_ok = idempotent_ok and orphan_prevented and no_duplicate_queue and compensation_ok
        status = "PASS" if all_ok else "FAIL"

        return DistributedConsistencyReport(
            idempotency_keys_enforced=idempotent_ok,
            orphan_documents_prevented=orphan_prevented,
            duplicate_queue_tasks_prevented=no_duplicate_queue,
            compensation_actions_verified=compensation_ok,
            status=status,
        )
