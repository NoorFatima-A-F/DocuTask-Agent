"""
Autonomous Reflection, Learning, Policy Evolution & Knowledge Intelligence Platform (ARLP-KIP).
Phase 13.5: Provides autonomous reflection across missions, pattern mining, institutional rule extraction,
knowledge graphs and indexes, versioned policy generation with counterfactual evaluation,
multi-stage governance pipelines, and cryptographic lineage tracking.
"""

# Legacy imports preserved for backward compatibility
from app.runtime.learning.weight_learner import WeightProposal, AdaptiveWeightLearner
from app.runtime.learning.policy_store import VersionedPolicy, PolicyStore, policy_store
from app.runtime.learning.adaptive_policy import AdaptivePolicyManager

# Phase 13.5 Domain Events
from app.runtime.learning.events.learning_events import (
    LearningDomainEvent,
    ReflectionStarted,
    ReflectionCompleted,
    PatternDetected,
    KnowledgeExtracted,
    LessonPublished,
    PolicyProposed,
    PolicyApproved,
    PolicyRejected,
    KnowledgeVersionCreated,
    KnowledgeDeprecated,
    StrategyGenerated,
    StrategyAdopted,
    LearningCompleted,
)

# Phase 13.5 Reflection Subsystem
from app.runtime.learning.reflection.reflection_engine import ReflectionEngine, reflection_engine, MissionReflectionReport
from app.runtime.learning.reflection.mission_reflector import MissionReflector, MacroKPIs
from app.runtime.learning.reflection.planner_reflector import PlannerReflector, PlannerReflectionMetrics
from app.runtime.learning.reflection.worker_reflector import WorkerReflector, WorkerReflectionMetrics
from app.runtime.learning.reflection.confidence_reflector import ConfidenceReflector, ConfidenceReflectionMetrics
from app.runtime.learning.reflection.failure_reflector import FailureReflector, FailureEpisode
from app.runtime.learning.reflection.success_reflector import SuccessReflector, SuccessEpisode
from app.runtime.learning.reflection.reflection_validator import ReflectionValidator, ReflectionValidationResult

# Phase 13.5 Learning Subsystem
from app.runtime.learning.learning.learning_engine import LearningEngine, learning_engine, MinedLesson
from app.runtime.learning.learning.pattern_miner import PatternMiner, ExecutionPattern
from app.runtime.learning.learning.lesson_extractor import LessonExtractor, ExtractedRule
from app.runtime.learning.learning.strategy_builder import StrategyBuilder, ExecutionStrategy
from app.runtime.learning.learning.knowledge_compiler import KnowledgeCompiler, CompiledKnowledgeBundle
from app.runtime.learning.learning.experience_ranker import ExperienceRanker, RankedExperience
from app.runtime.learning.learning.learning_validator import LearningValidator, LearningValidationResult

# Phase 13.5 Knowledge Subsystem
from app.runtime.learning.knowledge.knowledge_registry import KnowledgeRegistry, knowledge_registry, KnowledgeRecord
from app.runtime.learning.knowledge.knowledge_graph import KnowledgeGraph, knowledge_graph, KnowledgeNode, KnowledgeEdge
from app.runtime.learning.knowledge.knowledge_index import KnowledgeIndex, knowledge_index, SearchIndexEntry
from app.runtime.learning.knowledge.knowledge_search import KnowledgeSearchEngine, knowledge_search_engine, SearchMatch
from app.runtime.learning.knowledge.knowledge_versioning import KnowledgeVersioning, KnowledgeVersionRecord
from app.runtime.learning.knowledge.knowledge_lineage import KnowledgeLineageTracker, knowledge_lineage_tracker, LineageRecord
from app.runtime.learning.knowledge.knowledge_validator import KnowledgeValidator, KnowledgeValidationResult

# Phase 13.5 Policy Subsystem
from app.runtime.learning.policy.policy_engine import PolicyEngine, policy_engine, CandidatePolicy
from app.runtime.learning.policy.policy_generator import PolicyGenerator, PolicyAdjustment
from app.runtime.learning.policy.policy_evaluator import PolicyEvaluator, PolicySimulationResult
from app.runtime.learning.policy.policy_comparator import PolicyComparator, PolicyComparisonReport
from app.runtime.learning.policy.policy_validator import PolicyValidator, PolicyValidationResult
from app.runtime.learning.policy.policy_registry import EvolutionPolicyRegistry, evolution_policy_registry, ActivePolicyEntry
from app.runtime.learning.policy.policy_versioning import PolicyBranchVersioner, PolicyVersionEntry

