"""Service Resolver and DNS/Virtual Mesh Hostname Resolution."""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .registry import ServiceEndpoint, ServiceRegistry


@dataclass
class ResolvedTarget:
    service_name: str
    namespace: str
    endpoints: List[ServiceEndpoint] = field(default_factory=list)
    resolved_at: float = field(default_factory=time.time)
    ttl_seconds: float = 30.0

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.resolved_at) > self.ttl_seconds


class ServiceResolver:
    """Resolves virtual hostnames to active, locality-prioritized service endpoints."""

    def __init__(self, registry: Optional[ServiceRegistry] = None, cache_ttl_seconds: float = 30.0):
        self.registry = registry or ServiceRegistry()
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache: Dict[str, ResolvedTarget] = {}

    def parse_hostname(self, hostname: str) -> tuple[str, str]:
        """Parse service and namespace from various formats:
        - `service` -> (service, 'default')
        - `service.namespace` -> (service, namespace)
        - `service.namespace.mesh` -> (service, namespace)
        - `service.namespace.svc.cluster.local` -> (service, namespace)
        """
        clean = hostname.strip()
        if clean.endswith(".mesh"):
            clean = clean[:-5]
        elif clean.endswith(".svc.cluster.local"):
            clean = clean[:-18]

        parts = clean.split(".")
        if len(parts) >= 2:
            return parts[0], parts[1]
        return parts[0], "default"

    def resolve(
        self,
        target_name_or_host: str,
        caller_region: Optional[str] = None,
        caller_zone: Optional[str] = None,
        force_refresh: bool = False,
    ) -> ResolvedTarget:
        """Resolve a service target hostname to active healthy endpoints with locality sorting."""
        service_name, namespace = self.parse_hostname(target_name_or_host)
        cache_key = f"{namespace}/{service_name}"

        if not force_refresh and cache_key in self._cache:
            cached = self._cache[cache_key]
            if not cached.is_expired:
                return cached

        endpoints = self.registry.list_endpoints(
            service_name=service_name,
            namespace=namespace,
            healthy_only=True,
        )

        # Locality prioritization: same zone first, same region second, others third
        if caller_region or caller_zone:
            def locality_score(ep: ServiceEndpoint) -> int:
                if caller_zone and ep.zone == caller_zone:
                    return 0
                if caller_region and ep.region == caller_region:
                    return 1
                return 2

            endpoints.sort(key=locality_score)

        target = ResolvedTarget(
            service_name=service_name,
            namespace=namespace,
            endpoints=endpoints,
            resolved_at=time.time(),
            ttl_seconds=self.cache_ttl_seconds,
        )
        self._cache[cache_key] = target
        return target

    def clear_cache(self) -> None:
        self._cache.clear()
