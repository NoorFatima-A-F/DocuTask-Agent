"""Global Control Plane Manager orchestrating all regions and multi-cluster topologies."""

import threading
from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.models import RegionStatus
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.control_plane.global_cp.state import GlobalControlPlaneState
from app.infrastructure.control_plane.global_cp.coordinator import GlobalCoordinator


class GlobalControlPlane:
    """Master Control Plane coordinating multi-region infrastructure."""

    def __init__(
        self,
        cluster_registry: Optional[ClusterRegistry] = None,
        region_registry: Optional[RegionRegistry] = None,
        control_plane_id: str = "gcp_global_primary",
    ):
        self.cluster_registry = cluster_registry or ClusterRegistry()
        self.region_registry = region_registry or RegionRegistry()
        self.coordinator = GlobalCoordinator(self.region_registry)
        self.control_plane_id = control_plane_id
        self._lock = threading.RLock()

    def get_state(self) -> GlobalControlPlaneState:
        """Construct global control plane snapshot."""
        with self._lock:
            all_regions = self.region_registry.list_regions()
            active_regions = [r for r in all_regions if r.status == RegionStatus.ACTIVE]
            all_clusters = self.cluster_registry.list_clusters()
            healthy_clusters = [
                c for c in all_clusters
                if c.status in (ClusterStatus.READY, ClusterStatus.ACTIVE)
                and c.health_status == "HEALTHY"
            ]

            return GlobalControlPlaneState(
                control_plane_id=self.control_plane_id,
                version="3.1.0",
                is_leader=True,
                active_regions_count=len(active_regions),
                total_clusters_count=len(all_clusters),
                healthy_clusters_count=len(healthy_clusters),
                synced_at=datetime.now(timezone.utc),
                epoch=self.coordinator.epoch,
                metadata={
                    "total_regions": str(len(all_regions)),
                    "total_clusters": str(len(all_clusters)),
                },
            )

    def register_cluster_globally(self, cluster: Cluster) -> Cluster:
        """Register a cluster into the global registry and assign it to its designated region."""
        with self._lock:
            registered = self.cluster_registry.register_cluster(cluster)
            # Link cluster to region
            self.region_registry.assign_cluster_to_region(cluster.region_id, cluster.cluster_id)
            self.coordinator.bump_epoch()
            return registered

    def deregister_cluster_globally(self, cluster_id: str) -> bool:
        """Deregister cluster globally and remove from region association."""
        with self._lock:
            cluster = self.cluster_registry.get_cluster(cluster_id)
            if not cluster:
                return False
            self.region_registry.remove_cluster_from_region(cluster.region_id, cluster_id)
            self.cluster_registry.delete_cluster(cluster_id)
            self.coordinator.bump_epoch()
            return True

    def get_global_cluster_topology(self) -> Dict[str, List[Cluster]]:
        """Return topology grouped by region_id."""
        with self._lock:
            result: Dict[str, List[Cluster]] = {}
            for region in self.region_registry.list_regions():
                clusters = self.cluster_registry.list_clusters(region_id=region.region_id)
                result[region.region_id] = clusters
            return result
