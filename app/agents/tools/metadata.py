"""
Tool Metadata & Profiles.
Models security classifications, cost profiles, latency profiles, resource requirements, and auth requirements.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CostProfile(BaseModel):
    """Cost profile model for tool invocations."""
    cost_per_call_usd: float = Field(default=0.0, ge=0.0)
    cost_per_1k_tokens_usd: float = Field(default=0.0, ge=0.0)
    currency: str = Field(default="USD")
    model_config = {"frozen": True}


class LatencyProfile(BaseModel):
    """Latency profile model for tool invocations."""
    p50_latency_ms: float = Field(default=100.0, ge=0.0)
    p95_latency_ms: float = Field(default=500.0, ge=0.0)
    p99_latency_ms: float = Field(default=1000.0, ge=0.0)
    model_config = {"frozen": True}


class ToolSecurityProfile(BaseModel):
    """Security classification and authentication requirements."""
    security_classification: str = Field(default="INTERNAL")  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    requires_auth: bool = Field(default=False)
    auth_type: str = Field(default="NONE")  # API_KEY, OAUTH2, IAM_BEARER
    secret_manager_ref: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class ToolResourceRequirements(BaseModel):
    """Tool execution resource requirements."""
    cpu_cores: float = Field(default=0.1, gt=0.0)
    ram_mb: float = Field(default=256.0, gt=0.0)
    gpu_required: bool = Field(default=False)
    model_config = {"frozen": True}
