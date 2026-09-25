"""Domain Models for Phase 3H.3.5: Enterprise Health Monitoring Integration Verification Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ObservabilityTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    PRODUCTION_MONITORING_READY = "Production Monitoring Ready"  # 90 - 94
    ENTERPRISE_OBSERVABILITY_READY = "Enterprise Observability Ready"  # 95 - 100


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ServiceCategory(str, Enum):
    API = "api"
    AGENT_RUNTIME = "agent_runtime"
    WORKER = "worker"
    DATABASE = "database"
    QUEUE = "queue"
    STORAGE = "storage"
    OCR = "ocr"
    AI_PROVIDER = "ai_provider"


@dataclass
class ServiceInstrumentation:
    service_name: str
    category: ServiceCategory
    metrics_enabled: bool
    tracing_enabled: bool
    logging_structured: bool
    health_endpoint: str
    owner_team: str


@dataclass
class ObservabilityArchitectureReport:
    services_instrumented: int
    total_expected_services: int
    metrics_pipeline_active: bool
    tracing_pipeline_active: bool
    logging_pipeline_active: bool
    services: List[ServiceInstrumentation]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricDefinition:
    name: str
    service: str
    category: str
    metric_type: str  # counter, gauge, histogram, summary
    unit: str
    description: str
    sample_value: float


@dataclass
class HealthMetricsInventoryReport:
    total_metrics_cataloged: int
    categories_covered: List[str]
    services_covered: List[str]
    metrics: List[MetricDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PrometheusScrapeTarget:
    job_name: str
    endpoint: str
    scrape_interval: str
    scrape_timeout: str
    status: str  # UP / DOWN
    last_scrape_duration_ms: float
    metrics_count: int


@dataclass
class PrometheusVerificationReport:
    endpoint_exposed: bool
    scrape_successful: bool
    historical_query_supported: bool
    target_down_detection_verified: bool
    targets: List[PrometheusScrapeTarget]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GrafanaPanel:
    title: str
    panel_type: str  # timeseries, stat, gauge, table, heatmap
    promql_query: str
    thresholds: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class GrafanaDashboard:
    uid: str
    title: str
    category: str
    refresh_rate: str
    panels: List[GrafanaPanel]
    valid: bool


@dataclass
class GrafanaDashboardReport:
    total_dashboards: int
    dashboards_validated: List[GrafanaDashboard]
    dashboard_names: List[str]
    outage_tested: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertRule:
    alert_name: str
    service: str
    severity: AlertSeverity
    condition: str
    for_duration: str
    description: str
    owner: str
    runbook_url: str
    recovery_action: str


@dataclass
class AlertConfigurationReport:
    total_rules_configured: int
    critical_rules_count: int
    warning_rules_count: int
    rules: List[AlertRule]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertQualityMetrics:
    precision: float
    recall: float
    false_positive_rate: float
    false_negative_rate: float
    avg_detection_time_seconds: float
    noisy_alerts_detected: int
    duplicate_alerts_detected: int


@dataclass
class AlertQualityReport:
    metrics: AlertQualityMetrics
    benchmarks_met: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CorrelatedEvent:
    timestamp: str
    event_type: str  # metric_spike, error_log, trace_span, alert_fired
    source: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentDiagnosis:
    incident_id: str
    failure_timestamp: str
    root_cause: str
    affected_document_ids: List[str]
    failed_dependencies: List[str]
    recovery_action_executed: str
    recovery_verified: bool


@dataclass
class IncidentVisibilityReport:
    incident_id: str
    trace_id: str
    document_id: str
    correlated_events: List[CorrelatedEvent]
    diagnosis: IncidentDiagnosis
    correlation_complete: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationScenarioResult:
    scenario_id: str
    name: str
    target_service: str
    injected_failure: str
    detected: bool
    alert_fired: bool
    detection_time_seconds: float
    alert_time_seconds: float
    recovery_time_seconds: float
    passed: bool


@dataclass
class FailureSimulationReport:
    total_scenarios_run: int
    passed_scenarios: int
    scenarios: List[SimulationScenarioResult]
    avg_detection_time_seconds: float
    avg_alert_time_seconds: float
    avg_recovery_time_seconds: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceSpan:
    span_id: str
    parent_span_id: Optional[str]
    name: str
    service: str
    duration_ms: float
    status_code: str  # OK / ERROR
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DistributedTrace:
    trace_id: str
    root_span_name: str
    total_spans: int
    spans: List[TraceSpan]
    context_propagated: bool
    missing_spans_count: int


@dataclass
class TracingVerificationReport:
    trace: DistributedTrace
    propagation_verified: bool
    correlation_ids_valid: bool
    span_accuracy_pct: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityAuditItem:
    check_name: str
    category: str
    exposed_sensitive_data: bool
    redaction_active: bool
    passed: bool
    sample_safe_output: str


@dataclass
class MonitoringSecurityReport:
    total_security_checks: int
    secrets_leaked: bool
    redaction_verified: bool
    auth_enforced: bool
    checks: List[SecurityAuditItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringQualityScorecard:
    metric_coverage_score: float       # Weight 20%
    alert_accuracy_score: float        # Weight 20%
    dashboard_quality_score: float     # Weight 15%
    trace_visibility_score: float      # Weight 15%
    incident_diagnosis_score: float    # Weight 15%
    security_score: float              # Weight 15%
    overall_score: float               # Composite 0 - 100
    certification_tier: ObservabilityTier
    certification_verdict: str         # CERTIFIED / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
