"""
Execution Graph Edge Definitions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EdgeType(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    TIMEOUT = "TIMEOUT"
    CONDITIONAL = "CONDITIONAL"
    COMPENSATION = "COMPENSATION"
    CANCELLATION = "CANCELLATION"


@dataclass(frozen=True)
class GraphEdge:
    """Directed dependency edge between workflow nodes."""
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType = EdgeType.SUCCESS
    condition: Optional[str] = None  # Condition evaluation expression for CONDITIONAL edges
