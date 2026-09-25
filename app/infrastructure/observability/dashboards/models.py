"""
Dashboard Models & Widget Schemas.

Defines schemas for Operational, Executive, SRE, AI Runtime, and Infrastructure Dashboards.
"""

from __future__ import annotations

import enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WidgetType(str, enum.Enum):
    """Supported dashboard visualization widgets."""
    TIMESERIES = "TIMESERIES"
    GAUGE = "GAUGE"
    SINGLESTAT = "SINGLESTAT"
    HEATMAP = "HEATMAP"
    TABLE = "TABLE"
    LOG_STREAM = "LOG_STREAM"
    TRACE_GRAPH = "TRACE_GRAPH"


class DashboardWidget(BaseModel):
    """Visual widget specification."""
    widget_id: str
    title: str
    widget_type: WidgetType
    metric_query: Optional[str] = None
    log_query: Optional[str] = None
    width: int = Field(default=6, ge=1, le=12)
    height: int = Field(default=4, ge=1, le=12)
    options: Dict[str, Any] = Field(default_factory=dict)


class DashboardPanel(BaseModel):
    """Logical grouping of dashboard widgets."""
    panel_id: str
    title: str
    widgets: List[DashboardWidget] = Field(default_factory=list)


class Dashboard(BaseModel):
    """Complete multi-panel dashboard definition."""
    dashboard_id: str
    title: str
    category: str = "OPERATIONS"  # EXECUTIVE, SRE, OPERATIONS, AI_RUNTIME, WORKFLOW, TENANT, INFRASTRUCTURE
    description: str = ""
    panels: List[DashboardPanel] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
