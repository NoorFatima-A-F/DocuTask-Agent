"""
Domain Models and Schemas for Phase V10 — Enterprise Performance, Scalability & Reliability Engineering Validation Program (EPSR-VP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"


class WorkloadComplexity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    ENTERPRISE = "ENTERPRISE"


class FailureType(str, Enum):
    DATABASE_OUTAGE = "DATABASE_OUTAGE"
    REDIS_OUTAGE = "REDIS_OUTAGE"
    LLM_503 = "LLM_503"
    WORKER_CRASH = "WORKER_CRASH"
    NETWORK_PARTITION = "NETWORK_PARTITION"


class ReliabilityTier(str, Enum):
    SMB = "SMB"
    DEPARTMENT = "DEPARTMENT"
    GLOBAL_ENTERPRISE = "GLOBAL_ENTERPRISE"


@dataclass
class LatencyProfile:
    endpoint: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    sla_target_ms: float
    requests_per_sec: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "p50_ms": round(self.p50_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "sla_target_ms": round(self.sla_target_ms, 2),
            "requests_per_sec": round(self.requests_per_sec, 2),
        }


@dataclass
class AICostMetric:
    operation: str
    tokens_per_doc: int
    cost_per_doc: float
    caching_hit_rate_pct: float
    savings_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "tokens_per_doc": self.tokens_per_doc,
            "cost_per_doc": round(self.cost_per_doc, 5),
            "caching_hit_rate_pct": round(self.caching_hit_rate_pct, 2),
            "savings_pct": round(self.savings_pct, 2),
        }


@dataclass
class ChaosExperimentResult:
    experiment_id: str
    component: str
    fault_injected: FailureType
    rto_seconds: float
    rpo_seconds: float
    recovered: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "component": self.component,
            "fault_injected": self.fault_injected.value,
            "rto_seconds": round(self.rto_seconds, 2),
            "rpo_seconds": round(self.rpo_seconds, 2),
            "recovered": self.recovered,
        }


@dataclass
class PerformanceAssertionResult:
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
class PillarPerformanceResult:
    pillar_id: str
    title: str
    description: str
    status: VerificationStatus
    score: float
    weight: float
    assertions: List[PerformanceAssertionResult] = field(default_factory=list)
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
class PerformanceScorecard:
    pillars: Dict[str, PillarPerformanceResult] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
    availability_pct: float = 99.99
    production_ready: bool = True
    total_assertions: int = 0
    passed_assertions: int = 0
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "composite_score": round(self.composite_score, 2),
            "grade": self.grade,
            "availability_pct": round(self.availability_pct, 4),
            "production_ready": self.production_ready,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "pillars": {k: v.to_dict() for k, v in self.pillars.items()},
        }