# Phase 13.5 Governance Subsystem
from app.runtime.learning.governance.learning_governance import LearningGovernanceGatekeeper, learning_governance_gatekeeper, GovernanceEvaluation
from app.runtime.learning.governance.approval_workflow import ApprovalWorkflowManager, approval_workflow_manager, ReviewRecord
from app.runtime.learning.governance.promotion_pipeline import PromotionPipelineManager, promotion_pipeline_manager, PromotionRecord
from app.runtime.learning.governance.rollback_manager import RollbackManager, rollback_manager, RollbackRecord
from app.runtime.learning.governance.policy_guardrails import PolicyGuardrailsValidator, GuardrailEnforcement
from app.runtime.learning.governance.risk_assessment import RiskAssessmentEngine, RiskScoreResult

__all__ = [
    # Legacy
    "WeightProposal",
    "AdaptiveWeightLearner",
    "VersionedPolicy",
    "PolicyStore",
    "policy_store",
    "AdaptivePolicyManager",
    # Events
    "LearningDomainEvent",
    "ReflectionStarted",
    "ReflectionCompleted",
    "PatternDetected",
    "KnowledgeExtracted",
    "LessonPublished",
    "PolicyProposed",
    "PolicyApproved",
    "PolicyRejected",
    "KnowledgeVersionCreated",
    "KnowledgeDeprecated",
    "StrategyGenerated",
    "StrategyAdopted",
    "LearningCompleted",
    # Reflection
    "ReflectionEngine",
    "reflection_engine",
    "MissionReflectionReport",
    "MissionReflector",
    "MacroKPIs",
    "PlannerReflector",
    "PlannerReflectionMetrics",
    "WorkerReflector",
    "WorkerReflectionMetrics",
    "ConfidenceReflector",
    "ConfidenceReflectionMetrics",
    "FailureReflector",
    "FailureEpisode",
    "SuccessReflector",
    "SuccessEpisode",
    "ReflectionValidator",
    "ReflectionValidationResult",
    # Learning
    "LearningEngine",
    "learning_engine",
    "MinedLesson",
    "PatternMiner",
    "ExecutionPattern",
    "LessonExtractor",
    "ExtractedRule",
    "StrategyBuilder",
    "ExecutionStrategy",
    "KnowledgeCompiler",
    "CompiledKnowledgeBundle",
    "ExperienceRanker",
    "RankedExperience",
    "LearningValidator",
    "LearningValidationResult",
    # Knowledge
    "KnowledgeRegistry",
    "knowledge_registry",
    "KnowledgeRecord",
    "KnowledgeGraph",
    "knowledge_graph",
    "KnowledgeNode",
    "KnowledgeEdge",
    "KnowledgeIndex",
    "knowledge_index",
    "SearchIndexEntry",
    "KnowledgeSearchEngine",
    "knowledge_search_engine",
    "SearchMatch",
    "KnowledgeVersioning",
    "KnowledgeVersionRecord",
    "KnowledgeLineageTracker",
    "knowledge_lineage_tracker",
    "LineageRecord",
    "KnowledgeValidator",
    "KnowledgeValidationResult",
    # Policy
    "PolicyEngine",
    "policy_engine",
    "CandidatePolicy",
    "PolicyGenerator",
    "PolicyAdjustment",
    "PolicyEvaluator",
    "PolicySimulationResult",
    "PolicyComparator",
    "PolicyComparisonReport",
    "PolicyValidator",
    "PolicyValidationResult",
    "EvolutionPolicyRegistry",
    "evolution_policy_registry",
    "ActivePolicyEntry",
    "PolicyBranchVersioner",
    "PolicyVersionEntry",
    # Governance
    "LearningGovernanceGatekeeper",
    "learning_governance_gatekeeper",
    "GovernanceEvaluation",
    "ApprovalWorkflowManager",
    "approval_workflow_manager",
    "ReviewRecord",
    "PromotionPipelineManager",
    "promotion_pipeline_manager",
    "PromotionRecord",
    "RollbackManager",
    "rollback_manager",
    "RollbackRecord",
    "PolicyGuardrailsValidator",
    "GuardrailEnforcement",
    "RiskAssessmentEngine",
    "RiskScoreResult",
]
