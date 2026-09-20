"""Service Discovery Registry and Endpoint Catalog."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EndpointHealth(str, Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    DRAINING = "DRAINING"


@dataclass
class ServiceEndpoint:
    endpoint_id: str
    service_name: str
    host: str
    port: int
    namespace: str = "default"
    region: str = "us-central1"
    zone: str = "us-central1-a"
    protocol: str = "HTTP_2"
    weight: int = 100
    health: EndpointHealth = EndpointHealth.HEALTHY
    tags: Dict[str, str] = field(default_factory=dict)
    last_seen: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_healthy(self) -> bool:
        return self.health == EndpointHealth.HEALTHY


class ServiceRegistry:
    """Multi-region service discovery registry."""

    def __init__(self, stale_threshold_seconds: float = 60.0):
        self.stale_threshold_seconds = stale_threshold_seconds
        self._endpoints: Dict[str, ServiceEndpoint] = {}

    def register_endpoint(self, endpoint: ServiceEndpoint) -> ServiceEndpoint:
        endpoint.last_seen = time.time()
        self._endpoints[endpoint.endpoint_id] = endpoint
        return endpoint

    def deregister_endpoint(self, endpoint_id: str) -> bool:
        if endpoint_id in self._endpoints:
            del self._endpoints[endpoint_id]
            return True
        return False

    def get_endpoint(self, endpoint_id: str) -> Optional[ServiceEndpoint]:
        return self._endpoints.get(endpoint_id)

    def heartbeat(self, endpoint_id: str, health: EndpointHealth = EndpointHealth.HEALTHY) -> bool:
        ep = self._endpoints.get(endpoint_id)
        if ep:
            ep.last_seen = time.time()
            ep.health = health
            return True
        return False

    def list_endpoints(
        self,
        service_name: Optional[str] = None,
        namespace: Optional[str] = None,
        healthy_only: bool = True,
        region: Optional[str] = None,
    ) -> List[ServiceEndpoint]:
        """List endpoints matching criteria, excluding stale ones if healthy_only."""
        now = time.time()
        results: List[ServiceEndpoint] = []
        for ep in self._endpoints.values():
            if service_name and ep.service_name != service_name:
                continue
            if namespace and ep.namespace != namespace:
                continue
            if region and ep.region != region:
                continue
            if healthy_only:
                if not ep.is_healthy:
                    continue
                if (now - ep.last_seen) > self.stale_threshold_seconds:
                    continue
            results.append(ep)
        return results

    def prune_stale_endpoints(self) -> int:
        now = time.time()
        stale_ids = [
            ep_id for ep_id, ep in self._endpoints.items()
            if (now - ep.last_seen) > self.stale_threshold_seconds
        ]
        for s_id in stale_ids:
            del self._endpoints[s_id]
        return len(stale_ids)
