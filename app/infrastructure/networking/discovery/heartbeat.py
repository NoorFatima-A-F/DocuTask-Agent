"""Service Heartbeat & Liveness Management for Dynamic Discovery."""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
import logging
import threading

from .registry import ServiceDiscoveryRegistry, ServiceHealthState

logger = logging.getLogger("app.infrastructure.networking.heartbeat")


class ServiceHeartbeatManager:
    """Monitors service instance heartbeats, renews leases, and evicts stale instances."""

    def __init__(self, registry: ServiceDiscoveryRegistry) -> None:
        self.registry = registry
        self._lock = threading.RLock()

    def record_heartbeat(self, instance_id: str, active_connections: int = 0, latency_ms: float = 5.0) -> bool:
        """Process heartbeat ping from a service instance."""
        with self._lock:
            instance = self.registry.get_instance(instance_id)
            if not instance:
                return False

            instance.last_heartbeat_at = datetime.now(timezone.utc)
            instance.active_connections = active_connections
            instance.latency_ms = latency_ms
            if instance.health_state == ServiceHealthState.UNHEALTHY:
                instance.health_state = ServiceHealthState.HEALTHY
            return True

    def evict_stale_instances(self, grace_period_seconds: int = 10) -> List[str]:
        """Scan and deregister instances that exceeded their heartbeat TTL."""
        now = datetime.now(timezone.utc)
        evicted_ids: List[str] = []

        with self._lock:
            for instance in self.registry.list_all_instances():
                deadline = instance.last_heartbeat_at + timedelta(seconds=instance.ttl_seconds + grace_period_seconds)
                if now > deadline:
                    logger.warning(
                        "Evicting stale service instance: %s (service: %s, last heartbeat: %s)",
                        instance.instance_id,
                        instance.service_name,
                        instance.last_heartbeat_at.isoformat(),
                    )
                    self.registry.deregister_instance(instance.instance_id)
                    evicted_ids.append(instance.instance_id)

        return evicted_ids
