"""
First-Class AgentTask Domain Abstraction.
Defines executable task models (OCR, Extraction, Validation, Storage, Classification, etc.).
Tasks describe executable work without containing execution logic directly.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field

from app.agents.domain.capabilities import CapabilityRequirement
from app.agents.domain.constraints import DomainConstraint
from app.agents.domain.dependencies import TaskDependencyRelation
from app.agents.domain.enums import ExecutionStatus, PriorityLevel, TaskType
from app.agents.domain.policies import ExecutionPolicy
from app.agents.domain.resources import ExecutionResources
from app.agents.domain.value_objects import (
    ExecutionCost,
    ExecutionDuration,
    GoalID,
    TaskID,
)


class AgentTask(BaseModel):
    """Abstract executable task specification model."""

    task_id: TaskID = Field(default_factory=TaskID)
    goal_id: GoalID = Field(default_factory=GoalID)
    task_type: TaskType = Field(default=TaskType.CUSTOM)
    name: str = Field(default="AgentTask")
    description: str = Field(default="")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)
    
    dependencies: List[TaskDependencyRelation] = Field(default_factory=list)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    expected_artifacts: List[str] = Field(default_factory=list)
    
    execution_policy: ExecutionPolicy = Field(default_factory=ExecutionPolicy)
    estimated_cost: ExecutionCost = Field(default_factory=ExecutionCost)
    estimated_duration: ExecutionDuration = Field(default_factory=ExecutionDuration)
    
    required_capabilities: CapabilityRequirement = Field(default_factory=CapabilityRequirement)
    required_resources: ExecutionResources = Field(default_factory=ExecutionResources)
    execution_constraints: List[DomainConstraint] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OCRTask(AgentTask):
    """OCR text extraction task specification."""
    task_type: TaskType = TaskType.OCR
    name: str = Field(default="OCR Extraction Task")
    language: str = Field(default="eng")


class ExtractionTask(AgentTask):
    """AI structured extraction task specification."""
    task_type: TaskType = TaskType.EXTRACTION
    name: str = Field(default="Structured AI Extraction Task")
    document_type: str = Field(default="generic")
    json_schema: Dict[str, Any] = Field(default_factory=dict)


class ValidationTask(AgentTask):
    """Data and constraint validation task specification."""
    task_type: TaskType = TaskType.VALIDATION
    name: str = Field(default="Data Validation Task")


class StorageTask(AgentTask):
    """Database and object storage task specification."""
    task_type: TaskType = TaskType.STORAGE
    name: str = Field(default="Artifact Storage Task")


class NotificationTask(AgentTask):
    """Event and web notification task specification."""
    task_type: TaskType = TaskType.NOTIFICATION
    name: str = Field(default="Notification Task")


class ClassificationTask(AgentTask):
    """Document classification task specification."""
    task_type: TaskType = TaskType.CLASSIFICATION
    name: str = Field(default="Document Classification Task")


class SummarizationTask(AgentTask):
    """Text summarization task specification."""
    task_type: TaskType = TaskType.SUMMARIZATION
    name: str = Field(default="Text Summarization Task")


class TransformationTask(AgentTask):
    """Data transformation task specification."""
    task_type: TaskType = TaskType.TRANSFORMATION
    name: str = Field(default="Data Transformation Task")


class ReviewTask(AgentTask):
    """Human or automated review task specification."""
    task_type: TaskType = TaskType.REVIEW
    name: str = Field(default="Review Task")


class ArchiveTask(AgentTask):
    """Long-term archiving task specification."""
    task_type: TaskType = TaskType.ARCHIVE
    name: str = Field(default="Archive Task")


class CustomTask(AgentTask):
    """Custom user-defined task specification."""
    task_type: TaskType = TaskType.CUSTOM
    name: str = Field(default="Custom Task")
