"""
Workflow State and Variable Container.
Maintains state variables, node results, and execution payloads during a workflow run.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowState(BaseModel):
    """Dynamic state container updated as workflow progresses."""
    variables: Dict[str, Any] = Field(default_factory=dict)
    completed_nodes: List[str] = Field(default_factory=list)
    failed_nodes: List[str] = Field(default_factory=list)
    node_outputs: Dict[str, Any] = Field(default_factory=dict)
    version: int = Field(default=1, ge=1)

    def set_variable(self, key: str, value: Any) -> "WorkflowState":
        new_vars = dict(self.variables)
        new_vars[key] = value
        return self.model_copy(update={"variables": new_vars, "version": self.version + 1})

    def record_node_completion(self, node_id: str, output: Any = None) -> "WorkflowState":
        new_comp = [*self.completed_nodes, node_id]
        new_outputs = dict(self.node_outputs)
        if output is not None:
            new_outputs[node_id] = output
        return self.model_copy(update={
            "completed_nodes": new_comp,
            "node_outputs": new_outputs,
            "version": self.version + 1
        })
