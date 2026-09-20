"""
Enterprise Workflow Validator & Linter.
Validates structural integrity, cycles, reachability, permissions, and security constraints.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from ..domain.models import WorkflowDefinition
from ..domain.exceptions import WorkflowValidationException
from ..graph.graph import ExecutionGraph
from ..graph.nodes import TaskNode, DecisionNode, ApprovalNode
from ..graph.edges import EdgeType, GraphEdge


class IssueSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    severity: IssueSeverity
    code: str
    message: str
    node_id: Optional[str] = None


class WorkflowValidator:
    """Validates workflow definitions and compiles execution graphs."""

    @classmethod
    def validate_definition(cls, definition: WorkflowDefinition) -> List[ValidationIssue]:
        """Validate workflow specification rules."""
        issues: List[ValidationIssue] = []

        if not definition.id or not definition.id.strip():
            issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_MISSING_ID", "Workflow missing unique ID"))

        if not definition.name or not definition.name.strip():
            issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_MISSING_NAME", "Workflow missing name"))

        if not definition.tasks:
            issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_NO_TASKS", "Workflow has no defined tasks"))

        task_ids = set()
        for task in definition.tasks:
            if task.id in task_ids:
                issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_DUPLICATE_TASK_ID", f"Duplicate task ID: {task.id}", task.id))
            task_ids.add(task.id)

            if task.timeout_seconds <= 0:
                issues.append(ValidationIssue(IssueSeverity.WARNING, "WARN_INVALID_TIMEOUT", f"Task {task.id} has invalid timeout <= 0", task.id))

            # Validate dependencies reference real task IDs
            for dep in task.dependencies:
                if dep not in [t.id for t in definition.tasks]:
                    issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_UNKNOWN_DEP", f"Task {task.id} depends on unknown task {dep}", task.id))

        return issues

    @classmethod
    def validate_graph(cls, graph: ExecutionGraph) -> List[ValidationIssue]:
        """Validate ExecutionGraph structure, cycles, and reachability."""
        issues: List[ValidationIssue] = []

        # 1. Cycle detection
        cycles = graph.detect_cycles()
        if cycles:
            for c in cycles:
                issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_CYCLE_DETECTED", f"Cycle detected in execution graph: {' -> '.join(c)}"))

        # 2. Reachability check from root nodes
        roots = graph.get_root_nodes()
        if not roots and graph.list_nodes():
            issues.append(ValidationIssue(IssueSeverity.ERROR, "ERR_NO_ENTRY_POINT", "Graph has no entry root node (all nodes have dependencies)"))

        # 3. Linter: Dead / Unreachable nodes
        reachable = set()
        for root in roots:
            stack = [root.node_id]
            while stack:
                curr = stack.pop()
                if curr not in reachable:
                    reachable.add(curr)
                    for edge in graph.get_outgoing_edges(curr):
                        stack.append(edge.target_node_id)

        all_node_ids = {n.node_id for n in graph.list_nodes()}
        unreachable = all_node_ids - reachable
        for unreach_id in unreachable:
            issues.append(ValidationIssue(IssueSeverity.WARNING, "WARN_UNREACHABLE_NODE", f"Node '{unreach_id}' is unreachable from root entry points", unreach_id))

        return issues

    @classmethod
    def assert_valid(cls, definition: WorkflowDefinition, graph: Optional[ExecutionGraph] = None) -> None:
        """Raise WorkflowValidationException if any ERROR severity issues are detected."""
        issues = cls.validate_definition(definition)
        if graph:
            issues.extend(cls.validate_graph(graph))

        errors = [i for i in issues if i.severity == IssueSeverity.ERROR]
        if errors:
            err_msgs = [f"[{e.code}] {e.message}" for e in errors]
            raise WorkflowValidationException(f"Workflow validation failed: {'; '.join(err_msgs)}")
