"""
Fluent Builders for Reflection Subsystem.
Ensures fail-fast, validated instantiation of core reflection models.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from app.agents.reflection.context import ReflectionContext, ReflectionRequest
from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric, EvaluationReport
from app.agents.reflection.execution_feedback import ExecutionCritiqueItem, ExecutionFeedback
from app.agents.reflection.feedback_generator import SubsystemFeedbackBundle
from app.agents.reflection.learning_artifact import LearningArtifact, LearningArtifactType
from app.agents.reflection.memory_feedback import MemoryFeedback
from app.agents.reflection.metadata import ReflectionIdentity
from app.agents.reflection.planner_feedback import PlannerCritiqueItem, PlannerFeedback
from app.agents.reflection.recommendation_engine import Recommendation, SubsystemTarget
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope, TaskTrace
from app.agents.reflection.reflection_session import ReflectionSession
from app.agents.reflection.self_critique import CritiqueFinding, SelfCritique
from app.agents.reflection.tool_feedback import ToolFeedback
from app.agents.reflection.validators import ReflectionValidator


class ReflectionRequestBuilder:
    """Fluent builder for ReflectionRequest."""

    def __init__(self, execution_id: Optional[UUID] = None):
        self._execution_id = execution_id or uuid4()
        self._plan_id: Optional[UUID] = None
        self._goal: str = ""
        self._final_state: str = "COMPLETED"
        self._duration_ms: float = 0.0
        self._tasks: List[TaskTrace] = []
        self._token_usage: Dict[str, int] = {}
        self._cost_usd: float = 0.0
        self._final_outputs: Dict[str, Any] = {}
        self._errors: List[str] = []
        self._context = ReflectionContext()

    def with_goal(self, goal: str) -> "ReflectionRequestBuilder":
        self._goal = goal
        return self

    def with_plan_id(self, plan_id: UUID) -> "ReflectionRequestBuilder":
        self._plan_id = plan_id
        return self

    def with_final_state(self, state: str) -> "ReflectionRequestBuilder":
        self._final_state = state
        return self

    def with_duration(self, duration_ms: float) -> "ReflectionRequestBuilder":
        self._duration_ms = duration_ms
        return self

    def with_cost(self, cost_usd: float) -> "ReflectionRequestBuilder":
        self._cost_usd = cost_usd
        return self

    def with_tokens(self, prompt: int, completion: int) -> "ReflectionRequestBuilder":
        self._token_usage = {"prompt_tokens": prompt, "completion_tokens": completion}
        return self

    def add_task(self, task: TaskTrace) -> "ReflectionRequestBuilder":
        self._tasks.append(task)
        return self

    def with_outputs(self, outputs: Dict[str, Any]) -> "ReflectionRequestBuilder":
        self._final_outputs = outputs
        return self

    def add_error(self, error: str) -> "ReflectionRequestBuilder":
        self._errors.append(error)
        return self

    def build(self) -> ReflectionRequest:
        envelope = ExecutionTraceEnvelope(
            execution_id=self._execution_id,
            plan_id=self._plan_id,
            goal=self._goal,
            final_state=self._final_state,
            total_duration_ms=self._duration_ms,
            token_usage=self._token_usage,
            cost_usd=self._cost_usd,
            tasks=self._tasks,
            final_outputs=self._final_outputs,
            errors=self._errors
        )
        ReflectionValidator.validate_execution_trace(envelope)
        return ReflectionRequest(trace=envelope, context=self._context)


class LearningArtifactBuilder:
    """Fluent builder for LearningArtifact."""

    def __init__(self, source_execution_id: UUID):
        self._source_execution_id = source_execution_id
        self._type = LearningArtifactType.PLANNER_HEURISTIC
        self._title = ""
        self._description = ""
        self._heuristic: Dict[str, Any] = {}
        self._conditions: List[str] = []
        self._confidence = 0.9

    def with_type(self, artifact_type: LearningArtifactType) -> "LearningArtifactBuilder":
        self._type = artifact_type
        return self

    def with_title(self, title: str) -> "LearningArtifactBuilder":
        self._title = title
        return self

    def with_description(self, desc: str) -> "LearningArtifactBuilder":
        self._description = desc
        return self

    def with_heuristic(self, heuristic: Dict[str, Any]) -> "LearningArtifactBuilder":
        self._heuristic = heuristic
        return self

    def with_confidence(self, conf: float) -> "LearningArtifactBuilder":
        ReflectionValidator.validate_confidence_score(conf)
        self._confidence = conf
        return self

    def build(self) -> LearningArtifact:
        return LearningArtifact(
            artifact_id=uuid4(),
            artifact_type=self._type,
            title=self._title or "Untitled Heuristic",
            description=self._description or "Generated heuristic.",
            heuristic_content=self._heuristic,
            conditions=self._conditions,
            confidence_score=self._confidence,
            source_execution_id=self._source_execution_id
        )


class RecommendationBuilder:
    """Fluent builder for Recommendation."""

    def __init__(self, target_subsystem: SubsystemTarget):
        self._subsystem = target_subsystem
        self._title = ""
        self._rationale = ""
        self._expected_impact = ""
        self._confidence = 0.9
        self._evidence: List[str] = []

    def with_title(self, title: str) -> "RecommendationBuilder":
        self._title = title
        return self

    def with_rationale(self, rationale: str) -> "RecommendationBuilder":
        self._rationale = rationale
        return self

    def with_expected_impact(self, impact: str) -> "RecommendationBuilder":
        self._expected_impact = impact
        return self

    def with_confidence(self, confidence: float) -> "RecommendationBuilder":
        ReflectionValidator.validate_confidence_score(confidence)
        self._confidence = confidence
        return self

    def add_evidence(self, evidence: str) -> "RecommendationBuilder":
        self._evidence.append(evidence)
        return self

    def build(self) -> Recommendation:
        rec = Recommendation(
            recommendation_id=uuid4(),
            target_subsystem=self._subsystem,
            title=self._title,
            rationale=self._rationale,
            expected_impact=self._expected_impact,
            confidence=self._confidence,
            evidence=self._evidence
        )
        ReflectionValidator.validate_recommendation(rec)
        return rec


class CritiqueBuilder:
    """Fluent builder for SelfCritique."""

    def __init__(self, execution_id: UUID):
        self._execution_id = execution_id
        self._strengths: List[str] = []
        self._weaknesses: List[str] = []
        self._findings: List[CritiqueFinding] = []
        self._opportunities: List[str] = []

    def add_strength(self, s: str) -> "CritiqueBuilder":
        self._strengths.append(s)
        return self

    def add_weakness(self, w: str) -> "CritiqueBuilder":
        self._weaknesses.append(w)
        return self

    def add_finding(self, f: CritiqueFinding) -> "CritiqueBuilder":
        self._findings.append(f)
        return self

    def add_opportunity(self, opp: str) -> "CritiqueBuilder":
        self._opportunities.append(opp)
        return self

    def build(self) -> SelfCritique:
        critique = SelfCritique(
            critique_id=uuid4(),
            execution_id=self._execution_id,
            strengths=self._strengths,
            weaknesses=self._weaknesses,
            findings=self._findings,
            improvement_opportunities=self._opportunities,
            overall_critique_score=1.0 if not self._findings else 0.8
        )
        ReflectionValidator.validate_critique(critique)
        return critique


class EvaluationBuilder:
    """Fluent builder for EvaluationReport."""

    def __init__(self, execution_id: UUID):
        self._execution_id = execution_id
        self._overall_score = 1.0
        self._dimensions: Dict[str, DimensionEvaluation] = {}
        self._strengths: List[str] = []
        self._weaknesses: List[str] = []

    def with_dimension(self, dim: DimensionEvaluation) -> "EvaluationBuilder":
        self._dimensions[dim.dimension.value] = dim
        return self

    def with_overall_score(self, score: float) -> "EvaluationBuilder":
        ReflectionValidator.validate_confidence_score(score, "Overall Score")
        self._overall_score = score
        return self

    def build(self) -> EvaluationReport:
        return EvaluationReport(
            report_id=uuid4(),
            execution_id=self._execution_id,
            overall_score=self._overall_score,
            dimensions=self._dimensions,
            key_strengths=self._strengths,
            key_weaknesses=self._weaknesses
        )


class FeedbackBuilder:
    """Fluent builder for SubsystemFeedbackBundle."""

    def __init__(self, execution_id: UUID):
        self._execution_id = execution_id
        self._planner = PlannerFeedback(execution_id=execution_id)
        self._execution = ExecutionFeedback(execution_id=execution_id)
        self._memory = MemoryFeedback(execution_id=execution_id)
        self._tool = ToolFeedback(execution_id=execution_id)

    def with_planner_feedback(self, pf: PlannerFeedback) -> "FeedbackBuilder":
        self._planner = pf
        return self

    def with_execution_feedback(self, ef: ExecutionFeedback) -> "FeedbackBuilder":
        self._execution = ef
        return self

    def build(self) -> SubsystemFeedbackBundle:
        return SubsystemFeedbackBundle(
            planner_feedback=self._planner,
            execution_feedback=self._execution,
            memory_feedback=self._memory,
            tool_feedback=self._tool
        )


class ReflectionSessionBuilder:
    """Fluent builder for ReflectionSession."""

    def __init__(self, trace: ExecutionTraceEnvelope):
        self._trace = trace
        self._identity = ReflectionIdentity(execution_id=trace.execution_id)

    def build(self) -> ReflectionSession:
        return ReflectionSession(
            session_id=uuid4(),
            identity=self._identity,
            trace=self._trace
        )
