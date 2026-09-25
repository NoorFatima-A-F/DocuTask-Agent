"""
Widget Query Evaluator.

Executes data queries for dashboard widgets against live metric registries, log indices,
and trace streams.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.dashboards.models import DashboardWidget, WidgetType
from app.infrastructure.observability.metrics.aggregators import TimeWindowAggregator
from app.infrastructure.observability.metrics.registry import MetricRegistry

logger = logging.getLogger("infrastructure.observability.dashboards.widgets")


class RenderedWidgetData(BaseModel):
    """Processed data payload ready for frontend or API dashboard rendering."""
    widget_id: str
    title: str
    widget_type: WidgetType
    data: Any
    summary: Dict[str, Any] = Field(default_factory=dict)


class WidgetQueryEvaluator:
    """
    Evaluates queries for dashboard widgets.
    """

    def __init__(self, metric_registry: Optional[MetricRegistry] = None) -> None:
        self.metric_registry = metric_registry or MetricRegistry()

    def evaluate_widget(self, widget: DashboardWidget, window_seconds: float = 300.0) -> RenderedWidgetData:
        """Evaluate a single dashboard widget and return rendered data."""
        if widget.widget_type in (WidgetType.TIMESERIES, WidgetType.GAUGE, WidgetType.SINGLESTAT):
            series = self.metric_registry.get_series(widget.metric_query) if widget.metric_query else None
            if series and series.points:
                agg = TimeWindowAggregator.aggregate(series, window_seconds=window_seconds)
                val = agg.avg if widget.widget_type == WidgetType.GAUGE else (agg.sum if widget.widget_type == WidgetType.SINGLESTAT else [pt.model_dump() for pt in series.points[-20:]])
                return RenderedWidgetData(
                    widget_id=widget.widget_id,
                    title=widget.title,
                    widget_type=widget.widget_type,
                    data=val,
                    summary=agg.model_dump(mode="json"),
                )
            else:
                return RenderedWidgetData(
                    widget_id=widget.widget_id,
                    title=widget.title,
                    widget_type=widget.widget_type,
                    data=0.0,
                    summary={"status": "No data points collected"},
                )

        return RenderedWidgetData(
            widget_id=widget.widget_id,
            title=widget.title,
            widget_type=widget.widget_type,
            data={"placeholder": True},
        )
