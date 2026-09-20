"""Domain Models for Phase 3H.3.9: AI Health Monitoring Integration Verification."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AIMetricCategory(str, Enum):
    AVAILABILITY = "AVAILABILITY"
    PERFORMANCE = "PERFORMANCE"
    RELIABILITY = "RELIABILITY"
    QUALITY = "QUALITY"
    COST = "COST"


class AIObservabilityTier(str, Enum):
    FAILED = "Failed"                                                 # < 80%
    IMPROVEMENT_REQUIRED = "Improvement Required"                     # 80 - 89%
    PRODUCTION_AI_MONITORING_READY = "Production AI Monitoring Ready" # 90 - 94%
    ENTERPRISE_AI_OBSERVABILITY_READY = "Enterprise AI Observability Ready"  # 95 - 100%


@dataclass
class TelemetryPipelineStatus:
    pipeline_name: str
    collector_type: str
    storage_backend: str
    connected: bool
    data_delivery_latency_ms: float
    freshness_seconds: float
    status: str


@dataclass
class AIObservabilityArchitectureReport:
    metrics_pipeline: str
    logs_pipeline: str
    tracing_pipeline: str
    pipelines: List[TelemetryPipelineStatus]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIMetricDefinition:
    metric_name: str
    category: AIMetricCategory
    metric_type: str  # Gauge / Counter / Histogram
    description: str
    labels: List[str]
    current_value: float
    unit: str
    collected_successfully: bool


@dataclass
class AIMetricsReport:
    total_metrics_collected: int
    metrics_by_category: Dict[str, int]
    metrics: List[AIMetricDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIDashboardPanel:
    panel_id: str
    title: str
    promql_or_query: str
    visualization_type: str
    operational_question_answered: str


@dataclass
class AIDashboardDefinition:
    dashboard_id: str
    title: str
    category: str
    panel_count: int
    panels: List[AIDashboardPanel]
    verified: bool


@dataclass
class AIDashboardReport:
    total_dashboards_verified: int
    dashboards: List[AIDashboardDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AILogEventDefinition:
    event_type: str  # REQUEST / RESPONSE / FAILURE
    required_fields: List[str]
    json_structured: bool
    sensitive_data_redacted: bool
    sample_entry: Dict[str, Any]


@dataclass
class AILoggingReport:
    total_event_types_verified: int
    all_json_structured: bool
    all_sanitized: bool
    events: List[AILogEventDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AITraceSpanItem:
    span_name: str
    service_name: str
    avg_duration_ms: float
    is_bottleneck: bool
    status_code: str


@dataclass
class AITracingReport:
    trace_id: str
    total_spans_in_workflow: int
    total_workflow_duration_ms: float
    ai_inference_duration_ms: float
    ai_latency_percentage: float
    bottleneck_identified: str
    spans: List[AITraceSpanItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIAlertRuleDefinition:
    alert_name: str
    condition_expr: str
    duration_threshold: str
    severity: str
    prescribed_action: str
    notification_channels: List[str]
    rule_active: bool


@dataclass
class AIAlertingReport:
    total_alert_rules: int
    rules: List[AIAlertRuleDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AISLOTarget:
    slo_name: str
    target_threshold: str
    target_pct: float
    current_attainment_pct: float
    compliant: bool
    measurement_window: str


@dataclass
class AISLOReport:
    total_slos_tracked: int
    all_slos_met: bool
    slos: List[AISLOTarget]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIIncidentTestItem:
    scenario_id: str
    incident_type: str
    injected_anomaly: str
    alert_triggered: bool
    dashboard_updated: bool
    automated_response_executed: bool
    recovery_validated: bool
    passed: bool


@dataclass
class AIIncidentTestReport:
    total_incident_tests: int
    all_incidents_detected_and_handled: bool
    tests: List[AIIncidentTestItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIAutomatedResponseItem:
    trigger_signal: str
    automated_action: str
    latency_to_action_ms: float
    false_positive_rate_pct: float
    audit_logged: bool
    passed: bool


@dataclass
class AIAutomatedResponseReport:
    total_automation_rules: int
    all_rules_verified: bool
    rules: List[AIAutomatedResponseItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIMonitoringSecurityCheck:
    check_id: str
    name: str
    rbac_enforced: bool
    encryption_at_rest_in_transit: bool
    pii_scrubbed_in_telemetry: bool
    passed: bool
    details: str


@dataclass
class AIMonitoringSecurityReport:
    total_checks: int
    sensitive_data_exposed: bool
    checks: List[AIMonitoringSecurityCheck]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIObservabilityScorecard:
    telemetry_completeness_score: float  # Weight 20%
    metrics_coverage_score: float        # Weight 20%
    dashboard_quality_score: float       # Weight 15%
    logging_quality_score: float         # Weight 15%
    alert_reliability_score: float       # Weight 15%
    security_score: float                # Weight 15%
    overall_score: float                 # Composite 0 - 100
    certification_tier: AIObservabilityTier
    certification_verdict: str           # CERTIFIED / CONDITIONAL_APPROVAL / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
