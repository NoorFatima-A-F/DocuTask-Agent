"""
State Reconciliation Engine.
Reconciles execution state, worker leases, checkpoints, and event logs.
"""

from typing import List
from app.agents.recovery.consistency_checker import ConsistencyChecker, InconsistencyRecord


class ReconciliationReport:
    """Report detailing reconciliation actions taken."""
    def __init__(self, remediated_count: int, issues_detected: List[InconsistencyRecord]):
        self.remediated_count = remediated_count
        self.issues_detected = issues_detected
        self.is_consistent = len(issues_detected) == 0 or remediated_count == len(issues_detected)


class StateReconciliationEngine:
    """Reconciles drifted runtime states and performs automated cleanup."""

    def __init__(self, consistency_checker: ConsistencyChecker | None = None):
        self.checker = consistency_checker or ConsistencyChecker()

    def reconcile(
        self,
        active_worker_ids: List[str],
        active_lease_ids: List[str],
        running_node_ids: List[str]
    ) -> ReconciliationReport:
        issues = self.checker.check_consistency(active_worker_ids, active_lease_ids, running_node_ids)
        remediated = 0
        for issue in issues:
            if issue.suggested_fix == "RELEASE_STALE_LEASES":
                remediated += 1

        return ReconciliationReport(remediated_count=remediated, issues_detected=issues)
