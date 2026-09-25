"""Service Registry and Dependency Management Platform."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ServiceRegistration(BaseModel):
    """Metadata registered by an infrastructure service."""

    service_id: str
    name: str
    version: str = "1.0.0"
    owner: str = "runtime-team"
    dependencies: List[str] = Field(default_factory=list)
    health_endpoint: str = "/health"
    environment: str = "PRODUCTION"
    is_active: bool = True
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ServiceRegistry:
    """Catalog of registered platform microservices and dependencies."""

    def __init__(self) -> None:
        self._services: Dict[str, ServiceRegistration] = {}

    def register_service(
        self,
        name: str,
        version: str = "1.0.0",
        owner: str = "runtime-team",
        dependencies: Optional[List[str]] = None,
        health_endpoint: str = "/health",
        environment: str = "PRODUCTION",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ServiceRegistration:
        """Register a new service."""
        service_id = f"svc_{name}_{environment.lower()}"
        reg = ServiceRegistration(
            service_id=service_id,
            name=name,
            version=version,
            owner=owner,
            dependencies=dependencies or [],
            health_endpoint=health_endpoint,
            environment=environment,
            metadata=metadata or {},
        )
        self._services[service_id] = reg
        return reg

    def get_service(self, service_id: str) -> Optional[ServiceRegistration]:
        return self._services.get(service_id)

    def list_services(self, environment: Optional[str] = None) -> List[ServiceRegistration]:
        items = list(self._services.values())
        if environment:
            items = [s for s in items if s.environment == environment]
        return items

    def validate_dependencies(self, service_id: str) -> Tuple[bool, List[str]]:
        """Verify that all upstream dependencies are registered and active."""
        svc = self.get_service(service_id)
        if not svc:
            return False, [f"Service {service_id} not registered."]

        missing = []
        for dep_name in svc.dependencies:
            dep_id = f"svc_{dep_name}_{svc.environment.lower()}"
            if dep_id not in self._services or not self._services[dep_id].is_active:
                missing.append(dep_name)

        if missing:
            return False, [f"Missing or inactive dependency: {d}" for d in missing]
        return True, []
