"""
Tool Feedback Contracts.
Produces structured recommendations and performance feedback for the Tool Registry.
Never invokes tools directly.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ToolPerformanceFeedback(BaseModel):
    """Performance feedback on a specific tool definition or capability."""
    tool_name: str
    reliability_rate: float
    average_duration_ms: float
    failure_count: int
    recommendation: str  # MAINTAIN, APPLY_CIRCUIT_BREAKER, DEPRECATE, TUNE_TIMEOUT, REPLACE_WITH_ALTERNATE
    alternate_tool_suggestion: str = ""

    model_config = {"frozen": True}


class ToolFeedback(BaseModel):
    """Feedback payload for the Tool Registry and Tool Capability Resolution layer."""
    feedback_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    tool_evaluations: List[ToolPerformanceFeedback] = Field(default_factory=list)
    overall_tooling_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
