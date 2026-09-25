"""
Fluent Builders Suite for Intelligent Planner.
Provides PlannerRequestBuilder, PlannerContextBuilder, CandidatePlanBuilder,
PlanningTraceBuilder, and PlanningEvidenceBuilder.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.planner.context import PlannerContext, PlannerRequest
from app.agents.planner.metadata import CandidatePlan, PlanningEvidence, PlanningTrace, RejectedAlternative
from app.agents.planning.constraints import PlanConstraint
from app.agents.planning.contracts import Plan
from app.agents.planning.goals import PlanGoal


class PlannerContextBuilder:
    """Fluent builder for PlannerContext."""

    def __init__(self):
        self._document_id: Optional[UUID] = None
        self._user_id: Optional[UUID] = None
        self._budget_usd = 5.0
        self._max_candidates = 3
        self._parameters: Dict[str, Any] = {}

    def for_document(self, document_id: UUID, user_id: UUID) -> "PlannerContextBuilder":
        self._document_id = document_id
        self._user_id = user_id
        return self

    def with_budget(self, budget_usd: float) -> "PlannerContextBuilder":
        self._budget_usd = budget_usd
        return self

    def with_max_candidates(self, count: int) -> "PlannerContextBuilder":
        self._max_candidates = count
        return self

    def build(self) -> PlannerContext:
        return PlannerContext(
            document_id=self._document_id,
            user_id=self._user_id,
            planning_budget_usd=self._budget_usd,
            max_candidates=self._max_candidates,
            parameters=self._parameters
        )


class PlannerRequestBuilder:
    """Fluent builder for PlannerRequest."""

    def __init__(self, goal_name: str):
        self._goal_name = goal_name
        self._goal_id = "GOAL_REQ"
        self._context = PlannerContext()
        self._constraints: List[PlanConstraint] = []

    def with_goal_id(self, goal_id: str) -> "PlannerRequestBuilder":
        self._goal_id = goal_id
        return self

    def with_context(self, context: PlannerContext) -> "PlannerRequestBuilder":
        self._context = context
        return self

    def add_constraint(self, constraint: PlanConstraint) -> "PlannerRequestBuilder":
        self._constraints.append(constraint)
        return self

    def build(self) -> PlannerRequest:
        goal = PlanGoal(goal_id=self._goal_id, name=self._goal_name)
        return PlannerRequest(
            goal=goal,
            context=self._context,
            constraints=self._constraints
        )


class CandidatePlanBuilder:
    """Fluent builder for CandidatePlan."""

    def __init__(self, plan: Plan):
        self._plan = plan
        self._strategy = "HIERARCHICAL"
        self._rank_score = 0.5
        self._cost = 0.0
        self._duration = 0.0
        self._confidence = 0.9

    def with_strategy(self, strategy: str) -> "CandidatePlanBuilder":
        self._strategy = strategy
        return self

    def with_score(self, score: float) -> "CandidatePlanBuilder":
        self._rank_score = score
        return self

    def build(self) -> CandidatePlan:
        return CandidatePlan(
            plan=self._plan,
            strategy_used=self._strategy,
            rank_score=self._rank_score,
            estimated_cost_usd=self._cost,
            estimated_duration_seconds=self._duration,
            confidence=self._confidence
        )


class PlanningEvidenceBuilder:
    """Fluent builder for PlanningEvidence."""

    def __init__(self, description: str):
        self._description = description
        self._source = "TOOL_REGISTRY"
        self._confidence = 1.0
        self._data: Dict[str, Any] = {}

    def with_source(self, source: str) -> "PlanningEvidenceBuilder":
        self._source = source
        return self

    def with_data(self, key: str, value: Any) -> "PlanningEvidenceBuilder":
        self._data[key] = value
        return self

    def build(self) -> PlanningEvidence:
        return PlanningEvidence(
            description=self._description,
            source=self._source,
            confidence=self._confidence,
            data=self._data
        )


class PlanningTraceBuilder:
    """Fluent builder for PlanningTrace."""

    def __init__(self, goal_id: str):
        self._goal_id = goal_id
        self._strategy = "HIERARCHICAL"
        self._evidences: List[PlanningEvidence] = []
        self._rejected: List[RejectedAlternative] = []

    def with_strategy(self, strategy: str) -> "PlanningTraceBuilder":
        self._strategy = strategy
        return self

    def add_evidence(self, evidence: PlanningEvidence) -> "PlanningTraceBuilder":
        self._evidences.append(evidence)
        return self

    def add_rejected_alternative(self, name: str, reason: str, score: float = 0.0) -> "PlanningTraceBuilder":
        self._rejected.append(RejectedAlternative(plan_name=name, rejection_reason=reason, score=score))
        return self

    def build(self) -> PlanningTrace:
        return PlanningTrace(
            goal_id=self._goal_id,
            selected_strategy=self._strategy,
            evidences=self._evidences,
            rejected_alternatives=self._rejected
        )
