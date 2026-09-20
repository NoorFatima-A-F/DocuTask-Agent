"""
Phase 13.5 Learning & Reflection Domain Events (ARLP-KIP).
Typed immutable events capturing mission reflections, pattern mining, knowledge compilation, and policy promotions.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


def _gen_id(prefix: str = "lrn_evt") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseLearningEvent(BaseModel):
    event_id: str = Field(default_factory=_gen_id)
    mission_id: Optional[str] = None
    event_type: str
    timestamp: str = Field(default_factory=_now_iso)
    payload: Dict[str, Any] = Field(default_factory=dict)
    provenance_hash: Optional[str] = None


# Alias for domain event base
LearningDomainEvent = BaseLearningEvent


class ReflectionStarted(BaseLearningEvent):
    event_type: str = "learning.reflection.started"
    mission_id: str
    target_replay_hash: Optional[str] = "initial_replay_hash"


class ReflectionCompleted(BaseLearningEvent):
    event_type: str = "learning.reflection.completed"
    reflection_id: str = Field(default_factory=lambda: _gen_id("ref"))
    mission_id: str
    observations_count: int = 1
    overall_efficiency: float = 0.95
    confidence_score: float = 0.95


class PatternDetected(BaseLearningEvent):
    event_type: str = "learning.pattern.detected"
    pattern_id: str = Field(default_factory=lambda: _gen_id("pat"))
    pattern_type: str = "SEQUENTIAL_BURST"
    occurrences_count: int = 1
    frequency: int = 1
    affected_subsystems: List[str] = Field(default_factory=list)


class KnowledgeExtracted(BaseLearningEvent):
    event_type: str = "learning.knowledge.extracted"
    knowledge_id: str = Field(default_factory=lambda: _gen_id("kn"))
    title: str = "Extracted Knowledge Rule"
    category: str = "EXECUTION_RULE"
    confidence: float = 0.95


class LessonPublished(BaseLearningEvent):
    event_type: str = "learning.lesson.published"
    lesson_id: str = Field(default_factory=lambda: _gen_id("lsn"))
    summary: str = "Institutional execution lesson"
    recommended_action: str = "Apply adaptive concurrency"
    rule_count: int = 1


class PolicyProposed(BaseLearningEvent):
    event_type: str = "learning.policy.proposed"
    candidate_id: str = Field(default_factory=lambda: _gen_id("cand"))
    policy_id: Optional[str] = None
    policy_name: str = "Adaptive Dynamic Policy"
    target_component: str = "planner"
    version: str = "1.0.0"
    expected_improvement_pct: float = 12.5
    risk_score: float = 0.15


class PolicyApproved(BaseLearningEvent):
    event_type: str = "learning.policy.approved"
    candidate_id: str = Field(default_factory=lambda: _gen_id("cand"))
    policy_id: Optional[str] = None
    version: str = "1.0.0"
    approver: str = "gov-council"
    reviewer_id: Optional[str] = "gov-council"
    approval_tier: str = "GOVERNANCE_COUNCIL"


class PolicyRejected(BaseLearningEvent):
    event_type: str = "learning.policy.rejected"
    candidate_id: str = Field(default_factory=lambda: _gen_id("cand"))
    policy_id: Optional[str] = None
    version: str = "1.0.0"
    reason: str = "High risk threshold exceeded"


class KnowledgeVersionCreated(BaseLearningEvent):
    event_type: str = "learning.knowledge.version_created"
    record_id: str = Field(default_factory=lambda: _gen_id("rec"))
    knowledge_id: Optional[str] = None
    version: str = "1.0.0"
    previous_version: Optional[str] = None


class KnowledgeDeprecated(BaseLearningEvent):
    event_type: str = "learning.knowledge.deprecated"
    record_id: str = Field(default_factory=lambda: _gen_id("rec"))
    knowledge_id: Optional[str] = None
    superseded_by: Optional[str] = None


class StrategyGenerated(BaseLearningEvent):
    event_type: str = "learning.strategy.generated"
    strategy_id: str = Field(default_factory=lambda: _gen_id("strat"))
    strategy_name: str = "Dynamic Wavefront Execution Strategy"
    goal_type: str = "EXTRACTION"
    expected_success_rate: float = 0.98


class StrategyAdopted(BaseLearningEvent):
    event_type: str = "learning.strategy.adopted"
    strategy_id: str = Field(default_factory=lambda: _gen_id("strat"))
    planner_version: str = "2.0.0"


class LearningCompleted(BaseLearningEvent):
    event_type: str = "learning.cycle.completed"
    cycle_id: str = Field(default_factory=lambda: _gen_id("cycle"))
    total_reflections: int = 1
    total_lessons: int = 1
    total_policies_proposed: int = 1
    total_policies: int = 1
