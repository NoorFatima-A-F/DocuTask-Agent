"""
Phase 13.18: Distributed Platform Schemas & Data Models
Autonomous Cloud Runtime & Distributed Agent Fabric (ACR-DAF).
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class WorkerStatus(str, Enum):
    ONLINE = "ONLINE"
    BUSY = "BUSY"
    DRAINING = "DRAINING"
    OFFLINE = "OFFLINE"
    CRASHED = "CRASHED"


class JobPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    BATCH = "BATCH"


class JobState(str, Enum):
    QUEUED = "QUEUED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    CHECKPOINTED = "CHECKPOINTED"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MIGRATED = "MIGRATED"


class RegionName(str, Enum):
    US_EAST = "us-east-1"
    US_WEST = "us-west-2"
    EU_CENTRAL = "eu-central-1"
    ASIA_EAST = "asia-east-1"
    PK_SOUTH = "pk-south-1"


class ScalingAction(str, Enum):
    SCALE_UP = "SCALE_UP"
    SCALE_DOWN = "SCALE_DOWN"
    STABLE = "STABLE"


# ---------------------------------------------------------
# Worker Fleet & Node Metadata
# ---------------------------------------------------------

class WorkerCapacity(BaseModel):
    max_concurrent_jobs: int = 8
    allocated_jobs: int = 0
    cpu_cores: int = 4
    memory_mb: int = 8192
    cpu_utilization_pct: float = 15.0
    memory_utilization_pct: float = 22.0
    gpu_available: bool = False


class WorkerNode(BaseModel):
    worker_id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    hostname: str
    region: RegionName = RegionName.US_EAST
    status: WorkerStatus = WorkerStatus.ONLINE
    capabilities: List[str] = Field(default_factory=lambda: ["reasoning", "ocr", "planning", "tool_execution"])
    capacity: WorkerCapacity = Field(default_factory=WorkerCapacity)
    last_heartbeat: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    registered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: str = "v1.18.0"
    total_jobs_completed: int = 0
    historical_avg_latency_ms: float = 120.0


# ---------------------------------------------------------
# Distributed Scheduling & Priority Queues
# ---------------------------------------------------------

class ScheduledJob(BaseModel):
    job_id: str = Field(default_factory=lambda: f"job_{uuid.uuid4().hex[:10]}")
    workflow_id: str
    agent_id: str
    task_name: str
    priority: JobPriority = JobPriority.NORMAL
    state: JobState = JobState.QUEUED
    assigned_worker_id: Optional[str] = None
    target_region: Optional[RegionName] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    sla_deadline_ms: float = 5000.0
    enqueued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    execution_duration_ms: float = 0.0
    error_message: Optional[str] = None


# ---------------------------------------------------------
# Durable Workflow & Checkpointing
# ---------------------------------------------------------

class WorkflowStepState(BaseModel):
    step_index: int
    step_name: str
    status: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    duration_ms: float = 0.0


class WorkflowCheckpoint(BaseModel):
    checkpoint_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:10]}")
    workflow_id: str
    step_index: int
    completed_steps: List[WorkflowStepState] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    memory_context: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    fencing_token: int = 1
    state_hash: str = Field(default_factory=lambda: uuid.uuid4().hex)


class DurableWorkflow(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:10]}")
    title: str
    tenant_id: str = "tenant_enterprise_01"
    agent_id: str
    state: JobState = JobState.RUNNING
    current_step_index: int = 0
    total_steps: int = 5
    assigned_worker_id: Optional[str] = None
    checkpoints: List[WorkflowCheckpoint] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------
# Distributed Locks & Concurrency
# ---------------------------------------------------------

class LockLease(BaseModel):
    lock_key: str
    holder_id: str
    fencing_token: int
    acquired_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str
    lease_duration_sec: int = 15


# ---------------------------------------------------------
# Autoscaling & Cloud Metrics
# ---------------------------------------------------------

class AutoscalingPolicy(BaseModel):
    policy_id: str = "default_policy"
    min_workers: int = 3
    max_workers: int = 50
    target_cpu_utilization_pct: float = 70.0
    target_queue_latency_ms: float = 1500.0
    scale_up_threshold_jobs: int = 10
    scale_down_idle_sec: int = 60
    current_desired_workers: int = 5
    last_scaling_action: ScalingAction = ScalingAction.STABLE
    last_scaled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ClusterOverview(BaseModel):
    cluster_id: str = "acr_fabric_cluster_01"
    status: str = "HEALTHY"
    total_workers: int = 5
    active_workers: int = 4
    draining_workers: int = 0
    crashed_workers: int = 0
    total_queued_jobs: int = 12
    total_running_jobs: int = 6
    total_completed_jobs: int = 1420
    mean_cluster_cpu_pct: float = 24.5
    mean_cluster_memory_pct: float = 31.2
    throughput_jobs_per_sec: float = 48.5
    active_regions: List[str] = Field(default_factory=lambda: ["us-east-1", "eu-central-1", "asia-east-1"])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------
# Disaster Recovery & Backups
# ---------------------------------------------------------

class DisasterRecoverySnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:10]}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_region: RegionName = RegionName.US_EAST
    target_replicas: List[RegionName] = Field(default_factory=lambda: [RegionName.EU_CENTRAL, RegionName.ASIA_EAST])
    workflow_count: int = 25
    checkpoint_count: int = 110
    snapshot_size_bytes: int = 1048576
    status: str = "REPLICATED"
    rpo_seconds: float = 2.5
    rto_seconds: float = 12.0
