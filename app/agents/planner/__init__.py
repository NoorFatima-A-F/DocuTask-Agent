"""
Enterprise Intelligent Planner & Hierarchical Task Decomposition Engine Package.
Provides IntelligentPlanner, PlanningPipeline, HierarchicalTaskDecomposer, GoalAnalyzer,
CandidatePlanGenerator, PlanOptimizer, PlannerReflectionEngine, PlanRepairEngine, and PlannerFactory.
Synthesizes validated executable PlanGraphs from high-level goals without performing tool execution or holding business rules.
"""

from app.agents.planner.branching import BranchPlanner
from app.agents.planner.builders import (
    CandidatePlanBuilder,
    PlannerContextBuilder,
    PlannerRequestBuilder,
    PlanningEvidenceBuilder,
    PlanningTraceBuilder,
)
from app.agents.planner.cache import PlannerCache
from app.agents.planner.candidate_generator import CandidatePlanGenerator
from app.agents.planner.confidence import PlanConfidenceEstimator
from app.agents.planner.constraint_resolver import ConstraintResolver
from app.agents.planner.context import PlannerContext, PlannerRequest
from app.agents.planner.critical_path import CriticalPathPlanner
from app.agents.planner.decision_adapter import PlannerDecisionAdapter
from app.agents.planner.decomposer import HierarchicalTaskDecomposer
from app.agents.planner.dependency_resolver import DependencyResolver
from app.agents.planner.engine import PlanningEngine
from app.agents.planner.evaluation import CandidateEvaluator
from app.agents.planner.events import (
    GoalAnalyzedEvent,
    PlanCompletedEvent,
    PlanGeneratedEvent,
    PlanningFailedEvent,
    PlanningStartedEvent,
    PlanOptimizedEvent,
    PlanRankedEvent,
    PlanRepairedEvent,
    PlanValidatedEvent,
    TasksDecomposedEvent,
)
from app.agents.planner.exceptions import (
    AdapterIntegrationException,
    CandidateGenerationException,
    GoalAnalysisException,
    PlannerException,
    PlanReflectionException,
    PlanRepairException,
    TaskDecompositionException,
)
from app.agents.planner.factory import PlannerFactory
from app.agents.planner.fallback import FallbackPlanGenerator
from app.agents.planner.goal_analyzer import GoalAnalysisReport, GoalAnalyzer
from app.agents.planner.goal_normalizer import GoalNormalizer
from app.agents.planner.hierarchy import (
    AbstractionLevel,
    DecompositionNode,
    DecompositionTree,
)
from app.agents.planner.interfaces import IIntelligentPlanner, IPlanningPipeline
from app.agents.planner.lifecycle import PlannerLifecycleState
from app.agents.planner.llm_adapter import ILLMPlanningAdapter, MockLLMPlanningAdapter
from app.agents.planner.manager import PlannerManager
from app.agents.planner.memory_adapter import PlannerMemoryAdapter
from app.agents.planner.metadata import (
    CandidatePlan,
    PlanningEvidence,
    PlanningTrace,
    RejectedAlternative,
)
from app.agents.planner.metrics import PlannerMetricRecord, PlannerMetricsCollector
from app.agents.planner.orchestrator import PlanningOrchestrator
from app.agents.planner.parallelization import ParallelizationOptimizer
from app.agents.planner.pipeline import PlanningPipeline
from app.agents.planner.plan_merger import PlanMerger
from app.agents.planner.plan_optimizer import PlanOptimizer
from app.agents.planner.plan_ranker import PlanRanker
from app.agents.planner.planner import IntelligentPlanner
from app.agents.planner.prompt_builder import PlanningPromptBuilder
from app.agents.planner.reasoning import PlanningReasoningLog, PlanningReasoningStep
from app.agents.planner.reflection import PlannerReflectionEngine, ReflectionCritique
from app.agents.planner.repair import PlanRepairEngine
from app.agents.planner.repository import PlannerRepository
from app.agents.planner.resource_planner import ResourcePlanner
from app.agents.planner.scoring import PlanCandidateScorer
from app.agents.planner.serialization import PlannerSerializer
from app.agents.planner.strategies import (
    HierarchicalPlanningStrategy,
    LeastCostPlanningStrategy,
    LLMGuidedPlanningStrategy,
    TopDownPlanningStrategy,
)
from app.agents.planner.strategy import PlanningStrategy
from app.agents.planner.task_analyzer import TaskAnalysisResult, TaskAnalyzer
from app.agents.planner.timeline_planner import TimelinePlanner
from app.agents.planner.tool_adapter import PlannerToolAdapter
from app.agents.planner.validation import PlannerPlanValidator
from app.agents.planner.validators import PlannerRequestValidator

