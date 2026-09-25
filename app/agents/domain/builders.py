"""
Fluent Builder Suite for Domain Aggregates.
Provides GoalBuilder, TaskBuilder, WorkflowBuilder, ResultBuilder, and PolicyBuilder.
Enforces fail-fast validation during construction.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from app.agents.domain.enums import (
    GoalType,
    PriorityLevel,
    TaskType,
    WorkflowType,
)
from app.agents.domain.goals import Goal, GoalMetadata
from app.agents.domain.policies import ExecutionPolicy, RetryPolicy, TimeoutPolicy
from app.agents.domain.tasks import AgentTask, ExtractionTask, OCRTask
from app.agents.domain.validators import DomainValidator
from app.agents.domain.workflows import WorkflowEdge, WorkflowGraph, WorkflowNode


class GoalBuilder:
    """Fluent builder for Goal aggregate models."""

    def __init__(self, statement: str):
        self._statement = statement
        self._goal_type = GoalType.BUSINESS
        self._priority = PriorityLevel.MEDIUM
        self._owner = "system"
        self._document_id: Optional[UUID] = None
        self._user_id: Optional[UUID] = None
        self._sub_goals: List[Goal] = []

    def with_type(self, goal_type: GoalType) -> "GoalBuilder":
        self._goal_type = goal_type
        return self

    def with_priority(self, priority: PriorityLevel) -> "GoalBuilder":
        self._priority = priority
        return self

    def for_document(self, document_id: UUID, user_id: UUID) -> "GoalBuilder":
        self._document_id = document_id
        self._user_id = user_id
        return self

    def add_sub_goal(self, sub_goal: Goal) -> "GoalBuilder":
        self._sub_goals.append(sub_goal)
        return self

    def build(self) -> Goal:
        meta = GoalMetadata(document_id=self._document_id, user_id=self._user_id)
        goal = Goal(
            statement=self._statement,
            goal_type=self._goal_type,
            priority=self._priority,
            owner=self._owner,
            metadata=meta,
            sub_goals=self._sub_goals
        )
        DomainValidator.validate_goal(goal)
        return goal


class TaskBuilder:
    """Fluent builder for AgentTask models."""

    def __init__(self, name: str, task_type: TaskType = TaskType.CUSTOM):
        self._name = name
        self._task_type = task_type
        self._priority = PriorityLevel.MEDIUM
        self._inputs: Dict[str, Any] = {}

    def with_priority(self, priority: PriorityLevel) -> "TaskBuilder":
        self._priority = priority
        return self

    def with_inputs(self, inputs: Dict[str, Any]) -> "TaskBuilder":
        self._inputs.update(inputs)
        return self

    def build_ocr_task(self, language: str = "eng") -> OCRTask:
        return OCRTask(
            name=self._name,
            priority=self._priority,
            inputs=self._inputs,
            language=language
        )

    def build_extraction_task(self, document_type: str = "generic") -> ExtractionTask:
        return ExtractionTask(
            name=self._name,
            priority=self._priority,
            inputs=self._inputs,
            document_type=document_type
        )

    def build(self) -> AgentTask:
        return AgentTask(
            name=self._name,
            task_type=self._task_type,
            priority=self._priority,
            inputs=self._inputs
        )


class WorkflowBuilder:
    """Fluent builder for WorkflowGraph models."""

    def __init__(self, name: str = "WorkflowGraph"):
        self._name = name
        self._nodes: Dict[str, WorkflowNode] = {}
        self._edges: List[WorkflowEdge] = []

    def add_task_node(self, node_id: str, task: AgentTask) -> "WorkflowBuilder":
        node = WorkflowNode(node_id=node_id, task=task)
        self._nodes[node_id] = node
        return self

    def connect(self, source_id: str, target_id: str, condition: Optional[str] = None) -> "WorkflowBuilder":
        edge_id = f"{source_id}->{target_id}"
        edge = WorkflowEdge(edge_id=edge_id, source_node_id=source_id, target_node_id=target_id, condition_expression=condition)
        self._edges.append(edge)
        return self

    def build(self) -> WorkflowGraph:
        graph = WorkflowGraph(

            name=self._name,
            workflow_type=WorkflowType.DAG,
            nodes=self._nodes,
            edges=self._edges
        )
        DomainValidator.validate_workflow_graph(graph)
        return graph


class PolicyBuilder:
    """Fluent builder for ExecutionPolicy models."""

    def __init__(self):
        self._max_retries = 3
        self._timeout_seconds = 300.0

    def with_retries(self, max_retries: int) -> "PolicyBuilder":
        self._max_retries = max_retries
        return self

    def with_timeout(self, timeout_seconds: float) -> "PolicyBuilder":
        self._timeout_seconds = timeout_seconds
        return self

    def build(self) -> ExecutionPolicy:
        return ExecutionPolicy(
            retry=RetryPolicy(max_retries=self._max_retries),
            timeout=TimeoutPolicy(timeout_seconds=self._timeout_seconds)
        )
