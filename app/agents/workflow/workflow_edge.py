"""
Workflow Edge Model.
Defines directed dependencies and transition guards between workflow nodes.
"""

from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class WorkflowEdge(BaseModel):
    """Directed edge connecting source and target nodes with optional condition."""
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid4().hex[:8]}")
    source_node_id: str = Field(default="")
    target_node_id: str = Field(default="")
    condition_expression: Optional[str] = None  # Expression evaluated against workflow state
    is_default: bool = False

    model_config = {"frozen": False, "populate_by_name": True}

    def __init__(self, **data):
        if "from_node" in data and "source_node_id" not in data:
            data["source_node_id"] = data["from_node"]
        if "to_node" in data and "target_node_id" not in data:
            data["target_node_id"] = data["to_node"]
        super().__init__(**data)

    @property
    def from_node(self) -> str:
        return self.source_node_id

    @property
    def to_node(self) -> str:
        return self.target_node_id
