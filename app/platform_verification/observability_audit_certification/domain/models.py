"""
Phase 3H.4.12: Enterprise Observability Evidence, Audit & Certification Framework - Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class CertificationTier(str, Enum):
    ENTERPRISE_CERTIFIED = "Enterprise Certified"
    PRODUCTION_READY = "Production Ready"
    OPERATIONALLY_READY = "Operationally Ready"
    CONDITIONALLY_READY = "Conditionally Ready"
    NEEDS_REMEDIATION = "Needs Remediation"
    FAILED = "Failed"


class CICDDecision(str, Enum):
    DEPLOY = "Deploy"
    DEPLOY_WITH_WARNING = "Deploy with Warning"
    MANUAL_APPROVAL_REQUIRED = "Manual Approval Required"
    DEPLOYMENT_BLOCKED = "Deployment Blocked"


class EvidenceCategory(str, Enum):
    HEALTH = "Health"
    METRICS = "Metrics"
    DASHBOARDS = "Dashboards"
    ALERTS = "Alerts"
    INCIDENTS = "Incidents"
    FAILURE_TESTS = "Failure_Tests"
    AUDIT = "Audit"
    SECURITY = "Security"


class EvidenceManifestItem(BaseModel):
    category: EvidenceCategory
    filename: str
    relative_path: str
    sha256_hash: str
    size_bytes: int
    generated_at: str
    source_phase: str
    is_valid: bool


class EvidenceCollectionArchitectureReport(BaseModel):
    architecture_name: str
    total_sources_covered: int
    source_categories: List[str]
    evidence_manifest_count: int
    is_fully_automated: bool
    manifests: List[EvidenceManifestItem] = Field(default_factory=list)


class FileIntegrityRecord(BaseModel):
    filename: str
    calculated_hash: str
    expected_hash: str
    matched: bool
    size_bytes: int


class EvidenceIntegrityReport(BaseModel):
    total_files_audited: int
    all_hashes_matched: bool
    generator_version: str
    git_commit: str
    build_id: str
    environment: str
    records: List[FileIntegrityRecord] = Field(default_factory=list)
    tamper_resistance_verified: bool


class AuditEvent(BaseModel):
    event_id: str
    timestamp: str
    actor: str
    component: str
    test_identifier: str
    result: str
    duration_ms: float
    environment: str
    version: str


class ObservabilityAuditTrailReport(BaseModel):
    audit_id: str
    total_events: int
    audit_events: List[AuditEvent] = Field(default_factory=list)
    audit_trail_immutable: bool
    generated_at: str


class PRRCategoryEvaluation(BaseModel):
    category_name: str
    checks_evaluated: int
    checks_passed: int
    score: float
    status: str
    findings: List[str] = Field(default_factory=list)


class ProductionReadinessReviewReport(BaseModel):
    review_id: str
    overall_prr_score: float
    prr_status: str
    categories: List[PRRCategoryEvaluation] = Field(default_factory=list)
    signoff_approved: bool
    reviewer_role: str = "Staff Observability & Production Readiness Reviewer"


class ComplianceCheckItem(BaseModel):
    rule_id: str
    standard_name: str
    requirement: str
    status: str
    evidence_ref: str


class ObservabilityComplianceReport(BaseModel):
    total_rules_evaluated: int
    compliant_rules_count: int
    compliance_percentage: float
    compliance_matrix: List[ComplianceCheckItem] = Field(default_factory=list)
    compliance_passed: bool


class CategoryScore(BaseModel):
    category: str
    weight: float
    score: float
    weighted_score: float


class ObservabilityCertificationReport(BaseModel):
    certification_tier: CertificationTier
    composite_score: float
    min_threshold_met: bool
    category_scores: List[CategoryScore] = Field(default_factory=list)
    certified: bool
    certification_id: str
    certified_at: str


class CICDGateReport(BaseModel):
    gate_decision: CICDDecision
    composite_score: float
    tier: CertificationTier
    hard_gates_passed: bool
    blocking_reasons: List[str] = Field(default_factory=list)
    pipeline_exit_code: int
    evaluated_at: str
