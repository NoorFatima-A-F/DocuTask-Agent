"""Network Control Plane Core Models and Central Registry."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import threading
import uuid


class NetworkProtocol(str, Enum):
    """Supported network protocols."""
    HTTP = "http"
    HTTPS = "https"
    GRPC = "grpc"
    TCP = "tcp"
    UDP = "udp"
    WEBSOCKET = "websocket"


class MeshType(str, Enum):
    """Supported service mesh providers."""
    ISTIO = "istio"
    LINKERD = "linkerd"
    CONSUL = "consul"
    NATIVE = "native"
    STANDALONE = "standalone"


class RoutingStrategy(str, Enum):
    """Traffic routing algorithms and policies."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    LATENCY_BASED = "latency_based"
    GEO_AWARE = "geo_aware"
    CANARY = "canary"
    BLUE_GREEN = "blue_green"
    SHADOW = "shadow"
    FAILOVER = "failover"


class ZeroTrustAction(str, Enum):
    """Evaluation actions for zero-trust policies."""
    ALLOW = "allow"
    DENY = "deny"
    AUDIT = "audit"
    CHALLENGE = "challenge"


class CertificateStatus(str, Enum):
    """X.509 certificate lifecycle status."""
    ACTIVE = "active"
    ROTATING = "rotating"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class NetworkPolicyType(str, Enum):
    """Network policy directions."""
    INGRESS = "ingress"
    EGRESS = "egress"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class NetworkEndpoint:
    """Network endpoint target address and port."""
    host: str
    port: int
    protocol: NetworkProtocol = NetworkProtocol.HTTPS
    weight: int = 100
    healthy: bool = True
    active_connections: int = 0
    latency_ms: float = 10.0
    zone: str = "us-east-1a"
    region: str = "us-east-1"
    cluster_id: str = "cluster-alpha"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def address(self) -> str:
        """Formatted address string."""
        return f"{self.protocol.value}://{self.host}:{self.port}"


@dataclass
class RouteRule:
    """Traffic routing rule definition."""
    rule_id: str
    service_name: str
    strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN
    endpoints: List[NetworkEndpoint] = field(default_factory=list)
    canary_weight: float = 0.0  # Percentage between 0.0 and 1.0
    canary_endpoints: List[NetworkEndpoint] = field(default_factory=list)
    shadow_endpoints: List[NetworkEndpoint] = field(default_factory=list)
    headers_match: Dict[str, str] = field(default_factory=dict)
    timeout_ms: int = 5000
    retry_count: int = 3
    circuit_breaker_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class NetworkControlPlaneRegistry:
    """Thread-safe centralized registry for network control plane state."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._services: Dict[str, Any] = {}
        self._routes: Dict[str, RouteRule] = {}
        self._policies: Dict[str, Any] = {}
        self._certificates: Dict[str, Any] = {}
        self._mesh_configs: Dict[str, Any] = {}
        self._clusters: Dict[str, Dict[str, Any]] = {}
        self._updated_at: datetime = datetime.now(timezone.utc)

    def register_route(self, route: RouteRule) -> None:
        """Register or update a route rule."""
        with self._lock:
            self._routes[route.service_name] = route
            self._updated_at = datetime.now(timezone.utc)

    def get_route(self, service_name: str) -> Optional[RouteRule]:
        """Retrieve route rule by service name."""
        with self._lock:
            return self._routes.get(service_name)

    def list_routes(self) -> List[RouteRule]:
        """List all active route rules."""
        with self._lock:
            return list(self._routes.values())

    def delete_route(self, service_name: str) -> bool:
        """Delete route rule."""
        with self._lock:
            if service_name in self._routes:
                del self._routes[service_name]
                self._updated_at = datetime.now(timezone.utc)
                return True
            return False

    def get_snapshot(self) -> Dict[str, Any]:
        """Return a read-only snapshot of control plane registry state."""
        with self._lock:
            return {
                "route_count": len(self._routes),
                "service_count": len(self._services),
                "policy_count": len(self._policies),
                "certificate_count": len(self._certificates),
                "cluster_count": len(self._clusters),
                "updated_at": self._updated_at.isoformat(),
            }

    def clear(self) -> None:
        """Reset all registry state."""
        with self._lock:
            self._services.clear()
            self._routes.clear()
            self._policies.clear()
            self._certificates.clear()
            self._mesh_configs.clear()
            self._clusters.clear()
            self._updated_at = datetime.now(timezone.utc)
