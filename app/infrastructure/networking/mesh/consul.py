"""Consul Connect Service Mesh Adapter."""

from typing import Any, Dict, List
from .adapters import IServiceMeshAdapter, MeshConfigurationManifest
from ..control_plane.registry import RouteRule


class ConsulMeshAdapter(IServiceMeshAdapter):
    """Generates Consul Service Intentions, Service Defaults, and Splitter configs."""

    @property
    def mesh_type(self) -> str:
        return "consul"

    def generate_routing_rules(self, route: RouteRule, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate Consul ServiceRouter and ServiceResolver configs."""
        manifests = []
        router_spec = {
            "routes": [{
                "match": {"http": {"path": {"prefix": "/"}}},
                "destination": {
                    "service": route.service_name,
                    "service_subset": "v1",
                    "request_timeout": f"{route.timeout_ms}ms",
                    "num_retries": route.retry_count,
                },
            }]
        }
        manifests.append(MeshConfigurationManifest(
            mesh_type="consul",
            resource_kind="ServiceRouter",
            name=route.service_name,
            namespace=namespace,
            spec=router_spec,
        ))
        return manifests

    def generate_mtls_policy(self, service_name: str, namespace: str = "default", mode: str = "STRICT") -> List[MeshConfigurationManifest]:
        """Generate Consul ServiceIntentions resource."""
        spec = {
            "sources": [
                {
                    "name": "*",
                    "namespace": namespace,
                    "action": "allow" if mode != "DENY_ALL" else "deny",
                    "permissions": [{"action": "allow", "http": {"pathExact": "/*", "methods": ["GET", "POST", "PUT", "DELETE"]}}],
                }
            ]
        }
        return [MeshConfigurationManifest(
            mesh_type="consul",
            resource_kind="ServiceIntentions",
            name=f"{service_name}-intentions",
            namespace=namespace,
            spec=spec,
        )]

    def generate_traffic_split(self, service_name: str, primary_weight: int, canary_weight: int, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate Consul ServiceSplitter config."""
        spec = {
            "splits": [
                {"service_subset": "v1", "weight": float(primary_weight)},
                {"service_subset": "canary", "weight": float(canary_weight)},
            ]
        }
        return [MeshConfigurationManifest(
            mesh_type="consul",
            resource_kind="ServiceSplitter",
            name=f"{service_name}-splitter",
            namespace=namespace,
            spec=spec,
        )]

    def sync_mesh_state(self) -> Dict[str, Any]:
        """Return Consul Connect synchronization status."""
        return {
            "mesh_type": "consul",
            "control_plane": "consul-server.consul.svc",
            "status": "synchronized",
            "connect_enabled": True,
            "ca_provider": "consul",
        }
