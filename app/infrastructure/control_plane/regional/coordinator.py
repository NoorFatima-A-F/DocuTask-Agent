"""Regional Coordinator for local cluster reconciliation and heartbeat tracking."""

import threading
from typing import Dict
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.clusters.models import ClusterStatus


class RegionalCoordinator:
    """Coordinates local cluster reconciliation and health within a specific region."""

    def __init__(self, region_id: str, cluster_registry: ClusterRegistry):
        self.region_id = region_id
        self.cluster_registry = cluster_registry
        self.synced_epoch = 1
        self._lock = threading.RLock()

    def reconcile_local_clusters(self) -> Dict[str, str]:
        """Perform reconciliation of all clusters belonging to this region."""
        with self._lock:
            # Check for any expired leases or unreachable clusters
            expired = self.cluster_registry.health_aggregator.check_all_leases(
                self.cluster_registry.list_clusters(region_id=self.region_id)
            )
            for c_id in expired:
                self.cluster_registry.update_cluster_status(c_id, ClusterStatus.OFFLINE)
            
            # Return current status mapping
            clusters = self.cluster_registry.list_clusters(region_id=self.region_id)
            return {c.cluster_id: c.status.value for c in clusters}

    def update_epoch(self, new_epoch: int) -> None:
        """Update the synced epoch from Global Control Plane."""
        with self._lock:
            self.synced_epoch = new_epoch
