"""
Phase 13.19: Domain Events for Business Process Intelligence.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class BusinessEvent(BaseModel):
    event_id: str
    event_type: str
    process_id: Optional[str] = None
    department_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProcessStartedEvent(BusinessEvent):
    event_type: str = "PROCESS_STARTED"


class StepExecutedEvent(BusinessEvent):
    event_type: str = "STEP_EXECUTED"
    step_id: str = ""
    duration_sec: float = 0.0


class HumanApprovalRequestedEvent(BusinessEvent):
    event_type: str = "HUMAN_APPROVAL_REQUESTED"
    task_id: str = ""
    assigned_role: str = ""


class ApprovalDecidedEvent(BusinessEvent):
    event_type: str = "APPROVAL_DECIDED"
    task_id: str = ""
    decision: str = ""


class SLABreachPredictedEvent(BusinessEvent):
    event_type: str = "SLA_BREACH_PREDICTED"
    probability: float = 0.0


class GoalProgressUpdatedEvent(BusinessEvent):
    event_type: str = "GOAL_PROGRESS_UPDATED"
    goal_id: str = ""
    progress_pct: float = 0.0
