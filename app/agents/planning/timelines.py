"""
Planning Timeline Models.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from pydantic import BaseModel, Field


class EstimatedTimeline(BaseModel):
    """Estimated start and end timelines for plan or task nodes."""
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = Field(default=None)
    duration_seconds: float = Field(default=0.0, ge=0.0)
    node_timelines: Dict[str, float] = Field(default_factory=dict)
    model_config = {"frozen": True}
