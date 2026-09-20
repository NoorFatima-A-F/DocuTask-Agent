"""
Service Level Objectives (SLO) & Indicators (SLI).

Defines availability, latency, AI success rate, and workflow completion SLO specifications.
"""

from __future__ import annotations

import enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class SLIType(str, enum.Enum):
    """Supported SLI metric classifications."""
    AVAILABILITY = "AVAILABILITY"
    LATENCY = "LATENCY"
    ERROR_RATE = "ERROR_RATE"
    AI_SUCCESS_RATE = "AI_SUCCESS_RATE"
    WORKFLOW_COMPLETION = "WORKFLOW_COMPLETION"


class SLIIndicator(BaseModel):
    """Measured good events versus total valid events."""
    sli_type: SLIType
    good_events: int = 0
    total_events: int = 0

    @property
    def compliance_percent(self) -> float:
        if self.total_events == 0:
            return 100.0
        return (self.good_events / self.total_events) * 100.0


class SLOObjective(BaseModel):
    """Formal Service Level Objective specification."""
    slo_id: str
    name: str
    description: str = ""
    service_name: str
    sli_type: SLIType = SLIType.AVAILABILITY
    target_percent: float = Field(default=99.9, ge=0.0, le=100.0)
    window_days: int = Field(default=30, ge=1)
    labels: Dict[str, str] = Field(default_factory=dict)
