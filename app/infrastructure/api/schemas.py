"""Request and Response Schemas for Infrastructure REST API."""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class RuntimeDeployRequest(BaseModel):
    service: str = Field(..., min_length=2)
    environment: str = "PRODUCTION"
    replicas: int = 1
    version: str = "1.0.0"
    config: Dict[str, Any] = Field(default_factory=dict)


class RuntimeActionRequest(BaseModel):
    instance_id: str


class ResourceProvisionRequest(BaseModel):
    name: str
    category: str = "COMPUTE"  # COMPUTE, STORAGE, NETWORKING
    resource_type: str = "CONTAINER"
    cpu_cores: float = 1.0
    memory_mb: int = 1024
    storage_gb: int = 10
    environment: str = "PRODUCTION"


class ServiceHealthResponse(BaseModel):
    service_id: str
    status: str
    version: str
    cpu_percent: float
    memory_mb: float
    latency_p95_ms: float
    errors_per_minute: int
    region: str
    cluster: str
    last_check: datetime


class ServiceInstanceResponse(BaseModel):
    instance_id: str
    service_name: str
    environment: str
    replicas: int
    state: str
    version: str
    created_at: datetime
    error_message: Optional[str] = None


class ResourceResponse(BaseModel):
    resource_id: str
    name: str
    category: str
    resource_type: str
    state: str
    endpoint_url: Optional[str] = None
    allocated_at: datetime
