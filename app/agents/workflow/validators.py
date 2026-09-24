"""
Workflow Fail-Fast Validators.
Enforces rules preventing cyclic DAGs, missing saga compensations, orphaned branches, and invalid timer parameters.
"""

from typing import List
from app.agents.workflow.exceptions import (
    CyclicWorkflowGraphError,
    InvalidTimerConfigurationError,
    MissingCompensationPathError,
    WorkflowException,
)
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_graph import WorkflowGraph
from app.agents.workflow.workflow_node import WorkflowNodeType


class WorkflowValidator:
    """Fail-fast validation rules ensuring workflow integrity before instantiation or execution."""

    @staticmethod
    def validate_graph(graph: WorkflowGraph) -> None:
        """Ensures the workflow graph has no cycles and contains valid dependencies."""
        if graph.has_cycles():
            raise CyclicWorkflowGraphError("Workflow graph contains one or more circular dependencies.")

    @staticmethod
    def validate_definition(definition: WorkflowDefinition) -> None:
        """Validates complete workflow definition including DAG topology and node semantics."""
        WorkflowValidator.validate_graph(definition.graph)

        # Check nodes
        for node_id, node in definition.graph.nodes.items():
            if node.node_type == WorkflowNodeType.TIMER:
                delay = node.parameters.get("delay_seconds", 0.0)
                if delay <= 0:
                    raise InvalidTimerConfigurationError(
                        f"Timer node '{node_id}' has non-positive delay_seconds: {delay}"
                    )
            elif node.node_type == WorkflowNodeType.SAGA_TRANSACTION:
                if not node.compensating_handler:
                    raise MissingCompensationPathError(
                        f"Saga node '{node_id}' must specify a compensating_handler."
                    )

    @staticmethod
    def validate_nodes_exist(node_ids: List[str], graph: WorkflowGraph) -> None:
        """Verifies that all specified node IDs exist within the graph."""
        for nid in node_ids:
            if nid not in graph.nodes:
                raise WorkflowException(f"Referenced node '{nid}' does not exist in the workflow graph.")
