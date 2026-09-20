"""
Tests for Dependency Graphs, Health Analysis, Root Cause Analysis, and Dashboard Framework.
"""

import pytest

from app.infrastructure.observability.dashboards.builder import (
    DashboardBuilder,
)
from app.infrastructure.observability.dashboards.models import (
    DashboardWidget,
    WidgetType,
)
from app.infrastructure.observability.dashboards.widgets import (
    WidgetQueryEvaluator,
)
from app.infrastructure.observability.diagnostics.dependency_graph import (
    ServiceDependencyGraph,
)
from app.infrastructure.observability.diagnostics.health_analysis import (
    CrossLayerHealthAnalyzer,
)
from app.infrastructure.observability.diagnostics.root_cause import (
    RootCauseAnalyzer,
)
from app.infrastructure.observability.logs.models import LogLevel, LogRecord
from app.infrastructure.observability.metrics.registry import MetricRegistry
from app.infrastructure.observability.tracing.models import Span, SpanStatus


def test_service_dependency_graph():
    graph = ServiceDependencyGraph()

    # Record interactions
    graph.record_interaction("api-gateway", "workflow-engine", latency_ms=25.0)
    graph.record_interaction("api-gateway", "workflow-engine", latency_ms=35.0)
    graph.record_interaction("workflow-engine", "ai-gateway", latency_ms=120.0, is_error=True)

    edges = graph.list_all_edges()
    assert len(edges) == 2

    gw_edge = next(e for e in edges if e.caller_service == "api-gateway")
    assert gw_edge.call_count == 2
    assert gw_edge.avg_latency_ms == 30.0
    assert gw_edge.error_count == 0

    ai_edge = next(e for e in edges if e.callee_service == "ai-gateway")
    assert ai_edge.error_count == 1
    assert ai_edge.error_rate_percent == 100.0

    services = graph.list_all_services()
    assert services == ["ai-gateway", "api-gateway", "workflow-engine"]


def test_cross_layer_health_analysis():
    analyzer = CrossLayerHealthAnalyzer()

    # Normal state
    report_healthy = analyzer.analyze(
        cpu_usage_pct=30.0,
        memory_usage_pct=40.0,
        queue_depth=50,
        ai_error_rate_pct=0.0,
        db_latency_ms=8.0,
    )
    assert report_healthy.overall_health_score == 100.0
    assert "optimally" in report_healthy.summary_message.lower()

    # Degraded state
    report_degraded = analyzer.analyze(
        cpu_usage_pct=92.0,
        memory_usage_pct=95.0,
        queue_depth=2500,
        ai_error_rate_pct=8.0,
        db_latency_ms=150.0,
    )
    assert report_degraded.overall_health_score < 70.0
    assert len(report_degraded.layers["INFRASTRUCTURE"].active_anomalies) == 2


def test_automated_root_cause_analysis():
    rca = RootCauseAnalyzer()

    failed_span = Span(
        trace_id="tr-fail-1",
        span_id="sp-ocr-err",
        operation_name="process_ocr",
        service_name="ocr-service",
        status=SpanStatus.ERROR,
        status_message="Tesseract process timeout after 30s",
    )

    error_log = LogRecord(
        level=LogLevel.ERROR,
        message="OCR extraction timed out on page 14",
        service_name="ocr-service",
        trace_id="tr-fail-1",
        exception="TimeoutError: OCR worker stalled",
    )

    report = rca.analyze_incident(
        report_id="rca-ocr-timeout",
        spans=[failed_span],
        logs=[error_log],
        incident_title="OCR Service Degradation",
    )

    assert report.report_id == "rca-ocr-timeout"
    assert report.root_cause_service == "ocr-service"
    assert "timeout" in report.root_cause_summary.lower()
    assert report.confidence_score >= 0.90
    assert len(report.evidence) == 2


def test_dashboard_builder_and_widget_evaluator():
    dash = DashboardBuilder.build_sre_dashboard()
    assert dash.category == "SRE"
    assert len(dash.panels) == 2

    registry = MetricRegistry()
    registry.record("system_cpu_usage_percent", 48.5)

    evaluator = WidgetQueryEvaluator(metric_registry=registry)
    widget = DashboardWidget(
        widget_id="w-cpu",
        title="CPU Usage",
        widget_type=WidgetType.GAUGE,
        metric_query="system_cpu_usage_percent",
    )

    rendered = evaluator.evaluate_widget(widget)
    assert rendered.widget_id == "w-cpu"
    assert rendered.data == 48.5
