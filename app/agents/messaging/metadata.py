"""
Message Metadata & Context Models.
Provides immutable Pydantic v2 metadata models for all agent messages.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CorrelationContext(BaseModel):
    """Correlation and causation tracing context."""
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    causation_id: Optional[str] = Field(default=None)
    conversation_id: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None)
    execution_id: Optional[str] = Field(default=None)
    session_id: Optional[str] = Field(default=None)
    tenant_id: str = Field(default="default")
    model_config = {"frozen": True}


class TraceContext(BaseModel):
    """OpenTelemetry W3C distributed tracing context."""
    trace_id: str = Field(default_factory=lambda: uuid4().hex)
    span_id: str = Field(default_factory=lambda: uuid4().hex[:16])
    parent_span_id: Optional[str] = Field(default=None)
    trace_flags: str = Field(default="01")
    model_config = {"frozen": True}


class MessageMetadata(BaseModel):
    """Comprehensive Message Metadata."""
    message_id: UUID = Field(default_factory=uuid4)
    correlation: CorrelationContext = Field(default_factory=CorrelationContext)
    trace: TraceContext = Field(default_factory=TraceContext)
    sender: str = Field(default="DocumentAgent")
    receiver: Optional[str] = Field(default=None)
    priority: str = Field(default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = Field(default="v1.0")
    ttl_seconds: Optional[float] = Field(default=None)
    retry_count: int = Field(default=0, ge=0)
    security_classification: str = Field(default="INTERNAL")
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    custom: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
