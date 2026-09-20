"""
Domain models and schemas for Phase V12 Enterprise AI Platform Verification Certification & Readiness Assessment Program (EAP-VCRAP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class MaturityTier(str, Enum):
    LEVEL_0_EXPERIMENTAL = "LEVEL_0_EXPERIMENTAL"
    LEVEL_1_FUNCTIONAL = "LEVEL_1_FUNCTIONAL"
    LEVEL_2_ENGINEERED = "LEVEL_2_ENGINEERED"
    LEVEL_3_OPERATIONAL = "LEVEL_3_OPERATIONAL"
    LEVEL_4_ENTERPRISE_READY = "LEVEL_4_ENTERPRISE_READY"
    LEVEL_5_ADAPTIVE_INTELLIGENCE = "LEVEL_5_ADAPTIVE_INTELLIGENCE"


class RiskCategory(str, Enum):
    TECHNICAL = "TECHNICAL"
    AI_COGNITIVE = "AI_COGNITIVE"
    SECURITY = "SECURITY"
    BUSINESS_OPERATIONAL = "BUSINESS_OPERATIONAL"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class PhaseVerificationSummary:
    phase_id: str
    name: str
    category: str
    score: float
    status: str
    key_evidence_files: List[str]
    tests_passed: int
    total_tests: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "name": self.name,
            "category": self.category,
            "score": round(self.score, 1),
            "status": self.status,
            "key_evidence_files": self.key_evidence_files,
            "tests_passed": self.tests_passed,
            "total_tests": self.total_tests,
        }


@dataclass
class MaturityAssessment:
    current_maturity_level: float
    tier: MaturityTier
    tier_label: str
    architecture_maturity: float
    ai_engineering_maturity: float
    security_maturity: float
    reliability_maturity: float
    governance_maturity: float
    evaluation_criteria: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_maturity_level": round(self.current_maturity_level, 2),
            "tier": self.tier.value,
            "tier_label": self.tier_label,
            "architecture_maturity": round(self.architecture_maturity, 1),
            "ai_engineering_maturity": round(self.ai_engineering_maturity, 1),
            "security_maturity": round(self.security_maturity, 1),
            "reliability_maturity": round(self.reliability_maturity, 1),
            "governance_maturity": round(self.governance_maturity, 1),
            "evaluation_criteria": self.evaluation_criteria,
        }


@dataclass
class MasterReadinessScore:
    architecture_quality: float   # Weight: 15%
    ai_capability: float          # Weight: 20%
    security_posture: float       # Weight: 20%
    reliability_resilience: float # Weight: 15%
    operational_excellence: float # Weight: 10%
    business_value: float         # Weight: 15%
    governance_ethics: float      # Weight: 5%
    overall_readiness_score: float
    grade: str
    readiness_statement: str
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "architecture_quality": round(self.architecture_quality, 1),
            "ai_capability": round(self.ai_capability, 1),
            "security_posture": round(self.security_posture, 1),
            "reliability_resilience": round(self.reliability_resilience, 1),
            "operational_excellence": round(self.operational_excellence, 1),
            "business_value": round(self.business_value, 1),
            "governance_ethics": round(self.governance_ethics, 1),
            "overall_readiness_score": round(self.overall_readiness_score, 1),
            "grade": self.grade,
            "readiness_statement": self.readiness_statement,
            "evaluated_at": self.evaluated_at,
        }


@dataclass
class EvidenceNode:
    claim_id: str
    capability_claim: str
    verification_test: str
    evidence_artifact: str
    sha256_hash: str
    verified: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "capability_claim": self.capability_claim,
            "verification_test": self.verification_test,
            "evidence_artifact": self.evidence_artifact,
            "sha256_hash": self.sha256_hash,
            "verified": self.verified,
        }


@dataclass
class RiskEntry:
    risk_id: str
    category: RiskCategory
    description: str
    probability: str  # LOW, MEDIUM, HIGH
    impact: str       # LOW, MEDIUM, HIGH
    severity: RiskSeverity
    mitigation_control: str
    residual_risk: str
    status: str       # MITIGATED, CONTROLLED, MONITORED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "category": self.category.value,
            "description": self.description,
            "probability": self.probability,
            "impact": self.impact,
            "severity": self.severity.value,
            "mitigation_control": self.mitigation_control,
            "residual_risk": self.residual_risk,
            "status": self.status,
        }


@dataclass
class GovernanceAudit:
    transparency_score: float
    accountability_score: float
    demographic_fairness_score: float
    human_oversight_score: float
    safety_boundary_score: float
    overall_governance_score: float
    framework_alignment: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transparency_score": round(self.transparency_score, 1),
            "accountability_score": round(self.accountability_score, 1),
            "demographic_fairness_score": round(self.demographic_fairness_score, 1),
            "human_oversight_score": round(self.human_oversight_score, 1),
            "safety_boundary_score": round(self.safety_boundary_score, 1),
            "overall_governance_score": round(self.overall_governance_score, 1),
            "framework_alignment": self.framework_alignment,
        }


@dataclass
class PortfolioDocument:
    filename: str
    title: str
    target_audience: str
    summary: str
    size_bytes: int = 0
    sha256_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "title": self.title,
            "target_audience": self.target_audience,
            "summary": self.summary,
            "size_bytes": self.size_bytes,
            "sha256_hash": self.sha256_hash,
        }
