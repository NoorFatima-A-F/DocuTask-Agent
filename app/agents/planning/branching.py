"""
Branching Models for Workflow Graphs.
Defines ConditionalBranch, ParallelBranch, and BranchType.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.planning.conditions import BranchCondition


class BranchType(str, Enum):
    CONDITIONAL = "CONDITIONAL"
    PARALLEL = "PARALLEL"
    RETRY = "RETRY"
    COMPENSATION = "COMPENSATION"
    ROLLBACK = "ROLLBACK"


class ConditionalBranch(BaseModel):
    """Conditional branch routed based on boolean evaluation of condition."""
    branch_id: str
    condition: BranchCondition
    target_node_id: str
    fallback_node_id: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class ParallelBranch(BaseModel):
    """Set of independent node branches executed concurrently."""
    branch_id: str
    concurrent_node_ids: List[str] = Field(default_factory=list)
    join_node_id: Optional[str] = Field(default=None)
    model_config = {"frozen": True}
