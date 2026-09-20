"""
Enterprise Reflection, Self-Critique, Evaluation & Continuous Adaptation Engine.
Provides cognitive introspection, post-execution analysis, self-critique,
learning artifact generation, and cross-subsystem feedback.
"""

from app.agents.reflection.adaptation_engine import (
    AdaptationEngine,
    AdaptationProposal,
    AdaptationStatus,
    AdaptationType,
)
from app.agents.reflection.benchmark import BenchmarkCriteria, BenchmarkEvaluator, BenchmarkReport
from app.agents.reflection.builders import (
    CritiqueBuilder,
    EvaluationBuilder,
    FeedbackBuilder,
    LearningArtifactBuilder,
    RecommendationBuilder,
    ReflectionRequestBuilder,
    ReflectionSessionBuilder,
)
from app.agents.reflection.cache import ReflectionCache
from app.agents.reflection.comparative_analysis import ComparativeAnalyzer, ComparisonResult
from app.agents.reflection.confidence_evaluator import ConfidenceEvaluator
from app.agents.reflection.context import ReflectionContext, ReflectionRequest, ReflectionResult
from app.agents.reflection.correlation import CorrelationAnalyzer
from app.agents.reflection.correctness_evaluator import CorrectnessEvaluator
from app.agents.reflection.cost_evaluator import CostEvaluator
from app.agents.reflection.critique_engine import CritiqueEngine
from app.agents.reflection.decision_analyzer import DecisionAnalyzer
from app.agents.reflection.efficiency_evaluator import EfficiencyEvaluator
from app.agents.reflection.engine import ReflectionEngine
from app.agents.reflection.evaluation import (
    DimensionEvaluation,
    EvaluationDimension,
    EvaluationMetric,
    EvaluationReport,
)
from app.agents.reflection.evaluation_graph import EvaluationGraph, EvaluationStageNode
from app.agents.reflection.evaluation_pipeline import EvaluationPipeline
from app.agents.reflection.events import (
    AdaptationProposalCreatedEvent,
    CritiqueGeneratedEvent,
    EvaluationCompletedEvent,
    LearningArtifactCreatedEvent,
    PlannerFeedbackGeneratedEvent,
    RecommendationGeneratedEvent,
    ReflectionCompletedEvent,
    ReflectionFailedEvent,
    ReflectionStartedEvent,
)
from app.agents.reflection.exceptions import (
    AdaptationApprovalRequiredError,
    CircularCritiqueReferenceError,
    DuplicateLearningArtifactError,
    IncompleteExecutionTraceError,
    InconsistentEvidenceError,
    InvalidConfidenceScoreError,
    InvalidEvaluationGraphError,
    MalformedRecommendationError,
    ReflectionException,
)
from app.agents.reflection.execution_analyzer import ExecutionAnalyzer
from app.agents.reflection.execution_feedback import ExecutionCritiqueItem, ExecutionFeedback
from app.agents.reflection.factory import ReflectionFactory
from app.agents.reflection.failure_analyzer import FailureAnalyzer
from app.agents.reflection.feedback_generator import FeedbackGenerator, SubsystemFeedbackBundle
from app.agents.reflection.goal_evaluator import GoalEvaluator
from app.agents.reflection.hallucination_detector import HallucinationDetector
from app.agents.reflection.improvement_generator import ImprovementDirective, ImprovementGenerator
from app.agents.reflection.inconsistency_detector import InconsistencyDetector
from app.agents.reflection.interfaces import (
    IAdaptationEngine,
    ICritiqueEngine,
    IEvaluator,
    IExecutionAnalyzer,
    IFeedbackGenerator,
    IKnowledgeExtractor,
    IPlanAnalyzer,
    IReasoningAnalyzer,
    IRecommendationEngine,
    IReflectionEngine,
    IReflectionRepository,
    IToolUsageAnalyzer,
)
from app.agents.reflection.knowledge_extractor import KnowledgeExtractor
from app.agents.reflection.latency_evaluator import LatencyEvaluator
from app.agents.reflection.learning_artifact import LearningArtifact, LearningArtifactType
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.manager import ReflectionManager
from app.agents.reflection.memory_evaluator import MemoryEvaluator
from app.agents.reflection.memory_feedback import MemoryFeedback, MemoryUpdateRequest
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionMetadata, ReflectionStatistics
from app.agents.reflection.metrics import ReflectionMetrics, ReflectionMetricsCollector
from app.agents.reflection.orchestrator import ReflectionOrchestrator
from app.agents.reflection.pattern_detector import DetectedPattern, PatternDetector
from app.agents.reflection.performance_analyzer import PerformanceAnalyzer
from app.agents.reflection.plan_analyzer import PlanAnalyzer
from app.agents.reflection.planner_feedback import PlannerCritiqueItem, PlannerFeedback
from app.agents.reflection.quality_evaluator import QualityEvaluator
from app.agents.reflection.ranking import AlternativeRanker, RankedItem
from app.agents.reflection.reasoning_analyzer import ReasoningAnalyzer
from app.agents.reflection.reasoning_validator import ReasoningValidator
from app.agents.reflection.recommendation_engine import (
    Recommendation,
    RecommendationEngine,
    SubsystemTarget,
)
from app.agents.reflection.reflection import Reflection
from app.agents.reflection.reflection_context import (
    DecisionTrace,
    ExecutionTraceEnvelope,
    ReasoningStepTrace,
    TaskTrace,
    ToolCallTrace,
)
from app.agents.reflection.reflection_graph import ReflectionEdge, ReflectionGraph, ReflectionNode
from app.agents.reflection.reflection_session import ReflectionSession
from app.agents.reflection.repository import (
    EvaluationRepository,
    InMemoryEvaluationRepository,
    InMemoryLearningArtifactRepository,
    InMemoryRecommendationRepository,
    InMemoryReflectionRepository,
    LearningArtifactRepository,
    RecommendationRepository,
)
from app.agents.reflection.resource_analyzer import ResourceAnalyzer
from app.agents.reflection.risk_evaluator import RiskEvaluator
from app.agents.reflection.root_cause import ReflectionRootCauseAnalyzer, SystemicRootCause
from app.agents.reflection.runtime import ReflectionRuntime
from app.agents.reflection.scoring import CompositeScorer
from app.agents.reflection.self_critique import CritiqueFinding, SelfCritique
from app.agents.reflection.serialization import ReflectionSerializer
from app.agents.reflection.success_analyzer import SuccessAnalyzer
from app.agents.reflection.token_evaluator import TokenEvaluator
from app.agents.reflection.tool_feedback import ToolFeedback, ToolPerformanceFeedback
from app.agents.reflection.tool_usage_analyzer import ToolUsageAnalyzer
from app.agents.reflection.trend_analyzer import TrendAnalyzer, TrendReport
from app.agents.reflection.validation import ReflectionRequestValidator, ReflectionValidationReport
from app.agents.reflection.validators import ReflectionValidator

