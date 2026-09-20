"""Topology Selectors for Cluster and Regional Filtering."""

from typing import List, Optional, Set
from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.models import Region, RegionStatus
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.executions.workload import WorkloadRequest


class RegionSelector:
    """Selects eligible regions for a workload considering hard residency and constraints."""

    def __init__(self, region_registry: RegionRegistry):
        self.region_registry = region_registry

    def select_eligible_regions(self, workload: WorkloadRequest) -> List[Region]:
        all_regions = self.region_registry.list_regions(status=RegionStatus.ACTIVE)

        eligible = []
        for reg in all_regions:
            # 1. Hard region constraints
            if workload.region_constraints and reg.region_id not in workload.region_constraints:
                continue

            # 2. Jurisdiction check
            if workload.required_jurisdiction and workload.required_jurisdiction.upper() != "GLOBAL":
                if (
                    reg.data_residency_jurisdiction.upper() != workload.required_jurisdiction.upper()
                    and reg.geography.jurisdiction.upper() != workload.required_jurisdiction.upper()
                ):
                    continue

            eligible.append(reg)

        return eligible


class ClusterSelector:
    """Selects eligible clusters within a region for a workload."""

    def __init__(self, cluster_registry: ClusterRegistry):
        self.cluster_registry = cluster_registry

    def select_eligible_clusters(
        self, workload: WorkloadRequest, region_id: str
    ) -> List[Cluster]:
        clusters = self.cluster_registry.list_clusters(
            region_id=region_id, status=ClusterStatus.ACTIVE
        )

        eligible = []
        for cluster in clusters:
            if cluster.health_status != "HEALTHY":
                continue

            if workload.cluster_constraints and cluster.cluster_id not in workload.cluster_constraints:
                continue

            if workload.tenant_id and cluster.tenant_affinity:
                if workload.tenant_id not in cluster.tenant_affinity:
                    continue

            # Workload type support
            if workload.workload_type.value.lower() not in [w.lower() for w in cluster.supported_workloads]:
                # Generic fallback if custom
                if "custom" not in [w.lower() for w in cluster.supported_workloads] and "workflow" not in [w.lower() for w in cluster.supported_workloads]:
                    continue

            eligible.append(cluster)

        return eligible
