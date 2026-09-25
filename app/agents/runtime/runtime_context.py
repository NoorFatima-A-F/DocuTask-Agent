"""
Runtime Context & Distributed Propagation.
Encapsulates complete enterprise identifiers: tenant_id, workspace_id, runtime_id, workflow_id,
execution_id, agent_id, trace_id, span_id, correlation_id, and request_id.
"""

from typing import Any, Dict, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class RuntimeContext(BaseModel):
    """Contextual metadata propagated across platform layers and distributed workers."""
    tenant_id: str = Field(default="default")
    workspace_id: str = Field(default="default-workspace")
    runtime_id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_id: Optional[str] = None
    execution_id: Optional[str] = None
    agent_id: Optional[str] = None
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    trace_id: str = Field(default_factory=lambda: uuid4().hex)
    span_id: str = Field(default_factory=lambda: uuid4().hex[:16])
    user_id: Optional[str] = None
    environment: str = Field(default="DEV")
    attributes: Dict[str, Any] = Field(default_factory=dict)

    @property
    def traceparent(self) -> str:
        """Constructs canonical W3C traceparent header: 00-traceid-spanid-01."""
        return f"00-{self.trace_id}-{self.span_id}-01"

    def spawn_child_context(
        self,
        new_span: bool = True,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None,
    ) -> "RuntimeContext":
        """Generates child context inheriting tenant, correlation, and trace, with new span_id."""
        update_dict: Dict[str, Any] = {}
        if new_span:
            update_dict["span_id"] = uuid4().hex[:16]
        if agent_id:
            update_dict["agent_id"] = agent_id
        if workflow_id:
            update_dict["workflow_id"] = workflow_id
        if execution_id:
            update_dict["execution_id"] = execution_id

        return self.model_copy(update=update_dict)

    def to_carrier(self) -> Dict[str, str]:
        """Encodes context into carrier headers for HTTP/gRPC/PubSub transmission."""
        return {
            "traceparent": self.traceparent,
            "x-tenant-id": self.tenant_id,
            "x-workspace-id": self.workspace_id,
            "x-runtime-id": self.runtime_id,
            "x-correlation-id": self.correlation_id,
            "x-request-id": self.request_id,
            "x-workflow-id": self.workflow_id or "",
            "x-execution-id": self.execution_id or "",
            "x-agent-id": self.agent_id or "",
        }

    @classmethod
    def from_carrier(cls, carrier: Dict[str, str]) -> "RuntimeContext":
        """Decodes context from carrier headers."""
        traceparent = carrier.get("traceparent", "")
        parts = traceparent.split("-") if traceparent else []
        trace_id = parts[1] if len(parts) >= 3 else uuid4().hex
        span_id = parts[2] if len(parts) >= 3 else uuid4().hex[:16]

        return cls(
            tenant_id=carrier.get("x-tenant-id", "default"),
            workspace_id=carrier.get("x-workspace-id", "default-workspace"),
            runtime_id=carrier.get("x-runtime-id", str(uuid4())),
            correlation_id=carrier.get("x-correlation-id", str(uuid4())),
            request_id=carrier.get("x-request-id", str(uuid4())),
            workflow_id=carrier.get("x-workflow-id") or None,
            execution_id=carrier.get("x-execution-id") or None,
            agent_id=carrier.get("x-agent-id") or None,
            trace_id=trace_id,
            span_id=span_id,
        )

    model_config = {"frozen": True}


class ContextPropagationMiddleware:
    """Middleware attaching and extracting RuntimeContext across network boundaries."""

    @staticmethod
    def inject(context: RuntimeContext, headers: Dict[str, str]) -> Dict[str, str]:
        """Injects context carrier into headers dictionary."""
        headers.update(context.to_carrier())
        return headers

    @staticmethod
    def extract(headers: Dict[str, str]) -> RuntimeContext:
        """Extracts context from incoming headers."""
        return RuntimeContext.from_carrier(headers)
