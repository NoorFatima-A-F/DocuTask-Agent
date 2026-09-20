"""
Enterprise Workflow Compiler.
Transforms declarative WorkflowDefinition into executable ExecutionGraph with validation.
"""

from typing import Any, Dict
from ..domain.models import TaskDefinition, TaskType, WorkflowDefinition
from ..domain.exceptions import WorkflowCompilationException
from ..graph.graph import ExecutionGraph
from ..graph.nodes import (
    AgentNode,
    ApprovalNode,
    ConnectorNode,
    DecisionNode,
    EventNode,
    ParallelNode,
    SubWorkflowNode,
    TaskNode,
    TimerNode,
)
from ..graph.edges import EdgeType, GraphEdge
from ..validator.validator import WorkflowValidator


class WorkflowCompiler:
    """Compiles high-level declarative workflow models into low-level executable DAGs."""

    @classmethod
    def compile(cls, definition: WorkflowDefinition) -> ExecutionGraph:
        """Compile WorkflowDefinition to ExecutionGraph."""
        # 1. Validate definition first
        WorkflowValidator.assert_valid(definition)

        graph = ExecutionGraph(workflow_id=definition.id)

        # 2. Build Nodes
        for task in definition.tasks:
            node = cls._create_node(task)
            graph.add_node(node)

        # 3. Wire Dependency Edges
        for task in definition.tasks:
            for dep_id in task.dependencies:
                edge = GraphEdge(
                    source_node_id=dep_id,
                    target_node_id=task.id,
                    edge_type=EdgeType.SUCCESS,
                )
                graph.add_edge(edge)

        # 4. Validate resulting graph
        WorkflowValidator.assert_valid(definition, graph=graph)

        return graph

    @staticmethod
    def _create_node(task: TaskDefinition):
        """Map TaskDefinition to specific GraphNode subclass."""
        if task.type == TaskType.APPROVAL:
            return ApprovalNode(
                node_id=task.id,
                name=task.name,
                approver_role=task.metadata.get("role", "manager"),
                timeout_hours=task.metadata.get("timeout_hours", 24),
                required_approvals=task.metadata.get("required_approvals", 1),
                metadata=task.metadata,
            )
        elif task.type == TaskType.CONDITION:
            return DecisionNode(
                node_id=task.id,
                name=task.name,
                condition_expression=task.metadata.get("condition", ""),
                branches=task.metadata.get("branches", {}),
                metadata=task.metadata,
            )
        elif task.type == TaskType.TIMER:
            return TimerNode(
                node_id=task.id,
                name=task.name,
                duration_seconds=task.timeout_seconds,
                metadata=task.metadata,
            )
        elif task.type == TaskType.EVENT or task.type == TaskType.WEBHOOK:
            return EventNode(
                node_id=task.id,
                name=task.name,
                event_type=task.metadata.get("event_type", "webhook.received"),
                metadata=task.metadata,
            )
        elif task.type == TaskType.AI:
            return AgentNode(
                node_id=task.id,
                name=task.name,
                agent_role=task.metadata.get("role", "reasoning_agent"),
                prompt_template=task.metadata.get("prompt", ""),
                metadata=task.metadata,
            )
        elif task.type == TaskType.CONNECTOR:
            return ConnectorNode(
                node_id=task.id,
                name=task.name,
                connector_id=task.metadata.get("connector_id", ""),
                action_name=task.metadata.get("action", ""),
                metadata=task.metadata,
            )
        elif task.type == TaskType.SUBWORKFLOW:
            return SubWorkflowNode(
                node_id=task.id,
                name=task.name,
                sub_workflow_id=task.metadata.get("workflow_id", ""),
                metadata=task.metadata,
            )
        elif task.type == TaskType.PARALLEL:
            return ParallelNode(
                node_id=task.id,
                name=task.name,
                branch_node_ids=task.metadata.get("branches", []),
                metadata=task.metadata,
            )
        else:
            return TaskNode(
                node_id=task.id,
                name=task.name,
                task_def=task,
                metadata=task.metadata,
            )
