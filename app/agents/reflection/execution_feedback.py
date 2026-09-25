"""
Execution Feedback Contracts.
Produces structured, typed feedback for the Stateful Execution Engine and Runtime Scheduler.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ExecutionCritiqueItem(BaseModel):
    """Specific critique item targeting execution runtime, worker pools, or scheduling."""
    code: str  # BOTTLENECK, STARVATION, WORKER_WASTE, RETRY_EXCESS, IDLE_TIME, SEQUENTIAL_BOTTLENECK
    description: str
    affected_nodes: List[str] = Field(default_factory=list)
    suggested_runtime_action: str
    impact_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH

    model_config = {"frozen": True}


class ExecutionFeedback(BaseModel):
    """
    Structured feedback delivered to the Execution Runtime.
    Provides guidance on worker pool scaling, scheduling policies, and timeout tuning.
    """
    feedback_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    critique_items: List[ExecutionCritiqueItem] = Field(default_factory=list)
    recommended_worker_concurrency: Optional[int] = None
    recommended_scheduling_strategy: Optional[str] = None
    bottleneck_analysis: Dict[str, Any] = Field(default_factory=dict)
    runtime_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
