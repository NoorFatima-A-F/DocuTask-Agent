# Service Mesh Integration Guide

## 1. Unified Mesh Abstraction
DocuTask Agent abstracts service mesh implementations behind `IServiceMeshAdapter`.

Supported Mesh Implementations:
- **Istio**: Generates `VirtualService`, `DestinationRule`, and `PeerAuthentication`.
- **Linkerd**: Generates `ServiceProfile`, `TrafficSplit`, and `ServerAuthorization`.
- **Consul Connect**: Generates `ServiceRouter`, `ServiceSplitter`, and `ServiceIntentions`.

## 2. Generating Istio VirtualService & DestinationRules
```python
from app.infrastructure.networking.mesh import IstioMeshAdapter
from app.infrastructure.networking.control_plane import RouteRule, RoutingStrategy, NetworkEndpoint

adapter = IstioMeshAdapter()
route = RouteRule(
    rule_id="r1",
    service_name="document-classifier",
    strategy=RoutingStrategy.LEAST_CONNECTIONS,
    canary_weight=0.10,
    canary_endpoints=[NetworkEndpoint(host="10.0.1.20", port=443)],
)
manifests = adapter.generate_routing_rules(route, namespace="prod")
# Yields VirtualService and DestinationRule manifests
```
