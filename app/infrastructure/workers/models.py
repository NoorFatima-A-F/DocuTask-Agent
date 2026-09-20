"""Worker Domain Models, Types, Status Enums, and Resource Capacities."""

from datetime import datetime, timezone
from enum import Enum
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class WorkerType(str, Enum):
    WORKFLOW = "WORKFLOW"
    AGENT = "AGENT"
    CONNECTOR = "CONNECTOR"
    KNOWLEDGE = "KNOWLEDGE"
    EMBEDDING = "EMBEDDING"
    OCR = "OCR"
    EVALUATION = "EVALUATION"
    ANALYTICS = "ANALYTICS"
    NOTIFICATION = "NOTIFICATION"
    MAINTENANCE = "MAINTENANCE"
    CUSTOM = "CUSTOM"


class WorkerStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    REGISTERING = "REGISTERING"
    REGISTERED = "REGISTERED"
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    DRAINING = "DRAINING"
    UNAVAILABLE = "UNAVAILABLE"
    RECOVERING = "RECOVERING"
    TERMINATED = "TERMINATED"


class ResourceCapacity(BaseModel):
    """Normalized hardware and slot capacity metrics for a worker."""

    cpu_cores: float = 4.0
    memory_gb: float = 16.0
    gpu_count: int = 0
    gpu_type: Optional[str] = None  # e.g., "nvidia-t4", "nvidia-a100", "nvidia-v100"
    disk_gb: float = 100.0
    network_mbps: float = 1000.0
    worker_slots: int = 10


class WorkerLease(BaseModel):
    """Heartbeat lease representing active worker connectivity and claim validity."""

    lease_id: str = Field(default_factory=lambda: f"wkl_{secrets.token_hex(8)}")
    worker_id: str
    cluster_id: str
    runtime_version: str = "3.1.0"
    ttl_seconds: int = 60
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_renewed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    is_valid: bool = True


class Worker(BaseModel):
    """Complete first-class governed Worker entity."""

    worker_id: str
    worker_type: WorkerType = WorkerType.CUSTOM
    service_name: str = "docutask-worker"
    version: str = "3.1.0"
    region_id: str = "us-east-1"
    cluster_id: str = "cls-default"
    namespace: str = "docutask-runtime"
    status: WorkerStatus = WorkerStatus.DISCOVERED
    capabilities: Set[str] = Field(default_factory=set)
    labels: Dict[str, str] = Field(default_factory=dict)
    resource_capacity: ResourceCapacity = Field(default_factory=ResourceCapacity)
    resource_allocated: ResourceCapacity = Field(
        default_factory=lambda: ResourceCapacity(cpu_cores=0.0, memory_gb=0.0, gpu_count=0, disk_gb=0.0, worker_slots=0)
    )
    concurrency_limit: int = 10
    active_assignments: List[str] = Field(default_factory=list)
    tenant_restrictions: List[str] = Field(default_factory=list)  # Empty means all allowed
    supported_workloads: List[str] = Field(default_factory=lambda: ["workflow", "agent", "ocr"])
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    health_status: str = "HEALTHY"
    active_lease: Optional[WorkerLease] = None
    drain_reason: Optional[str] = None
    quarantine_reason: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)

    @property
    def resource_available(self) -> ResourceCapacity:
        """Calculate unallocated available capacity."""
        return ResourceCapacity(
            cpu_cores=max(0.0, self.resource_capacity.cpu_cores - self.resource_allocated.cpu_cores),
            memory_gb=max(0.0, self.resource_capacity.memory_gb - self.resource_allocated.memory_gb),
            gpu_count=max(0, self.resource_capacity.gpu_count - self.resource_allocated.gpu_count),
            gpu_type=self.resource_capacity.gpu_type,
            disk_gb=max(0.0, self.resource_capacity.disk_gb - self.resource_allocated.disk_gb),
            network_mbps=self.resource_capacity.network_mbps,
            worker_slots=max(0, self.resource_capacity.worker_slots - self.resource_allocated.worker_slots),
        )
