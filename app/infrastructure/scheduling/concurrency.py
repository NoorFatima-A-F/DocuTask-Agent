"""Multi-Level Concurrency Limit Controller."""

from collections import defaultdict
import threading
from typing import Dict, List, Optional, Tuple
from app.infrastructure.executions.workload import WorkloadRequest


class ConcurrencyController:
    """Tracks and enforces concurrency bounds across platform, region, cluster, worker, and tenant."""

    def __init__(
        self,
        platform_limit: int = 10000,
        tenant_default_limit: int = 50,
        region_default_limit: int = 2000,
        cluster_default_limit: int = 500,
    ) -> None:
        self.platform_limit = platform_limit
        self.tenant_default_limit = tenant_default_limit
        self.region_default_limit = region_default_limit
        self.cluster_default_limit = cluster_default_limit

        self._custom_tenant_limits: Dict[str, int] = {}
        self._tenant_counts: Dict[str, int] = defaultdict(int)
        self._region_counts: Dict[str, int] = defaultdict(int)
        self._cluster_counts: Dict[str, int] = defaultdict(int)
        self._total_platform_count: int = 0
        self._lock = threading.RLock()

    def set_tenant_limit(self, tenant_id: str, limit: int) -> None:
        with self._lock:
            self._custom_tenant_limits[tenant_id] = limit

    def can_admit_workload(
        self, workload: WorkloadRequest, region_id: str, cluster_id: str
    ) -> Tuple[bool, List[str]]:
        """Evaluate whether placing workload would breach any concurrency limit."""
        with self._lock:
            reasons = []

            # 1. Platform limit
            if self._total_platform_count + 1 > self.platform_limit:
                reasons.append(f"Global platform concurrency limit ({self.platform_limit}) reached.")

            # 2. Tenant limit
            tenant_limit = self._custom_tenant_limits.get(workload.tenant_id, self.tenant_default_limit)
            curr_tenant = self._tenant_counts[workload.tenant_id]
            if curr_tenant + 1 > tenant_limit:
                reasons.append(
                    f"Tenant '{workload.tenant_id}' concurrency limit ({tenant_limit}) reached (current={curr_tenant})."
                )

            # 3. Region limit
            curr_region = self._region_counts[region_id]
            if curr_region + 1 > self.region_default_limit:
                reasons.append(f"Region '{region_id}' concurrency limit ({self.region_default_limit}) reached.")

            # 4. Cluster limit
            curr_cluster = self._cluster_counts[cluster_id]
            if curr_cluster + 1 > self.cluster_default_limit:
                reasons.append(f"Cluster '{cluster_id}' concurrency limit ({self.cluster_default_limit}) reached.")

            return len(reasons) == 0, reasons

    def track_admission(self, workload: WorkloadRequest, region_id: str, cluster_id: str) -> None:
        with self._lock:
            self._total_platform_count += 1
            self._tenant_counts[workload.tenant_id] += 1
            self._region_counts[region_id] += 1
            self._cluster_counts[cluster_id] += 1

    def track_release(self, workload: WorkloadRequest, region_id: str, cluster_id: str) -> None:
        with self._lock:
            self._total_platform_count = max(0, self._total_platform_count - 1)
            self._tenant_counts[workload.tenant_id] = max(0, self._tenant_counts[workload.tenant_id] - 1)
            self._region_counts[region_id] = max(0, self._region_counts[region_id] - 1)
            self._cluster_counts[cluster_id] = max(0, self._cluster_counts[cluster_id] - 1)
