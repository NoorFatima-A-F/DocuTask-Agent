"""
Autonomous Agent Framework Architecture Package.
Provides production-grade agent lifecycle base classes, validated state machines,
immutable execution context, domain events, configuration models, DI containers,
and the Enterprise Multi-Agent Intelligence Platform (EMAIP).
"""

from app.agents.base.agent import BaseAgent
from app.agents.config import AgentConfig
from app.agents.context import AgentContext, ExecutionMetadata, SharedVariables
from app.agents.dependency.container import AgentContainer
from app.agents.document_agent import DocumentAgent
from app.agents.events import (
    AgentCompletedEvent,
    AgentEvent,
    AgentFailedEvent,
    ExecutionCompletedEvent,
    ExecutionStartedEvent,
    GoalReceivedEvent,
    ObservationCompletedEvent,
    PlanningCompletedEvent,
    PlanningStartedEvent,
    ReflectionStartedEvent,
    RetryRequestedEvent,
)
from app.agents.exceptions import (
    AgentException,
    ConfigurationException,
    ExecutionException,
    InvalidStateTransitionException,
    MemoryException,
    ObservationException,
    PlanningException,
    RecoveryException,
    ReflectionException,
    ToolSelectionException,
    WorkflowException,
)
from app.agents.logging import AgentLogger
from app.agents.metrics import AgentMetricsCollector, NoOpAgentMetricsCollector
from app.agents.observability import AgentObservabilityHook, NoOpAgentObservabilityHook
from app.agents.state import AgentState, AgentStateMachine

# EMAIP Phase 4 Extensions
from app.agents.domain.agent_entity import (
    Agent,
    AgentLifecycleState,
    AgentPlan,
    AgentType,
    GoalModel,
    PlanStep,
    ReasoningSummary,
    TrustLevel,
)
from app.agents.lifecycle.manager import AgentLifecycleEvent, AgentLifecycleManager
from app.agents.registry.agent_registry import AgentRegistry
from app.agents.goals.goal_manager import GoalManager
from app.agents.decomposition.task_decomposer import TaskDecomposer
from app.agents.planning.planning_engine import PlanningEngine
from app.agents.reasoning.reasoning_framework import ReasoningFramework
from app.agents.context.context_manager import CognitiveContext, ContextManager
from app.agents.memory.platform import EnterpriseMemoryPlatform, MemoryTier
from app.agents.skills.skill_registry import AgentSkill, SkillRegistry
from app.agents.communication.message_bus import (
    AgentMessage,
    AgentMessageBus,
    AgentMessageType,
)
from app.agents.collaboration.supervisor import SupervisorAgent, SupervisorExecutionReport
from app.agents.collaboration.worker import WorkerAgent
from app.agents.reflection.reflection_engine import ReflectionEngine, ReflectionReport
from app.agents.critic.critic_engine import CriticEngine, CriticReport
from app.agents.evaluation.evaluation_engine import EvaluationEngine, EvaluationMetrics
from app.agents.confidence.confidence_engine import ConfidenceEngine, ConfidenceReport
from app.agents.human.escalation_engine import (
    EscalationReason,
    EscalationRecord,
    EscalationStatus,
    HumanEscalationEngine,
)
from app.agents.policies.policy_engine import AgentPolicyEngine, PolicyEvaluationResult
from app.agents.governance.governance_manager import (
    AgentGovernanceManager,
    AgentGovernanceRecord,
)
from app.agents.security.safety_layer import AISafetyLayer, SafetyScanResult
from app.agents.scheduling.agent_scheduler import (
    AgentScheduler,
    ScheduledTask,
    TaskPriority,
)
from app.agents.budgeting.budget_manager import (
    AgentResourceUsage,
    BudgetAction,
    BudgetManager,
)
from app.agents.analytics.agent_analytics import AgentAnalytics, FleetAnalyticsSummary
from app.agents.sdk.builder import AgentBuilder

__all__ = [
    # Base
    "BaseAgent",
    "DocumentAgent",
    "AgentConfig",
    "AgentContext",
    "ExecutionMetadata",
    "SharedVariables",
    "AgentContainer",
    "AgentState",
    "AgentStateMachine",
    "AgentLogger",
    "AgentMetricsCollector",
    "NoOpAgentMetricsCollector",
    "AgentObservabilityHook",
    "NoOpAgentObservabilityHook",
    "AgentEvent",
    "GoalReceivedEvent",
    "PlanningStartedEvent",
    "PlanningCompletedEvent",
    "ExecutionStartedEvent",
    "ExecutionCompletedEvent",
    "ObservationCompletedEvent",
    "ReflectionStartedEvent",
    "AgentCompletedEvent",
    "AgentFailedEvent",
    "RetryRequestedEvent",
    "AgentException",
    "InvalidStateTransitionException",
    "PlanningException",
    "ExecutionException",
    "ObservationException",
    "ReflectionException",
    "MemoryException",
    "RecoveryException",
    "ConfigurationException",
    "ToolSelectionException",
    "WorkflowException",
    # EMAIP Phase 4
    "Agent",
    "AgentType",
    "AgentLifecycleState",
    "TrustLevel",
    "GoalModel",
    "PlanStep",
    "AgentPlan",
    "ReasoningSummary",
    "AgentLifecycleManager",
    "AgentLifecycleEvent",
    "AgentRegistry",
    "GoalManager",
    "TaskDecomposer",
    "PlanningEngine",
    "ReasoningFramework",
    "ContextManager",
    "CognitiveContext",
    "EnterpriseMemoryPlatform",
    "MemoryTier",
    "SkillRegistry",
    "AgentSkill",
    "AgentMessageBus",
    "AgentMessage",
    "AgentMessageType",
    "SupervisorAgent",
    "SupervisorExecutionReport",
    "WorkerAgent",
    "ReflectionEngine",
    "ReflectionReport",
    "CriticEngine",
    "CriticReport",
    "EvaluationEngine",
    "EvaluationMetrics",
    "ConfidenceEngine",
    "ConfidenceReport",
    "HumanEscalationEngine",
    "EscalationRecord",
    "EscalationReason",
    "EscalationStatus",
    "AgentPolicyEngine",
    "PolicyEvaluationResult",
    "AgentGovernanceManager",
    "AgentGovernanceRecord",
    "AISafetyLayer",
    "SafetyScanResult",
    "AgentScheduler",
    "ScheduledTask",
    "TaskPriority",
    "BudgetManager",
    "BudgetAction",
    "AgentResourceUsage",
    "AgentAnalytics",
    "FleetAnalyticsSummary",
    "AgentBuilder",
]
