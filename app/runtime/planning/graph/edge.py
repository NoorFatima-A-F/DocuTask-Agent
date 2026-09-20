"""
Dynamic DAG Execution Edge Schema.

Defines directional dependencies between nodes, data schema mappings,
conditional branch guards, and temporal synchronization barriers.
"""

from __future__ import annotations

import enum
import uuid
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EdgeType(str, enum.Enum):
    DATA_FLOW = "DATA_FLOW"                 # Passes output dictionary of source as input to target
    CONTROL_FLOW = "CONTROL_FLOW"           # Enforces sequential ordering without direct data transfer
    CONDITIONAL_BRANCH = "CONDITIONAL_BRANCH"  # Evaluates branch guard predicate before activating target
    TEMPORAL_BARRIER = "TEMPORAL_BARRIER"   # Synchronization barrier (e.g. join / wait-all)


class DAGEdge(BaseModel):
    """Directional dependency edge linking source_node -> target_node."""
    edge_id: str = Field(default_factory=lambda: f"edge-{uuid.uuid4().hex[:8]}")
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType = EdgeType.DATA_FLOW
    condition_expression: Optional[str] = None
    data_mapping: Dict[str, str] = Field(default_factory=dict)  # {"source_key": "target_key"}
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def evaluate_condition(self, context_data: Dict[str, Any]) -> bool:
        """Evaluates whether conditional branch is activated."""
        if not self.condition_expression:
            return True
        try:
            # Safe evaluation of boolean expressions over context variables
            allowed_names = {"True": True, "False": False, "None": None, **context_data}
            return bool(eval(self.condition_expression, {"__builtins__": {}}, allowed_names))
        except Exception:
            return False
