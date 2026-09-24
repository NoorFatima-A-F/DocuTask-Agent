"""
Workflow Edge Model.
Defines directed dependencies and transition guards between workflow nodes.
"""

from typing import Optional
from pydantic import BaseModel


class WorkflowEdge(BaseModel):
    """Directed edge connecting source and target nodes with optional condition."""
    edge_id: str
    source_node_id: str
    target_node_id: str
    condition_expression: Optional[str] = None  # Expression evaluated against workflow state
    is_default: bool = False

    model_config = {"frozen": True}
