"""Unified Observability & SRE Platform SDK Client."""

from __future__ import annotations


from ..core.context import get_current_context
from ..core.events import EventCategory, EventStream, PlatformEvent
from ..core.telemetry import InMemoryTelemetryExporter, TelemetryPipeline
from ..metrics.aggregation import RollingAggregationEngine
from ..metrics.collector import PlatformMetricsCollector
from ..metrics.registry import MetricRegistry
from ..tracing.propagation import TraceContextPropagator
from ..tracing.tracer import TracingEngine
from ..logging.logger import StructuredLogger
from ..logging.storage import LogStorageBackend
from ..events.analyzer import EventAnalyzer
from ..events.processor import EventProcessor
from ..dashboards.builder import DashboardEngine
from ..alerts.engine import AlertEngine
from ..alerts.notifications import AlertRouter
from ..slo.budgets import ErrorBudgetEngine
from ..slo.calculator import SLOCalculator
from ..incidents.manager import IncidentManager
from ..incidents.postmortem import PostmortemGenerator
from ..incidents.rca import RCAEngine
from ..profiling.analyzer import HotspotAnalyzer
from ..profiling.profiler import ContinuousProfiler
from ..capacity.planner import CapacityPlanner
from ..cost.analyzer import CostAnalyzer
from ..cost.optimization import CostOptimizationEngine
from ..automation.framework import SREAutomationFramework


class ObservabilitySDK:
    """Unified developer and SRE interface for platform-wide operational intelligence."""

    def __init__(self, service_name: str = "docutask-app", environment: str = "production"):
        self.service_name = service_name
        self.environment = environment

        # Telemetry Core
        self.pipeline = TelemetryPipeline()
        self.in_memory_exporter = InMemoryTelemetryExporter()
        self.pipeline.add_exporter(self.in_memory_exporter)

        # Metrics
        self.metric_registry = MetricRegistry()
        self.metrics_collector = PlatformMetricsCollector(registry=self.metric_registry)
        self.aggregation_engine = RollingAggregationEngine()

        # Tracing
        self.tracer = TracingEngine(service_name=self.service_name)
        self.propagator = TraceContextPropagator()

        # Logging
        self.log_storage = LogStorageBackend()
        self.logger = StructuredLogger(service_name=self.service_name, storage=self.log_storage)

        # Events
        self.event_stream = EventStream()
        self.event_processor = EventProcessor(event_stream=self.event_stream)
        self.event_analyzer = EventAnalyzer(event_stream=self.event_stream)

        # Dashboards
        self.dashboard_engine = DashboardEngine(metric_registry=self.metric_registry)

        # Alerts & Notifications
        self.alert_engine = AlertEngine(metric_registry=self.metric_registry)
        self.alert_router = AlertRouter()
        self.alert_engine.on_fire(self.alert_router.dispatch)

        # SLOs
        self.slo_calculator = SLOCalculator()
        self.error_budget_engine = ErrorBudgetEngine()

        # Incidents & RCA
        self.incident_manager = IncidentManager()
        self.postmortem_generator = PostmortemGenerator()
        self.rca_engine = RCAEngine()

        # Profiling
        self.profiler = ContinuousProfiler()
        self.hotspot_analyzer = HotspotAnalyzer(profiler=self.profiler)

        # Capacity & Cost
        self.capacity_planner = CapacityPlanner()
        self.cost_analyzer = CostAnalyzer()
        self.cost_optimization = CostOptimizationEngine()

        # SRE Automation & Self-Healing
        self.automation = SREAutomationFramework()
        self.alert_engine.on_fire(self.automation.handle_alert)

    def record_heartbeat(self, node_id: str, healthy: bool = True) -> None:
        """Convenience method to emit heartbeat telemetry."""
        ctx = get_current_context()
        ctx.node_id = node_id
        self.metrics_collector.record_infrastructure(
            node_id=node_id,
            cpu_usage_pct=25.0,
            memory_usage_pct=40.0,
            disk_usage_pct=30.0,
            healthy=healthy,
        )
        self.event_processor.process(
            PlatformEvent(
                name="platform.node.heartbeat",
                category=EventCategory.INFRASTRUCTURE,
                source=self.service_name,
                payload={"node_id": node_id, "healthy": healthy},
            )
        )
