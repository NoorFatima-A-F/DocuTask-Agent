"""Service Discovery Registry and Dynamic Instance Tracking."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import threading
import uuid


class ServiceHealthState(str, Enum):
    """Service instance health state."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    DRAINING = "draining"
    TERMINATED = "terminated"


@dataclass
class ServiceEndpoint:
    """Network connection details for a service endpoint."""
    port: int
    protocol: str = "https"
    path_prefix: str = "/"
    name: str = "default"


@dataclass
class ServiceInstance:
    """A registered running instance of a service workload."""
    instance_id: str
    service_id: str
    service_name: str
    host: str
    port: int
    namespace: str = "default"
    cluster_id: str = "cluster-alpha"
    region: str = "us-east-1"
    environment: str = "production"
    version: str = "1.0.0"
    health_state: ServiceHealthState = ServiceHealthState.HEALTHY
    endpoints: List[ServiceEndpoint] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    tenant_scope: List[str] = field(default_factory=lambda: ["*"])
    security_profile: Dict[str, Any] = field(default_factory=lambda: {"mtls_required": True, "spiffe_id": ""})
    weight: int = 100
    active_connections: int = 0
    latency_ms: float = 5.0
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_heartbeat_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def address(self) -> str:
        """Formatted host:port."""
        return f"{self.host}:{self.port}"

    @property
    def url(self) -> str:
        """Default HTTPS endpoint URL."""
        return f"https://{self.host}:{self.port}"


@dataclass
class ServiceRegistration:
    """Request payload for registering a service instance."""
    service_name: str
    host: str
    port: int
    instance_id: Optional[str] = None
    namespace: str = "default"
    cluster_id: str = "cluster-alpha"
    region: str = "us-east-1"
    environment: str = "production"
    version: str = "1.0.0"
    labels: Dict[str, str] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    tenant_scope: List[str] = field(default_factory=lambda: ["*"])
    security_profile: Dict[str, Any] = field(default_factory=dict)
    ttl_seconds: int = 30


class ServiceDiscoveryRegistry:
    """Thread-safe dynamic service discovery catalog."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._instances: Dict[str, ServiceInstance] = {}  # instance_id -> ServiceInstance
        self._services: Dict[str, Set[str]] = {}  # service_name -> Set[instance_id]
        self._namespaces: Dict[str, Set[str]] = {}  # namespace -> Set[instance_id]
        self._regions: Dict[str, Set[str]] = {}  # region -> Set[instance_id]

    def register_instance(self, registration: ServiceRegistration) -> ServiceInstance:
        """Register a new service instance or update existing heartbeat."""
        instance_id = registration.instance_id or f"{registration.service_name}-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)

        with self._lock:
            instance = ServiceInstance(
                instance_id=instance_id,
                service_id=registration.service_name,
                service_name=registration.service_name,
                host=registration.host,
                port=registration.port,
                namespace=registration.namespace,
                cluster_id=registration.cluster_id,
                region=registration.region,
                environment=registration.environment,
                version=registration.version,
                health_state=ServiceHealthState.HEALTHY,
                labels=registration.labels,
                capabilities=registration.capabilities,
                tenant_scope=registration.tenant_scope,
                security_profile=registration.security_profile or {"mtls_required": True, "spiffe_id": f"spiffe://docutask.internal/ns/{registration.namespace}/sa/{registration.service_name}"},
                registered_at=now,
                last_heartbeat_at=now,
                ttl_seconds=registration.ttl_seconds,
            )
            self._instances[instance_id] = instance

            self._services.setdefault(instance.service_name, set()).add(instance_id)
            self._namespaces.setdefault(instance.namespace, set()).add(instance_id)
            self._regions.setdefault(instance.region, set()).add(instance_id)

            return instance

    def deregister_instance(self, instance_id: str) -> bool:
        """Deregister an instance by ID."""
        with self._lock:
            instance = self._instances.pop(instance_id, None)
            if not instance:
                return False

            if instance.service_name in self._services:
                self._services[instance.service_name].discard(instance_id)
            if instance.namespace in self._namespaces:
                self._namespaces[instance.namespace].discard(instance_id)
            if instance.region in self._regions:
                self._regions[instance.region].discard(instance_id)

            return True

    def get_instance(self, instance_id: str) -> Optional[ServiceInstance]:
        """Retrieve instance by ID."""
        with self._lock:
            return self._instances.get(instance_id)

    def get_instances_for_service(
        self,
        service_name: str,
        healthy_only: bool = True,
        namespace: Optional[str] = None,
        region: Optional[str] = None,
        tenant_id: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> List[ServiceInstance]:
        """Query instances matching criteria."""
        with self._lock:
            instance_ids = self._services.get(service_name, set())
            result = []

            for iid in instance_ids:
                inst = self._instances.get(iid)
                if not inst:
                    continue

                if healthy_only and inst.health_state != ServiceHealthState.HEALTHY:
                    continue
                if namespace and inst.namespace != namespace:
                    continue
                if region and inst.region != region:
                    continue
                if capability and capability not in inst.capabilities:
                    continue
                if tenant_id and "*" not in inst.tenant_scope and tenant_id not in inst.tenant_scope:
                    continue

                result.append(inst)

            return result

    def list_all_instances(self) -> List[ServiceInstance]:
        """Return list of all registered instances."""
        with self._lock:
            return list(self._instances.values())

    def list_all_services(self) -> List[str]:
        """Return list of all registered service names."""
        with self._lock:
            return list(self._services.keys())

    def update_instance_health(self, instance_id: str, state: ServiceHealthState) -> bool:
        """Update health state of an instance."""
        with self._lock:
            inst = self._instances.get(instance_id)
            if inst:
                inst.health_state = state
                return True
            return False

    def clear(self) -> None:
        """Reset service discovery catalog."""
        with self._lock:
            self._instances.clear()
            self._services.clear()
            self._namespaces.clear()
            self._regions.clear()
