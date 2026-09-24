"""
Distributed Trace Context Manager.

Provides OpenTelemetry-compatible tracing across asynchronous tasks and coroutines
using Python's `contextvars`. Ensures every runtime action inherits trace_id, span_id,
parent_span_id, depth, and baggage.
"""

from __future__ import annotations

import contextvars
import time
import uuid
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Dict, Iterator, Optional

from app.runtime.observability.schemas import TraceContext

# Global ContextVar for active trace context
_active_trace_context: contextvars.ContextVar[Optional[TraceContext]] = contextvars.ContextVar(
    "_active_trace_context", default=None
)


def get_current_trace_context() -> TraceContext:
    """Returns the currently active TraceContext, or creates a root context if none exists."""
    ctx = _active_trace_context.get()
    if ctx is None:
        ctx = TraceContext(
            trace_id=uuid.uuid4().hex,
            span_id=uuid.uuid4().hex[:16],
            parent_span_id=None,
            execution_depth=0,
            component="runtime",
            operation="root",
            timestamp_ns=time.time_ns(),
        )
        _active_trace_context.set(ctx)
    return ctx


def set_trace_context(ctx: TraceContext) -> contextvars.Token:
    """Explicitly sets the active trace context."""
    return _active_trace_context.set(ctx)


def reset_trace_context(token: contextvars.Token) -> None:
    """Resets the trace context to a previous token."""
    _active_trace_context.reset(token)


@contextmanager
def trace_span(
    operation: str,
    component: str = "runtime",
    worker_id: Optional[str] = None,
    node_id: Optional[str] = None,
    baggage: Optional[Dict[str, str]] = None,
) -> Iterator[TraceContext]:
    """Synchronous context manager for creating a child span."""
    parent = _active_trace_context.get()
    new_span_id = uuid.uuid4().hex[:16]
    
    if parent is None:
        child_ctx = TraceContext(
            trace_id=uuid.uuid4().hex,
            span_id=new_span_id,
            parent_span_id=None,
            execution_depth=0,
            component=component,
            operation=operation,
            worker_id=worker_id,
            node_id=node_id,
            timestamp_ns=time.time_ns(),
            baggage=baggage or {},
        )
    else:
        merged_baggage = {**parent.baggage, **(baggage or {})}
        child_ctx = TraceContext(
            trace_id=parent.trace_id,
            span_id=new_span_id,
            parent_span_id=parent.span_id,
            execution_depth=parent.execution_depth + 1,
            component=component,
            operation=operation,
            worker_id=worker_id or parent.worker_id,
            node_id=node_id or parent.node_id,
            timestamp_ns=time.time_ns(),
            baggage=merged_baggage,
        )
    
    token = _active_trace_context.set(child_ctx)
    try:
        yield child_ctx
    finally:
        _active_trace_context.reset(token)


@asynccontextmanager
async def async_trace_span(
    operation: str,
    component: str = "runtime",
    worker_id: Optional[str] = None,
    node_id: Optional[str] = None,
    baggage: Optional[Dict[str, str]] = None,
) -> AsyncIterator[TraceContext]:
    """Asynchronous context manager for creating a child span across async coroutines."""
    parent = _active_trace_context.get()
    new_span_id = uuid.uuid4().hex[:16]
    
    if parent is None:
        child_ctx = TraceContext(
            trace_id=uuid.uuid4().hex,
            span_id=new_span_id,
            parent_span_id=None,
            execution_depth=0,
            component=component,
            operation=operation,
            worker_id=worker_id,
            node_id=node_id,
            timestamp_ns=time.time_ns(),
            baggage=baggage or {},
        )
    else:
        merged_baggage = {**parent.baggage, **(baggage or {})}
        child_ctx = TraceContext(
            trace_id=parent.trace_id,
            span_id=new_span_id,
            parent_span_id=parent.span_id,
            execution_depth=parent.execution_depth + 1,
            component=component,
            operation=operation,
            worker_id=worker_id or parent.worker_id,
            node_id=node_id or parent.node_id,
            timestamp_ns=time.time_ns(),
            baggage=merged_baggage,
        )
    
    token = _active_trace_context.set(child_ctx)
    try:
        yield child_ctx
    finally:
        _active_trace_context.reset(token)
