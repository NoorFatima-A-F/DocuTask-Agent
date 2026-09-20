"""
Domain Models and Schemas for Phase V12 — Enterprise AI Platform Certification & Production Readiness System (EAI-CPRS).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class CertificationLevel(str, Enum):
    LEVEL_1_EXPERIMENTAL = "LEVEL_1_EXPERIMENTAL"          # < 60%
    LEVEL_2_INTERNAL_PRODUCTION = "LEVEL_2_INTERNAL_PROD"  # 60 - 75%
    LEVEL_3_ENTERPRISE_READY = "LEVEL_3_ENTERPRISE_READY"  # 75 - 90%
    LEVEL_4_ENTERPRISE_CERTIFIED = "LEVEL_4_CERTIFIED"     # 90%+


class CertificationDecisionStatus(str, Enum):
    APPROVED_FOR_PRODUCTION = "APPROVED_FOR_PRODUCTION"
    APPROVED_WITH_CONDITIONS = "APPROVED_WITH_CONDITIONS"
    NOT_READY = "NOT_READY"


class RiskCategory(str, Enum):
    AI_HALLUCINATION = "AI_HALLUCINATION"
    SECURITY = "SECURITY"
    OPERATIONAL = "OPERATIONAL"
    FINANCIAL = "FINANCIAL"
    COMPLIANCE = "COMPLIANCE"
    SCALABILITY = "SCALABILITY"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskProbability(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    MITIGATED = "MITIGATED"
    CONTROLLED = "CONTROLLED"
    MONITORED = "MONITORED"


class PRRPillar(str, Enum):
    ENGINEERING_READINESS = "ENGINEERING_READINESS"
    OPERATIONS_READINESS = "OPERATIONS_READINESS"
    SECURITY_READINESS = "SECURITY_READINESS"
    BUSINESS_READINESS = "BUSINESS_READINESS"


@dataclass
class VerificationEvidence:
    evidence_id: str
    verification_phase: str
    subsystem: str
    test_category: str
    execution_date: str
    environment: str
    metrics: Dict[str, Any]
    artifacts: List[str]
    confidence_score: float  # 0.0 - 1.0
    reviewer_status: str     # APPROVED / VERIFIED
    sha256_checksum: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "verification_phase": self.verification_phase,
            "subsystem": self.subsystem,
            "test_category": self.test_category,
            "execution_date": self.execution_date,
            "environment": self.environment,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "confidence_score": round(self.confidence_score, 4),
            "reviewer_status": self.reviewer_status,
            "sha256_checksum": self.sha256_checksum,
        }


@dataclass
class ScoringDimensionResult:
    dimension_name: str
    raw_score: float
    weight: float
    weighted_score: float
    subsystems_evaluated: List[str]
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension_name": self.dimension_name,
            "raw_score": round(self.raw_score, 2),
            "weight": round(self.weight, 2),
            "weighted_score": round(self.weighted_score, 2),
            "subsystems_evaluated": self.subsystems_evaluated,
            "details": self.details,
        }


@dataclass
class PRRChecklistItem:
    item_id: str
    pillar: PRRPillar
    question: str
    passed: bool
    evidence_reference: str
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "pillar": self.pillar.value,
            "question": self.question,
            "passed": self.passed,
            "evidence_reference": self.evidence_reference,
            "notes": self.notes,
        }


@dataclass
class RiskEntry:
    risk_id: str
    category: RiskCategory
    title: str
    severity: RiskSeverity
    probability: RiskProbability
    impact: str
    mitigation: str
    owner: str
    status: RiskStatus
    residual_score: float  # Scale 1-100 (lower is better, <25 is safe)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "category": self.category.value,
            "title": self.title,
            "severity": self.severity.value,
            "probability": self.probability.value,
            "impact": self.impact,
            "mitigation": self.mitigation,
            "owner": self.owner,
            "status": self.status.value,
            "residual_score": round(self.residual_score, 1),
        }


@dataclass
class CertificationAssertionResult:
    name: str
    passed: bool
    message: str
    execution_time_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "execution_time_ms": round(self.execution_time_ms, 3),
            "details": self.details,
        }


@dataclass
class CertificationPillarResult:
    pillar_id: str
    title: str
    description: str
    passed: bool
    score: float
    weight: float
    assertions: List[CertificationAssertionResult] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    @property
    def passed_assertions_count(self) -> int:
        return sum(1 for a in self.assertions if a.passed)

    @property
    def total_assertions_count(self) -> int:
        return len(self.assertions)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pillar_id": self.pillar_id,
            "title": self.title,
            "description": self.description,
            "passed": self.passed,
            "score": round(self.score, 2),
            "weight": round(self.weight, 2),
            "passed_assertions": self.passed_assertions_count,
            "total_assertions": self.total_assertions_count,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "metrics": self.metrics,
            "assertions": [a.to_dict() for a in self.assertions],
        }


@dataclass
class EnterpriseReadinessScorecard:
    overall_readiness_score: float = 100.0
    certification_level: CertificationLevel = CertificationLevel.LEVEL_4_ENTERPRISE_CERTIFIED
    decision: CertificationDecisionStatus = CertificationDecisionStatus.APPROVED_FOR_PRODUCTION
    dimensions: Dict[str, ScoringDimensionResult] = field(default_factory=dict)
    pillar_results: Dict[str, CertificationPillarResult] = field(default_factory=dict)
    critical_risks_count: int = 0
    total_assertions: int = 0
    passed_assertions: int = 0
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "overall_readiness_score": round(self.overall_readiness_score, 2),
            "certification_level": self.certification_level.value,
            "decision": self.decision.value,
            "critical_risks_count": self.critical_risks_count,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
            "pillar_results": {k: v.to_dict() for k, v in self.pillar_results.items()},
        }
