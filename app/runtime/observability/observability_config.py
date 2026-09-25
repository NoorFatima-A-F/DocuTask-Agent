"""
Observability Subsystem Configuration.

Configurable parameters for queue capacities, retention limits, sampling frequencies,
and anomaly detection sensitivity.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ObservabilityConfig(BaseModel):
    """Configuration settings for AROL (Autonomous Runtime Observability Layer)."""

    max_event_queue_size: int = Field(default=10000, description="Max capacity of EventBus priority queues")
    max_event_store_capacity: int = Field(default=100000, description="In-memory retention limit for raw events")
    resource_sample_interval_sec: float = Field(default=1.0, description="Interval for CPU/Memory sampling")
    anomaly_z_score_threshold: float = Field(default=3.0, description="Standard deviations for anomaly triggering")
    enable_hash_validation: bool = Field(default=True, description="Enforce SHA-256 hash chaining")
    enable_background_workers: bool = Field(default=True, description="Run async event dispatchers")
    ws_broadcast_rate_limit_ms: int = Field(default=50, description="Minimum interval between live websocket pushes")
