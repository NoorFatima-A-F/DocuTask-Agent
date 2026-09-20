"""
Workflow Sequence Planner.
Extracts ordered node sequences from WorkflowGraph definitions. Never generates AI plans.
"""

from typing import List
from app.agents.workflow.workflow_definition import WorkflowDefinition


class WorkflowSequencePlanner:
    """Determines topological execution sequence from predefined workflow definitions."""

    @staticmethod
    def plan_sequence(definition: WorkflowDefinition) -> List[str]:
        """Returns node IDs ordered by dependencies."""
        return definition.graph.get_topological_order()
