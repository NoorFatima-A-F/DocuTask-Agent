"""
Autonomous Goal Intelligence & Mission Management System
========================================================
Stage 1 of the Autonomous Cognition Loop:
Goal -> Goal Intelligence -> Mission Definition -> Validation -> Capability Analysis
-> Risk Assessment -> Resource Planning -> Success Criteria -> Mission Graph -> Ready For Observation
"""

from research_validation.goal.constants import NonFabricationState
from research_validation.goal.exceptions import (
    GoalIntelligenceError, GoalValidationError, InvalidStateTransitionError,
    MissingCapabilityError, CircularDependencyError, BudgetExceededError,
    RiskThresholdExceededError, EntityNotFoundError
)
from research_validation.goal.models import (
    Goal, GoalType, PriorityLevel, GoalStatus, GoalConstraints,
    ConfidenceLevel, ConfidenceThreshold, StoppingConditionType, StoppingCondition,
    Comparator, SuccessCriterion, ResourceBudget, ExecutionBudget,
    CapabilityCriticality, CapabilityRequirement, DependencyType, GoalDependency,
    RiskSeverity, RiskItem, RiskProfile, EvidenceRequirement, MissionMetrics,
    MissionState, StateTransitionRecord, MissionStateMachine,
    MissionNode, ActionNode, TaskNode, SubgoalNode, MilestoneNode, ObjectiveNode, Mission
)
from research_validation.goal.interfaces import (
    IClock, SystemClock, FrozenClock, IIdGenerator, Uuid4IdGenerator, DeterministicIdGenerator,
    GoalIntelligenceDomainEvent, IEventBus, InMemoryEventBus, EventHandler,
    IGoalRepository, IMissionRepository, DiscoveredCapability, ICapabilityProvider,
    DefaultSystemCapabilityProvider
)
from research_validation.goal.repositories import (
    InMemoryGoalRepository, InMemoryMissionRepository, SqliteGoalRepository, SqliteMissionRepository
)
from research_validation.goal.services import (
    MissionHashingService, MissionSerializer, ConfidenceEstimatorService, ConstraintEngine,
    CapabilityAnalysisResult, CapabilityAnalyzer, DependencyAnalysisResult, DependencyAnalyzer,
    RiskAssessor, BudgetEstimator, GoalDecomposer, GoalValidationResult, GoalValidator,
    MissionBuilder, GoalManager, MissionRegistry, MissionScheduler
)

__all__ = [
    "NonFabricationState",
    "GoalIntelligenceError",
    "GoalValidationError",
    "InvalidStateTransitionError",
    "MissingCapabilityError",
    "CircularDependencyError",
    "BudgetExceededError",
    "RiskThresholdExceededError",
    "EntityNotFoundError",
    "Goal",
    "GoalType",
    "PriorityLevel",
    "GoalStatus",
    "GoalConstraints",
    "ConfidenceLevel",
    "ConfidenceThreshold",
    "StoppingConditionType",
    "StoppingCondition",
    "Comparator",
    "SuccessCriterion",
    "ResourceBudget",
    "ExecutionBudget",
    "CapabilityCriticality",
    "CapabilityRequirement",
    "DependencyType",
    "GoalDependency",
    "RiskSeverity",
    "RiskItem",
    "RiskProfile",
    "EvidenceRequirement",
    "MissionMetrics",
    "MissionState",
    "StateTransitionRecord",
    "MissionStateMachine",
    "MissionNode",
    "ActionNode",
    "TaskNode",
    "SubgoalNode",
    "MilestoneNode",
    "ObjectiveNode",
    "Mission",
    "IClock",
    "SystemClock",
    "FrozenClock",
    "IIdGenerator",
    "Uuid4IdGenerator",
    "DeterministicIdGenerator",
    "GoalIntelligenceDomainEvent",
    "IEventBus",
    "InMemoryEventBus",
    "EventHandler",
    "IGoalRepository",
    "IMissionRepository",
    "DiscoveredCapability",
    "ICapabilityProvider",
    "DefaultSystemCapabilityProvider",
    "InMemoryGoalRepository",
    "InMemoryMissionRepository",
    "SqliteGoalRepository",
    "SqliteMissionRepository",
    "MissionHashingService",
    "MissionSerializer",
    "ConfidenceEstimatorService",
    "ConstraintEngine",
    "CapabilityAnalysisResult",
    "CapabilityAnalyzer",
    "DependencyAnalysisResult",
    "DependencyAnalyzer",
    "RiskAssessor",
    "BudgetEstimator",
    "GoalDecomposer",
    "GoalValidationResult",
    "GoalValidator",
    "MissionBuilder",
    "GoalManager",
    "MissionRegistry",
    "MissionScheduler",
]
