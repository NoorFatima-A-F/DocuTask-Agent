"""
app/core/telemetry.py
OpenTelemetry instrumentation helper for GenAI tracing and document spans.
"""

from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Dict, Generator


@contextmanager
def trace_agent_execution(
    agent_name: str, document_id: str, **attributes: Any
) -> Generator[Dict[str, Any], None, None]:
    """Context manager for tracing agent execution spans with GenAI attributes."""
    span_data: Dict[str, Any] = {
        "gen_ai.system": "docutask",
        "gen_ai.agent.name": agent_name,
        "document.id": document_id,
        **attributes,
    }
    try:
        # Yield active span dictionary (can be hooked into OpenTelemetry tracer)
        yield span_data
    finally:
        pass
