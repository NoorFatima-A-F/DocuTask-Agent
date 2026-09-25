"""
Phase 3H.5.10: Enterprise Health Security, Privacy & Information Exposure Verification — Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class SecurityTier(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    ADMIN_DIAGNOSTIC = "ADMIN_DIAGNOSTIC"


class EndpointAccessLevel(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    OPERATOR_BEARER = "OPERATOR_BEARER"
    ADMIN_MUTUAL_TLS = "ADMIN_MUTUAL_TLS"


class RedactionState(str, Enum):
    FULLY_REDACTED = "FULLY_REDACTED"
    MASKED = "MASKED"
    HASHED = "HASHED"
    UNREDACTED_VIOLATION = "UNREDACTED_VIOLATION"


class ComplianceFramework(str, Enum):
    OWASP_ASVS = "OWASP_ASVS_V4"
    OWASP_API_SECURITY = "OWASP_API_TOP_10"
    SOC2_TYPE2 = "SOC2_TYPE_II"
    GDPR_PRIVACY = "GDPR_ART_25_32"
    HIPAA_SECURITY = "HIPAA_SECURITY_RULE"


class HealthSecurityCertificationTier(str, Enum):
    SECURE_OBSERVABILITY_READY = "Secure Observability Ready"
    ENTERPRISE_HEALTH_HARDENED = "Enterprise Health Hardened"
    SECURITY_REVIEW_REQUIRED = "Security Review Required"
    HEALTH_SECURITY_NON_COMPLIANT = "Health Security Non-Compliant"


# ─── 3H.5.10.1: Health Endpoint Security & Information Exposure ─────────────

class EndpointAuditItem(BaseModel):
    endpoint_path: str
    access_tier: SecurityTier
    status_code: int
    leaks_internal_ip: bool = False
    leaks_database_credentials: bool = False
    leaks_software_versions: bool = False
    leaks_stack_traces: bool = False
    leaks_hostnames: bool = False
    sanitized_response: Dict[str, Any] = Field(default_factory=dict)
    is_secure: bool = True
    audit_notes: str = ""


class EndpointSecurityReport(BaseModel):
    report_title: str = "Health Endpoint Security & Information Exposure Report"
    total_endpoints_audited: int = 0
    secure_endpoints_count: int = 0
    insecure_endpoints_count: int = 0
    audited_endpoints: List[EndpointAuditItem] = Field(default_factory=list)
    information_exposure_prevented: bool = True
    public_tier_sanitized: bool = True
    internal_tier_controlled: bool = True


# ─── 3H.5.10.2: Health Access Control & RBAC Verification ───────────────────

class AuthTestItem(BaseModel):
    endpoint_path: str
    required_role: str
    presented_credentials: Optional[str] = None
    expected_status: int
    actual_status: int
    access_granted: bool
    rbac_policy_enforced: bool = True


class HealthAuthorizationReport(BaseModel):
    report_title: str = "Health Endpoint Access Control & RBAC Verification Report"
    total_auth_tests: int = 0
    passed_auth_tests: int = 0
    failed_auth_tests: int = 0
    auth_test_matrix: List[AuthTestItem] = Field(default_factory=list)
    rbac_enforcement_active: bool = True
    anonymous_admin_blocked: bool = True
    token_validation_active: bool = True


# ─── 3H.5.10.3: Metrics Privacy & Label Sanitization ────────────────────────

class MetricLabelAuditItem(BaseModel):
    metric_name: str
    labels_inspected: List[str] = Field(default_factory=list)
    cardinality_safe: bool = True
    contains_pii: bool = False
    contains_user_identifiers: bool = False
    contains_document_content: bool = False
    is_compliant: bool = True
    violations: List[str] = Field(default_factory=list)


class MetricsPrivacyReport(BaseModel):
    report_title: str = "Metrics Privacy & Label Sanitization Report"
    total_metrics_audited: int = 0
    compliant_metrics_count: int = 0
    violations_count: int = 0
    metric_audits: List[MetricLabelAuditItem] = Field(default_factory=list)
    high_cardinality_mitigation_active: bool = True
    pii_free_telemetry_guaranteed: bool = True


# ─── 3H.5.10.4: Operational Log Sanitization Verification ────────────────────

class LogSanitizationItem(BaseModel):
    log_sample_id: str
    category: str  # db_error, auth_failure, health_probe, llm_inference
    raw_snippet: str
    sanitized_snippet: str
    redaction_state: RedactionState
    redacted_patterns: List[str] = Field(default_factory=list)
    clean: bool = True


class LogSecurityReport(BaseModel):
    report_title: str = "Operational Log Sanitization & PII Protection Report"
    total_log_streams_audited: int = 0
    sanitized_streams_count: int = 0
    violations_detected: int = 0
    log_samples: List[LogSanitizationItem] = Field(default_factory=list)
    zero_secret_leakage_in_logs: bool = True
    automated_masking_verified: bool = True


# ─── 3H.5.10.5: Alert Notification Sanitization & Channel Security ───────────

class AlertChannelAuditItem(BaseModel):
    channel_name: str  # Slack, PagerDuty, Webhook, Email
    encryption_in_transit: str = "TLS_1_3"
    payload_sanitized: bool = True
    contains_runbook_link: bool = True
    contains_sensitive_data: bool = False
    sample_alert_title: str = ""
    sanitized_alert_body: str = ""


class AlertSecurityReport(BaseModel):
    report_title: str = "Alert Notification Sanitization & Channel Security Report"
    total_channels_audited: int = 0
    secure_channels_count: int = 0
    channel_audits: List[AlertChannelAuditItem] = Field(default_factory=list)
    alert_payload_privacy_enforced: bool = True
    runbook_safe_references_only: bool = True


# ─── 3H.5.10.6: Distributed Tracing Privacy & Payload Protection ────────────

class TraceSpanAuditItem(BaseModel):
    span_name: str
    service_name: str
    attributes_inspected: List[str] = Field(default_factory=list)
    contains_raw_prompts: bool = False
    contains_bearer_tokens: bool = False
    user_id_hashed: bool = True
    trace_safe: bool = True


class TraceSecurityReport(BaseModel):
    report_title: str = "Distributed Tracing Privacy & Payload Protection Report"
    total_spans_audited: int = 0
    secure_spans_count: int = 0
    span_audits: List[TraceSpanAuditItem] = Field(default_factory=list)
    trace_payload_masking_active: bool = True
    telemetry_header_sanitization_valid: bool = True


# ─── 3H.5.10.7: Secret Exposure Scanning Across Health & Observability ───────

class SecretScanFinding(BaseModel):
    surface: str  # health_api, prometheus_metrics, system_logs, alert_stream, otel_traces
    detector_pattern: str  # API_KEY, JWT_SECRET, DB_PASSWORD, CLOUD_CREDS
    occurrences_found: int = 0
    status: str = "CLEAN"  # CLEAN or EXPOSURE_DETECTED
    entropy_score: float = 0.0
    passed: bool = True


class SecretScanReport(BaseModel):
    report_title: str = "Secret Exposure Scan & Telemetry Leakage Report"
    surfaces_scanned: int = 0
    scanned_surfaces: List[str] = Field(default_factory=list)
    total_scans_performed: int = 0
    findings: List[SecretScanFinding] = Field(default_factory=list)
    zero_secrets_exposed: bool = True
    entropy_analysis_clean: bool = True


# ─── 3H.5.10.8: Operational Dashboard & Telemetry Storage Security ───────────

class DashboardSecurityItem(BaseModel):
    component: str  # Grafana, Prometheus_TSDB, OpenSearch_Logs, Jaeger_Traces
    rbac_enabled: bool = True
    anonymous_access_disabled: bool = True
    tls_enforced: bool = True
    retention_days: int = 30
    audit_logging_active: bool = True
    is_hardened: bool = True


class DashboardSecurityReport(BaseModel):
    report_title: str = "Operational Dashboard & Telemetry Storage Security Report"
    total_components_audited: int = 0
    hardened_components_count: int = 0
    components: List[DashboardSecurityItem] = Field(default_factory=list)
    dashboard_rbac_enforced: bool = True
    storage_encryption_at_rest: bool = True


# ─── 3H.5.10.9: Security Failure Injection & Resilience Testing ──────────────

class SecurityInjectionScenario(BaseModel):
    scenario_id: str
    name: str
    attack_vector: str
    injected_payload: str
    expected_defense: str
    actual_outcome: str
    neutralized: bool = True
    mitigation_latency_ms: float = 0.0


class SecurityFailureInjectionReport(BaseModel):
    report_title: str = "Health Security Failure Injection & Resilience Report"
    total_injection_scenarios: int = 0
    neutralized_scenarios_count: int = 0
    scenarios: List[SecurityInjectionScenario] = Field(default_factory=list)
    all_attacks_neutralized: bool = True
    fail_secure_verified: bool = True


# ─── 3H.5.10.10: Compliance & Standards Certification ────────────────────────

class ComplianceCheckItem(BaseModel):
    framework: ComplianceFramework
    control_id: str
    control_title: str
    verification_status: str  # PASS, FAIL
    evidence_reference: str
    score: float = 100.0


class ComplianceSecurityReport(BaseModel):
    report_title: str = "Health Security Compliance & Enterprise Standards Report"
    frameworks_evaluated: List[str] = Field(default_factory=list)
    total_controls: int = 0
    passed_controls: int = 0
    compliance_percentage: float = 100.0
    controls: List[ComplianceCheckItem] = Field(default_factory=list)
    owasp_asvs_compliant: bool = True
    owasp_api_security_compliant: bool = True
    soc2_cc6_compliant: bool = True
    gdpr_art25_compliant: bool = True


# ─── Master Scorecard & Certification ────────────────────────────────────────

class HealthSecurityCategoryScore(BaseModel):
    category_name: str
    weight_percentage: float
    raw_score: float
    weighted_score: float
    status: str
    details: str = ""


class HealthSecurityScorecard(BaseModel):
    verification_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_health_security_score: float = 0.0
    certification_tier: HealthSecurityCertificationTier = HealthSecurityCertificationTier.HEALTH_SECURITY_NON_COMPLIANT
    passed: bool = False
    category_scores: List[HealthSecurityCategoryScore] = Field(default_factory=list)
    total_audits_performed: int = 0
    zero_critical_vulnerabilities: bool = True
