"""
Domain models and schemas for Phase V7 — Enterprise Cognitive Intelligence Verification & Validation Program (ECIVVP).
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
    PART_01_REASONING = "PART_01_REASONING"
    PART_02_GRAPH = "PART_02_GRAPH"
    PART_03_HYPOTHESIS = "PART_03_HYPOTHESIS"
    PART_04_DECISION = "PART_04_DECISION"
    PART_05_SIMULATION = "PART_05_SIMULATION"
    PART_06_LEARNING = "PART_06_LEARNING"
    PART_07_EXPERIENCE = "PART_07_EXPERIENCE"
    PART_08_PROCESS_DISCOVERY = "PART_08_PROCESS_DISCOVERY"
    PART_09_ALIGNMENT = "PART_09_ALIGNMENT"
    PART_10_RECOMMENDATIONS = "PART_10_RECOMMENDATIONS"
    PART_11_CONTINUOUS_LEARNING = "PART_11_CONTINUOUS_LEARNING"
    PART_12_OPTIMIZATION = "PART_12_OPTIMIZATION"
    PART_13_EXECUTIVE = "PART_13_EXECUTIVE"
    PART_14_EXPLAINABILITY = "PART_14_EXPLAINABILITY"
    PART_15_CALIBRATION = "PART_15_CALIBRATION"
    PART_16_ADVERSARIAL = "PART_16_ADVERSARIAL"
    PART_17_SCALABILITY = "PART_17_SCALABILITY"
    PART_18_BENCHMARKS = "PART_18_BENCHMARKS"
    PART_19_DASHBOARDS = "PART_19_DASHBOARDS"
    PART_20_EVIDENCE = "PART_20_EVIDENCE"


class ReasoningType(str, Enum):
    DEDUCTIVE = "DEDUCTIVE"
    INDUCTIVE = "INDUCTIVE"
    ABDUCTIVE = "ABDUCTIVE"
    CAUSAL = "CAUSAL"
    COUNTERFACTUAL = "COUNTERFACTUAL"
    CONSTRAINT = "CONSTRAINT"
    RULE_BASED = "RULE_BASED"
    PROBABILISTIC = "PROBABILISTIC"
    TEMPORAL = "TEMPORAL"
    HIERARCHICAL = "HIERARCHICAL"
    DEPENDENCY = "DEPENDENCY"
    GOAL = "GOAL"
    EXCEPTION_HANDLING = "EXCEPTION_HANDLING"
    MULTI_STEP = "MULTI_STEP"
    RECURSIVE = "RECURSIVE"
    CROSS_DOCUMENT = "CROSS_DOCUMENT"
    MULTI_HOP = "MULTI_HOP"
    BUSINESS_POLICY = "BUSINESS_POLICY"
    ORGANIZATIONAL = "ORGANIZATIONAL"
    MIXED_CHAINS = "MIXED_CHAINS"


class HypothesisType(str, Enum):
    ROOT_CAUSE = "ROOT_CAUSE"
    BUSINESS_IMPROVEMENT = "BUSINESS_IMPROVEMENT"
    RISK = "RISK"
    FAILURE = "FAILURE"
    OPTIMIZATION = "OPTIMIZATION"
    STRATEGIC = "STRATEGIC"
    PREDICTIVE = "PREDICTIVE"
    ALTERNATIVE = "ALTERNATIVE"


class GoalLevel(str, Enum):
    TASK = "TASK"
    AGENT = "AGENT"
    TEAM = "TEAM"
    DEPARTMENT = "DEPARTMENT"
    EXECUTIVE = "EXECUTIVE"
    ENTERPRISE_KPI = "ENTERPRISE_KPI"


@dataclass
class ReasoningTrace:
    trace_id: str
    reasoning_type: ReasoningType
    premises: List[str]
    inferences: List[str]
    conclusion: str
    confidence: float
    is_valid: bool = True
    contradiction_detected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "reasoning_type": self.reasoning_type.value,
            "premises": self.premises,
            "inferences": self.inferences,
            "conclusion": self.conclusion,
            "confidence": round(self.confidence, 4),
            "is_valid": self.is_valid,
            "contradiction_detected": self.contradiction_detected,
        }


@dataclass
class CognitiveNode:
    node_id: str
    node_type: str
    label: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CognitiveEdge:
    source_id: str
    target_id: str
    relation_type: str  # CAUSES, DEPENDS_ON, SUBGOAL_OF, CONSTRAINS
    confidence: float = 1.0


@dataclass
class Hypothesis:
    hypothesis_id: str
    hypothesis_type: HypothesisType
    statement: str
    plausibility: float
    evidence_support_count: int
    contradiction_count: int = 0
    rank: int = 1


@dataclass
class DecisionRecord:
    decision_id: str
    objective: str
    chosen_alternative: str
    evaluated_alternatives: List[str]
    expected_outcome: Dict[str, Any]
    confidence: float
    regret_score: float = 0.0
    audit_trail: List[str] = field(default_factory=list)


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
class CognitiveReadinessScorecard:
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
