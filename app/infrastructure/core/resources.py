"""Resource Abstraction Layer for Compute, Storage, and Networking."""

from datetime import datetime, timezone
from enum import Enum
import secrets
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .exceptions import ResourceAllocationError
from .lifecycle import ResourceLifecycleStateMachine, ResourceState


class ResourceCategory(str, Enum):
    COMPUTE = "COMPUTE"
    STORAGE = "STORAGE"
    NETWORKING = "NETWORKING"


class ComputeType(str, Enum):
    CONTAINER = "CONTAINER"
    VM = "VM"
    SERVERLESS = "SERVERLESS"


class StorageType(str, Enum):
    DATABASE = "DATABASE"
    OBJECT_STORAGE = "OBJECT_STORAGE"
    CACHE = "CACHE"
    VOLUME = "VOLUME"


class NetworkType(str, Enum):
    LOAD_BALANCER = "LOAD_BALANCER"
    NETWORK = "NETWORK"
    ENDPOINT = "ENDPOINT"


class ResourceSpecification(BaseModel):
    """Declarative specification of a requested resource."""

    name: str
    category: ResourceCategory
    resource_type: str  # CONTAINER, DATABASE, etc.
    cpu_cores: Optional[float] = 1.0
    memory_mb: Optional[int] = 1024
    storage_gb: Optional[int] = 10
    region: str = "us-east-1"
    environment: str = "PRODUCTION"
    tags: Dict[str, str] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class AllocatedResource(BaseModel):
    """Representation of an active or provisioned resource."""

    resource_id: str
    name: str
    category: ResourceCategory
    resource_type: str
    state: ResourceState = ResourceState.REQUESTED
    spec: ResourceSpecification
    provider: str = "kubernetes"
    endpoint_url: Optional[str] = None
    allocated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResourceManager:
    """Manages resource allocation, lifecycle transitions, and de-provisioning."""

    def __init__(self) -> None:
        self._resources: Dict[str, AllocatedResource] = {}

    def request_resource(self, spec: ResourceSpecification, provider: str = "kubernetes") -> AllocatedResource:
        """Submit resource allocation request."""
        res_id = f"res_{secrets.token_hex(8)}"
        res = AllocatedResource(
            resource_id=res_id,
            name=spec.name,
            category=spec.category,
            resource_type=spec.resource_type,
            state=ResourceState.REQUESTED,
            spec=spec,
            provider=provider,
        )
        self._resources[res_id] = res
        return res

    def allocate_resource(self, resource_id: str, endpoint_url: Optional[str] = None) -> AllocatedResource:
        """Transition resource from REQUESTED to ALLOCATING to READY/ACTIVE."""
        res = self._resources.get(resource_id)
        if not res:
            raise ResourceAllocationError(f"Resource {resource_id} not found.")

        # Transition to ALLOCATING
        new_state = ResourceLifecycleStateMachine.transition(res.state, ResourceState.ALLOCATING)
        res.state = new_state

        # Transition to READY
        new_state = ResourceLifecycleStateMachine.transition(res.state, ResourceState.READY)
        res.state = new_state
        res.endpoint_url = endpoint_url or f"https://{res.name}.internal.mesh"

        # Transition to ACTIVE
        new_state = ResourceLifecycleStateMachine.transition(res.state, ResourceState.ACTIVE)
        res.state = new_state
        res.updated_at = datetime.now(timezone.utc)
        return res

    def drain_resource(self, resource_id: str) -> AllocatedResource:
        """Transition resource to DRAINING for graceful termination."""
        res = self._resources.get(resource_id)
        if not res:
            raise ResourceAllocationError(f"Resource {resource_id} not found.")

        new_state = ResourceLifecycleStateMachine.transition(res.state, ResourceState.DRAINING)
        res.state = new_state
        res.updated_at = datetime.now(timezone.utc)
        return res

    def release_resource(self, resource_id: str) -> AllocatedResource:
        """Release/Deallocate a resource."""
        res = self._resources.get(resource_id)
        if not res:
            raise ResourceAllocationError(f"Resource {resource_id} not found.")

        if res.state == ResourceState.ACTIVE:
            self.drain_resource(resource_id)

        new_state = ResourceLifecycleStateMachine.transition(res.state, ResourceState.RELEASED)
        res.state = new_state
        res.updated_at = datetime.now(timezone.utc)
        return res

    def get_resource(self, resource_id: str) -> Optional[AllocatedResource]:
        return self._resources.get(resource_id)

    def list_resources(
        self,
        category: Optional[ResourceCategory] = None,
        state: Optional[ResourceState] = None,
        environment: Optional[str] = None,
    ) -> List[AllocatedResource]:
        items = list(self._resources.values())
        if category:
            items = [r for r in items if r.category == category]
        if state:
            items = [r for r in items if r.state == state]
        if environment:
            items = [r for r in items if r.spec.environment == environment]
        return items
