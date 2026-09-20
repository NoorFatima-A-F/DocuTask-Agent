"""Linkerd Service Mesh Adapter for generating ServiceProfile and TrafficSplit."""

from typing import Any, Dict, List
from .adapters import IServiceMeshAdapter, MeshConfigurationManifest
from ..control_plane.registry import RouteRule


class LinkerdMeshAdapter(IServiceMeshAdapter):
    """Generates Linkerd ServiceProfile and TrafficSplit manifests."""

    @property
    def mesh_type(self) -> str:
        return "linkerd"

    def generate_routing_rules(self, route: RouteRule, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate Linkerd ServiceProfile."""
        manifests = []
        profile_spec = {
            "routes": [{
                "name": "default-route",
                "isRetryable": True,
                "timeout": f"{route.timeout_ms}ms",
            }],
            "retryBudget": {
                "retryRatio": 0.2,
                "minRetriesPerSecond": 10,
                "ttl": "10s",
            },
        }
        manifests.append(MeshConfigurationManifest(
            mesh_type="linkerd",
            resource_kind="ServiceProfile",
            name=f"{route.service_name}.{namespace}.svc.cluster.local",
            namespace=namespace,
            spec=profile_spec,
        ))
        return manifests

    def generate_mtls_policy(self, service_name: str, namespace: str = "default", mode: str = "STRICT") -> List[MeshConfigurationManifest]:
        """Generate Linkerd ServerAuthorization manifest."""
        spec = {
            "server": {"name": f"{service_name}-server"},
            "client": {
                "meshTLS": {
                    "identities": [f"*.{namespace}.serviceaccount.identity.linkerd.cluster.local"],
                }
            }
        }
        return [MeshConfigurationManifest(
            mesh_type="linkerd",
            resource_kind="ServerAuthorization",
            name=f"{service_name}-server-auth",
            namespace=namespace,
            spec=spec,
        )]

    def generate_traffic_split(self, service_name: str, primary_weight: int, canary_weight: int, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate Linkerd TrafficSplit resource."""
        spec = {
            "service": service_name,
            "backends": [
                {"service": f"{service_name}-primary", "weight": f"{primary_weight}m"},
                {"service": f"{service_name}-canary", "weight": f"{canary_weight}m"},
            ]
        }
        return [MeshConfigurationManifest(
            mesh_type="linkerd",
            resource_kind="TrafficSplit",
            name=f"{service_name}-traffic-split",
            namespace=namespace,
            spec=spec,
        )]

    def sync_mesh_state(self) -> Dict[str, Any]:
        """Return Linkerd synchronization status."""
        return {
            "mesh_type": "linkerd",
            "control_plane": "linkerd-destination.linkerd.svc",
            "status": "synchronized",
            "identity_healthy": True,
            "proxy_injector_healthy": True,
        }
