"""Tests for ClusterSDK and Infrastructure REST API Endpoints."""

from app.infrastructure.sdk.clusters import ClusterSDK
from app.infrastructure.clusters.models import (
    CapacityModel,
    ClusterStatus,
    ClusterType,
)
from app.infrastructure.clusters.health import SubComponentHealth
from app.infrastructure.regions.models import RegionStatus
from app.infrastructure.regions.affinity import TenantAffinityRule
from app.infrastructure.routing.metadata import WorkloadRoutingRequest
from app.infrastructure.api.cluster_routes import (
    register_cluster,
    get_cluster,
    list_clusters,
    transition_cluster_state,
    cluster_heartbeat,
    get_cluster_diagnostics,
    RegisterClusterRequest,
    StateTransitionRequest,
    HeartbeatRequest,
)
from app.infrastructure.api.region_routes import (
    register_region,
    get_region,
    list_regions,
    update_region_status,
    set_tenant_affinity,
    evaluate_routing,
    get_topology,
    RegisterRegionRequest,
    UpdateRegionStatusRequest,
)


def test_cluster_sdk_end_to_end():
    sdk = ClusterSDK()

    # 1. Register region
    region = sdk.register_region(
        region_id="us-west-2",
        name="us-west-2",
        display_name="US West (Oregon)",
        provider="aws",
        data_residency_jurisdiction="US",
        is_primary=True,
    )
    assert region.region_id == "us-west-2"
    assert sdk.get_region("us-west-2") is not None

    # 2. Register cluster
    cluster = sdk.register_cluster(
        cluster_id="cls-us-west-2a",
        name="Production US West",
        region_id="us-west-2",
        cluster_type=ClusterType.PRODUCTION,
        capabilities={"gpu_a100", "nvme"},
        capacity=CapacityModel(allocatable_cpu_cores=128.0, utilized_cpu_cores=20.0),
    )
    assert cluster.cluster_id == "cls-us-west-2a"

    # 3. Transition state
    sdk.transition_cluster_state("cls-us-west-2a", ClusterStatus.VALIDATING)
    sdk.transition_cluster_state("cls-us-west-2a", ClusterStatus.READY)
    sdk.transition_cluster_state("cls-us-west-2a", ClusterStatus.ACTIVE)
    assert sdk.get_cluster("cls-us-west-2a").status == ClusterStatus.ACTIVE

    # 4. Heartbeat
    lease = sdk.heartbeat(
        "cls-us-west-2a",
        sub_components=[SubComponentHealth(component_name="node", is_healthy=True)],
        ttl_seconds=120,
    )
    assert lease is not None
    assert lease.is_valid is True

    # 5. Routing
    req = WorkloadRoutingRequest(
        tenant_id="tenant-123",
        workload_type="ocr",
        required_jurisdiction="US",
    )
    decision = sdk.evaluate_routing(req)
    assert decision.is_routable is True
    assert decision.selected_cluster_id == "cls-us-west-2a"

    # 6. Global Topology
    topology = sdk.get_global_topology()
    assert len(topology["nodes"]) >= 2  # region node + cluster node
    assert topology["global_state"]["active_regions_count"] == 1


def test_api_cluster_and_region_routes_direct():
    # 1. Register region via API function
    reg_resp = register_region(
        RegisterRegionRequest(
            region_id="eu-central-1",
            name="eu-central-1",
            display_name="Europe (Frankfurt)",
            provider="aws",
            data_residency_jurisdiction="EU",
        )
    )
    assert reg_resp["region_id"] == "eu-central-1"

    # 2. Register cluster via API function
    cls_resp = register_cluster(
        RegisterClusterRequest(
            cluster_id="cls-eu-central-1a",
            name="EU Production Frankfurt",
            region_id="eu-central-1",
            provider="kubernetes",
            cluster_type=ClusterType.PRODUCTION,
            labels={"zone": "a"},
            capabilities={"ocr_engine", "gpu_t4"},
        )
    )
    assert cls_resp["cluster_id"] == "cls-eu-central-1a"

    # 3. Get cluster
    get_cls = get_cluster("cls-eu-central-1a")
    assert get_cls["name"] == "EU Production Frankfurt"

    # 4. List clusters
    listed_cls = list_clusters(region_id="eu-central-1")
    assert len(listed_cls) >= 1

    # 5. Transition state via API function
    t_resp = transition_cluster_state(
        "cls-eu-central-1a",
        StateTransitionRequest(target_state=ClusterStatus.VALIDATING, reason="Pre-flight check"),
    )
    assert t_resp["status"] == ClusterStatus.VALIDATING.value

    # 6. Heartbeat via API function
    hb_resp = cluster_heartbeat(
        "cls-eu-central-1a",
        HeartbeatRequest(
            sub_components=[SubComponentHealth(component_name="node", is_healthy=True)],
            ttl_seconds=60,
        ),
    )
    assert hb_resp["is_valid"] is True

    # 7. Diagnostics via API function
    diag_resp = get_cluster_diagnostics("cls-eu-central-1a")
    assert diag_resp["cluster_id"] == "cls-eu-central-1a"

    # 8. Set affinity and evaluate routing
    set_tenant_affinity(
        TenantAffinityRule(
            tenant_id="tenant-eu-bank",
            allowed_region_ids=["eu-central-1"],
            exclusive=True,
        )
    )

    decision = evaluate_routing(
        WorkloadRoutingRequest(
            tenant_id="tenant-eu-bank",
            workload_type="ocr",
            required_jurisdiction="EU",
        )
    )
    assert isinstance(decision, dict)
    assert "is_routable" in decision

    # 9. Topology via API function
    top_resp = get_topology()
    assert "nodes" in top_resp
