"""Declarative Infrastructure Configuration Schemas."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ResourceLimits(BaseModel):
    """Resource bounds for container/service workloads."""

    cpu: float = Field(1.0, ge=0.1, le=128.0)
    memory_gb: float = Field(2.0, ge=0.1, le=1024.0)
    storage_gb: float = Field(10.0, ge=1.0, le=10000.0)


class RuntimeConfig(BaseModel):
    """Runtime process and scaling properties."""

    replicas: int = Field(1, ge=1, le=200)
    image: str = "docutask/agent-runtime:latest"
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    health_check_path: str = "/health"


class RegionConfig(BaseModel):
    """Multi-region deployment topology."""

    primary: str = "us-east-1"
    failover: Optional[str] = "eu-west-1"
    supported_regions: List[str] = Field(default_factory=lambda: ["us-east-1", "eu-west-1"])


class ScalingPolicy(BaseModel):
    """Autoscaling policy parameters."""

    enabled: bool = True
    min_replicas: int = 1
    max_replicas: int = 10
    target_cpu_utilization_pct: int = 75


class InfrastructureManifest(BaseModel):
    """Declarative versioned infrastructure manifest."""

    manifest_id: str
    service_name: str
    version: str = "1.0.0"
    environment: str = "PRODUCTION"
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    region: RegionConfig = Field(default_factory=RegionConfig)
    scaling: ScalingPolicy = Field(default_factory=ScalingPolicy)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
