"""Fairness Scheduling across Multi-Tenant Workloads."""

from collections import defaultdict
import threading
from typing import Dict, List, Optional
from app.infrastructure.executions.workload import WorkloadRequest


class FairnessScheduler:
    """Fairness Engine preventing tenant starvation using Deficit Fair Share."""

    def __init__(self, default_quantum: int = 10):
        self.default_quantum = default_quantum
        self._tenant_deficits: Dict[str, float] = defaultdict(lambda: float(default_quantum))
        self._tenant_active_counts: Dict[str, int] = defaultdict(int)
        self._lock = threading.RLock()

    def record_workload_start(self, tenant_id: str) -> None:
        with self._lock:
            self._tenant_active_counts[tenant_id] += 1
            self._tenant_deficits[tenant_id] = max(0.0, self._tenant_deficits[tenant_id] - 1.0)

    def record_workload_finish(self, tenant_id: str) -> None:
        with self._lock:
            self._tenant_active_counts[tenant_id] = max(0, self._tenant_active_counts[tenant_id] - 1)
            self._tenant_deficits[tenant_id] += 1.0

    def calculate_fairness_penalty(self, tenant_id: str) -> float:
        """Calculate penalty factor (0.0 to 1.0) based on tenant load compared to deficit."""
        with self._lock:
            active = self._tenant_active_counts.get(tenant_id, 0)
            if active <= 0:
                return 0.0
            # Higher active jobs relative to baseline increases fairness penalty
            return min(1.0, active / float(self.default_quantum * 2))

    def sort_workloads_fairly(self, workloads: List[WorkloadRequest]) -> List[WorkloadRequest]:
        """Interleave workloads across tenants using Deficit Fair Share order."""
        with self._lock:
            by_tenant: Dict[str, List[WorkloadRequest]] = defaultdict(list)
            for w in workloads:
                by_tenant[w.tenant_id].append(w)

            result: List[WorkloadRequest] = []
            active_tenants = list(by_tenant.keys())

            while active_tenants:
                remaining_tenants = []
                for t in active_tenants:
                    queue = by_tenant[t]
                    if queue:
                        result.append(queue.pop(0))
                        if queue:
                            remaining_tenants.append(t)
                active_tenants = remaining_tenants

            return result
