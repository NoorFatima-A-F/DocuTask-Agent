"""Priority Scheduling and Anti-Starvation Aging Engine."""

from datetime import datetime, timezone
from typing import Dict, List
from app.infrastructure.executions.workload import WorkloadPriority, WorkloadRequest


class PriorityScheduler:
    """Calculates dynamic workload priorities with aging factors to eliminate starvation."""

    PRIORITY_BASE_SCORES: Dict[WorkloadPriority, float] = {
        WorkloadPriority.CRITICAL: 1000.0,
        WorkloadPriority.HIGH: 500.0,
        WorkloadPriority.NORMAL: 100.0,
        WorkloadPriority.LOW: 50.0,
        WorkloadPriority.BACKGROUND: 10.0,
        WorkloadPriority.MAINTENANCE: 1.0,
    }

    def __init__(self, aging_rate_per_sec: float = 0.5):
        self.aging_rate_per_sec = aging_rate_per_sec

    def calculate_priority_score(self, workload: WorkloadRequest) -> float:
        """Calculate dynamic priority score = base_score + (wait_time * aging_rate)."""
        base = self.PRIORITY_BASE_SCORES.get(workload.priority, 100.0)
        now = datetime.now(timezone.utc)
        wait_seconds = max(0.0, (now - workload.submitted_at).total_seconds())
        aging_bonus = wait_seconds * self.aging_rate_per_sec
        return base + aging_bonus

    def order_workloads_by_priority(self, workloads: List[WorkloadRequest]) -> List[WorkloadRequest]:
        """Sort workloads descending by dynamic priority score."""
        return sorted(workloads, key=self.calculate_priority_score, reverse=True)
