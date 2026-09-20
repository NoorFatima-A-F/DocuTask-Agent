"""Workload Request Specifications, Priority Classes, and Execution Contracts."""

from datetime import datetime, timezone
from enum import Enum
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class WorkloadType(str, Enum):
    WORKFLOW_TASK = "WORKFLOW_TASK"
    AGENT_TASK = "AGENT_TASK"
    CONNECTOR_TASK = "CONNECTOR_TASK"
    OCR_JOB = "OCR_JOB"
    EMBEDDING_JOB = "EMBEDDING_JOB"
    KNOWLEDGE_SYNC = "KNOWLEDGE_SYNC"
    EVALUATION_JOB = "EVALUATION_JOB"
    ANALYTICS_JOB = "ANALYTICS_JOB"
    MAINTENANCE_JOB = "MAINTENANCE_JOB"
    CUSTOM = "CUSTOM"


class WorkloadState(str, Enum):
    SUBMITTED = "SUBMITTED"
    VALIDATING = "VALIDATING"
    ELIGIBLE = "ELIGIBLE"
    WAITING = "WAITING"
    RESERVING = "RESERVING"
    ASSIGNED = "ASSIGNED"
    DISPATCHING = "DISPATCHING"
    RUNNING = "RUNNING"
    RETRY_PENDING = "RETRY_PENDING"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class WorkloadPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"
    BACKGROUND = "BACKGROUND"
    MAINTENANCE = "MAINTENANCE"


class ResourceRequirements(BaseModel):
    """Resource bounds required to schedule and execute the workload."""

    cpu_cores: float = 1.0
    memory_gb: float = 2.0
    gpu_count: int = 0
    gpu_type: Optional[str] = None
    disk_gb: float = 5.0
    worker_slots: int = 1


class WorkloadRequest(BaseModel):
    """Generic, declarative contract defining a workload submission."""

    workload_id: str = Field(default_factory=lambda: f"wkl_{secrets.token_hex(8)}")
    workload_type: WorkloadType = WorkloadType.CUSTOM
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    execution_id: Optional[str] = None
    task_id: Optional[str] = None
    priority: WorkloadPriority = WorkloadPriority.NORMAL
    state: WorkloadState = WorkloadState.SUBMITTED

    required_capabilities: Set[str] = Field(default_factory=set)
    optional_capabilities: Set[str] = Field(default_factory=set)
    resource_requirements: ResourceRequirements = Field(default_factory=ResourceRequirements)

    region_preferences: List[str] = Field(default_factory=list)
    region_constraints: List[str] = Field(default_factory=list)  # Hard allowed region IDs
    required_jurisdiction: Optional[str] = None                   # e.g., "US", "EU", "GLOBAL"
    cluster_constraints: List[str] = Field(default_factory=list)
    worker_constraints: List[str] = Field(default_factory=list)

    affinity_tags: Dict[str, str] = Field(default_factory=dict)
    anti_affinity_tags: Dict[str, str] = Field(default_factory=dict)

    data_locality_uri: Optional[str] = None  # e.g., s3://bucket-eu/doc.pdf
    idempotency_key: Optional[str] = None
    cost_budget_usd: Optional[float] = None
    deadline: Optional[datetime] = None
    timeout_seconds: int = 3600

    security_context: Dict[str, str] = Field(default_factory=dict)
    compliance_context: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
