"""
Platform Service Registry.
Tracks service instances, operational status, dependencies, module owners, and endpoints.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from ..kernel.versioning import SemanticVersion


class ServiceStatus(str, Enum):
    STARTING = "STARTING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    STOPPED = "STOPPED"


@dataclass
class ServiceRecord:
    """Registered platform service record."""
    name: str
    version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    module_owner: str = "core"
    status: ServiceStatus = ServiceStatus.HEALTHY
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": str(self.version),
            "module_owner": self.module_owner,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "capabilities": self.capabilities,
            "endpoints": self.endpoints,
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat(),
        }


class ServiceRegistry:
    """Central registry of platform services."""

    def __init__(self):
        self._services: Dict[str, ServiceRecord] = {}

    def register_service(
        self,
        name: str,
        version: Optional[SemanticVersion] = None,
        module_owner: str = "core",
        dependencies: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        endpoints: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ServiceRecord:
        """Register a new service."""
        record = ServiceRecord(
            name=name,
            version=version or SemanticVersion(1, 0, 0),
            module_owner=module_owner,
            dependencies=dependencies or [],
            capabilities=capabilities or [],
            endpoints=endpoints or [],
            metadata=metadata or {},
        )
        self._services[name] = record
        return record

    def update_status(self, name: str, status: ServiceStatus) -> None:
        """Update operational status of a service."""
        if name in self._services:
            self._services[name].status = status

    def get_service(self, name: str) -> Optional[ServiceRecord]:
        """Get service record by name."""
        return self._services.get(name)

    def list_services(self, module_owner: Optional[str] = None) -> List[ServiceRecord]:
        """List all services, optionally filtered by module owner."""
        if module_owner is None:
            return list(self._services.values())
        return [s for s in self._services.values() if s.module_owner == module_owner]

    def unregister_service(self, name: str) -> None:
        """Unregister a service."""
        self._services.pop(name, None)
