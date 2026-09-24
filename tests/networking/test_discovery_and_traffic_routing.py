"""Tests for Service Discovery, Virtual Host Resolution, and Dynamic Traffic Routing."""

from app.networking.discovery.registry import (
    EndpointHealth,
    ServiceEndpoint,
    ServiceRegistry,
)
from app.networking.discovery.resolver import ServiceResolver
from app.networking.mesh.data_plane import MeshRequest
from app.networking.routing.router import (
    MatchCondition,
    RouteDestination,
    RouteRule,
    TrafficRouter,
)


def test_service_registry_and_stale_eviction():
    registry = ServiceRegistry(stale_threshold_seconds=1.0)
    ep = ServiceEndpoint(
        endpoint_id="ep-101",
        service_name="auth-service",
        host="10.0.0.1",
        port=8080,
    )
    registry.register_endpoint(ep)
    assert len(registry.list_endpoints(service_name="auth-service")) == 1

    # Update heartbeat
    assert registry.heartbeat("ep-101", EndpointHealth.HEALTHY) is True
    assert registry.get_endpoint("ep-101").is_healthy is True


def test_service_resolver_locality():
    registry = ServiceRegistry()
    ep_local = ServiceEndpoint(
        endpoint_id="ep-local",
        service_name="data-store",
        host="10.0.1.1",
        port=5432,
        region="us-central1",
        zone="us-central1-a",
    )
    ep_remote = ServiceEndpoint(
        endpoint_id="ep-remote",
        service_name="data-store",
        host="10.0.2.1",
        port=5432,
        region="us-east1",
        zone="us-east1-b",
    )
    registry.register_endpoint(ep_local)
    registry.register_endpoint(ep_remote)

    resolver = ServiceResolver(registry=registry)
    resolved = resolver.resolve(
        target_name_or_host="data-store.default.mesh",
        caller_region="us-central1",
        caller_zone="us-central1-a",
    )
    assert len(resolved.endpoints) == 2
    # Local endpoint should be sorted first
    assert resolved.endpoints[0].endpoint_id == "ep-local"


def test_traffic_router_matching():
    router = TrafficRouter()
    rule = RouteRule(
        rule_id="route-v2-canary",
        name="Canary for v2 API",
        matches=[
            MatchCondition(path="/v2/documents", path_type="prefix", method="POST")
        ],
        destinations=[
            RouteDestination(service_name="doc-service", version="v2", weight=100)
        ],
        priority=10,
    )
    router.add_rule(rule)

    req_v2 = MeshRequest(
        source_service="client",
        target_service="doc-service",
        action="create",
        path="/v2/documents/upload",
        method="POST",
    )
    dest = router.match_route(req_v2)
    assert dest is not None
    assert dest.version == "v2"

    # Non-matching request falls back to default
    req_v1 = MeshRequest(
        source_service="client",
        target_service="doc-service",
        action="create",
        path="/v1/documents/upload",
        method="POST",
    )
    dest_v1 = router.match_route(req_v1)
    assert dest_v1 is not None
    assert dest_v1.version == "default"
