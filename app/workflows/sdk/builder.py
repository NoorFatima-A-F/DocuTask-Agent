"""
Enterprise Workflow Fluent SDK & Builder.
Enables programmatic, type-safe construction of declarative WorkflowDefinitions.
"""

from typing import Any, Dict, List, Optional
import uuid
from ..domain.models import TaskDefinition, TaskPriority, TaskType, WorkflowDefinition
from ...platform.kernel.versioning import SemanticVersion


class WorkflowBuilder:
    """Fluent Builder for Declarative Workflow Definitions."""

    def __init__(self, name: str, workflow_id: Optional[str] = None):
        self.workflow_id = workflow_id or f"wf_{name.lower().replace(' ', '_')}_{str(uuid.uuid4())[:8]}"
        self.name = name
        self.version = SemanticVersion(1, 0, 0)
        self.description = ""
        self.category = "custom"
        self.tags: List[str] = []
        self.organization_id = "default_org"
        self.tasks: List[TaskDefinition] = []
        self.variables: Dict[str, Any] = {}
        self.policies: Dict[str, Any] = {}
        self.timeout_seconds = 3600
        self.compensation_policy: Dict[str, Any] = {"enabled": True}

    def with_version(self, version_str: str) -> "WorkflowBuilder":
        self.version = SemanticVersion.parse(version_str)
        return self

    def with_description(self, desc: str) -> "WorkflowBuilder":
        self.description = desc
        return self

    def with_category(self, category: str) -> "WorkflowBuilder":
        self.category = category
        return self

    def with_organization(self, org_id: str) -> "WorkflowBuilder":
        self.organization_id = org_id
        return self

    def with_variable(self, key: str, value: Any) -> "WorkflowBuilder":
        self.variables[key] = value
        return self

    def task(
        self,
        task_id: str,
        name: Optional[str] = None,
        task_type: TaskType = TaskType.SYSTEM,
        capability: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        outputs: Optional[Dict[str, Any]] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout_seconds: int = 60,
        retry_policy: Optional[Dict[str, Any]] = None,
        compensation_action: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "WorkflowBuilder":
        """Add a generic task to the workflow."""
        t_def = TaskDefinition(
            id=task_id,
            name=name or task_id,
            type=task_type,
            capability=capability,
            dependencies=dependencies or [],
            inputs=inputs or {},
            outputs=outputs or {},
            priority=priority,
            timeout_seconds=timeout_seconds,
            retry_policy=retry_policy or {"max_attempts": 3, "backoff": "exponential"},
            compensation_action=compensation_action,
            metadata=metadata or {},
        )
        self.tasks.append(t_def)
        return self

    def approval(
        self,
        task_id: str,
        name: Optional[str] = None,
        role: str = "manager",
        dependencies: Optional[List[str]] = None,
        timeout_hours: int = 24,
    ) -> "WorkflowBuilder":
        """Add human approval gate."""
        return self.task(
            task_id=task_id,
            name=name or f"Approval: {task_id}",
            task_type=TaskType.APPROVAL,
            dependencies=dependencies,
            metadata={"role": role, "timeout_hours": timeout_hours},
        )

    def condition(
        self,
        task_id: str,
        condition_expression: str,
        dependencies: Optional[List[str]] = None,
    ) -> "WorkflowBuilder":
        """Add conditional decision branching task."""
        return self.task(
            task_id=task_id,
            name=f"Condition: {task_id}",
            task_type=TaskType.CONDITION,
            dependencies=dependencies,
            metadata={"condition": condition_expression},
        )

    def build(self) -> WorkflowDefinition:
        """Construct the immutable WorkflowDefinition."""
        return WorkflowDefinition(
            id=self.workflow_id,
            name=self.name,
            version=self.version,
            organization_id=self.organization_id,
            description=self.description,
            category=self.category,
            tags=self.tags,
            tasks=self.tasks,
            variables=self.variables,
            policies=self.policies,
            timeout_seconds=self.timeout_seconds,
            compensation_policy=self.compensation_policy,
        )
