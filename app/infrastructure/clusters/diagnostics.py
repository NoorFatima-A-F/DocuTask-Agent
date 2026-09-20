"""Cluster Diagnostics and Inspection Platform."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .health import ClusterHealthAggregator
from .models import CapacityModel, Cluster, ClusterStatus


class ClusterDiagnosticsReport(BaseModel):
    """Structured operational diagnostic report for a cluster."""

    cluster_id: str
    name: str
    region_id: str
    environment: str
    status: str
    health_status: str
    control_plane_version: str
    data_plane_version: str
    capabilities: List[str]
    capacity: CapacityModel
    lease_active: bool
    quarantined: bool
    maintenance: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClusterDiagnosticsService:
    """Produces comprehensive diagnostics snapshots for clusters."""

    def __init__(self, provider: Union[ClusterHealthAggregator, Any]) -> None:
        # Can accept ClusterHealthAggregator or ClusterRegistry
        if hasattr(provider, "health_aggregator"):
            self.registry = provider
            self.health_aggregator = provider.health_aggregator
        else:
            self.registry = None
            self.health_aggregator = provider

    def generate_diagnostics(self, cluster: Cluster) -> ClusterDiagnosticsReport:
        computed_health = self.health_aggregator.calculate_cluster_health(cluster)
        lease_valid = self.health_aggregator.check_lease(cluster.cluster_id) or (
            cluster.active_lease is not None and cluster.active_lease.is_valid
        )

        return ClusterDiagnosticsReport(
            cluster_id=cluster.cluster_id,
            name=cluster.name,
            region_id=cluster.region_id,
            environment=cluster.environment,
            status=cluster.status.value,
            health_status=computed_health,
            control_plane_version=cluster.control_plane_version,
            data_plane_version=cluster.data_plane_version,
            capabilities=sorted(list(cluster.capabilities)),
            capacity=cluster.capacity,
            lease_active=lease_valid,
            quarantined=cluster.status == ClusterStatus.SUSPENDED,
            maintenance=cluster.status == ClusterStatus.MAINTENANCE,
        )

    def generate_cluster_report(self, target: Union[str, Cluster]) -> ClusterDiagnosticsReport:
        if isinstance(target, Cluster):
            return self.generate_diagnostics(target)

        if not self.registry:
            raise ValueError("Registry required to resolve cluster by ID.")

        cluster = self.registry.get_cluster(target)
        if not cluster:
            raise ValueError(f"Cluster '{target}' not found in registry.")

        return self.generate_diagnostics(cluster)
