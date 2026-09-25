"""
Execution Resource Requirements Domain Models.
Models CPU, Memory, GPU, LLM, Storage, Database, Queue, Cache, and External API resource requests.
"""

from typing import Dict
from pydantic import BaseModel, Field


class ExecutionResources(BaseModel):
    """Resource requirement specifications for executing agent tasks."""

    cpu_vcpu: float = Field(default=0.25, gt=0.0)
    memory_mb: float = Field(default=512.0, gt=0.0)
    gpu_units: float = Field(default=0.0, ge=0.0)
    llm_tokens: int = Field(default=4000, ge=0)
    storage_mb: float = Field(default=100.0, ge=0.0)
    db_connections: int = Field(default=1, ge=0)
    external_api_calls: int = Field(default=1, ge=0)
    custom_resources: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}
