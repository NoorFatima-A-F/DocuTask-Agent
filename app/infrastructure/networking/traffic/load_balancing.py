"""Traffic Load Balancing Engine implementing L4/L7 Algorithms."""

from typing import Any, Dict, List, Optional
import random
import threading

from ..control_plane.registry import NetworkEndpoint, RoutingStrategy


class LoadBalancerEngine:
    """Selects target endpoints using configurable load-balancing algorithms."""

    def __init__(self) -> None:
        self._round_robin_counters: Dict[str, int] = {}
        self._lock = threading.Lock()

    def select_endpoint(
        self,
        endpoints: List[NetworkEndpoint],
        strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN,
        service_key: str = "default",
        preferred_zone: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> Optional[NetworkEndpoint]:
        """Select an endpoint based on strategy and constraints."""
        healthy = [ep for ep in endpoints if ep.healthy]
        if not healthy:
            return None

        # Tenant affinity / Locality aware pre-filtering
        if tenant_id:
            tenant_matched = [
                ep for ep in healthy
                if "*" in ep.metadata.get("tenant_scope", ["*"]) or tenant_id in ep.metadata.get("tenant_scope", [])
            ]
            if tenant_matched:
                healthy = tenant_matched

        if preferred_zone:
            zone_matched = [ep for ep in healthy if ep.zone == preferred_zone]
            if zone_matched:
                healthy = zone_matched

        if strategy == RoutingStrategy.ROUND_ROBIN:
            with self._lock:
                idx = self._round_robin_counters.get(service_key, 0)
                ep = healthy[idx % len(healthy)]
                self._round_robin_counters[service_key] = idx + 1
                return ep

        elif strategy == RoutingStrategy.LEAST_CONNECTIONS:
            return min(healthy, key=lambda ep: ep.active_connections)

        elif strategy == RoutingStrategy.LATENCY_BASED:
            return min(healthy, key=lambda ep: ep.latency_ms)

        elif strategy == RoutingStrategy.WEIGHTED:
            weights = [max(1, ep.weight) for ep in healthy]
            return random.choices(healthy, weights=weights, k=1)[0]

        elif strategy == RoutingStrategy.GEO_AWARE:
            # Pick lowest latency endpoint
            return min(healthy, key=lambda ep: ep.latency_ms)

        return healthy[0]
