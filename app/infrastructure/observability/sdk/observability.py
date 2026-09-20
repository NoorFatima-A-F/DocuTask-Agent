"""
Unified Enterprise Observability SDK.

Provides clean, unified developer and operations APIs across metrics, logs,
distributed traces, profiling, alerts, SLOs, service dependencies, and diagnostics.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Generator, List, Optional

from app.infrastructure.observability.alerts.models import AlertInstance, AlertRule, AlertSeverity
from app.infrastructure.observability.alerts.notifications import AlertDispatcher
from app.infrastructure.observability.alerts.rules import AlertRuleEvaluator
from app.infrastructure.observability.dashboards.builder import DashboardBuilder
from app.infrastructure.observability.dashboards.models import Dashboard
from app.infrastructure.observability.dashboards.widgets import WidgetQueryEvaluator
from app.infrastructure.observability.diagnostics.dependency_graph import DependencyEdge, ServiceDependencyGraph
from app.infrastructure.observability.diagnostics.health_analysis import CrossLayerHealthAnalyzer, PlatformHealthReport
from app.infrastructure.observability.diagnostics.root_cause import RCAReport, RootCauseAnalyzer
from app.infrastructure.observability.logs.indexing import LogIndex
from app.infrastructure.observability.logs.ingestion import LogIngestionPipeline
from app.infrastructure.observability.logs.models import LogLevel, LogRecord
from app.infrastructure.observability.metrics.collectors import (
    AIMetricCollector,
    SystemMetricCollector,
    WorkflowMetricCollector,
)
from app.infrastructure.observability.metrics.registry import MetricRegistry
from app.infrastructure.observability.metrics.types import MetricSeries, MetricType
from app.infrastructure.observability.profiling.cpu import CPUHotspot, CPUProfiler, StackFrame
from app.infrastructure.observability.profiling.memory import MemoryLeakWarning, MemoryProfiler
from app.infrastructure.observability.slo.budgets import ErrorBudgetStatus, ErrorBudgetTracker
from app.infrastructure.observability.slo.objectives import SLOObjective
from app.infrastructure.observability.telemetry.collector import TelemetryCollectorPipeline
from app.infrastructure.observability.telemetry.context import TelemetryContext, get_current_context
from app.infrastructure.observability.telemetry.sdk import TelemetrySDK
from app.infrastructure.observability.tracing.models import Span, SpanKind
from app.infrastructure.observability.tracing.spans import TraceAnalysisReport, TraceTreeAnalyzer
from app.infrastructure.observability.tracing.tracer import Tracer


class ObservabilitySDK:
    """
    Unified platform SDK for the entire DocuTask Agent Observability Platform.
    """

    def __init__(
        self,
        collector_pipeline: Optional[TelemetryCollectorPipeline] = None,
        metric_registry: Optional[MetricRegistry] = None,
        log_index: Optional[LogIndex] = None,
        tracer: Optional[Tracer] = None,
        cpu_profiler: Optional[CPUProfiler] = None,
        memory_profiler: Optional[MemoryProfiler] = None,
        alert_evaluator: Optional[AlertRuleEvaluator] = None,
        alert_dispatcher: Optional[AlertDispatcher] = None,
        error_budget_tracker: Optional[ErrorBudgetTracker] = None,
        dependency_graph: Optional[ServiceDependencyGraph] = None,
        rca_analyzer: Optional[RootCauseAnalyzer] = None,
    ) -> None:
        self.collector = collector_pipeline or TelemetryCollectorPipeline()
        self.telemetry = TelemetrySDK(self.collector)
        self.metric_registry = metric_registry or MetricRegistry()
        self.system_metrics = SystemMetricCollector(self.metric_registry)
        self.workflow_metrics = WorkflowMetricCollector(self.metric_registry)
        self.ai_metrics = AIMetricCollector(self.metric_registry)

        self.log_index = log_index or LogIndex()
        self.log_pipeline = LogIngestionPipeline(sink_callback=self.log_index.index_batch)

        self.tracer = tracer or Tracer()
        self.cpu_profiler = cpu_profiler or CPUProfiler()
        self.memory_profiler = memory_profiler or MemoryProfiler()

        self.alert_evaluator = alert_evaluator or AlertRuleEvaluator()
        self.alert_dispatcher = alert_dispatcher or AlertDispatcher()

        self.error_budget_tracker = error_budget_tracker or ErrorBudgetTracker()
        self.dependency_graph = dependency_graph or ServiceDependencyGraph()
        self.health_analyzer = CrossLayerHealthAnalyzer()
        self.rca_analyzer = rca_analyzer or RootCauseAnalyzer()
        self.widget_evaluator = WidgetQueryEvaluator(self.metric_registry)

    # --- Metrics ---
    def record_metric(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, labels: Optional[Dict[str, str]] = None) -> None:
        self.metric_registry.record(name, value, metric_type, labels)
        self.telemetry.gauge(name, value, labels)

    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        self.metric_registry.increment(name, value, labels)
        self.telemetry.counter(name, value, labels)

    def get_metrics(self, prefix: Optional[str] = None) -> List[MetricSeries]:
        return self.metric_registry.list_series(prefix=prefix)

    # --- Logs ---
    def log(self, level: LogLevel, message: str, exception: Optional[Exception] = None, **kwargs: Any) -> LogRecord:
        record = self.log_pipeline.emit(level=level, message=message, exception=exception, attributes=kwargs)
        self.log_index.index(record)
        self.telemetry.log(level.value, message, **kwargs)
        return record

    def search_logs(self, **kwargs: Any) -> List[LogRecord]:
        return self.log_index.search(**kwargs)

    # --- Distributed Tracing ---
    def trace_span(self, operation_name: str, span_kind: SpanKind = SpanKind.INTERNAL, attributes: Optional[Dict] = None):
        return self.tracer.trace(operation_name, span_kind=span_kind, attributes=attributes)

    def analyze_trace(self, trace_id: str) -> Optional[TraceAnalysisReport]:
        spans = self.tracer.get_spans_for_trace(trace_id)
        if spans:
            self.dependency_graph.ingest_spans(spans)
        return TraceTreeAnalyzer.analyze_trace(spans)

    # --- Alerts ---
    def evaluate_alert(self, rule_id: str, value: float, **kwargs: Any) -> Optional[AlertInstance]:
        alert = self.alert_evaluator.evaluate(rule_id=rule_id, current_value=value, **kwargs)
        if alert and alert.status.value == "FIRING":
            self.alert_dispatcher.dispatch(alert)
        return alert

    # --- SLOs ---
    def record_slo_events(self, slo_id: str, good_count: int, bad_count: int) -> ErrorBudgetStatus:
        self.error_budget_tracker.record_events(slo_id, good_count, bad_count)
        return self.error_budget_tracker.evaluate_budget(slo_id)

    # --- Diagnostics ---
    def run_root_cause_analysis(self, trace_id: Optional[str] = None) -> RCAReport:
        spans = self.tracer.get_spans_for_trace(trace_id) if trace_id else self.tracer.list_all_spans()
        logs = self.log_index.search(trace_id=trace_id) if trace_id else self.log_index.search(min_level=LogLevel.ERROR)
        return self.rca_analyzer.analyze_incident(report_id="rca-latest", spans=spans, logs=logs)

    def get_service_dependencies(self) -> List[DependencyEdge]:
        return self.dependency_graph.list_all_edges()
