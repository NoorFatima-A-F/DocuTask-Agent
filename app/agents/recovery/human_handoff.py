"""
Human Handoff Manager.
Generates human-in-the-loop escalation tickets with root cause diagnostic summaries.
"""

from typing import Any, Dict
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.recovery.failure import Failure
from app.agents.recovery.root_cause import RootCauseReport


class HumanHandoffTicket(BaseModel):
    """Ticket presented to human operator when autonomous recovery cannot proceed safely."""
    execution_id: UUID
    failure_id: UUID
    summary: str
    suggested_actions: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class HumanHandoffManager:
    """Manages handoff of failed operations to human operators."""

    def create_ticket(self, failure: Failure, report: RootCauseReport) -> HumanHandoffTicket:
        return HumanHandoffTicket(
            execution_id=failure.identity.execution_id,
            failure_id=failure.identity.failure_id,
            summary=f"Failure: {failure.category.value} - {report.primary_cause}",
            suggested_actions={"remedy": report.remediation_recommendation}
        )
