"""
Domain Models and Schemas for Phase V9 — Enterprise AI Security Validation & Adversarial Assurance Program (EA-SVAAP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Any


class SecurityStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    DEFENDED = "DEFENDED"
    BLOCKED = "BLOCKED"


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class SecurityPillar(str, Enum):
    FRAMEWORK_AND_SCANNERS = "FRAMEWORK_AND_SCANNERS"
    APPLICATION_SECURITY = "APPLICATION_SECURITY"
    OWASP_ASVS = "OWASP_ASVS"
    AI_SECURITY_LLM = "AI_SECURITY_LLM"
    MITRE_ATLAS_AGENT = "MITRE_ATLAS_AGENT"
    IDENTITY_ACCESS = "IDENTITY_ACCESS"
    DATA_PROTECTION = "DATA_PROTECTION"
    TENANT_ISOLATION = "TENANT_ISOLATION"
    COMPLIANCE_GOVERNANCE = "COMPLIANCE_GOVERNANCE"
    DASHBOARDS_OBSERVABILITY = "DASHBOARDS_OBSERVABILITY"


class AttackCategory(str, Enum):
    DIRECT_PROMPT_INJECTION = "DIRECT_PROMPT_INJECTION"
    INDIRECT_PROMPT_INJECTION = "INDIRECT_PROMPT_INJECTION"
    JAILBREAK = "JAILBREAK"
    DATA_POISONING = "DATA_POISONING"
    SENSITIVE_DATA_DISCLOSURE = "SENSITIVE_DATA_DISCLOSURE"
    SUPPLY_CHAIN_RISK = "SUPPLY_CHAIN_RISK"
    IMPROPER_OUTPUT_HANDLING = "IMPROPER_OUTPUT_HANDLING"
    EXCESSIVE_AGENCY = "EXCESSIVE_AGENCY"
    SYSTEM_PROMPT_LEAKAGE = "SYSTEM_PROMPT_LEAKAGE"
    VECTOR_DB_EXPLOITATION = "VECTOR_DB_EXPLOITATION"
    MISINFORMATION_HALLUCINATION = "MISINFORMATION_HALLUCINATION"
    UNBOUNDED_CONSUMPTION = "UNBOUNDED_CONSUMPTION"
    GOAL_HIJACKING = "GOAL_HIJACKING"
    TOOL_MISUSE = "TOOL_MISUSE"
    MEMORY_CORRUPTION = "MEMORY_CORRUPTION"
    BOLA_IDOR = "BOLA_IDOR"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    CROSS_TENANT_LEAKAGE = "CROSS_TENANT_LEAKAGE"


class ComplianceFramework(str, Enum):
    NIST_AI_RMF = "NIST_AI_RMF"
    OWASP_TOP_10_LLM = "OWASP_TOP_10_LLM"
    OWASP_ASVS = "OWASP_ASVS"
    MITRE_ATLAS = "MITRE_ATLAS"
    ISO_27001 = "ISO_27001"
    ISO_42001 = "ISO_42001"
    ISO_23894 = "ISO_23894"
    SOC_2 = "SOC_2"
    ZERO_TRUST = "ZERO_TRUST"


@dataclass
class AttackPayload:
    payload_id: str
    category: AttackCategory
    raw_payload: str
    target_component: str
    expected_action: str
    severity: SeverityLevel = SeverityLevel.HIGH
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_id": self.payload_id,
            "category": self.category.value,
            "raw_payload": self.raw_payload,
            "target_component": self.target_component,
            "expected_action": self.expected_action,
            "severity": self.severity.value,
            "metadata": self.metadata,
        }


@dataclass
class SecurityFinding:
    finding_id: str
    title: str
    pillar: SecurityPillar
    severity: SeverityLevel
    status: SecurityStatus
    description: str
    remediation_recommendation: str
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "title": self.title,
            "pillar": self.pillar.value,
            "severity": self.severity.value,
            "status": self.status.value,
            "description": self.description,
            "remediation_recommendation": self.remediation_recommendation,
            "evidence": self.evidence,
        }


@dataclass
class SecurityAssertionResult:
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
class PillarVerificationResult:
    pillar: SecurityPillar
    title: str
    description: str
    status: SecurityStatus
    score: float
    weight: float
    assertions: List[SecurityAssertionResult] = field(default_factory=list)
    findings: List[SecurityFinding] = field(default_factory=list)
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
            "pillar": self.pillar.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "score": round(self.score, 2),
            "weight": round(self.weight, 2),
            "passed_assertions": self.passed_assertions_count,
            "total_assertions": self.total_assertions_count,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "metrics": self.metrics,
            "assertions": [a.to_dict() for a in self.assertions],
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass
class SecurityScorecard:
    pillars: Dict[str, PillarVerificationResult] = field(default_factory=dict)
    weighted_scores: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
    critical_vulnerabilities: int = 0
    high_vulnerabilities: int = 0
    total_assertions: int = 0
    passed_assertions: int = 0
    production_ready: bool = True
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "composite_score": round(self.composite_score, 2),
            "grade": self.grade,
            "production_ready": self.production_ready,
            "critical_vulnerabilities": self.critical_vulnerabilities,
            "high_vulnerabilities": self.high_vulnerabilities,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "weighted_scores": {k: round(v, 2) for k, v in self.weighted_scores.items()},
            "pillars": {k: v.to_dict() for k, v in self.pillars.items()},
        }
