"""
Tests for Workflow Compiler, DAG Graph Engine, and Validation.
"""

import pytest
from app.workflows.domain.models import TaskDefinition, TaskType, WorkflowDefinition
from app.workflows.domain.exceptions import WorkflowValidationException
from app.workflows.compiler.compiler import WorkflowCompiler
from app.workflows.validator.validator import WorkflowValidator
from app.workflows.graph.graph import ExecutionGraph
from app.workflows.graph.nodes import TaskNode
from app.workflows.graph.edges import EdgeType, GraphEdge


def test_compiler_builds_valid_dag():
    defn = WorkflowDefinition(
        id="test_pipeline",
        name="Test Pipeline",
        tasks=[
            TaskDefinition(id="t1", name="Task 1", type=TaskType.SYSTEM),
            TaskDefinition(id="t2", name="Task 2", type=TaskType.SYSTEM, dependencies=["t1"]),
            TaskDefinition(id="t3", name="Task 3", type=TaskType.SYSTEM, dependencies=["t2"]),
        ],
    )

    graph = WorkflowCompiler.compile(defn)
    assert len(graph.list_nodes()) == 3
    assert len(graph.list_edges()) == 2

    ordered = graph.topological_sort()
    assert [n.node_id for n in ordered] == ["t1", "t2", "t3"]


def test_validator_detects_cycles():
    defn = WorkflowDefinition(
        id="cycle_pipeline",
        name="Cycle Pipeline",
        tasks=[
            TaskDefinition(id="a", name="A", type=TaskType.SYSTEM, dependencies=["c"]),
            TaskDefinition(id="b", name="B", type=TaskType.SYSTEM, dependencies=["a"]),
            TaskDefinition(id="c", name="C", type=TaskType.SYSTEM, dependencies=["b"]),
        ],
    )

    with pytest.raises(WorkflowValidationException) as exc_info:
        WorkflowCompiler.compile(defn)

    assert "Cycle detected" in str(exc_info.value) or "validation failed" in str(exc_info.value)


def test_validator_detects_unknown_dependencies():
    defn = WorkflowDefinition(
        id="invalid_pipeline",
        name="Invalid Pipeline",
        tasks=[
            TaskDefinition(id="t1", name="Task 1", dependencies=["non_existent_task"]),
        ],
    )

    with pytest.raises(WorkflowValidationException) as exc_info:
        WorkflowValidator.assert_valid(defn)

    assert "depends on unknown task" in str(exc_info.value)
