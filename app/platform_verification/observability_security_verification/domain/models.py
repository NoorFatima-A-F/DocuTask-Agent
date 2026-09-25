"""
Phase 3H.4.10: Enterprise Observability Security Verification Framework - Domain Models
"""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class SecurityTier(str, Enum):
    ENTERPRISE_OBSERVABILITY_SECURITY_CERTIFIED = "Enterprise Observability Security Certified"
    PRODUCTION_SECURE = "Production Secure"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


class RBACRole(str, Enum):
    VIEWER = "Viewer"
    OPERATOR = "Operator"
    ENGINEER = "Engineer"
    ADMINISTRATOR = "Administrator"


class ClassificationAuditItem(BaseModel):
    field_name: str
    telemetry_type: str  # log, metric, trace, alert
    classification: DataClassification
    allowed_in_observability: bool
    sanitization_required: bool


class DataClassificationReport(BaseModel):
    total_fields_audited: int
    public_fields: int
    internal_fields: int
    confidential_fields: int
    restricted_fields: int
    items: List[ClassificationAuditItem] = Field(default_factory=list)
    classification_policy_passed: bool


class LogScanFinding(BaseModel):
    rule_id: str
    category: str  # credentials, pii, document_content
    pattern_matched: str
    sample_raw: str
    redacted_sample: str
    is_safe_after_sanitization: bool


class LogSecurityReport(BaseModel):
    scanned_log_sources: List[str] = Field(default_factory=list)
    total_log_entries_scanned: int
    raw_sensitive_occurrences: int
    sanitized_properly_count: int
    unmasked_leaks_count: int
    scanned_findings: List[LogScanFinding] = Field(default_factory=list)
    log_security_passed: bool


class SanitizationRule(BaseModel):
    rule_name: str
    target_pattern: str
    replacement_template: str
    active: bool


class LogSanitizationReport(BaseModel):
    active_sanitization_rules: List[SanitizationRule] = Field(default_factory=list)
    sample_tests_passed: int
    sample_tests_failed: int
    sanitization_verified: bool


class MetricLabelAudit(BaseModel):
    metric_name: str
    labels_inspected: List[str]
    contains_forbidden_labels: bool
    forbidden_labels_detected: List[str] = Field(default_factory=list)
    cardinality_safe: bool


class MetricSecurityReport(BaseModel):
    total_metrics_audited: int
    metrics_passed: int
    metrics_failed: int
    audits: List[MetricLabelAudit] = Field(default_factory=list)
    metric_privacy_passed: bool


class TraceAttributeAudit(BaseModel):
    span_name: str
    retained_attributes: List[str]
    scrubbed_attributes: List[str]
    no_auth_headers: bool
    no_raw_prompts: bool
    is_compliant: bool


class TraceSecurityReport(BaseModel):
    total_spans_inspected: int
    compliant_spans: int
    audits: List[TraceAttributeAudit] = Field(default_factory=list)
    trace_security_passed: bool


class RBACPermissionCheck(BaseModel):
    role: RBACRole
    action: str
    resource: str
    allowed: bool
    test_result_status: int  # 200 or 403
    enforced_correctly: bool


class DashboardAccessReport(BaseModel):
    roles_evaluated: List[str] = Field(default_factory=list)
    permission_checks: List[RBACPermissionCheck] = Field(default_factory=list)
    unauthorized_attempts_blocked: int
    rbac_enforcement_passed: bool


class AlertTemplateAudit(BaseModel):
    alert_name: str
    contains_pii: bool
    contains_document_content: bool
    contains_credentials: bool
    has_diagnostic_context: bool
    is_safe: bool


class AlertSecurityReport(BaseModel):
    total_alert_templates_audited: int
    safe_templates_count: int
    audits: List[AlertTemplateAudit] = Field(default_factory=list)
    alert_privacy_passed: bool


class PipelineSecurityReport(BaseModel):
    transport_encryption_tls13: bool
    telemetry_ingestion_auth_required: bool
    data_integrity_signing_active: bool
    log_retention_days: int
    trace_retention_days: int
    retention_lifecycle_enforced: bool
    storage_encryption_at_rest: bool
    pipeline_security_passed: bool


class AITelemetryAudit(BaseModel):
    workflow_stage: str
    retains_raw_prompt: bool
    retains_model_response: bool
    retains_agent_memory: bool
    retains_abstract_metadata: bool
    is_privacy_compliant: bool


class AISecurityReport(BaseModel):
    workflow_stages_audited: List[AITelemetryAudit] = Field(default_factory=list)
    zero_prompt_leakage_verified: bool
    zero_response_leakage_verified: bool
    ai_observability_safe: bool


class SecurityFailureSimulationResult(BaseModel):
    test_name: str
    injection_type: str
    payload_injected: str
    defense_mechanism: str
    blocked_or_redacted: bool
    result_status: str


class ObservabilitySecurityScorecard(BaseModel):
    data_classification_score: float = Field(..., ge=0.0, le=100.0)
    log_protection_score: float = Field(..., ge=0.0, le=100.0)
    metric_security_score: float = Field(..., ge=0.0, le=100.0)
    trace_security_score: float = Field(..., ge=0.0, le=100.0)
    access_control_score: float = Field(..., ge=0.0, le=100.0)
    pipeline_security_score: float = Field(..., ge=0.0, le=100.0)
    ai_telemetry_security_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: SecurityTier
    certified_enterprise_ready: bool
