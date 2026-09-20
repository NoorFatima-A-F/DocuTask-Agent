"""
Planning Graph Node Models.
Defines PlanNode and NodeType (TASK, JOIN, SPLIT, MERGE, BARRIER, CHECKPOINT, APPROVAL).
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.planning.constraints import PlanConstraint
from app.agents.planning.resources import ResourceRequirement


class NodeType(str, Enum):
    TASK = "TASK"
    JOIN = "JOIN"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    BARRIER = "BARRIER"
    CHECKPOINT = "CHECKPOINT"
    APPROVAL = "APPROVAL"
    SUBGRAPH = "SUBGRAPH"


class PlanNode(BaseModel):
    """Immutable Graph Node representing an execution or control unit in the plan."""
    node_id: str
    name: str
    node_type: NodeType = Field(default=NodeType.TASK)
    task_id: Optional[str] = Field(default=None)
    capability_requirement: Optional[str] = Field(default=None)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    constraints: List[PlanConstraint] = Field(default_factory=list)
    resource_requirements: List[ResourceRequirement] = Field(default_factory=list)
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    retry_count: int = Field(default=0, ge=0)
    model_config = {"frozen": True}
