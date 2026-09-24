"""Service Resolver for name resolution, multi-region failover, and alias lookup."""

from dataclasses import dataclass
from typing import Any, Dict, Optional
import time
import threading

from .registry import ServiceDiscoveryRegistry, ServiceInstance


@dataclass
class ResolvedServiceTarget:
    """Resolved service target address and metadata."""
    service_name: str
    host: str
    port: int
    url: str
    instance_id: str
    region: str
    cluster_id: str
    spiffe_id: str
    resolved_via: str = "direct"  # direct, alias, multi-region-failover
    ttl_seconds: int = 5


class ServiceResolver:
    """Provides dynamic DNS-style resolution, multi-region failover resolving, and alias mapping."""

    def __init__(self, registry: ServiceDiscoveryRegistry) -> None:
        self.registry = registry
        self._aliases: Dict[str, str] = {}  # alias -> canonical service_name
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl_seconds = 5.0
        self._lock = threading.RLock()

    def register_alias(self, alias: str, canonical_service_name: str) -> None:
        """Register a service alias (e.g. 'ai-ocr' -> 'document-processing-worker')."""
        with self._lock:
            self._aliases[alias] = canonical_service_name

    def resolve(
        self,
        service_or_alias: str,
        caller_region: Optional[str] = None,
        tenant_id: Optional[str] = None,
        capability: Optional[str] = None,
        use_cache: bool = True,
    ) -> Optional[ResolvedServiceTarget]:
        """Resolve a service name or alias to a healthy endpoint."""
        # Check alias
        canonical_name = self._aliases.get(service_or_alias, service_or_alias)
        cache_key = f"{canonical_name}:{caller_region}:{tenant_id}:{capability}"

        now = time.time()
        if use_cache:
            with self._lock:
                entry = self._cache.get(cache_key)
                if entry and entry["expires_at"] > now:
                    return entry["target"]

        # Step 1: Query matching regional instances
        instances = self.registry.get_instances_for_service(
            service_name=canonical_name,
            healthy_only=True,
            region=caller_region,
            tenant_id=tenant_id,
            capability=capability,
        )
        resolved_via = "direct"

        # Step 2: Multi-region failover if local region has no healthy instances
        if not instances and caller_region:
            instances = self.registry.get_instances_for_service(
                service_name=canonical_name,
                healthy_only=True,
                region=None,  # any region
                tenant_id=tenant_id,
                capability=capability,
            )
            resolved_via = "multi-region-failover"

        if not instances:
            return None

        # Pick least-connections / lowest latency instance
        selected: ServiceInstance = min(instances, key=lambda i: (i.active_connections, i.latency_ms))

        spiffe = selected.security_profile.get("spiffe_id", f"spiffe://docutask.internal/ns/{selected.namespace}/sa/{selected.service_name}")
        target = ResolvedServiceTarget(
            service_name=canonical_name,
            host=selected.host,
            port=selected.port,
            url=selected.url,
            instance_id=selected.instance_id,
            region=selected.region,
            cluster_id=selected.cluster_id,
            spiffe_id=spiffe,
            resolved_via=resolved_via,
            ttl_seconds=int(self._cache_ttl_seconds),
        )

        # Cache result
        with self._lock:
            self._cache[cache_key] = {
                "target": target,
                "expires_at": now + self._cache_ttl_seconds,
            }

        return target

    def invalidate_cache(self, service_name: Optional[str] = None) -> None:
        """Clear resolver cache."""
        with self._lock:
            if service_name:
                self._cache = {k: v for k, v in self._cache.items() if not k.startswith(f"{service_name}:")}
            else:
                self._cache.clear()
