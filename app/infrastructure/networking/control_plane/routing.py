"""Global Network Routing Engine synthesizing mesh rules, topologies, and latencies."""

from typing import Any, Dict, List, Optional
import random
import threading

from .registry import NetworkControlPlaneRegistry, RouteRule, RoutingStrategy, NetworkEndpoint


class GlobalNetworkRouter:
    """Evaluates routing rules, endpoint health, and multi-region network latency to route requests."""

    def __init__(self, registry: NetworkControlPlaneRegistry) -> None:
        self.registry = registry
        self._round_robin_counters: Dict[str, int] = {}
        self._lock = threading.Lock()

    def resolve_endpoint(
        self,
        service_name: str,
        preferred_region: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[NetworkEndpoint]:
        """Select best endpoint for a target service based on routing rules and strategy."""
        route = self.registry.get_route(service_name)
        if not route or not route.endpoints:
            return None

        # Filter to healthy endpoints
        healthy_endpoints = [ep for ep in route.endpoints if ep.healthy]
        if not healthy_endpoints:
            return None

        # Check for Canary routing
        if route.canary_endpoints and route.canary_weight > 0.0:
            if random.random() < route.canary_weight:
                canary_healthy = [ep for ep in route.canary_endpoints if ep.healthy]
                if canary_healthy:
                    return random.choice(canary_healthy)

        # Apply routing strategy
        strategy = route.strategy

        if strategy == RoutingStrategy.ROUND_ROBIN:
            with self._lock:
                idx = self._round_robin_counters.get(service_name, 0)
                selected = healthy_endpoints[idx % len(healthy_endpoints)]
                self._round_robin_counters[service_name] = idx + 1
                return selected

        elif strategy == RoutingStrategy.LEAST_CONNECTIONS:
            return min(healthy_endpoints, key=lambda ep: ep.active_connections)

        elif strategy == RoutingStrategy.LATENCY_BASED:
            return min(healthy_endpoints, key=lambda ep: ep.latency_ms)

        elif strategy == RoutingStrategy.GEO_AWARE and preferred_region:
            regional = [ep for ep in healthy_endpoints if ep.region == preferred_region]
            if regional:
                return regional[0]
            return healthy_endpoints[0]

        elif strategy == RoutingStrategy.WEIGHTED:
            weights = [max(1, ep.weight) for ep in healthy_endpoints]
            return random.choices(healthy_endpoints, weights=weights, k=1)[0]

        elif strategy == RoutingStrategy.FAILOVER:
            # First healthy endpoint acts as primary, others as standby
            return healthy_endpoints[0]

        # Default fallback
        return healthy_endpoints[0]

    def get_shadow_endpoints(self, service_name: str) -> List[NetworkEndpoint]:
        """Get shadow (traffic mirroring) endpoints for a service."""
        route = self.registry.get_route(service_name)
        if not route:
            return []
        return [ep for ep in route.shadow_endpoints if ep.healthy]
