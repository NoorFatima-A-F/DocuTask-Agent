"""
Delegation Domain Models.
Defines models for single-agent, multi-agent, hierarchical, recursive, and fallback delegations.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DelegationMode(str, Enum):
    """Supported delegation topologies."""
    SINGLE = "SINGLE"
    MULTI_AGENT = "MULTI_AGENT"
    HIERARCHICAL = "HIERARCHICAL"
    RECURSIVE = "RECURSIVE"
    CONDITIONAL = "CONDITIONAL"
    FALLBACK = "FALLBACK"


class DelegationStatus(str, Enum):
    """Lifecycle of a delegation job."""
    PENDING = "PENDING"
    DISPATCHED = "DISPATCHED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    FALLBACK_TRIGGERED = "FALLBACK_TRIGGERED"


class DelegationTask(BaseModel):
    """Specification of an individual task to delegate."""
    task_id: str
    task_name: str
    required_skills: List[str] = Field(default_factory=list)
    payload: Dict[str, Any] = Field(default_factory=dict)
    assigned_agent_id: Optional[UUID] = None
    fallback_agent_id: Optional[UUID] = None
    delegation_depth: int = Field(default=0, ge=0)

    model_config = {"frozen": True}


class DelegationRequest(BaseModel):
    """Request envelope initiating task delegation across agents."""
    delegation_id: UUID = Field(default_factory=uuid4)
    delegator_agent_id: UUID
    mode: DelegationMode = Field(default=DelegationMode.SINGLE)
    tasks: List[DelegationTask] = Field(default_factory=list)
    max_recursion_depth: int = Field(default=3, ge=0)
    timeout_seconds: float = Field(default=60.0, gt=0.0)

    model_config = {"frozen": True}


class DelegationResult(BaseModel):
    """Outcome payload of completed or failed task delegation."""
    delegation_id: UUID
    status: DelegationStatus = Field(default=DelegationStatus.COMPLETED)
    results: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    delegation_chain: List[UUID] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
