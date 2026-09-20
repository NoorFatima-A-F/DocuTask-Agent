"""
Tool Execution & Invocation Context Models.
Provides strongly typed execution contexts for tool invocation, provider tracing, and capability resolution.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ProviderContext(BaseModel):
    """Context information for tool provider interaction."""
    provider_name: str
    region: str = Field(default="us-central1")
    credentials_ref: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class CapabilityContext(BaseModel):
    """Context information for target capability matching."""
    capability_name: str
    min_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    max_cost_usd: float = Field(default=1.0, ge=0.0)
    max_latency_ms: float = Field(default=5000.0, ge=0.0)
    model_config = {"frozen": True}


class InvocationContext(BaseModel):
    """Context for a specific tool execution invocation."""
    invocation_id: UUID = Field(default_factory=uuid4)
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class ToolExecutionContext(BaseModel):
    """Aggregate execution context for tool execution."""
    tool_id: str
    invocation: InvocationContext = Field(default_factory=InvocationContext)
    provider: ProviderContext = Field(default_factory=lambda: ProviderContext(provider_name="default"))
    capability: CapabilityContext = Field(default_factory=lambda: CapabilityContext(capability_name="default"))
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
