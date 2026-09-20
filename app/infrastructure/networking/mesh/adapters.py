"""Service Mesh Integration Base Adapters and Abstract Interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..control_plane.registry import RouteRule, RoutingStrategy, NetworkEndpoint


@dataclass
class MeshConfigurationManifest:
    """A generated native mesh configuration manifest."""
    mesh_type: str
    resource_kind: str
    name: str
    namespace: str
    spec: Dict[str, Any]
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class IServiceMeshAdapter(ABC):
    """Vendor-neutral service mesh adapter interface."""

    @property
    @abstractmethod
    def mesh_type(self) -> str:
        """Return the mesh provider identifier (e.g. 'istio', 'linkerd', 'consul')."""
        pass

    @abstractmethod
    def generate_routing_rules(self, route: RouteRule, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Convert platform route rule to native mesh routing manifests."""
        pass

    @abstractmethod
    def generate_mtls_policy(self, service_name: str, namespace: str = "default", mode: str = "STRICT") -> List[MeshConfigurationManifest]:
        """Generate mesh mutual TLS security manifests."""
        pass

    @abstractmethod
    def generate_traffic_split(self, service_name: str, primary_weight: int, canary_weight: int, namespace: str = "default") -> List[MeshConfigurationManifest]:
        """Generate traffic splitting configuration for canary or blue/green deployments."""
        pass

    @abstractmethod
    def sync_mesh_state(self) -> Dict[str, Any]:
        """Synchronize and return current mesh health and active endpoints."""
        pass
