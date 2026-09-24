"""High-Level Multi-Cluster & Multi-Region Management SDK."""

from typing import Any, Dict, List, Optional, Set
from app.infrastructure.clusters.models import (
    CapacityModel,
    Cluster,
    ClusterLease,
    ClusterStatus,
    ClusterType,
)
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.clusters.diagnostics import ClusterDiagnosticsService
from app.infrastructure.clusters.health import SubComponentHealth
from app.infrastructure.regions.models import Geography, Region, RegionStatus
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.affinity import TenantAffinityManager, TenantAffinityRule
from app.infrastructure.control_plane.global_cp.manager import GlobalControlPlane
from app.infrastructure.control_plane.topology.discovery import TopologyDiscoveryService
from app.infrastructure.control_plane.config.distributor import ConfigurationDistributor
from app.infrastructure.routing.metadata import WorkloadRoutingRequest, RoutingDecision
from app.infrastructure.routing.eligibility import RoutingEligibilityEngine


class ClusterSDK:
    """Unified Enterprise SDK for Multi-Cluster, Multi-Region & Control Plane operations."""

    def __init__(
        self,
        cluster_registry: Optional[ClusterRegistry] = None,
        region_registry: Optional[RegionRegistry] = None,
        persistence_dir: Optional[str] = None,
    ):
        c_path = f"{persistence_dir}/clusters.json" if persistence_dir else None
        r_path = f"{persistence_dir}/regions.json" if persistence_dir else None

        self.cluster_registry = cluster_registry or ClusterRegistry(persistence_path=c_path)
        self.region_registry = region_registry or RegionRegistry(persistence_path=r_path)
        self.affinity_manager = TenantAffinityManager()
        self.config_distributor = ConfigurationDistributor()
        self.global_control_plane = GlobalControlPlane(
            cluster_registry=self.cluster_registry,
            region_registry=self.region_registry,
        )
        self.routing_engine = RoutingEligibilityEngine(
            cluster_registry=self.cluster_registry,
            region_registry=self.region_registry,
            affinity_manager=self.affinity_manager,
        )
        self.topology_service = TopologyDiscoveryService(
            cluster_registry=self.cluster_registry,
            region_registry=self.region_registry,
        )
        self.diagnostics_service = ClusterDiagnosticsService(self.cluster_registry)

    # --- Cluster Operations ---

    def register_cluster(
        self,
        cluster_id: str,
        name: str,
        region_id: str,
        provider: str = "kubernetes",
        cluster_type: ClusterType = ClusterType.PRODUCTION,
        labels: Optional[Dict[str, str]] = None,
        capabilities: Optional[Set[str]] = None,
        capacity: Optional[CapacityModel] = None,
    ) -> Cluster:
        """Register a new cluster and link to its designated region."""
        cluster = Cluster(
            cluster_id=cluster_id,
            name=name,
            region_id=region_id,
            provider=provider,
            cluster_type=cluster_type,
            labels=labels or {},
            capabilities=capabilities or set(),
            capacity=capacity or CapacityModel(),
            status=ClusterStatus.REGISTERED,
        )
        return self.global_control_plane.register_cluster_globally(cluster)

    def get_cluster(self, cluster_id: str) -> Optional[Cluster]:
        return self.cluster_registry.get_cluster(cluster_id)

    def list_clusters(
        self,
        region_id: Optional[str] = None,
        status: Optional[ClusterStatus] = None,
        environment: Optional[str] = None,
    ) -> List[Cluster]:
        return self.cluster_registry.list_clusters(
            region_id=region_id, status=status, environment=environment
        )

    def transition_cluster_state(
        self, cluster_id: str, target_state: ClusterStatus, reason: Optional[str] = None
    ) -> Optional[Cluster]:
        return self.cluster_registry.transition_state(cluster_id, target_state, reason=reason)

    def heartbeat(
        self,
        cluster_id: str,
        sub_components: Optional[List[SubComponentHealth]] = None,
        ttl_seconds: int = 60,
    ) -> Optional[ClusterLease]:
        return self.cluster_registry.heartbeat(
            cluster_id=cluster_id, sub_components=sub_components, ttl_seconds=ttl_seconds
        )

    def get_cluster_diagnostics(self, cluster_id: str) -> Dict[str, Any]:
        report = self.diagnostics_service.generate_cluster_report(cluster_id)
        return report.model_dump(mode="json")

    # --- Region Operations ---

    def register_region(
        self,
        region_id: str,
        name: str,
        display_name: str,
        provider: str = "aws",
        data_residency_jurisdiction: str = "US",
        is_primary: bool = False,
        routing_priority: int = 100,
        geography: Optional[Geography] = None,
        failover_region_id: Optional[str] = None,
    ) -> Region:
        """Register a region in the platform topology."""
        region = Region(
            region_id=region_id,
            name=name,
            display_name=display_name,
            provider=provider,
            data_residency_jurisdiction=data_residency_jurisdiction,
            is_primary=is_primary,
            routing_priority=routing_priority,
            geography=geography or Geography(jurisdiction=data_residency_jurisdiction),
            failover_region_id=failover_region_id,
        )
        return self.region_registry.register_region(region)

    def get_region(self, region_id: str) -> Optional[Region]:
        return self.region_registry.get_region(region_id)

    def list_regions(
        self,
        status: Optional[RegionStatus] = None,
        jurisdiction: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> List[Region]:
        return self.region_registry.list_regions(
            status=status, jurisdiction=jurisdiction, provider=provider
        )

    def set_tenant_affinity(self, rule: TenantAffinityRule) -> TenantAffinityRule:
        return self.affinity_manager.set_tenant_affinity(rule)

    # --- Routing & Control Plane ---

    def evaluate_routing(self, request: WorkloadRoutingRequest) -> RoutingDecision:
        return self.routing_engine.evaluate_routing(request)

    def get_global_topology(self) -> Dict[str, Any]:
        graph = self.topology_service.discover_and_sync()
        nodes = [n.model_dump() for n in graph.list_nodes()]
        return {
            "nodes": nodes,
            "global_state": self.global_control_plane.get_state().model_dump(mode="json"),
        }
