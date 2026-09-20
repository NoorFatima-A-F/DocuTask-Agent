"""
Distributed Correlation and Tracing Context Primitives.
Propagates identifiers across asynchronous task boundaries.
"""
from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import Optional, Dict, Any, Generator
import uuid
import contextvars

@dataclass(frozen=True)
class CorrelationContext:
    """Immutable context propagation model."""
    correlation_id: str = field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:16]}")
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    request_id: Optional[str] = None
    execution_id: Optional[str] = None
    session_id: Optional[str] = None
    causation_id: Optional[str] = None
    tenant_id: str = "default-tenant"
    originator: str = "system"
    baggage: Dict[str, Any] = field(default_factory=dict)

    def with_execution(self, execution_id: str) -> "CorrelationContext":
        return CorrelationContext(
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            span_id=self.span_id,
            request_id=self.request_id,
            execution_id=execution_id,
            session_id=self.session_id,
            causation_id=self.causation_id,
            tenant_id=self.tenant_id,
            originator=self.originator,
            baggage=dict(self.baggage)
        )

    def with_causation(self, causation_id: str) -> "CorrelationContext":
        return CorrelationContext(
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            span_id=self.span_id,
            request_id=self.request_id,
            execution_id=self.execution_id,
            session_id=self.session_id,
            causation_id=causation_id,
            tenant_id=self.tenant_id,
            originator=self.originator,
            baggage=dict(self.baggage)
        )

_current_context: contextvars.ContextVar[CorrelationContext] = contextvars.ContextVar(
    "correlation_context",
    default=CorrelationContext()
)

def get_current_correlation() -> CorrelationContext:
    return _current_context.get()

def set_current_correlation(ctx: CorrelationContext) -> contextvars.Token:
    return _current_context.set(ctx)

@contextmanager
def correlation_scope(ctx: CorrelationContext) -> Generator[CorrelationContext, None, None]:
    token = set_current_correlation(ctx)
    try:
        yield ctx
    finally:
        _current_context.reset(token)
