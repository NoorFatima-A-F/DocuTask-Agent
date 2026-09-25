"""Dashboard Widgets and Visual Component Definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class WidgetType(str, Enum):
    TIMESERIES = "TIMESERIES"
    GAUGE = "GAUGE"
    TABLE = "TABLE"
    SLO_HEATMAP = "SLO_HEATMAP"
    LOG_STREAM = "LOG_STREAM"
    ALERT_SUMMARY = "ALERT_SUMMARY"


@dataclass
class DashboardWidget:
    widget_id: str
    title: str
    widget_type: WidgetType
    metric_queries: List[str] = field(default_factory=list)
    refresh_interval_seconds: int = 15
    grid_position: Dict[str, int] = field(default_factory=lambda: {"x": 0, "y": 0, "w": 6, "h": 4})
    options: Dict[str, Any] = field(default_factory=dict)