__all__ = [
    "ReflectionEngine",
    "ReflectionRuntime",
    "ReflectionManager",
    "ReflectionOrchestrator",
    "ReflectionFactory",
    "Reflection",
    "ReflectionSession",
    "ReflectionContext",
    "ReflectionRequest",
    "ReflectionResult",
    "ReflectionLifecycleState",
    "ReflectionIdentity",
    "ReflectionMetadata",
    "ReflectionStatistics",
    "EvaluationReport",
    "EvaluationPipeline",
    "EvaluationGraph",
    "EvaluationDimension",
    "EvaluationMetric",
    "DimensionEvaluation",
    "SelfCritique",
    "CritiqueFinding",
    "CritiqueEngine",
    "ReasoningValidator",
    "HallucinationDetector",
    "InconsistencyDetector",
    "LearningArtifact",
    "LearningArtifactType",
    "KnowledgeExtractor",
    "Recommendation",
    "RecommendationEngine",
    "SubsystemTarget",
    "AdaptationProposal",
    "AdaptationEngine",
    "AdaptationType",
    "AdaptationStatus",
    "PlannerFeedback",
    "ExecutionFeedback",
    "MemoryFeedback",
    "ToolFeedback",
    "FeedbackGenerator",
    "SubsystemFeedbackBundle",
    "PatternDetector",
    "DetectedPattern",
    "TrendAnalyzer",
    "TrendReport",
    "ReflectionRootCauseAnalyzer",
    "SystemicRootCause",
    "CorrelationAnalyzer",
    "ComparativeAnalyzer",
    "ComparisonResult",
    "BenchmarkEvaluator",
    "BenchmarkCriteria",
    "BenchmarkReport",
    "CompositeScorer",
    "AlternativeRanker",
    "RankedItem",
    "ReflectionSerializer",
    "ReflectionValidator",
    "ReflectionRequestValidator",
    "ReflectionValidationReport",
    "ReflectionRequestBuilder",
    "LearningArtifactBuilder",
    "RecommendationBuilder",
    "CritiqueBuilder",
    "EvaluationBuilder",
    "FeedbackBuilder",
    "ReflectionSessionBuilder",
    "InMemoryReflectionRepository",
    "InMemoryEvaluationRepository",
    "InMemoryLearningArtifactRepository",
    "InMemoryRecommendationRepository",
    "ReflectionCache",
    "ReflectionMetrics",
    "ReflectionMetricsCollector",
    "ExecutionTraceEnvelope",
    "TaskTrace",
    "ToolCallTrace",
    "ReasoningStepTrace",
    "DecisionTrace",
    # Autonomous Reflection OS (Phase 25.0)
    "ReflectionAgent",
    "QualityEvaluation",
    "SelfCorrectionTrigger",
    "CorrectionAction",
]

from app.agents.reflection.reflection_agent import (
    ReflectionAgent,
    QualityEvaluation,
    SelfCorrectionTrigger,
    CorrectionAction,
)

