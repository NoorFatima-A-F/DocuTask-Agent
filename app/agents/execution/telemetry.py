"""
Runtime Observability and Telemetry Integration.
Collects task latency, execution latency, queue latency, scheduling latency, and OpenTelemetry spans.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class LatencyRecord(BaseModel):
    """Latency measurements for a specific node execution."""
    node_id: str
    queue_latency_ms: float = Field(default=0.0, ge=0.0)
    scheduling_latency_ms: float = Field(default=0.0, ge=0.0)
    execution_latency_ms: float = Field(default=0.0, ge=0.0)
    total_latency_ms: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class ExecutionTelemetry(BaseModel):
    """Runtime observability telemetry record."""
    execution_id: str
    trace_id: str
    span_id: str
    node_latencies: Dict[str, LatencyRecord] = Field(default_factory=dict)
    tokens_consumed: int = Field(default=0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}
