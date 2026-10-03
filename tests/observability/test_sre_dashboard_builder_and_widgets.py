"""Tests for Dashboard Engine and Widget Rendering."""

from app.observability.dashboards.builder import DashboardEngine, DashboardType
from app.observability.metrics.registry import MetricRegistry


def test_dashboard_engine_default_dashboards():
    registry = MetricRegistry()
    registry.gauge("node_cpu_usage_percent").set(55.0)
    registry.counter("ai_model_requests_total").inc(120.0)

    engine = DashboardEngine(metric_registry=registry)
    dashboards = engine.list_dashboards()
    assert len(dashboards) == 4

    # Fetch and render SRE Golden Signals
    sre_data = engine.render_dashboard_data("db-sre-golden-signals")
    assert sre_data["dashboard_type"] == DashboardType.SRE_GOLDEN_SIGNALS.value
    assert len(sre_data["widgets"]) == 4

    # Fetch and render AI Operations
    ai_data = engine.render_dashboard_data("db-ai-operations")
    assert ai_data["dashboard_type"] == DashboardType.AI_OPERATIONS.value
    assert "ai_model_requests_total" in str(ai_data)
