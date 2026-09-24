"""
Domain models for Enterprise Verification Quality Gate, Risk Evaluation & Certification Engine (PART 6).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional, Union


class GateCategory(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    RELIABILITY = "RELIABILITY"
    SECURITY = "SECURITY"
    AI_QUALITY = "AI_QUALITY"
    COMPLIANCE = "COMPLIANCE"


class GateComparisonOperator(str, Enum):
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    EQUALS = "=="
    NOT_EQUALS = "!="
    IN = "in"
    BETWEEN = "between"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class FailureAction(str, Enum):
    BLOCK_RELEASE = "BLOCK_RELEASE"
    REQUIRE_MANUAL_APPROVAL = "REQUIRE_MANUAL_APPROVAL"
    ALLOW_WITH_WARNING = "ALLOW_WITH_WARNING"
    QUARANTINE = "QUARANTINE"


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"   # Auto-reject
    HIGH = "HIGH"           # Manual approval required
    MEDIUM = "MEDIUM"       # Conditional approval allowed
    LOW = "LOW"             # Allow release


class ReleaseDecisionType(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CONDITIONAL_APPROVAL = "CONDITIONAL_APPROVAL"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    EXPIRED = "EXPIRED"


class CertificationLevel(str, Enum):
    LEVEL_0_NOT_CERTIFIED = "LEVEL_0_NOT_CERTIFIED"
    LEVEL_1_DEVELOPMENT_VERIFIED = "LEVEL_1_DEVELOPMENT_VERIFIED"
    LEVEL_2_COMPONENT_CERTIFIED = "LEVEL_2_COMPONENT_CERTIFIED"
    LEVEL_3_INTEGRATION_CERTIFIED = "LEVEL_3_INTEGRATION_CERTIFIED"
    LEVEL_4_SYSTEM_CERTIFIED = "LEVEL_4_SYSTEM_CERTIFIED"
    LEVEL_5_PRODUCTION_CERTIFIED = "LEVEL_5_PRODUCTION_CERTIFIED"
    LEVEL_6_ADVERSARIAL_CERTIFIED = "LEVEL_6_ADVERSARIAL_CERTIFIED"
    LEVEL_7_ENTERPRISE_CERTIFIED = "LEVEL_7_ENTERPRISE_CERTIFIED"


class CertificationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PROVISIONAL = "PROVISIONAL"
    SUSPENDED = "SUSPENDED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class ApprovalAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    ADD_COMMENT = "ADD_COMMENT"


class ExceptionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class ChangeType(str, Enum):
    CODE = "CODE"
    PROMPT = "PROMPT"
    MODEL = "MODEL"
    DATASET = "DATASET"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    POLICY = "POLICY"


@dataclass(frozen=True)
class QualityGateCondition:
    """A single conditional check on a metric."""
    metric_name: str
    operator: GateComparisonOperator
    threshold: Union[float, int, str, List[Any]]
    tolerance: float = 0.0
    description: str = ""

    def evaluate(self, actual_value: Any) -> bool:
        if actual_value is None:
            return False
        try:
            if self.operator == GateComparisonOperator.LESS_THAN:
                return float(actual_value) < float(self.threshold) + self.tolerance
            elif self.operator == GateComparisonOperator.LESS_THAN_OR_EQUAL:
                return float(actual_value) <= float(self.threshold) + self.tolerance
            elif self.operator == GateComparisonOperator.GREATER_THAN:
                return float(actual_value) > float(self.threshold) - self.tolerance
            elif self.operator == GateComparisonOperator.GREATER_THAN_OR_EQUAL:
                return float(actual_value) >= float(self.threshold) - self.tolerance
            elif self.operator == GateComparisonOperator.EQUALS:
                return actual_value == self.threshold
            elif self.operator == GateComparisonOperator.NOT_EQUALS:
                return actual_value != self.threshold
            elif self.operator == GateComparisonOperator.IN:
                return actual_value in self.threshold if isinstance(self.threshold, (list, set, tuple)) else False
            elif self.operator == GateComparisonOperator.BETWEEN:
                if isinstance(self.threshold, (list, tuple)) and len(self.threshold) == 2:
                    return self.threshold[0] <= float(actual_value) <= self.threshold[1]
                return False
        except (ValueError, TypeError):
            return False
        return False


@dataclass
class QualityGateDefinition:
    """Configurable quality gate specification."""
    id: str
    name: str
    category: GateCategory
    conditions: List[QualityGateCondition]
    failure_action: FailureAction = FailureAction.BLOCK_RELEASE
    approval_required: bool = False
    severity: Severity = Severity.HIGH
    description: str = ""


@dataclass
class PolicyRule:
    """Atomic policy condition."""
    name: str
    metric_name: str
    operator: GateComparisonOperator
    threshold: Union[float, int, str, List[Any]]
    severity: Severity = Severity.HIGH
    is_blocking: bool = True
    description: str = ""


@dataclass
class PolicyDefinition:
    """Group of rules evaluated under logical operators (AND/OR)."""
    id: str
    name: str
    rules: List[PolicyRule]
    logical_operator: str = "AND"  # "AND" | "OR"
    description: str = ""


@dataclass
class RiskAssessment:
    """Calculated risk assessment using Probability * Impact * Exposure."""
    risk_id: str
    system_id: str
    probability: int  # 1 (Rare) to 5 (Almost Certain)
    impact: int       # 1 (Negligible) to 5 (Catastrophic)
    exposure: int     # 1 (Isolated) to 5 (Full Production)
    risk_score: int = 0
    risk_level: RiskLevel = RiskLevel.LOW
    identified_risks: List[str] = field(default_factory=list)
    mitigating_controls: List[str] = field(default_factory=list)
    automatic_action: str = "ALLOW"

    def __post_init__(self):
        if self.risk_score == 0:
            self.risk_score = self.probability * self.impact * self.exposure
        
        # Risk Score range: 1 to 125
        if self.risk_score >= 60:
            self.risk_level = RiskLevel.CRITICAL
            self.automatic_action = "AUTO_REJECT"
        elif self.risk_score >= 30:
            self.risk_level = RiskLevel.HIGH
            self.automatic_action = "MANUAL_APPROVAL_REQUIRED"
        elif self.risk_score >= 12:
            self.risk_level = RiskLevel.MEDIUM
            self.automatic_action = "CONDITIONAL_APPROVAL"
        else:
            self.risk_level = RiskLevel.LOW
            self.automatic_action = "ALLOW_RELEASE"


@dataclass
class ConditionEvaluationResult:
    """Result of evaluating a single condition."""
    metric_name: str
    operator: str
    threshold: Any
    actual_value: Any
    passed: bool
    message: str = ""


@dataclass
class GateEvaluationResult:
    """Result of evaluating a full quality gate."""
    gate_id: str
    gate_name: str
    category: GateCategory
    passed: bool
    condition_results: List[ConditionEvaluationResult]
    severity: Severity
    failure_action: FailureAction
    failure_reasons: List[str] = field(default_factory=list)


@dataclass
class QualityGateDecision:
    """Final release decision generated by the decision engine."""
    decision_id: str
    system_id: str
    system_version: str
    model_version: str
    decision: ReleaseDecisionType
    total_score: float
    gate_results: List[GateEvaluationResult]
    risk_assessment: RiskAssessment
    explainable_reasons: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_certification_level: CertificationLevel = CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED
    requires_human_approval: bool = False
    active_exceptions: List[str] = field(default_factory=list)


@dataclass
class CertificationRecord:
    """Immutable certification state record."""
    id: str
    system_id: str
    system_version: str
    model_version: str
    certification_level: CertificationLevel
    score: float
    evidence_package_id: str
    decision_id: str
    approved_by: str
    issued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = field(default_factory=lambda: (datetime.now(timezone.utc) + timedelta(days=90)).isoformat())
    status: CertificationStatus = CertificationStatus.ACTIVE
    signature: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)

    def generate_signature(self, secret_key: str = "enterprise_verification_sec_key") -> str:
        payload = f"{self.id}:{self.system_id}:{self.system_version}:{self.model_version}:{self.certification_level.value}:{self.score}:{self.evidence_package_id}:{self.issued_at}:{self.expires_at}:{secret_key}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def verify_integrity(self, secret_key: str = "enterprise_verification_sec_key") -> bool:
        expected = self.generate_signature(secret_key)
        return self.signature == expected


@dataclass
class ApprovalReview:
    """Human or automated review submission."""
    review_id: str
    certification_id: str
    reviewer_id: str
    reviewer_role: str
    action: ApprovalAction
    comments: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    signature: str = ""


@dataclass
class ExceptionRequest:
    """Request for quality gate exception / risk acceptance."""
    exception_id: str
    system_id: str
    component: str
    gate_id: str
    metric_name: str
    risk_level: RiskLevel
    reason: str
    owner: str
    duration_days: int
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = ""
    status: ExceptionStatus = ExceptionStatus.PENDING
    approver: Optional[str] = None
    approved_at: Optional[str] = None
    mitigating_controls: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.expires_at:
            created_dt = datetime.fromisoformat(self.created_at) if "T" in self.created_at else datetime.now(timezone.utc)
            self.expires_at = (created_dt + timedelta(days=self.duration_days)).isoformat()


@dataclass
class ChangeImpactReport:
    """Analysis of change impacts on active certifications."""
    change_id: str
    change_type: ChangeType
    changed_entity: str
    version_before: str
    version_after: str
    affected_certification_levels: List[CertificationLevel]
    invalidated_certifications: List[str]
    required_reverification_suites: List[str]
    analysis_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CertificationDashboardView:
    """Summary dashboard view for certification and governance state."""
    active_certifications_count: int
    system_certifications: List[CertificationRecord]
    gate_summary: Dict[str, int]
    risk_summary: Dict[str, int]
    pending_approvals_count: int
    active_exceptions_count: int
    expiring_soon_count: int
    recent_decisions: List[QualityGateDecision]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
