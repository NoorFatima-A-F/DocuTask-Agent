"""Regional Control Plane Manager for intra-region cluster management and health monitoring."""

import threading
from typing import List, Optional
from datetime import datetime, timezone

from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.control_plane.regional.state import RegionalControlPlaneState
from app.infrastructure.control_plane.regional.coordinator import RegionalCoordinator


class RegionalControlPlane:
    """Controls clusters, health, and admission within a dedicated region."""

    def __init__(
        self,
        region_id: str,
        cluster_registry: ClusterRegistry,
        control_plane_id: Optional[str] = None,
    ):
        self.region_id = region_id
        self.cluster_registry = cluster_registry
        self.control_plane_id = control_plane_id or f"rcp_{region_id}"
        self.coordinator = RegionalCoordinator(self.region_id, self.cluster_registry)
        self._lock = threading.RLock()

    def get_state(self) -> RegionalControlPlaneState:
        """Construct Regional Control Plane state snapshot."""
        with self._lock:
            local_clusters = self.cluster_registry.list_clusters(region_id=self.region_id)
            active_count = sum(1 for c in local_clusters if c.status == ClusterStatus.ACTIVE)
            degraded_count = sum(1 for c in local_clusters if c.status == ClusterStatus.DEGRADED)

            return RegionalControlPlaneState(
                region_id=self.region_id,
                control_plane_id=self.control_plane_id,
                is_active=True,
                local_clusters_count=len(local_clusters),
                active_clusters_count=active_count,
                degraded_clusters_count=degraded_count,
                last_heartbeat=datetime.now(timezone.utc),
                synced_epoch=self.coordinator.synced_epoch,
                metadata={"cluster_ids": ",".join(c.cluster_id for c in local_clusters)},
            )

    def admit_cluster(self, cluster: Cluster) -> Cluster:
        """Admit a cluster into this region, ensuring region_id alignment and initial transition."""
        with self._lock:
            cluster.region_id = self.region_id
            return self.cluster_registry.register_cluster(cluster)

    def list_local_clusters(self, status: Optional[ClusterStatus] = None) -> List[Cluster]:
        """List clusters strictly belonging to this region."""
        with self._lock:
            return self.cluster_registry.list_clusters(
                region_id=self.region_id, status=status
            )
