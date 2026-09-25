"""Istio Service Mesh Adapter for generating VirtualService, DestinationRule, and PeerAuthentication."""

from typing import Any, Dict, List
from .adapters import IServiceMeshAdapter, MeshConfigurationManifest
from ..control_plane.registry import RouteRule, RoutingStrategy


class IstioMeshAdapter(IServiceMeshAdapter):
    """Generates and manages Istio CRDs and Envoy configurations."""

    @property
    def mesh_type(self) -> str:
        return "istio"

    def generate_routing_rules(self, route: RouteRule, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate Istio VirtualService and DestinationRule."""
        manifests = []

        # 1. VirtualService
        routes = []
        if route.canary_endpoints and route.canary_weight > 0.0:
            routes.append({
                "destination": {"host": f"{route.service_name}.{namespace}.svc.cluster.local", "subset": "primary"},
                "weight": int((1.0 - route.canary_weight) * 100),
            })
            routes.append({
                "destination": {"host": f"{route.service_name}.{namespace}.svc.cluster.local", "subset": "canary"},
                "weight": int(route.canary_weight * 100),
            })
        else:
            routes.append({
                "destination": {"host": f"{route.service_name}.{namespace}.svc.cluster.local", "subset": "primary"},
                "weight": 100,
            })

        vs_spec = {
            "hosts": [f"{route.service_name}.{namespace}.svc.cluster.local"],
            "http": [{
                "route": routes,
                "timeout": f"{route.timeout_ms / 1000.0}s",
                "retries": {
                    "attempts": route.retry_count,
                    "perTryTimeout": "1s",
                    "retryOn": "5xx,connect-failure,refused-stream",
                },
            }],
        }
        if route.shadow_endpoints:
            vs_spec["http"][0]["mirror"] = {
                "host": f"{route.service_name}-shadow.{namespace}.svc.cluster.local"
            }

        manifests.append(MeshConfigurationManifest(
            mesh_type="istio",
            resource_kind="VirtualService",
            name=f"{route.service_name}-vs",
            namespace=namespace,
            spec=vs_spec,
        ))

        # 2. DestinationRule
        lb_policy = "ROUND_ROBIN"
        if route.strategy == RoutingStrategy.LEAST_CONNECTIONS:
            lb_policy = "LEAST_CONN"
        elif route.strategy == RoutingStrategy.LATENCY_BASED:
            lb_policy = "LEAST_REQUEST"

        dr_spec = {
            "host": f"{route.service_name}.{namespace}.svc.cluster.local",
            "trafficPolicy": {
                "loadBalancer": {"simple": lb_policy},
                "tls": {"mode": "ISTIO_MUTUAL"},
                "connectionPool": {
                    "tcp": {"maxConnections": 1024},
                    "http": {"http1MaxPendingRequests": 100, "maxRequestsPerConnection": 10},
                },
            },
            "subsets": [
                {"name": "primary", "labels": {"version": "primary"}},
                {"name": "canary", "labels": {"version": "canary"}},
            ],
        }
        manifests.append(MeshConfigurationManifest(
            mesh_type="istio",
            resource_kind="DestinationRule",
            name=f"{route.service_name}-dr",
            namespace=namespace,
            spec=dr_spec,
        ))

        return manifests

    def generate_mtls_policy(self, service_name: str, namespace: str = "default", mode: str = "STRICT") -> List[MeshConfigurationManifest]:
        """Generate Istio PeerAuthentication resource."""
        spec = {
            "selector": {"matchLabels": {"app": service_name}},
            "mtls": {"mode": mode},
        }
        return [MeshConfigurationManifest(
            mesh_type="istio",
            resource_kind="PeerAuthentication",
            name=f"{service_name}-peer-auth",
            namespace=namespace,
            spec=spec,
        )]

    def generate_traffic_split(self, service_name: str, primary_weight: int, canary_weight: int, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate VirtualService traffic split."""
        vs_spec = {
            "hosts": [f"{service_name}.{namespace}.svc.cluster.local"],
            "http": [{
                "route": [
                    {"destination": {"host": f"{service_name}.{namespace}.svc.cluster.local", "subset": "primary"}, "weight": primary_weight},
                    {"destination": {"host": f"{service_name}.{namespace}.svc.cluster.local", "subset": "canary"}, "weight": canary_weight},
                ]
            }],
        }
        return [MeshConfigurationManifest(
            mesh_type="istio",
            resource_kind="VirtualService",
            name=f"{service_name}-traffic-split",
            namespace=namespace,
            spec=vs_spec,
        )]

    def sync_mesh_state(self) -> Dict[str, Any]:
        """Return Istio synchronization status."""
        return {
            "mesh_type": "istio",
            "control_plane": "istiod.istio-system.svc",
            "status": "synchronized",
            "pilot_healthy": True,
            "citadel_healthy": True,
        }
