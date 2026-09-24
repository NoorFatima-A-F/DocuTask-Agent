"""Advanced Traffic Routing Engine supporting Canary, Blue/Green, and Shadow Mirroring."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import random
import threading

from ..control_plane.registry import NetworkEndpoint, RouteRule


@dataclass
class RoutingDecision:
    """Detailed record of a traffic routing decision."""
    target_endpoint: NetworkEndpoint
    is_canary: bool = False
    is_blue_green: bool = False
    shadow_endpoints: List[NetworkEndpoint] = field(default_factory=list)
    reason: str = "standard_route"
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class TrafficRouter:
    """Manages canary percentages, blue/green version switching, and traffic shadowing."""

    def __init__(self) -> None:
        self._blue_green_active_version: Dict[str, str] = {}  # service_name -> active_version ("blue" or "green")
        self._lock = threading.RLock()

    def set_blue_green_version(self, service_name: str, active_version: str) -> None:
        """Switch active version between 'blue' and 'green'."""
        with self._lock:
            self._blue_green_active_version[service_name] = active_version.lower()

    def get_blue_green_version(self, service_name: str) -> str:
        """Get currently active blue/green version."""
        with self._lock:
            return self._blue_green_active_version.get(service_name, "blue")

    def route_request(
        self,
        route: RouteRule,
        headers: Optional[Dict[str, str]] = None,
        tenant_id: Optional[str] = None,
    ) -> Optional[RoutingDecision]:
        """Compute routing destination applying headers, canary split, blue/green, and shadow."""
        headers = headers or {}

        # 1. Header-based routing override
        if route.headers_match:
            for k, v in route.headers_match.items():
                if headers.get(k) == v and route.canary_endpoints:
                    canary_healthy = [ep for ep in route.canary_endpoints if ep.healthy]
                    if canary_healthy:
                        return RoutingDecision(
                            target_endpoint=random.choice(canary_healthy),
                            is_canary=True,
                            reason="header_match_canary",
                            headers=headers,
                        )

        # 2. Canary traffic splitting
        if route.canary_endpoints and route.canary_weight > 0.0:
            if random.random() < route.canary_weight:
                canary_healthy = [ep for ep in route.canary_endpoints if ep.healthy]
                if canary_healthy:
                    shadow = [ep for ep in route.shadow_endpoints if ep.healthy]
                    return RoutingDecision(
                        target_endpoint=random.choice(canary_healthy),
                        is_canary=True,
                        shadow_endpoints=shadow,
                        reason="canary_weighted_split",
                        headers=headers,
                    )

        # 3. Standard / Primary endpoints
        healthy_primary = [ep for ep in route.endpoints if ep.healthy]
        if not healthy_primary:
            return None

        # Check blue/green tag if present
        active_bg = self.get_blue_green_version(route.service_name)
        bg_endpoints = [ep for ep in healthy_primary if ep.metadata.get("version") == active_bg]
        if bg_endpoints:
            target = random.choice(bg_endpoints)
            is_bg = True
        else:
            target = random.choice(healthy_primary)
            is_bg = False

        shadow = [ep for ep in route.shadow_endpoints if ep.healthy]
        return RoutingDecision(
            target_endpoint=target,
            is_blue_green=is_bg,
            shadow_endpoints=shadow,
            reason="primary_routing",
            headers=headers,
        )
