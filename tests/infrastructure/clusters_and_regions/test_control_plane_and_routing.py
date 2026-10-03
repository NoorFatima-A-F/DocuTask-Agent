"""Tests for Hierarchical Control Plane, Topology, Configuration, and Routing Eligibility."""

from app.infrastructure.clusters.models import (
    CapacityModel,
    Cluster,
    ClusterStatus,
)
from app.infrastructure.clusters.registry import ClusterRegistry
from app.infrastructure.regions.models import Region
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.control_plane.global_cp.manager import GlobalControlPlane
from app.infrastructure.control_plane.regional.manager import RegionalControlPlane
from app.infrastructure.control_plane.topology.graph import NodeType, TopologyGraph
from app.infrastructure.control_plane.config.distributor import ConfigurationDistributor
from app.infrastructure.control_plane.config.versions import CompatibilityMatrix
from app.infrastructure.routing.metadata import WorkloadRoutingRequest
from app.infrastructure.routing.eligibility import RoutingEligibilityEngine


def test_control_plane_hierarchical_coordination():
    c_reg = ClusterRegistry()
    r_reg = RegionRegistry()

    r1 = Region(region_id="us-east-1", name="us-east-1", display_name="US East")
    r_reg.register_region(r1)

    global_cp = GlobalControlPlane(cluster_registry=c_reg, region_registry=r_reg)
    regional_cp = RegionalControlPlane(region_id="us-east-1", cluster_registry=c_reg)

    cluster = Cluster(
        cluster_id="cls-cp-1",
        name="CP Cluster 1",
        region_id="us-east-1",
        status=ClusterStatus.ACTIVE,
    )
    global_cp.register_cluster_globally(cluster)

    # State snapshot
    g_state = global_cp.get_state()
    assert g_state.total_clusters_count == 1
    assert g_state.active_regions_count == 1

    r_state = regional_cp.get_state()
    assert r_state.local_clusters_count == 1
    assert r_state.active_clusters_count == 1


def test_topology_graph_and_shortest_path():
    graph = TopologyGraph()
    graph.add_node("us-east-1", NodeType.REGION)
    graph.add_node("eu-west-1", NodeType.REGION)
    graph.add_node("ap-southeast-1", NodeType.REGION)

    graph.add_edge("us-east-1", "eu-west-1", latency_ms=70.0)
    graph.add_edge("eu-west-1", "ap-southeast-1", latency_ms=120.0)
    graph.add_edge("us-east-1", "ap-southeast-1", latency_ms=250.0)

    # Shortest path from US East to AP Southeast via EU West: 70 + 120 = 190ms < 250ms direct
    path, latency = graph.find_shortest_latency_path("us-east-1", "ap-southeast-1")
    assert path == ["us-east-1", "eu-west-1", "ap-southeast-1"]
    assert latency == 190.0


def test_configuration_distributor_and_compatibility():
    distributor = ConfigurationDistributor()
    bundle = distributor.create_bundle(version="v1.0.0", payload={"log_level": "INFO"})

    assert distributor.distribute_to_cluster(bundle.bundle_id, "cls-1") is True
    assert distributor.get_cluster_config("cls-1").version == "v1.0.0"

    # Rollback
    bundle_v2 = distributor.create_bundle(version="v2.0.0", payload={"log_level": "DEBUG"})
    distributor.distribute_to_cluster(bundle_v2.bundle_id, "cls-1")
    assert distributor.get_cluster_config("cls-1").version == "v2.0.0"

    distributor.rollback_cluster("cls-1", bundle.bundle_id)
    assert distributor.get_cluster_config("cls-1").version == "v1.0.0"

    # Version compatibility
    valid, errs = CompatibilityMatrix.validate_cluster_versions("1.30.0", "3.1.0", "3.1.0")
    assert valid is True

    invalid, errs = CompatibilityMatrix.validate_cluster_versions("1.20.0", "3.1.0", "3.1.0")
    assert invalid is False
    assert any("Kubernetes" in e for e in errs)


def test_routing_eligibility_engine():
    c_reg = ClusterRegistry()
    r_reg = RegionRegistry()

    r_us = Region(region_id="us-east-1", name="us-east-1", display_name="US East", data_residency_jurisdiction="US")
    r_eu = Region(region_id="eu-west-1", name="eu-west-1", display_name="EU West", data_residency_jurisdiction="EU")
    r_reg.register_region(r_us)
    r_reg.register_region(r_eu)

    c1 = Cluster(
        cluster_id="cls-us-ocr",
        name="US OCR Cluster",
        region_id="us-east-1",
        status=ClusterStatus.ACTIVE,
        capabilities={"gpu_t4", "nvme"},
        supported_workloads=["ocr", "agent"],
        capacity=CapacityModel(allocatable_cpu_cores=64.0, utilized_cpu_cores=10.0),
        labels={"tier": "high_throughput"},
    )
    c2 = Cluster(
        cluster_id="cls-eu-ocr",
        name="EU OCR Cluster",
        region_id="eu-west-1",
        status=ClusterStatus.ACTIVE,
        capabilities={"gpu_t4"},
        supported_workloads=["ocr"],
        capacity=CapacityModel(allocatable_cpu_cores=32.0, utilized_cpu_cores=2.0),
    )
    c_reg.register_cluster(c1)
    c_reg.register_cluster(c2)

    engine = RoutingEligibilityEngine(cluster_registry=c_reg, region_registry=r_reg)

    # US Request
    req_us = WorkloadRoutingRequest(
        tenant_id="tenant-1",
        workload_type="ocr",
        required_jurisdiction="US",
        required_capabilities={"gpu_t4"},
    )
    decision = engine.evaluate_routing(req_us)
    assert decision.is_routable is True
    assert decision.selected_cluster_id == "cls-us-ocr"
    assert decision.selected_region_id == "us-east-1"

    # Capability mismatch request
    req_unsupported = WorkloadRoutingRequest(
        tenant_id="tenant-1",
        workload_type="ocr",
        required_capabilities={"tpu_v4"},
    )
    decision_fail = engine.evaluate_routing(req_unsupported)
    assert decision_fail.is_routable is False
    assert len(decision_fail.rejection_reasons) > 0
