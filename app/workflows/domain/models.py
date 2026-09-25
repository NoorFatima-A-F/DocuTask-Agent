"""
Enterprise Workflow Orchestration Engine Domain Models.
Complete declarative workflow specifications, lifecycle state machines, execution contexts, and task definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from ...platform.kernel.versioning import SemanticVersion


class WorkflowLifecycleState(str, Enum):
    """15 formal lifecycle states of a workflow definition."""
    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    REGISTERED = "REGISTERED"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    RESUMED = "RESUMED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    ARCHIVED = "ARCHIVED"
    DEPRECATED = "DEPRECATED"


class ExecutionState(str, Enum):
    """Execution lifecycle of a specific workflow instance."""
    CREATED = "CREATED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    SUSPENDED = "SUSPENDED"
    RETRYING = "RETRYING"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TaskType(str, Enum):
    """17 generic platform task types."""
    SYSTEM = "SYSTEM"
    AI = "AI"
    CONNECTOR = "CONNECTOR"
    HUMAN = "HUMAN"
    APPROVAL = "APPROVAL"
    TIMER = "TIMER"
    EVENT = "EVENT"
    CONDITION = "CONDITION"
    LOOP = "LOOP"
    SUBWORKFLOW = "SUBWORKFLOW"
    WEBHOOK = "WEBHOOK"
    NOTIFICATION = "NOTIFICATION"
    TRANSFORM = "TRANSFORM"
    VALIDATION = "VALIDATION"
    MEMORY = "MEMORY"
    REFLECTION = "REFLECTION"
    PARALLEL = "PARALLEL"


class TaskPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"
    BACKGROUND = "BACKGROUND"


@dataclass
class TaskDefinition:
    """Declarative task specification within a workflow."""
    id: str
    name: str
    type: TaskType = TaskType.SYSTEM
    capability: Optional[str] = None  # e.g., 'document.ocr', 'ai.reasoning'
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    timeout_seconds: int = 60
    retry_policy: Dict[str, Any] = field(default_factory=lambda: {"max_attempts": 3, "backoff": "exponential"})
    compensation_action: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "capability": self.capability,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "priority": self.priority.value,
            "timeout_seconds": self.timeout_seconds,
            "retry_policy": self.retry_policy,
            "compensation_action": self.compensation_action,
            "dependencies": self.dependencies,
            "conditions": self.conditions,
            "metadata": self.metadata,
        }


@dataclass
class WorkflowDefinition:
    """Declarative definition of an enterprise workflow."""
    id: str
    name: str
    version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    organization_id: str = "default_org"
    owner: str = "platform_admin"
    description: str = ""
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    visibility: str = "organization"  # private, workspace, organization, public
    status: WorkflowLifecycleState = WorkflowLifecycleState.CREATED
    trigger: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    tasks: List[TaskDefinition] = field(default_factory=list)
    policies: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 3600
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    approval_policy: Dict[str, Any] = field(default_factory=dict)
    compensation_policy: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": str(self.version),
            "organization_id": self.organization_id,
            "owner": self.owner,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "visibility": self.visibility,
            "status": self.status.value,
            "trigger": self.trigger,
            "variables": self.variables,
            "tasks": [t.to_dict() for t in self.tasks],
            "policies": self.policies,
            "timeout_seconds": self.timeout_seconds,
            "retry_policy": self.retry_policy,
            "approval_policy": self.approval_policy,
            "compensation_policy": self.compensation_policy,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class WorkflowContext:
    """Execution context and boundary envelope for a running workflow."""
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str = ""
    workflow_version: str = "1.0.0"
    organization_id: str = "default_org"
    workspace_id: str = "default_workspace"
    actor: str = "system"
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    deadline: Optional[datetime] = None
    permissions: List[str] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    feature_flags: Dict[str, bool] = field(default_factory=dict)
    parent_execution: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "workflow_version": self.workflow_version,
            "organization_id": self.organization_id,
            "workspace_id": self.workspace_id,
            "actor": self.actor,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "permissions": self.permissions,
            "variables": self.variables,
            "feature_flags": self.feature_flags,
            "parent_execution": self.parent_execution,
        }


@dataclass
class TaskExecutionRecord:
    """Runtime execution record of a single task."""
    task_id: str
    task_name: str
    status: ExecutionState = ExecutionState.READY
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    attempts: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    compensation_status: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "attempts": self.attempts,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "error_message": self.error_message,
            "compensation_status": self.compensation_status,
        }


@dataclass
class Checkpoint:
    """Immutable checkpoint of a running workflow for crash recovery."""
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str = ""
    execution_state: ExecutionState = ExecutionState.RUNNING
    variables: Dict[str, Any] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    pending_tasks: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "execution_id": self.execution_id,
            "execution_state": self.execution_state.value,
            "variables": self.variables,
            "completed_tasks": self.completed_tasks,
            "pending_tasks": self.pending_tasks,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ExecutionRecord:
    """Durable state record of a workflow execution instance."""
    execution_id: str
    workflow_id: str
    workflow_version: str
    status: ExecutionState = ExecutionState.CREATED
    context: WorkflowContext = field(default_factory=WorkflowContext)
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    tasks: Dict[str, TaskExecutionRecord] = field(default_factory=dict)
    current_checkpoint_id: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "workflow_version": self.workflow_version,
            "status": self.status.value,
            "context": self.context.to_dict(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "tasks": {k: v.to_dict() for k, v in self.tasks.items()},
            "current_checkpoint_id": self.current_checkpoint_id,
            "error_message": self.error_message,
        }
