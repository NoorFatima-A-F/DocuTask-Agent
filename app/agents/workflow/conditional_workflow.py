"""
Conditional Workflow Engine.
Evaluates conditional edge guards against workflow state variables to determine execution branching.
"""

from typing import Any, Dict, List, Optional
from app.agents.workflow.workflow_edge import WorkflowEdge


class ConditionalWorkflowEngine:
    """Evaluates edge condition expressions against workflow state variables."""

    def select_next_edge(
        self,
        outgoing_edges: List[WorkflowEdge],
        state_vars: Dict[str, Any]
    ) -> Optional[WorkflowEdge]:
        """Selects the first edge whose condition evaluates True, or default edge."""
        default_edge = None
        for edge in outgoing_edges:
            if edge.is_default:
                default_edge = edge
                continue
            if edge.condition_expression:
                # Simple evaluator: "key == val" or "key in state_vars"
                expr = edge.condition_expression.strip()
                if "==" in expr:
                    k, v = [part.strip() for part in expr.split("==", 1)]
                    if str(state_vars.get(k, "")).lower() == v.lower().strip("'\""):
                        return edge
                elif expr in state_vars and bool(state_vars[expr]):
                    return edge

        return default_edge
