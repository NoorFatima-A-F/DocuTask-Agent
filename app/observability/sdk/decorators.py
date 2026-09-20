"""Observability and SRE Instrumentation Decorators."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, Optional

from ..core.context import get_current_context
from ..logging.logger import LogLevel, StructuredLogger
from ..metrics.registry import MetricRegistry
from ..profiling.profiler import ContinuousProfiler
from ..tracing.spans import SpanKind
from ..tracing.tracer import TracingEngine

_global_tracer = TracingEngine()
_global_logger = StructuredLogger()
_global_metrics = MetricRegistry()
_global_profiler = ContinuousProfiler()


def trace(operation: str, kind: SpanKind = SpanKind.INTERNAL):
    """Function/method decorator that starts an active trace span automatically."""
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with _global_tracer.start_as_current_span(name=operation, kind=kind) as span:
                span.set_attribute("function", func.__qualname__)
                return func(*args, **kwargs)
        return wrapper
    return decorator


def metric_counter(name: str, description: str = ""):
    """Function decorator that increments a counter on each execution."""
    c = _global_metrics.counter(name, description)

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            c.inc(1.0)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def profile(block_name: Optional[str] = None):
    """Function decorator recording continuous profiling latency and memory samples."""
    def decorator(func: Callable[..., Any]):
        name = block_name or func.__qualname__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with _global_profiler.profile_block(name):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def audit_log(action: str):
    """Function decorator recording an audit log event upon successful invocation."""
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            _global_logger.info(f"Audit action completed: {action}", action=action, function=func.__qualname__)
            return res
        return wrapper
    return decorator
