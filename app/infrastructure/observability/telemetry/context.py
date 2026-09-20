"""
Unified Telemetry Context & Correlation Model.

Defines the shared correlation context automatically propagated across all platform
components (traces, spans, logs, metrics, alerts, events) and data masking utilities.
"""

from __future__ import annotations

import re
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# Sensitive data masking patterns (PII, tokens, keys)
REDACTION_PATTERNS = [
    (re.compile(r"(api[_-]?key|secret|password|auth[_-]?token|bearer)\s*[:=]\s*['\"]?([^'\"\s,]+)['\"]?", re.IGNORECASE), r"\1=***REDACTED***"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"), "***@***.***"),
    (re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b"), "****-****-****-****"),
]


def mask_sensitive_data(text: str) -> str:
    """Mask sensitive keys, tokens, emails, and card numbers from strings."""
    if not isinstance(text, str):
        return text
    masked = text
    for pattern, replacement in REDACTION_PATTERNS:
        masked = pattern.sub(replacement, masked)
    return masked


class TelemetryContext(BaseModel):
    """
    Standardized correlation context attached to all telemetry records.
    """
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    correlation_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    request_id: Optional[str] = None
    tenant_id: str = Field(default="global")
    workspace_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    connector_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    user_id: Optional[str] = None
    region: str = Field(default="us-east-1")
    cluster: str = Field(default="cluster-primary")
    service_name: str = Field(default="docutask-service")
    service_version: str = Field(default="3.1.0")
    environment: str = Field(default="production")
    attributes: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def fork_child_span(self, new_span_id: Optional[str] = None) -> TelemetryContext:
        """Create a child context inheriting trace & correlation attributes with a new span ID."""
        return TelemetryContext(
            trace_id=self.trace_id,
            span_id=new_span_id or uuid.uuid4().hex[:16],
            parent_span_id=self.span_id,
            correlation_id=self.correlation_id,
            request_id=self.request_id,
            tenant_id=self.tenant_id,
            workspace_id=self.workspace_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            connector_id=self.connector_id,
            model_id=self.model_id,
            prompt_id=self.prompt_id,
            user_id=self.user_id,
            region=self.region,
            cluster=self.cluster,
            service_name=self.service_name,
            service_version=self.service_version,
            environment=self.environment,
            attributes=dict(self.attributes),
        )

    def to_header_dict(self) -> Dict[str, str]:
        """Serialize context into standard HTTP/gRPC headers."""
        headers = {
            "x-trace-id": self.trace_id,
            "x-span-id": self.span_id,
            "x-correlation-id": self.correlation_id,
            "x-tenant-id": self.tenant_id,
            "x-region": self.region,
            "x-cluster": self.cluster,
            "x-service-name": self.service_name,
            "x-service-version": self.service_version,
            "x-environment": self.environment,
        }
        if self.parent_span_id:
            headers["x-parent-span-id"] = self.parent_span_id
        if self.request_id:
            headers["x-request-id"] = self.request_id
        if self.workflow_id:
            headers["x-workflow-id"] = self.workflow_id
        if self.agent_id:
            headers["x-agent-id"] = self.agent_id
        if self.model_id:
            headers["x-model-id"] = self.model_id
        if self.prompt_id:
            headers["x-prompt-id"] = self.prompt_id
        if self.user_id:
            headers["x-user-id"] = self.user_id
        return headers

    @classmethod
    def from_header_dict(cls, headers: Dict[str, str]) -> TelemetryContext:
        """Hydrate context from HTTP/gRPC headers."""
        lower = {k.lower(): v for k, v in headers.items()}
        return cls(
            trace_id=lower.get("x-trace-id", uuid.uuid4().hex),
            span_id=lower.get("x-span-id", uuid.uuid4().hex[:16]),
            parent_span_id=lower.get("x-parent-span-id"),
            correlation_id=lower.get("x-correlation-id", uuid.uuid4().hex),
            request_id=lower.get("x-request-id"),
            tenant_id=lower.get("x-tenant-id", "global"),
            workflow_id=lower.get("x-workflow-id"),
            agent_id=lower.get("x-agent-id"),
            model_id=lower.get("x-model-id"),
            prompt_id=lower.get("x-prompt-id"),
            user_id=lower.get("x-user-id"),
            region=lower.get("x-region", "us-east-1"),
            cluster=lower.get("x-cluster", "cluster-primary"),
            service_name=lower.get("x-service-name", "docutask-service"),
            service_version=lower.get("x-service-version", "3.1.0"),
            environment=lower.get("x-environment", "production"),
        )


# ContextVar for implicit task/thread propagation
_CURRENT_CONTEXT: ContextVar[TelemetryContext] = ContextVar(
    "current_telemetry_context",
    default=TelemetryContext(),
)


def get_current_context() -> TelemetryContext:
    """Retrieve active telemetry context for the current async task or thread."""
    return _CURRENT_CONTEXT.get()


def set_current_context(context: TelemetryContext) -> None:
    """Set active telemetry context for the current async task or thread."""
    _CURRENT_CONTEXT.set(context)
