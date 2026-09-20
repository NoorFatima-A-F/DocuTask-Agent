"""Multidimensional Observability Context for Telemetry and Distributed Systems."""

from __future__ import annotations

import contextvars
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ObservabilityContext:
    """Carries complete multidimensional execution and identity context."""
    request_id: str = field(default_factory=lambda: f"req-{uuid.uuid4().hex[:10]}")
    trace_id: str = field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:12]}")
    span_id: str = field(default_factory=lambda: f"span-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    org_id: str = "default-org"
    workspace_id: str = "default-ws"
    service_name: str = "docutask-platform"
    service_version: str = "1.0.0"
    environment: str = "production"
    region: str = "us-central1"
    cluster_id: str = "cluster-primary"
    node_id: str = "node-01"
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    task_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    severity: str = "INFO"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "tenant_id": self.tenant_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "service_name": self.service_name,
            "service_version": self.service_version,
            "environment": self.environment,
            "region": self.region,
            "cluster_id": self.cluster_id,
            "node_id": self.node_id,
            "workflow_id": self.workflow_id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "metadata": self.metadata,
        }

    def fork_span(self, new_service: Optional[str] = None) -> ObservabilityContext:
        """Fork context for a child span / downstream service hop."""
        return ObservabilityContext(
            request_id=self.request_id,
            trace_id=self.trace_id,
            span_id=f"span-{uuid.uuid4().hex[:8]}",
            tenant_id=self.tenant_id,
            org_id=self.org_id,
            workspace_id=self.workspace_id,
            service_name=new_service or self.service_name,
            service_version=self.service_version,
            environment=self.environment,
            region=self.region,
            cluster_id=self.cluster_id,
            node_id=self.node_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            task_id=self.task_id,
            user_id=self.user_id,
            severity=self.severity,
            metadata=dict(self.metadata),
        )


_CURRENT_CONTEXT: contextvars.ContextVar[Optional[ObservabilityContext]] = contextvars.ContextVar(
    "current_observability_context", default=None
)


def get_current_context() -> ObservabilityContext:
    """Retrieve the current active thread/coroutine context, or generate a default one."""
    ctx = _CURRENT_CONTEXT.get()
    if ctx is None:
        ctx = ObservabilityContext()
        _CURRENT_CONTEXT.set(ctx)
    return ctx


def set_current_context(ctx: ObservabilityContext) -> None:
    """Set the active thread/coroutine observability context."""
    _CURRENT_CONTEXT.set(ctx)
