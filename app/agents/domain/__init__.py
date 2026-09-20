"""
Enterprise Agent Domain Model Package.
Provides strongly typed domain contracts for goals, tasks, results, workflows, artifacts,
policies, constraints, dependencies, resources, capabilities, value objects, builders, and validators.
"""

from app.agents.domain.artifacts import ExecutionArtifact
from app.agents.domain.builders import (
    GoalBuilder,
    PolicyBuilder,
    TaskBuilder,
    WorkflowBuilder,
)
from app.agents.domain.capabilities import AgentCapability, CapabilityRequirement
from app.agents.domain.constraints import (
    BudgetConstraint,
    ConfidenceConstraint,
    DomainConstraint,
    TimeConstraint,
    TokenConstraint,
)
from app.agents.domain.dependencies import TaskDependencyRelation
from app.agents.domain.enums import (
    ArtifactType,
    CapabilityType,
    ConstraintType,
    DependencyType,
    ExecutionStatus,
    GoalType,
    PriorityLevel,
    ResultStatus,
    RetryStrategy,
    TaskType,
    WorkflowType,
)
from app.agents.domain.goals import Goal, GoalMetadata
from app.agents.domain.policies import (
    CheckpointPolicy,
    ConcurrencyPolicy,
    ExecutionPolicy,
    FailurePolicy,
    FallbackPolicy,
    HumanReviewPolicy,
    RetryPolicy,
    TimeoutPolicy,
)
from app.agents.domain.resources import ExecutionResources
from app.agents.domain.results import (
    AgentResult,
    BaseDomainResult,
    ExecutionResult,
    GoalResult,
    ObservationResult,
    PlanningResult,
    RecoveryResult,
    ReflectionResult,
    TaskResult,
    ToolSelectionResult,
    ValidationResult,
    WorkflowResult,
)
from app.agents.domain.tasks import (
    AgentTask,
    ArchiveTask,
    ClassificationTask,
    CustomTask,
    ExtractionTask,
    NotificationTask,
    OCRTask,
    ReviewTask,
    StorageTask,
    SummarizationTask,
    TransformationTask,
    ValidationTask,
)
from app.agents.domain.validators import DomainValidationException, DomainValidator
from app.agents.domain.value_objects import (
    ArtifactID,
    ConfidenceScore,
    CorrelationID,
    ExecutionCost,
    ExecutionDuration,
    ExecutionID,
    GoalID,
    Latency,
    RetryCount,
    TaskID,
    TokenUsage,
    WorkflowID,
)
from app.agents.domain.workflows import (
    WorkflowEdge,
    WorkflowGraph,
    WorkflowNode,
    WorkflowSnapshot,
    WorkflowStage,
    WorkflowTemplate,
)

__all__ = [
    # Enumerations
    "GoalType",
    "TaskType",
    "WorkflowType",
    "ResultStatus",
    "ExecutionStatus",
    "PriorityLevel",
    "ArtifactType",
    "RetryStrategy",
    "DependencyType",
    "ConstraintType",
    "CapabilityType",
    # Value Objects
    "GoalID",
    "TaskID",
    "WorkflowID",
    "ExecutionID",
    "CorrelationID",
    "ArtifactID",
    "ConfidenceScore",
    "ExecutionDuration",
    "RetryCount",
    "TokenUsage",
    "ExecutionCost",
    "Latency",
    # Goals
    "Goal",
    "GoalMetadata",
    # Tasks
    "AgentTask",
    "OCRTask",
    "ExtractionTask",
    "ValidationTask",
    "StorageTask",
    "NotificationTask",
    "ClassificationTask",
    "SummarizationTask",
    "TransformationTask",
    "ReviewTask",
    "ArchiveTask",
    "CustomTask",
    # Results
    "BaseDomainResult",
    "PlanningResult",
    "ExecutionResult",
    "ObservationResult",
    "ReflectionResult",
    "RecoveryResult",
    "TaskResult",
    "ValidationResult",
    "ToolSelectionResult",
    "WorkflowResult",
    "GoalResult",
    "AgentResult",
    # Workflows
    "WorkflowNode",
    "WorkflowEdge",
    "WorkflowGraph",
    "WorkflowStage",
    "WorkflowTemplate",
    "WorkflowSnapshot",
    # Dependencies & Policies & Constraints
    "TaskDependencyRelation",
    "ExecutionPolicy",
    "RetryPolicy",
    "TimeoutPolicy",
    "ConcurrencyPolicy",
    "FailurePolicy",
    "HumanReviewPolicy",
    "FallbackPolicy",
    "CheckpointPolicy",
    "DomainConstraint",
    "TimeConstraint",
    "BudgetConstraint",
    "TokenConstraint",
    "ConfidenceConstraint",
    # Artifacts & Resources & Capabilities
    "ExecutionArtifact",
    "ExecutionResources",
    "AgentCapability",
    "CapabilityRequirement",
    # Validators & Builders
    "DomainValidator",
    "DomainValidationException",
    "GoalBuilder",
    "TaskBuilder",
    "WorkflowBuilder",
    "PolicyBuilder",
]
