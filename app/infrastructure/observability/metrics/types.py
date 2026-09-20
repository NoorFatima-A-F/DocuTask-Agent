"""
Metrics Types & Data Models.

Defines the 8 metric classifications (COUNTER, GAUGE, HISTOGRAM, SUMMARY, TIMER, RATE,
PERCENTILE, DISTRIBUTION) and time-series data point representations.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MetricType(str, enum.Enum):
    """Eight core enterprise metric types."""
    COUNTER = "COUNTER"
    GAUGE = "GAUGE"
    HISTOGRAM = "HISTOGRAM"
    SUMMARY = "SUMMARY"
    TIMER = "TIMER"
    RATE = "RATE"
    PERCENTILE = "PERCENTILE"
    DISTRIBUTION = "DISTRIBUTION"


class MetricPoint(BaseModel):
    """Single measured time-series sample."""
    timestamp: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)


class MetricSeries(BaseModel):
    """Time-series stream for a specific metric and label set."""
    name: str
    metric_type: MetricType
    description: str = ""
    unit: str = ""
    labels: Dict[str, str] = Field(default_factory=dict)
    points: List[MetricPoint] = Field(default_factory=list)


class AggregatedMetricSummary(BaseModel):
    """Statistical summary of a metric over a time window."""
    name: str
    count: int
    sum: float
    min: float
    max: float
    avg: float
    p50: float
    p90: float
    p95: float
    p99: float
    p999: float
    rate_per_sec: float
