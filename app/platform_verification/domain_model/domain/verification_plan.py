"""
Verification Plan Domain: Execution Strategies, Orders, Concurrency, and Resource Policies.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class ExecutionStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    ADAPTIVE_BATCH = "ADAPTIVE_BATCH"
    CANARY_STEPPED = "CANARY_STEPPED"
    DISTRIBUTED_SHARDED = "DISTRIBUTED_SHARDED"


class TimeoutPolicy(BaseModel):
    max_total_timeout_seconds: int = 600
    per_stage_timeout_seconds: int = 120
    grace_period_seconds: int = 15


class RetryPolicy(BaseModel):
    max_attempts: int = 3
    initial_interval_seconds: float = 1.0
    backoff_multiplier: float = 2.0
    retryable_errors: List[str] = Field(default_factory=lambda: ["RATE_LIMIT_EXCEEDED", "NETWORK_TIMEOUT", "GPU_OOM_RECOVERABLE"])


class ResourceRequirements(BaseModel):
    min_cpu_cores: int = 2
    min_ram_gb: float = 8.0
    gpu_required: bool = False
    max_concurrent_workers: int = 8


class VerificationPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"vplan_{uuid.uuid4().hex[:8]}")
    definition_id: str
    tenant_id: str = "default-tenant"
    version: str = "1.0.0"
    execution_strategy: ExecutionStrategy = ExecutionStrategy.PARALLEL
    execution_order: List[str] = Field(default_factory=list)
    parallelism: int = 4
    timeout_policy: TimeoutPolicy = Field(default_factory=TimeoutPolicy)
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    resource_requirements: ResourceRequirements = Field(default_factory=ResourceRequirements)
    dataset_version_ids: List[str] = Field(default_factory=list)
    configuration_snapshot_id: Optional[str] = None
    environment_snapshot_id: Optional[str] = None
    plugin_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
