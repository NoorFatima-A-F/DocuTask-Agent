"""
Phase 3O: Enterprise Infrastructure Quality Scoring, Certification & Readiness Assessment — Domain Models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class CertificationLevel(str, Enum):
    ENTERPRISE_READY = "Enterprise Infrastructure Ready"  # Level 4: 95-100%
    PRODUCTION_READY = "Production Ready"                  # Level 3: 90-94.99%
    TESTING_READY = "Testing Ready"                        # Level 2: 80-89.99%
    DEVELOPMENT_READY = "Development Ready"                # Level 1: 60-79.99%
    BLOCKED = "Blocked / Not Production Ready"             # Critical Failure / <60%


class MaturityLevel(str, Enum):
    LEVEL_0 = "Level 0: No Verification"
    LEVEL_1 = "Level 1: Basic Deployment"
    LEVEL_2 = "Level 2: Automated Testing"
    LEVEL_3 = "Level 3: Observable Infrastructure"
    LEVEL_4 = "Level 4: Resilient Infrastructure"
    LEVEL_5 = "Level 5: Enterprise Autonomous Operations"


# ─── 1. Evidence Models ────────────────────────────────────────────────────────

class NormalizedEvidenceItem(BaseModel):
    category: str
    subcategory: str = ""
    test_id: str
    name: str
    status: VerificationStatus = VerificationStatus.PASSED
    score: float = 100.0
    severity: RiskLevel = RiskLevel.NONE
    weight: float = 1.0
    details: str = ""
    metrics: Dict[str, Any] = Field(default_factory=dict)


class RawEvidenceBundle(BaseModel):
    source_phase: str
    collected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_count: int = 0
    raw_payloads: List[Dict[str, Any]] = Field(default_factory=list)


# ─── 2. Quality Scoring Models ────────────────────────────────────────────────

class CategoryQualityScore(BaseModel):
    category: str
    weight: float
    score: float
    contribution: float
    passed_items: int
    total_items: int
    status: VerificationStatus = VerificationStatus.PASSED


class QualityScorecard(BaseModel):
    overall_score: float = 100.0
    grade: str = "PRODUCTION_READY"
    categories: Dict[str, CategoryQualityScore] = Field(default_factory=dict)
    total_evidence_evaluated: int = 0
    total_evidence_passed: int = 0
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_time_seconds: float = 0.0


# ─── 3. Risk Assessment Models ────────────────────────────────────────────────

class RiskFinding(BaseModel):
    risk_level: RiskLevel
    category: str
    title: str
    reason: str
    impact: str
    remediation: str
    is_blocker: bool = False


class RiskAssessmentReport(BaseModel):
    highest_risk: RiskLevel = RiskLevel.NONE
    total_risks: int = 0
    critical_risks_count: int = 0
    high_risks_count: int = 0
    medium_risks_count: int = 0
    low_risks_count: int = 0
    production_blocker_present: bool = False
    risks: List[RiskFinding] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─── 4. Certification & Decision Models ───────────────────────────────────────

class CertificationDecision(BaseModel):
    project: str = "DocuTask Agent"
    overall_score: float = 100.0
    certification: CertificationLevel = CertificationLevel.ENTERPRISE_READY
    status: VerificationStatus = VerificationStatus.PASSED
    deployment_approved: bool = True
    blocker_reasons: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    categories: Dict[str, float] = Field(default_factory=dict)
    risks_summary: Dict[str, int] = Field(default_factory=dict)
    issued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─── 5. Maturity Assessment Models ────────────────────────────────────────────

class MaturityAssessment(BaseModel):
    maturity_level: MaturityLevel = MaturityLevel.LEVEL_5
    maturity_score: float = 100.0
    pillar_ratings: Dict[str, str] = Field(default_factory=dict)
    capabilities_achieved: List[str] = Field(default_factory=list)
    next_level_requirements: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─── 6. Regression Models ─────────────────────────────────────────────────────

class RegressionFinding(BaseModel):
    category: str
    metric_name: str
    previous_score: float
    current_score: float
    delta: float
    is_regression: bool = False
    severity: RiskLevel = RiskLevel.NONE


class QualityRegressionReport(BaseModel):
    previous_version: str = "1.0.0"
    current_version: str = "3.17.0"
    previous_overall_score: float = 95.0
    current_overall_score: float = 100.0
    score_delta: float = 5.0
    regression_detected: bool = False
    findings: List[RegressionFinding] = Field(default_factory=list)
    analyzed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─── 7. Manifest Models ───────────────────────────────────────────────────────

class ManifestEntry(BaseModel):
    filename: str
    report_title: str
    sha256: str
    size_bytes: int


class VerificationManifest(BaseModel):
    project: str = "DocuTask-Agent"
    framework: str = "Enterprise Infrastructure Quality & Certification Framework"
    version: str = "3.17.0"
    commit: str = "HEAD"
    environment: str = "Enterprise Production Readiness Lab"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_score: float = 100.0
    certification: str = "Enterprise Infrastructure Ready"
    deployment_approved: bool = True
    files: List[ManifestEntry] = Field(default_factory=list)