__all__ = [
    # Core Planner & Pipeline
    "IIntelligentPlanner",
    "IPlanningPipeline",
    "IntelligentPlanner",
    "PlanningPipeline",
    "PlanningEngine",
    "PlanningOrchestrator",
    "PlannerManager",
    "PlannerLifecycleState",
    "PlannerContext",
    "PlannerRequest",
    # Goal Analysis & Normalization
    "GoalAnalyzer",
    "GoalAnalysisReport",
    "GoalNormalizer",
    "TaskAnalyzer",
    "TaskAnalysisResult",
    # Hierarchical Decomposition
    "HierarchicalTaskDecomposer",
    "DecompositionTree",
    "DecompositionNode",
    "AbstractionLevel",
    # Resolvers & Sub-Planners
    "DependencyResolver",
    "ConstraintResolver",
    "ResourcePlanner",
    "TimelinePlanner",
    "CriticalPathPlanner",
    "ParallelizationOptimizer",
    "BranchPlanner",
    # Candidate Generation & Ranking
    "CandidatePlanGenerator",
    "CandidatePlan",
    "CandidateEvaluator",
    "PlanRanker",
    "PlanOptimizer",
    "PlanMerger",
    "PlanCandidateScorer",
    "PlanConfidenceEstimator",
    # Reflection & Repair & Fallback
    "PlannerReflectionEngine",
    "ReflectionCritique",
    "PlanRepairEngine",
    "FallbackPlanGenerator",
    # Strategies
    "PlanningStrategy",
    "HierarchicalPlanningStrategy",
    "TopDownPlanningStrategy",
    "LeastCostPlanningStrategy",
    "LLMGuidedPlanningStrategy",
    # Reasoning & Evidence & Metadata
    "PlanningReasoningStep",
    "PlanningReasoningLog",
    "PlanningEvidence",
    "RejectedAlternative",
    "PlanningTrace",
    # Adapters & Prompts
    "ILLMPlanningAdapter",
    "MockLLMPlanningAdapter",
    "PlannerMemoryAdapter",
    "PlannerDecisionAdapter",
    "PlannerToolAdapter",
    "PlanningPromptBuilder",
    # Validation & Storage & Factory
    "PlannerPlanValidator",
    "PlannerRequestValidator",
    "PlannerSerializer",
    "PlannerCache",
    "PlannerRepository",
    "PlannerMetricsCollector",
    "PlannerMetricRecord",
    "PlannerFactory",
    # Fluent Builders
    "PlannerContextBuilder",
    "PlannerRequestBuilder",
    "CandidatePlanBuilder",
    "PlanningEvidenceBuilder",
    "PlanningTraceBuilder",
    # Events
    "PlanningStartedEvent",
    "GoalAnalyzedEvent",
    "TasksDecomposedEvent",
    "PlanGeneratedEvent",
    "PlanValidatedEvent",
    "PlanOptimizedEvent",
    "PlanRankedEvent",
    "PlanRepairedEvent",
    "PlanCompletedEvent",
    "PlanningFailedEvent",
    # Exceptions
    "PlannerException",
    "GoalAnalysisException",
    "TaskDecompositionException",
    "CandidateGenerationException",
    "PlanReflectionException",
    "PlanRepairException",
    "AdapterIntegrationException",
]
