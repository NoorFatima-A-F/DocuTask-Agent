"""
Enterprise Decision, Policy & Governance Engine Package.
Provides IDecisionEngine, DecisionEngine, DecisionRequest, DecisionResult,
GovernanceFramework, RiskAssessment, DecisionExplanation, and DecisionFactory.
Decouples Planners and Executors from business rule evaluation.
"""

from app.agents.decision.approvals import ApprovalRequirement, ApprovalWorkflow, EscalationRequirement
from app.agents.decision.authorization import AuthorizationPolicy
from app.agents.decision.budgeting import CostBudgetEvaluator
from app.agents.decision.builders import (
    DecisionBuilder,
    ExplanationBuilder,
    OptimizationBuilder,
    PolicyBuilder,
    RecommendationBuilder,
    RuleBuilder,
)
from app.agents.decision.cache import DecisionCache
from app.agents.decision.compliance import ComplianceCheck, ComplianceViolation, PolicyViolation
from app.agents.decision.constraints import PolicyConstraints
from app.agents.decision.context import DecisionContext
from app.agents.decision.costing import CostEstimate
from app.agents.decision.engine import DecisionEngine, DecisionRequest, DecisionResult
from app.agents.decision.evaluator import (
    ConstraintEvaluator,
    DecisionEvaluator,
    PolicyEvaluator,
    RuleEvaluator,
)
from app.agents.decision.events import (
    DecisionApprovedEvent,
    DecisionCompletedEvent,
    DecisionFailedEvent,
    DecisionRejectedEvent,
    DecisionRequestedEvent,
    DecisionStartedEvent,
    EscalationTriggeredEvent,
    PolicyEvaluatedEvent,
    RiskDetectedEvent,
    RuleTriggeredEvent,
)
from app.agents.decision.exceptions import (
    DecisionEvaluationException,
    DecisionException,
    GovernanceException,
    PolicyViolationException,
    RiskThresholdExceededException,
)
from app.agents.decision.explanations import (
    DecisionExplanation,
    DecisionGraph,
    DecisionGraphEdge,
    DecisionGraphNode,
    Evidence,
)
from app.agents.decision.factory import DecisionFactory
from app.agents.decision.governance import GovernanceFramework
from app.agents.decision.interfaces import IDecisionEngine, IPolicyEvaluator, IRuleEvaluator
from app.agents.decision.lifecycle import DecisionLifecycleState
from app.agents.decision.manager import DecisionManager
from app.agents.decision.metadata import (
    DecisionIdentity,
    DecisionMetadata,
    DecisionStatistics,
    DecisionTrace,
)
from app.agents.decision.metrics import DecisionMetricRecord, DecisionMetricsCollector
from app.agents.decision.objectives import StrategicObjective
from app.agents.decision.optimization import (
    OptimizationConstraint,
    OptimizationEngine,
    OptimizationScore,
    OptimizationStrategy,
)
from app.agents.decision.optimization_targets import OptimizationMetric, OptimizationTarget
from app.agents.decision.policies import (
    ApprovalPolicy,
    CompliancePolicy,
    CostPolicy,
    DataPolicy,
    EscalationPolicy,
    ExecutionPolicy,
    HumanReviewPolicy,
    PlannerPolicy,
    PrivacyPolicy,
    ResourcePolicy,
    RetryPolicy,
    SchedulingPolicy,
    SecurityPolicy,
    ToolSelectionPolicy,
    WorkflowPolicy,
)
from app.agents.decision.priorities import PriorityEvaluator
from app.agents.decision.ranking import DecisionRanker
from app.agents.decision.reasoning import ReasoningStep
from app.agents.decision.recommendations import Recommendation, RecommendationEngine
from app.agents.decision.repository import DecisionRepository
from app.agents.decision.risk import RiskAssessment, RiskProfile, RiskScore
from app.agents.decision.rules import (
    BusinessRule,
    ComplianceRule,
    CostRule,
    DecisionRule,
    ExecutionRule,
    PlannerRule,
    RoutingRule,
    RuleGroup,
    SecurityRule,
    ToolRule,
    ValidationRule,
    WorkflowRule,
)
from app.agents.decision.scoring import DecisionScorer
from app.agents.decision.security import SecurityClassification
from app.agents.decision.serializers import DecisionSerializer
from app.agents.decision.simulations import DecisionSimulator
from app.agents.decision.strategies import DecisionStrategy
from app.agents.decision.validators import DecisionValidator

