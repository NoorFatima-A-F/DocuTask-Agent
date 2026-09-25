"""
Domain models for Part 3E: Enterprise Observability & Reliability Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime, timezone


class ObservabilityCertificationTier(str, Enum):
    ENTERPRISE_OBSERVABILITY_READY = "ENTERPRISE_OBSERVABILITY_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    IMPROVEMENT_REQUIRED = "IMPROVEMENT_REQUIRED"
    FAILED = "FAILED"


ObservabilityCertificationTier.__test__ = False


class AlertSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class TelemetryCategory(str, Enum):
    LOG = "LOG"
    METRIC = "METRIC"
    TRACE = "TRACE"
    EVENT = "EVENT"
    ALERT = "ALERT"


class IncidentPhase(str, Enum):
    DETECTED = "DETECTED"
    ALERTED = "ALERTED"
    INVESTIGATING = "INVESTIGATING"
    RECOVERED = "RECOVERED"
    POSTMORTEM = "POSTMORTEM"


@dataclass
class ObservabilityArchitectureReport:
    total_services: int
    instrumented_services: int
    missing_instrumentation: List[str] = field(default_factory=list)
    coverage_score: float = 100.0
    status: str = "PASS"


@dataclass
class LoggingQualityReport:
    structured_json_compliant: bool
    required_fields_present: bool
    sensitive_data_leaks_detected: List[str] = field(default_factory=list)
    logging_quality_score: float = 100.0
    status: str = "PASS"


@dataclass
class MetricDefinition:
    name: str
    category: str
    unit: str
    is_golden_signal: bool = False
    is_ai_specific: bool = False


@dataclass
class MetricsInventoryReport:
    total_metrics_collected: int
    golden_signals_complete: bool
    ai_metrics_complete: bool
    missing_golden_signals: List[str] = field(default_factory=list)
    missing_ai_metrics: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class TraceSpanSummary:
    span_name: str
    service: str
    has_trace_id: bool
    has_span_id: bool
    has_parent_id: bool
    duration_ms: float


@dataclass
class DistributedTraceReport:
    total_spans: int
    unbroken_context_propagation: bool
    missing_context_spans: List[str] = field(default_factory=list)
    document_lifecycle_reconstructable: bool = True
    status: str = "PASS"


@dataclass
class AiWorkflowObservabilityReport:
    agent_executions_tracked: int
    tool_calls_instrumented: bool
    retrieval_chunks_logged: bool
    model_parameters_recorded: bool
    token_usage_attributed: bool
    status: str = "PASS"


@dataclass
class AlertRuleDefinition:
    name: str
    severity: AlertSeverity
    has_symptoms: bool
    has_probable_cause: bool
    has_remediation_link: bool


@dataclass
class AlertQualityReport:
    total_alert_rules: int
    actionable_alerts_count: int
    unactionable_alerts: List[str] = field(default_factory=list)
    alert_quality_score: float = 100.0
    status: str = "PASS"


@dataclass
class SloDefinition:
    name: str
    target_percentage: float
    actual_percentage: float
    error_budget_remaining_pct: float
    is_compliant: bool


@dataclass
class SloComplianceReport:
    total_slos: int
    compliant_slos_count: int
    failing_slos: List[str] = field(default_factory=list)
    slo_compliance_score: float = 100.0
    status: str = "PASS"


@dataclass
class IncidentSimulationResult:
    incident_name: str
    phase: IncidentPhase
    mttd_seconds: float
    mttr_seconds: float
    recovery_successful: bool


@dataclass
class IncidentResponseReport:
    simulated_incidents: int
    average_mttd_seconds: float
    average_mttr_seconds: float
    recovery_success_rate: float
    status: str = "PASS"


@dataclass
class DashboardValidationReport:
    dashboards_validated: List[str] = field(default_factory=list)
    all_panels_functional: bool = True
    status: str = "PASS"


@dataclass
class ReliabilityEngineeringMetricsReport:
    availability_pct: float = 99.95
    mtbf_hours: float = 720.0
    mttr_minutes: float = 4.2
    failure_rate_pct: float = 0.05
    recovery_success_rate: float = 100.0


@dataclass
class ObservabilityCertificationReport:
    logging_quality_score: float
    metrics_coverage_score: float
    distributed_tracing_score: float
    alerting_score: float
    slo_management_score: float
    incident_response_score: float
    composite_score: float
    tier: ObservabilityCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ObservabilityVerificationEvidencePackage:
    package_id: str
    commit_sha: str
    scorecard: ObservabilityCertificationReport
    architecture_report: ObservabilityArchitectureReport
    logging_report: LoggingQualityReport
    metrics_report: MetricsInventoryReport
    tracing_report: DistributedTraceReport
    ai_workflow_report: AiWorkflowObservabilityReport
    alert_report: AlertQualityReport
    slo_report: SloComplianceReport
    incident_report: IncidentResponseReport
    dashboard_report: DashboardValidationReport
    reliability_metrics_report: ReliabilityEngineeringMetricsReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
