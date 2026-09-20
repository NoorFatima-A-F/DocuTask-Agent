"""
Domain models and schemas for Phase V8 — Enterprise Autonomous Agent Workforce Verification & Validation Program (EAAWVVP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class PartId(str, Enum):
    PART_01_REGISTRY = "PART_01_REGISTRY"
    PART_02_CAPABILITIES = "PART_02_CAPABILITIES"
    PART_03_HIERARCHY = "PART_03_HIERARCHY"
    PART_04_TEAMS = "PART_04_TEAMS"
    PART_05_MARKETPLACE = "PART_05_MARKETPLACE"
    PART_06_NEGOTIATION = "PART_06_NEGOTIATION"
    PART_07_COLLABORATION = "PART_07_COLLABORATION"
    PART_08_MANAGEMENT = "PART_08_MANAGEMENT"
    PART_09_COUNCIL = "PART_09_COUNCIL"
    PART_10_ECONOMICS = "PART_10_ECONOMICS"
    PART_11_HIRING = "PART_11_HIRING"
    PART_12_CAREER = "PART_12_CAREER"
    PART_13_SCHEDULER = "PART_13_SCHEDULER"
    PART_14_CONFLICT = "PART_14_CONFLICT"
    PART_15_MEMORY = "PART_15_MEMORY"
    PART_16_TRUST = "PART_16_TRUST"
    PART_17_SECURITY = "PART_17_SECURITY"
    PART_18_SCALABILITY = "PART_18_SCALABILITY"
    PART_19_BENCHMARKS = "PART_19_BENCHMARKS"
    PART_20_DASHBOARDS = "PART_20_DASHBOARDS"
    PART_21_EVIDENCE = "PART_21_EVIDENCE"


class AgentRole(str, Enum):
    CEO = "CEO"
    EXECUTIVE = "EXECUTIVE"
    DEPARTMENT_MANAGER = "DEPARTMENT_MANAGER"
    TEAM_LEAD = "TEAM_LEAD"
    SPECIALIST = "SPECIALIST"
    WORKER = "WORKER"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"


class AgentLifecycleState(str, Enum):
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    ON_DUTY = "ON_DUTY"
    UNDER_REVIEW = "UNDER_REVIEW"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class ClearanceLevel(int, Enum):
    LEVEL_1_PUBLIC = 1
    LEVEL_2_INTERNAL = 2
    LEVEL_3_CONFIDENTIAL = 3
    LEVEL_4_RESTRICTED = 4
    LEVEL_5_EXECUTIVE = 5


@dataclass
class AgentProfile:
    agent_id: str
    name: str
    role: AgentRole
    department: str
    clearance: ClearanceLevel
    skills: List[str]
    state: AgentLifecycleState = AgentLifecycleState.ACTIVE
    trust_score: float = 1.0
    cost_per_task: float = 0.01
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "department": self.department,
            "clearance": self.clearance.value,
            "skills": self.skills,
            "state": self.state.value,
            "trust_score": round(self.trust_score, 4),
            "cost_per_task": round(self.cost_per_task, 4),
            "created_at": self.created_at,
        }


@dataclass
class TeamDefinition:
    team_id: str
    name: str
    lead_agent_id: str
    member_agent_ids: List[str]
    mission: str
    fitness_score: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "team_id": self.team_id,
            "name": self.name,
            "lead_agent_id": self.lead_agent_id,
            "member_agent_ids": self.member_agent_ids,
            "mission": self.mission,
            "fitness_score": round(self.fitness_score, 4),
        }


@dataclass
class MarketplaceBid:
    bid_id: str
    task_id: str
    agent_id: str
    proposed_cost: float
    estimated_duration_ms: float
    reputation_score: float
    is_winning_bid: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bid_id": self.bid_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "proposed_cost": round(self.proposed_cost, 4),
            "estimated_duration_ms": round(self.estimated_duration_ms, 2),
            "reputation_score": round(self.reputation_score, 4),
            "is_winning_bid": self.is_winning_bid,
        }


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
class PartVerificationResult:
    part_id: PartId
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
            "part_id": self.part_id.value,
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
class WorkforceReadinessScorecard:
    parts: Dict[str, PartVerificationResult] = field(default_factory=dict)
    indices: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
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
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "indices": {k: round(v, 2) for k, v in self.indices.items()},
            "parts": {k: v.to_dict() for k, v in self.parts.items()},
        }
