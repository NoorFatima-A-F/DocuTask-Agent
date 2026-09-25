"""
Domain models for Enterprise Verification Reporting, Audit Intelligence & Governance Dashboards (PART 8).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List


class ReportType(str, Enum):
    VERIFICATION_REPORT = "VERIFICATION_REPORT"
    CERTIFICATION_REPORT = "CERTIFICATION_REPORT"
    SECURITY_ASSESSMENT_REPORT = "SECURITY_ASSESSMENT_REPORT"
    AI_EVALUATION_REPORT = "AI_EVALUATION_REPORT"
    SOC2_COMPLIANCE_REPORT = "SOC2_COMPLIANCE_REPORT"
    EXECUTIVE_SUMMARY_REPORT = "EXECUTIVE_SUMMARY_REPORT"


class ReportFormat(str, Enum):
    JSON = "JSON"
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    CSV = "CSV"


class UserRole(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    ENGINEER = "ENGINEER"
    AUDITOR = "AUDITOR"
    SECURITY_OFFICER = "SECURITY_OFFICER"


class NotificationEventType(str, Enum):
    CERTIFICATION_EXPIRING = "CERTIFICATION_EXPIRING"
    QUALITY_REGRESSION = "QUALITY_REGRESSION"
    SECURITY_FAILURE = "SECURITY_FAILURE"
    DEPLOYMENT_BLOCKED = "DEPLOYMENT_BLOCKED"
    AUDIT_PACKAGE_GENERATED = "AUDIT_PACKAGE_GENERATED"


class ControlStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass
class VerificationSummary:
    """Consolidated summary of a verification run for reporting."""
    execution_id: str
    system_version: str
    model_version: str
    environment: str
    timestamp: str
    overall_score: float
    certification_status: str
    risk_level: str
    total_tests: int
    failed_tests_count: int
    hallucination_rate: float
    p95_latency_ms: float
    critical_vulnerabilities: int


@dataclass
class QualityTrend:
    """Historical data point for a metric trend."""
    metric_name: str
    timestamp: str
    value: float
    baseline: float
    deviation_pct: float
    is_regression: bool = False


@dataclass
class ComplianceControlMapping:
    """Mapping of verification evidence to formal governance standards (NIST AI RMF, ISO 42001, SOC 2)."""
    control_id: str
    framework: str  # e.g. "NIST_AI_RMF", "ISO_42001", "SOC_2", "ISO_27001"
    control_name: str
    description: str
    evidence_references: List[str]
    status: ControlStatus
    last_verified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AuditReportRecord:
    """Formally compiled, hashed audit report."""
    report_id: str
    report_type: ReportType
    title: str
    scope: str
    generated_by: str
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_references: List[str] = field(default_factory=list)
    content: Dict[str, Any] = field(default_factory=dict)
    sha256_digest: str = ""
    generator_version: str = "v1.0.0"

    def compute_sha256(self) -> str:
        payload = f"{self.report_id}:{self.report_type.value}:{self.title}:{self.generated_at}:{json.dumps(self.content, sort_keys=True)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        return self.sha256_digest == self.compute_sha256()


@dataclass
class AuditPackage:
    """Complete multi-artifact audit package export."""
    package_id: str
    system_version: str
    generated_at: str
    reports: List[AuditReportRecord]
    evidence_manifest: List[str]
    metrics_snapshot: Dict[str, Any]
    certification_records: List[Dict[str, Any]]
    approval_history: List[Dict[str, Any]]
    package_checksum: str = ""


@dataclass
class NotificationAlert:
    """System notification dispatched to stakeholders."""
    alert_id: str
    event_type: NotificationEventType
    severity: str
    title: str
    message: str
    recipient_roles: List[UserRole]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    acknowledged: bool = False


# Dashboard Views
@dataclass
class ExecutiveDashboardView:
    """Executive-level bird's-eye governance view."""
    system_name: str = "DocuTask Agent"
    production_readiness_pct: float = 96.4
    current_certification_level: str = "LEVEL_7_ENTERPRISE_CERTIFIED"
    overall_quality_score: float = 95.8
    risk_summary: Dict[str, int] = field(default_factory=dict)
    deployment_health: Dict[str, Any] = field(default_factory=dict)
    historical_quality_trend: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EngineeringDashboardView:
    """Technical dashboard for software and ML engineers."""
    recent_runs: List[VerificationSummary]
    failed_test_breakdown: List[Dict[str, Any]]
    performance_p95_trend: List[Dict[str, Any]]
    ai_quality_metrics: Dict[str, float]
    code_coverage_pct: float = 92.4


@dataclass
class SecurityComplianceDashboardView:
    """Dashboard for security and compliance officers."""
    vulnerability_counts: Dict[str, int]
    prompt_injection_resistance_pct: float
    pii_leakage_rate_pct: float
    active_compliance_controls: List[ComplianceControlMapping]
    unresolved_security_findings: List[str]


@dataclass
class AiGovernanceDashboardView:
    """Specialized AI lifecycle and prompt governance dashboard."""
    active_model_version: str
    active_prompt_version: str
    hallucination_rate: float
    grounding_score: float
    model_comparisons: List[Dict[str, Any]]
    dataset_drift_summary: Dict[str, Any]
