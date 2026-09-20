"""Enterprise Observability, SRE Platform & Operational Intelligence System."""

# Core
from .core.context import (
    ObservabilityContext,
    get_current_context,
    set_current_context,
)
from .core.telemetry import (
    TelemetryType,
    TelemetryRecord,
    ITelemetryExporter,
    InMemoryTelemetryExporter,
    TelemetryPipeline,
)
from .core.events import (
    EventCategory,
    PlatformEvent,
    EventStream,
)

# Metrics
from .metrics.registry import (
    MetricType,
    Counter,
    Gauge,
    Histogram,
    MetricRegistry,
)
from .metrics.collector import (
    PlatformMetricsCollector,
)
from .metrics.aggregation import (
    AggregatedWindow,
    RollingAggregationEngine,
)

# Tracing
from .tracing.spans import (
    SpanStatus,
    SpanKind,
    SpanEvent,
    SpanContext,
    Span,
)
from .tracing.tracer import (
    SamplingStrategy,
    TracingEngine,
)
from .tracing.propagation import (
    TraceContextPropagator,
)

# Logging
from .logging.formatter import (
    JSONLogFormatter,
)
from .logging.storage import (
    LogEntry,
    LogStorageBackend,
)
from .logging.logger import (
    LogLevel,
    StructuredLogger,
)

# Events
from .events.processor import (
    EventProcessor,
)
from .events.analyzer import (
    OperationalInsight,
    EventAnalyzer,
)

# Dashboards
from .dashboards.widgets import (
    WidgetType,
    DashboardWidget,
)
from .dashboards.builder import (
    DashboardType,
    Dashboard,
    DashboardEngine,
)

# Alerts
from .alerts.rules import (
    AlertSeverity,
    RuleConditionType,
    AlertRule,
)
from .alerts.engine import (
    AlertState,
    ActiveAlert,
    AlertEngine,
)
from .alerts.notifications import (
    ChannelType,
    NotificationChannel,
    NotificationDispatchRecord,
    AlertRouter,
)

# SLO
from .slo.models import (
    SLIType,
    SLI,
    ServiceLevelObjective,
)
from .slo.calculator import (
    SLIComplianceResult,
    SLOCalculator,
)
from .slo.budgets import (
    BudgetStatus,
    ErrorBudgetSnapshot,
    ErrorBudgetEngine,
)

# Incidents & RCA
from .incidents.timeline import (
    TimelineEventType,
    TimelineEntry,
    IncidentTimeline,
)
from .incidents.manager import (
    IncidentSeverity,
    IncidentStatus,
    IncidentRecord,
    IncidentManager,
)
from .incidents.postmortem import (
    PreventativeAction,
    PostmortemReport,
    PostmortemGenerator,
)
from .incidents.rca import (
    CausalHop,
    RCACorrelationResult,
    RCAEngine,
)

# Profiling
from .profiling.profiler import (
    ProfileSample,
    ContinuousProfiler,
)
from .profiling.analyzer import (
    Hotspot,
    HotspotAnalyzer,
)

# Capacity & Cost
from .capacity.planner import (
    ResourceSaturationForecast,
    CapacityPlanner,
)
from .cost.analyzer import (
    CostBreakdown,
    CostAnalyzer,
)
from .cost.optimization import (
    RecommendationType,
    CostRecommendation,
    CostOptimizationEngine,
)

# Automation
from .automation.actions import (
    AutoActionType,
    AutomationExecutionResult,
    SREActionExecutor,
)
from .automation.framework import (
    SelfHealingRule,
    SREAutomationFramework,
)

# SDK & Decorators
from .sdk.client import (
    ObservabilitySDK,
)
from .sdk.decorators import (
    trace,
    metric_counter,
    profile,
    audit_log,
)

# API
from .api.routes import (
    observability_router,
    get_observability_sdk,
)

__all__ = [
    # Core
    "ObservabilityContext",
    "get_current_context",
    "set_current_context",
    "TelemetryType",
    "TelemetryRecord",
    "ITelemetryExporter",
    "InMemoryTelemetryExporter",
    "TelemetryPipeline",
    "EventCategory",
    "PlatformEvent",
    "EventStream",
    # Metrics
    "MetricType",
    "Counter",
    "Gauge",
    "Histogram",
    "MetricRegistry",
    "PlatformMetricsCollector",
    "AggregatedWindow",
    "RollingAggregationEngine",
    # Tracing
    "SpanStatus",
    "SpanKind",
    "SpanEvent",
    "SpanContext",
    "Span",
    "SamplingStrategy",
    "TracingEngine",
    "TraceContextPropagator",
    # Logging
    "JSONLogFormatter",
    "LogEntry",
    "LogStorageBackend",
    "LogLevel",
    "StructuredLogger",
    # Events
    "EventProcessor",
    "OperationalInsight",
    "EventAnalyzer",
    # Dashboards
    "WidgetType",
    "DashboardWidget",
    "DashboardType",
    "Dashboard",
    "DashboardEngine",
    # Alerts
    "AlertSeverity",
    "RuleConditionType",
    "AlertRule",
    "AlertState",
    "ActiveAlert",
    "AlertEngine",
    "ChannelType",
    "NotificationChannel",
    "NotificationDispatchRecord",
    "AlertRouter",
    # SLO
    "SLIType",
    "SLI",
    "ServiceLevelObjective",
    "SLIComplianceResult",
    "SLOCalculator",
    "BudgetStatus",
    "ErrorBudgetSnapshot",
    "ErrorBudgetEngine",
    # Incidents
    "TimelineEventType",
    "TimelineEntry",
    "IncidentTimeline",
    "IncidentSeverity",
    "IncidentStatus",
    "IncidentRecord",
    "IncidentManager",
    "PreventativeAction",
    "PostmortemReport",
    "PostmortemGenerator",
    "CausalHop",
    "RCACorrelationResult",
    "RCAEngine",
    # Profiling
    "ProfileSample",
    "ContinuousProfiler",
    "Hotspot",
    "HotspotAnalyzer",
    # Capacity & Cost
    "ResourceSaturationForecast",
    "CapacityPlanner",
    "CostBreakdown",
    "CostAnalyzer",
    "RecommendationType",
    "CostRecommendation",
    "CostOptimizationEngine",
    # Automation
    "AutoActionType",
    "AutomationExecutionResult",
    "SREActionExecutor",
    "SelfHealingRule",
    "SREAutomationFramework",
    # SDK
    "ObservabilitySDK",
    "trace",
    "metric_counter",
    "profile",
    "audit_log",
    # API
    "observability_router",
    "get_observability_sdk",
]
