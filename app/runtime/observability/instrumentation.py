"""
Runtime Instrumentation Decorators & Context Managers.

Provides non-intrusive annotations (`@instrument_task`, `@trace_execution`, `async with record_span`)
that automatically attach distributed trace contexts, measure exact durations,
and emit structured lifecycle events (`STARTED`, `COMPLETED`, `FAILED`).
"""

from __future__ import annotations

import functools
import inspect
import time
from typing import Any, Callable
from app.runtime.observability.schemas import (
    EventCategory,
    EventPriority,
    EventSeverity,
    ExecutionEvent,
)
from app.runtime.observability.trace_context import async_trace_span, get_current_trace_context


def instrument_task(
    stage: str = "execution",
    category: EventCategory = EventCategory.EXECUTION,
    priority: EventPriority = EventPriority.NORMAL,
) -> Callable:
    """Decorator for automatic task timing, span propagation, and event emission."""
    def decorator(func: Callable) -> Callable:
        op_name = func.__name__

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                from app.runtime.observability.runtime_monitor import get_runtime_monitor
                monitor = get_runtime_monitor()

                async with async_trace_span(operation=op_name, component=stage) as ctx:
                    mission_id = kwargs.get("mission_id") or getattr(args[0], "mission_id", "default_mission") if args else "default_mission"
                    node_id = kwargs.get("node_id") or getattr(args[0], "node_id", None) if args else None
                    start_t = time.time()

                    # Start Event
                    start_evt = ExecutionEvent(
                        category=category,
                        event_type=f"{op_name.upper()}_STARTED",
                        mission_id=str(mission_id),
                        node_id=str(node_id) if node_id else None,
                        stage=stage,
                        trace_context=ctx,
                        priority=priority,
                        status="RUNNING",
                    )
                    await monitor.emit_event(start_evt)

                    try:
                        result = await func(*args, **kwargs)
                        dur_ms = max(0.1, (time.time() - start_t) * 1000.0)

                        # Success Event
                        success_evt = ExecutionEvent(
                            category=category,
                            event_type=f"{op_name.upper()}_COMPLETED",
                            mission_id=str(mission_id),
                            node_id=str(node_id) if node_id else None,
                            stage=stage,
                            trace_context=ctx,
                            duration_ms=dur_ms,
                            priority=priority,
                            status="SUCCESS",
                        )
                        await monitor.emit_event(success_evt)
                        return result
                    except Exception as ex:
                        dur_ms = max(0.1, (time.time() - start_t) * 1000.0)
                        fail_evt = ExecutionEvent(
                            category=category,
                            event_type=f"{op_name.upper()}_FAILED",
                            mission_id=str(mission_id),
                            node_id=str(node_id) if node_id else None,
                            stage=stage,
                            trace_context=ctx,
                            duration_ms=dur_ms,
                            priority=EventPriority.HIGH,
                            severity=EventSeverity.ERROR,
                            status="FAILED",
                            payload={"error": str(ex), "exception_type": type(ex).__name__},
                        )
                        await monitor.emit_event(fail_evt)
                        raise

            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                from app.runtime.observability.runtime_monitor import get_runtime_monitor
                monitor = get_runtime_monitor()

                ctx = get_current_trace_context()
                mission_id = kwargs.get("mission_id") or "default_mission"
                start_t = time.time()

                try:
                    result = func(*args, **kwargs)
                    dur_ms = max(0.1, (time.time() - start_t) * 1000.0)
                    evt = ExecutionEvent(
                        category=category,
                        event_type=f"{op_name.upper()}_COMPLETED",
                        mission_id=str(mission_id),
                        stage=stage,
                        trace_context=ctx,
                        duration_ms=dur_ms,
                        priority=priority,
                        status="SUCCESS",
                    )
                    monitor.emit_event_sync(evt)
                    return result
                except Exception as ex:
                    dur_ms = max(0.1, (time.time() - start_t) * 1000.0)
                    fail_evt = ExecutionEvent(
                        category=category,
                        event_type=f"{op_name.upper()}_FAILED",
                        mission_id=str(mission_id),
                        stage=stage,
                        trace_context=ctx,
                        duration_ms=dur_ms,
                        priority=EventPriority.HIGH,
                        severity=EventSeverity.ERROR,
                        status="FAILED",
                        payload={"error": str(ex)},
                    )
                    monitor.emit_event_sync(fail_evt)
                    raise

            return sync_wrapper

    return decorator
