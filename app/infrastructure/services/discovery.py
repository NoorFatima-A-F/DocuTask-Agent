"""Service Discovery and Dynamic Endpoint Resolution."""

from typing import Dict, List, Optional
from .registry import ServiceRegistry


class ServiceDiscovery:
    """Resolves DNS, Mesh, and HTTP endpoints for registered services."""

    def __init__(self, registry: Optional[ServiceRegistry] = None) -> None:
        self.registry = registry or ServiceRegistry()
        self._endpoints: Dict[str, List[str]] = {}

    def register_endpoint(self, service_name: str, environment: str, endpoint_url: str) -> None:
        key = f"{service_name}:{environment}"
        if key not in self._endpoints:
            self._endpoints[key] = []
        if endpoint_url not in self._endpoints[key]:
            self._endpoints[key].append(endpoint_url)

    def resolve_endpoint(self, service_name: str, environment: str = "PRODUCTION") -> Optional[str]:
        """Resolve primary endpoint for a service."""
        key = f"{service_name}:{environment}"
        endpoints = self._endpoints.get(key, [])
        if endpoints:
            return endpoints[0]

        # Default mesh DNS pattern
        return f"http://{service_name}.{environment.lower()}.svc.cluster.local:8000"

    def list_endpoints(self, service_name: str, environment: str = "PRODUCTION") -> List[str]:
        key = f"{service_name}:{environment}"
        return list(self._endpoints.get(key, [f"http://{service_name}.{environment.lower()}.svc.cluster.local:8000"]))
