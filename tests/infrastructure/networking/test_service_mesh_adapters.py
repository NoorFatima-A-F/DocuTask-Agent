"""Tests for Service Mesh Adapters (Istio, Linkerd, Consul)."""

from app.infrastructure.networking.control_plane import RouteRule, RoutingStrategy, NetworkEndpoint
from app.infrastructure.networking.mesh import (
    IstioMeshAdapter,
    LinkerdMeshAdapter,
    ConsulMeshAdapter,
)


def test_istio_mesh_adapter_manifest_generation() -> None:
    adapter = IstioMeshAdapter()
    assert adapter.mesh_type == "istio"

    route = RouteRule(
        rule_id="r1",
        service_name="document-classifier",
        strategy=RoutingStrategy.LEAST_CONNECTIONS,
        canary_weight=0.25,
        canary_endpoints=[NetworkEndpoint(host="10.0.1.2", port=443)],
        shadow_endpoints=[NetworkEndpoint(host="10.0.1.3", port=443)],
    )

    manifests = adapter.generate_routing_rules(route, namespace="prod")
    assert len(manifests) == 2  # VirtualService and DestinationRule

    vs = next(m for m in manifests if m.resource_kind == "VirtualService")
    dr = next(m for m in manifests if m.resource_kind == "DestinationRule")

    assert vs.spec["hosts"] == ["document-classifier.prod.svc.cluster.local"]
    assert len(vs.spec["http"][0]["route"]) == 2
    assert vs.spec["http"][0]["mirror"]["host"] == "document-classifier-shadow.prod.svc.cluster.local"

    assert dr.spec["trafficPolicy"]["loadBalancer"]["simple"] == "LEAST_CONN"

    # Test mTLS policy
    mtls_manifests = adapter.generate_mtls_policy("document-classifier", namespace="prod")
    assert len(mtls_manifests) == 1
    assert mtls_manifests[0].resource_kind == "PeerAuthentication"
    assert mtls_manifests[0].spec["mtls"]["mode"] == "STRICT"


def test_linkerd_mesh_adapter() -> None:
    adapter = LinkerdMeshAdapter()
    assert adapter.mesh_type == "linkerd"

    route = RouteRule(rule_id="r2", service_name="pdf-extractor")
    manifests = adapter.generate_routing_rules(route, namespace="default")
    assert len(manifests) == 1
    assert manifests[0].resource_kind == "ServiceProfile"

    split_manifests = adapter.generate_traffic_split("pdf-extractor", primary_weight=900, canary_weight=100)
    assert len(split_manifests) == 1
    assert split_manifests[0].resource_kind == "TrafficSplit"


def test_consul_mesh_adapter() -> None:
    adapter = ConsulMeshAdapter()
    assert adapter.mesh_type == "consul"

    route = RouteRule(rule_id="r3", service_name="queue-router")
    manifests = adapter.generate_routing_rules(route, namespace="default")
    assert len(manifests) == 1
    assert manifests[0].resource_kind == "ServiceRouter"

    intentions = adapter.generate_mtls_policy("queue-router", namespace="default")
    assert len(intentions) == 1
    assert intentions[0].resource_kind == "ServiceIntentions"
