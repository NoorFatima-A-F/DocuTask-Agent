"""
Domain models and schemas for Part 4 - Enterprise Platform Core Services Verification.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Any


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class SectionId(str, Enum):
    SECTION_A_ORCHESTRATOR = "SECTION_A_ORCHESTRATOR"
    SECTION_B_AGENT_KERNEL = "SECTION_B_AGENT_KERNEL"
    SECTION_C_WORKFLOW_ENGINE = "SECTION_C_WORKFLOW_ENGINE"
    SECTION_D_SCHEDULER = "SECTION_D_SCHEDULER"
    SECTION_E_QUEUES = "SECTION_E_QUEUES"
    SECTION_F_STORAGE = "SECTION_F_STORAGE"
    SECTION_G_API_GATEWAY = "SECTION_G_API_GATEWAY"
    SECTION_H_EVENT_BUS = "SECTION_H_EVENT_BUS"
    SECTION_I_CONFIG_SECRETS = "SECTION_I_CONFIG_SECRETS"
    SECTION_J_CACHING = "SECTION_J_CACHING"
    SECTION_K_IDENTITY_AUTH = "SECTION_K_IDENTITY_AUTH"
    SECTION_L_OBSERVABILITY = "SECTION_L_OBSERVABILITY"
    SECTION_M_RESILIENCE = "SECTION_M_RESILIENCE"
    SECTION_N_CROSS_SERVICE = "SECTION_N_CROSS_SERVICE"


@dataclass
class AssertionResult:
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
class SectionVerificationResult:
    section_id: SectionId
    title: str
    description: str
    status: VerificationStatus
    score: float
    weight: float
    assertions: List[AssertionResult] = field(default_factory=list)
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
            "section_id": self.section_id.value,
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
        }


@dataclass
class PlatformCoreVerificationScorecard:
    sections: Dict[str, SectionVerificationResult] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
    total_assertions: int = 0
    passed_assertions: int = 0
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "composite_score": round(self.composite_score, 2),
            "grade": self.grade,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "sections": {k: v.to_dict() for k, v in self.sections.items()},
        }
