"""Network Control Plane Manager for coordinating lifecycle and synchronization."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import logging
import threading

from .registry import NetworkControlPlaneRegistry, RouteRule, RoutingStrategy, NetworkEndpoint

logger = logging.getLogger("app.infrastructure.networking.control_plane")


class NetworkControlPlaneManager:
    """Coordinates service discovery, mesh synchronization, routing, and zero-trust policies."""

    def __init__(self, registry: Optional[NetworkControlPlaneRegistry] = None) -> None:
        self.registry = registry or NetworkControlPlaneRegistry()
        self._lock = threading.RLock()
        self._active = False
        self._sync_interval_seconds = 10.0
        self._clusters: Dict[str, Dict[str, Any]] = {}

    def start(self) -> None:
        """Start control plane reconciliation loops."""
        with self._lock:
            self._active = True
            logger.info("Network Control Plane Manager started.")

    def stop(self) -> None:
        """Stop control plane reconciler."""
        with self._lock:
            self._active = False
            logger.info("Network Control Plane Manager stopped.")

    @property
    def is_active(self) -> bool:
        """Check if control plane is active."""
        return self._active

    def register_cluster(self, cluster_id: str, region: str, mesh_type: str = "native", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register a participating cluster in the global network topology."""
        with self._lock:
            self._clusters[cluster_id] = {
                "cluster_id": cluster_id,
                "region": region,
                "mesh_type": mesh_type,
                "status": "connected",
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata or {},
            }

    def deregister_cluster(self, cluster_id: str) -> bool:
        """Deregister cluster from network topology."""
        with self._lock:
            if cluster_id in self._clusters:
                del self._clusters[cluster_id]
                return True
            return False

    def list_clusters(self) -> List[Dict[str, Any]]:
        """List registered clusters."""
        with self._lock:
            return list(self._clusters.values())

    def reconcile_routes(self, service_name: str, endpoints: List[NetworkEndpoint], strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN) -> RouteRule:
        """Reconcile and update routing configuration for a service."""
        with self._lock:
            existing = self.registry.get_route(service_name)
            if existing:
                existing.endpoints = endpoints
                existing.strategy = strategy
                self.registry.register_route(existing)
                return existing
            else:
                rule = RouteRule(
                    rule_id=f"rule-{service_name}",
                    service_name=service_name,
                    strategy=strategy,
                    endpoints=endpoints,
                )
                self.registry.register_route(rule)
                return rule

    def get_health_status(self) -> Dict[str, Any]:
        """Return control plane operational health status."""
        snapshot = self.registry.get_snapshot()
        return {
            "status": "healthy" if self._active else "idle",
            "active": self._active,
            "registered_clusters": len(self._clusters),
            "registry_snapshot": snapshot,
        }
