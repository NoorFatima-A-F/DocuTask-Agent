"""Routing Eligibility Engine for Deterministic Cluster & Region Selection."""

from typing import List, Optional
from app.infrastructure.clusters.models import Cluster, ClusterStatus
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.clusters.policies import ClusterPolicyEngine
from app.infrastructure.clusters.labels import ClusterLabelingSystem
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.policies import RegionPolicyEngine
from app.infrastructure.regions.affinity import TenantAffinityManager
from app.infrastructure.routing.metadata import RoutingDecision, WorkloadRoutingRequest


class RoutingEligibilityEngine:
    """Evaluates cluster and regional eligibility for workloads across the enterprise topology."""

    def __init__(
        self,
        cluster_registry: ClusterRegistry,
        region_registry: RegionRegistry,
        affinity_manager: Optional[TenantAffinityManager] = None,
        cluster_policy_engine: Optional[ClusterPolicyEngine] = None,
        region_policy_engine: Optional[RegionPolicyEngine] = None,
    ):
        self.cluster_registry = cluster_registry
        self.region_registry = region_registry
        self.affinity_manager = affinity_manager or TenantAffinityManager()
        self.cluster_policy_engine = cluster_policy_engine or ClusterPolicyEngine()
        self.region_policy_engine = region_policy_engine or RegionPolicyEngine()
        self.label_system = ClusterLabelingSystem()

    def evaluate_routing(self, request: WorkloadRoutingRequest) -> RoutingDecision:
        """Evaluate all clusters and regions to select an optimal eligible cluster for the workload."""
        rejection_reasons: List[str] = []
        candidate_clusters: List[Cluster] = []

        all_clusters = self.cluster_registry.list_clusters()
        if not all_clusters:
            return RoutingDecision(
                is_routable=False,
                rejection_reasons=["No clusters registered in the platform."],
            )

        for cluster in all_clusters:
            cluster_id = cluster.cluster_id

            # 1. State & Health check
            if cluster.status not in (ClusterStatus.READY, ClusterStatus.ACTIVE):
                rejection_reasons.append(f"Cluster '{cluster_id}' is in non-routable state '{cluster.status.value}'.")
                continue

            if cluster.health_status != "HEALTHY":
                rejection_reasons.append(f"Cluster '{cluster_id}' health status is '{cluster.health_status}'.")
                continue

            # Check heartbeat lease
            if cluster.active_lease and not cluster.active_lease.is_valid:
                rejection_reasons.append(f"Cluster '{cluster_id}' heartbeat lease has expired.")
                continue

            # 2. Region & Jurisdiction check
            region = self.region_registry.get_region(cluster.region_id)
            if not region:
                rejection_reasons.append(f"Cluster '{cluster_id}' belongs to unregistered region '{cluster.region_id}'.")
                continue

            if request.target_region and cluster.region_id != request.target_region:
                continue

            if request.required_jurisdiction:
                res_ok, res_errs = self.region_policy_engine.evaluate_data_residency(
                    region, request.required_jurisdiction
                )
                if not res_ok:
                    rejection_reasons.extend(res_errs)
                    continue

            # 3. Tenant Affinity check
            if not self.affinity_manager.is_region_allowed_for_tenant(request.tenant_id, cluster.region_id):
                rejection_reasons.append(
                    f"Tenant '{request.tenant_id}' is not permitted in region '{cluster.region_id}'."
                )
                continue

            if cluster.tenant_affinity and request.tenant_id not in cluster.tenant_affinity:
                rejection_reasons.append(
                    f"Tenant '{request.tenant_id}' not allowed in dedicated cluster '{cluster_id}'."
                )
                continue

            # 4. Workload, Capabilities & Compliance
            if request.workload_type not in cluster.supported_workloads:
                rejection_reasons.append(
                    f"Cluster '{cluster_id}' does not support workload '{request.workload_type}'."
                )
                continue

            if not request.required_capabilities.issubset(cluster.capabilities):
                missing_caps = request.required_capabilities - cluster.capabilities
                rejection_reasons.append(
                    f"Cluster '{cluster_id}' is missing required capabilities: {list(missing_caps)}."
                )
                continue

            comp_ok, comp_errs = self.region_policy_engine.validate_compliance(
                region, request.required_compliance
            )
            if not comp_ok:
                rejection_reasons.extend(comp_errs)
                continue

            # 5. Labels selector
            if request.labels_selector:
                match_ok, match_errs = self.label_system.matches_selector(
                    cluster.labels, request.labels_selector
                )
                if not match_ok:
                    rejection_reasons.extend([f"Cluster '{cluster_id}': {e}" for e in match_errs])
                    continue

            # 6. Capacity check
            avail_cpu = cluster.capacity.allocatable_cpu_cores - cluster.capacity.utilized_cpu_cores
            avail_mem = cluster.capacity.allocatable_memory_gb - cluster.capacity.utilized_memory_gb
            if avail_cpu < request.min_cpu_cores or avail_mem < request.min_memory_gb:
                rejection_reasons.append(
                    f"Cluster '{cluster_id}' has insufficient capacity: free_cpu={avail_cpu}, free_mem={avail_mem}."
                )
                continue

            candidate_clusters.append(cluster)

        if not candidate_clusters:
            return RoutingDecision(
                is_routable=False,
                rejection_reasons=rejection_reasons,
            )

        # Rank candidate clusters by available CPU capacity (highest available first)
        candidate_clusters.sort(
            key=lambda c: (
                c.capacity.allocatable_cpu_cores - c.capacity.utilized_cpu_cores
            ),
            reverse=True,
        )

        selected = candidate_clusters[0]
        return RoutingDecision(
            is_routable=True,
            selected_cluster_id=selected.cluster_id,
            selected_region_id=selected.region_id,
            candidate_cluster_ids=[c.cluster_id for c in candidate_clusters],
            rejection_reasons=[],
        )