__all__ = [
    # Core Engine & Context
    "IDecisionEngine",
    "IPolicyEvaluator",
    "IRuleEvaluator",
    "DecisionEngine",
    "DecisionRequest",
    "DecisionResult",
    "DecisionContext",
    "DecisionManager",
    "DecisionLifecycleState",
    # Metadata & Statistics & Trace
    "DecisionIdentity",
    "DecisionMetadata",
    "DecisionStatistics",
    "DecisionTrace",
    # Rules & Grouping
    "BusinessRule",
    "DecisionRule",
    "ValidationRule",
    "SecurityRule",
    "ComplianceRule",
    "CostRule",
    "RoutingRule",
    "WorkflowRule",
    "PlannerRule",
    "ToolRule",
    "ExecutionRule",
    "RuleGroup",
    # Evaluators
    "RuleEvaluator",
    "PolicyEvaluator",
    "ConstraintEvaluator",
    "DecisionEvaluator",
    # Policies & Governance
    "ExecutionPolicy",
    "RetryPolicy",
    "CostPolicy",
    "SecurityPolicy",
    "CompliancePolicy",
    "PrivacyPolicy",
    "DataPolicy",
    "ToolSelectionPolicy",
    "WorkflowPolicy",
    "PlannerPolicy",
    "ApprovalPolicy",
    "HumanReviewPolicy",
    "EscalationPolicy",
    "ResourcePolicy",
    "SchedulingPolicy",
    "GovernanceFramework",
    "ApprovalRequirement",
    "EscalationRequirement",
    "ApprovalWorkflow",
    "AuthorizationPolicy",
    "SecurityClassification",
    # Risk & Costing & Budgeting
    "RiskAssessment",
    "RiskProfile",
    "RiskScore",
    "ComplianceCheck",
    "PolicyViolation",
    "ComplianceViolation",
    "CostEstimate",
    "CostBudgetEvaluator",
    "PolicyConstraints",
    # Optimization & Scoring & Recommendations
    "OptimizationTarget",
    "OptimizationMetric",
    "OptimizationConstraint",
    "OptimizationStrategy",
    "OptimizationScore",
    "OptimizationEngine",
    "DecisionScorer",
    "DecisionRanker",
    "Recommendation",
    "RecommendationEngine",
    "StrategicObjective",
    "DecisionStrategy",
    # Explainability & Evidence & Simulations
    "ReasoningStep",
    "Evidence",
    "DecisionGraphNode",
    "DecisionGraphEdge",
    "DecisionGraph",
    "DecisionExplanation",
    "DecisionSimulator",
    # Storage & Serialization & Factory
    "DecisionRepository",
    "DecisionCache",
    "DecisionValidator",
    "DecisionSerializer",
    "DecisionBuilder",
    "RuleBuilder",
    "PolicyBuilder",
    "OptimizationBuilder",
    "RecommendationBuilder",
    "ExplanationBuilder",
    "DecisionMetricsCollector",
    "DecisionMetricRecord",
    "DecisionFactory",
    # Events
    "DecisionRequestedEvent",
    "DecisionStartedEvent",
    "DecisionCompletedEvent",
    "DecisionApprovedEvent",
    "DecisionRejectedEvent",
    "DecisionFailedEvent",
    "PolicyEvaluatedEvent",
    "RuleTriggeredEvent",
    "RiskDetectedEvent",
    "EscalationTriggeredEvent",
    # Exceptions
    "DecisionException",
    "PolicyViolationException",
    "GovernanceException",
    "RiskThresholdExceededException",
    "DecisionEvaluationException",
]
