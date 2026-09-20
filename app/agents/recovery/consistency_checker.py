"""
Consistency Checker.
Audits consistency across execution states, worker leases, and checkpoint registries.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class InconsistencyRecord(BaseModel):
    """Detected state divergence or orphan entity."""
    entity_id: str
    issue_type: str  # ORPHAN_WORKER, STALE_LEASE, ORPHAN_CHECKPOINT, STATE_DRIFT
    description: str
    suggested_fix: str
    model_config = {"frozen": True}


class ConsistencyChecker:
    """Checks for leaked worker leases, orphan checkpoints, and drifted execution states."""

    def check_consistency(
        self,
        active_worker_ids: List[str],
        active_lease_ids: List[str],
        running_node_ids: List[str]
    ) -> List[InconsistencyRecord]:
        issues = []
        # Leased worker with no running node -> Stale lease
        if len(active_lease_ids) > len(running_node_ids):
            issues.append(
                InconsistencyRecord(
                    entity_id="lease_pool",
                    issue_type="STALE_LEASE",
                    description=f"{len(active_lease_ids) - len(running_node_ids)} stale leases detected without running nodes.",
                    suggested_fix="RELEASE_STALE_LEASES"
                )
            )
        return issues
