"""Cluster Health Aggregation and Heartbeat Lease System."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .models import Cluster, ClusterLease, ClusterStatus


class ComponentHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class SubComponentHealth(BaseModel):
    """Health status of an individual subsystem component."""

    component_name: str
    is_healthy: bool = True
    status: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    message: Optional[str] = None


class ClusterHealthReport(BaseModel):
    """Aggregated health report across all sub-components of a cluster."""

    cluster_id: Optional[str] = None
    is_healthy: bool = True
    status: str = "HEALTHY"  # HEALTHY, DEGRADED, UNHEALTHY, UNREACHABLE, MAINTENANCE
    degraded_components: List[str] = Field(default_factory=list)
    sub_components: List[SubComponentHealth] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClusterComponentHealth(BaseModel):
    """Health status of standard infrastructure subsystems in a cluster."""

    node_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    service_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    worker_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    queue_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    database_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    cache_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    storage_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    network_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    telemetry_health: ComponentHealthStatus = ComponentHealthStatus.HEALTHY
    last_reported: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClusterHealthAggregator:
    """Aggregates sub-component signals and manages heartbeat leases."""

    def __init__(self) -> None:
        self._component_health: Dict[str, ClusterComponentHealth] = {}
        self._leases: Dict[str, ClusterLease] = {}

    def report_heartbeat(
        self,
        cluster_id: str,
        components: Optional[ClusterComponentHealth] = None,
        ttl_seconds: int = 60,
    ) -> ClusterLease:
        """Renew cluster lease and record component telemetry."""
        return self.create_or_renew_lease(cluster_id, ttl_seconds=ttl_seconds, components=components)

    def create_or_renew_lease(
        self,
        cluster_id: str,
        ttl_seconds: int = 60,
        components: Optional[ClusterComponentHealth] = None,
    ) -> ClusterLease:
        """Create or renew heartbeat lease for a cluster."""
        now = datetime.now(timezone.utc)
        lease = self._leases.get(cluster_id)
        if not lease:
            lease = ClusterLease(cluster_id=cluster_id, ttl_seconds=ttl_seconds, last_renewed=now, is_valid=True)
            self._leases[cluster_id] = lease
        else:
            lease.last_renewed = now
            lease.ttl_seconds = ttl_seconds
            lease.is_valid = True

        if components:
            self._component_health[cluster_id] = components

        return lease

    def is_lease_valid(self, lease: Optional[ClusterLease]) -> bool:
        """Check if lease object is non-expired."""
        if not lease:
            return False
        now = datetime.now(timezone.utc)
        elapsed = (now - lease.last_renewed).total_seconds()
        if elapsed > lease.ttl_seconds:
            lease.is_valid = False
            return False
        return lease.is_valid

    def check_lease(self, cluster_id: str) -> bool:
        """Verify if cluster lease is currently active in memory."""
        lease = self._leases.get(cluster_id)
        return self.is_lease_valid(lease)

    def evaluate_health(
        self, sub_components: List[SubComponentHealth], cluster_id: Optional[str] = None
    ) -> ClusterHealthReport:
        """Evaluate a list of sub-components and produce a health report."""
        degraded = [s.component_name for s in sub_components if not s.is_healthy]
        is_healthy = len(degraded) == 0
        status_str = "HEALTHY" if is_healthy else "DEGRADED"

        return ClusterHealthReport(
            cluster_id=cluster_id,
            is_healthy=is_healthy,
            status=status_str,
            degraded_components=degraded,
            sub_components=sub_components,
        )

    def calculate_cluster_health(self, cluster: Cluster) -> str:
        """Compute composite cluster health."""
        if cluster.status == ClusterStatus.MAINTENANCE:
            return "MAINTENANCE"

        if cluster.active_lease and not self.is_lease_valid(cluster.active_lease):
            return "UNREACHABLE"

        if not self.check_lease(cluster.cluster_id) and not cluster.active_lease:
            return "HEALTHY"  # If no lease tracking configured yet

        comp = self._component_health.get(cluster.cluster_id)
        if not comp:
            return "HEALTHY"

        statuses = [
            comp.node_health,
            comp.service_health,
            comp.worker_health,
            comp.queue_health,
            comp.database_health,
            comp.cache_health,
            comp.storage_health,
            comp.network_health,
            comp.telemetry_health,
        ]

        if any(s == ComponentHealthStatus.UNHEALTHY for s in statuses):
            return "UNHEALTHY"
        elif any(s == ComponentHealthStatus.DEGRADED for s in statuses):
            return "DEGRADED"

        return "HEALTHY"

    def check_all_leases(self, clusters: List[Cluster]) -> List[str]:
        """Check all leases and return IDs of expired clusters."""
        expired = []
        for c in clusters:
            if c.active_lease and not self.is_lease_valid(c.active_lease):
                expired.append(c.cluster_id)
            elif c.cluster_id in self._leases and not self.check_lease(c.cluster_id):
                expired.append(c.cluster_id)
        return expired

    def get_expired_clusters(self) -> List[str]:
        """Return list of cluster IDs whose heartbeat lease has lapsed."""
        return [cid for cid in self._leases.keys() if not self.check_lease(cid)]
