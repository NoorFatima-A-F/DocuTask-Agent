"""
Feedback Processor for Human-In-The-Loop Collaboration.
Parses human operator responses into deterministic runtime execution directives.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from app.agents.human.approval_queue import HumanTaskTicket, TicketStatus

logger = logging.getLogger(__name__)


class HumanActionType(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    RETRY_WITH_HINT = "RETRY_WITH_HINT"


@dataclass
class HumanFeedbackDirective:
    """Actionable instruction emitted for the autonomous runtime."""

    action_type: HumanActionType
    execution_id: str
    task_id: str
    effective_data: Dict[str, Any] = field(default_factory=dict)
    guidance_notes: str = ""
    should_resume_graph: bool = True
    should_abort: bool = False
    operator_id: str = "human_operator"


class FeedbackProcessor:
    """Translates human operator choices into formal execution directives."""

    def process_decision(
        self,
        ticket: HumanTaskTicket,
        action: HumanActionType,
        operator_id: str,
        corrected_data: Optional[Dict[str, Any]] = None,
        notes: str = "",
    ) -> HumanFeedbackDirective:
        """Applies human decision to ticket and constructs runtime directive."""
        ticket.resolved_at = datetime.now(timezone.utc)
        ticket.operator_id = operator_id
        ticket.operator_decision = action.value
        ticket.operator_notes = notes

        if action == HumanActionType.APPROVE:
            ticket.status = TicketStatus.APPROVED
            return HumanFeedbackDirective(
                action_type=HumanActionType.APPROVE,
                execution_id=ticket.execution_id,
                task_id=ticket.task_id,
                effective_data=ticket.extracted_data,
                guidance_notes=notes or "Approved by operator as accurate.",
                should_resume_graph=True,
                should_abort=False,
                operator_id=operator_id,
            )

        elif action == HumanActionType.MODIFY:
            ticket.status = TicketStatus.MODIFIED
            ticket.corrected_data = corrected_data or {}
            return HumanFeedbackDirective(
                action_type=HumanActionType.MODIFY,
                execution_id=ticket.execution_id,
                task_id=ticket.task_id,
                effective_data=ticket.corrected_data,
                guidance_notes=notes or "Operator provided direct field corrections.",
                should_resume_graph=True,
                should_abort=False,
                operator_id=operator_id,
            )

        elif action == HumanActionType.RETRY_WITH_HINT:
            ticket.status = TicketStatus.MODIFIED
            return HumanFeedbackDirective(
                action_type=HumanActionType.RETRY_WITH_HINT,
                execution_id=ticket.execution_id,
                task_id=ticket.task_id,
                effective_data=ticket.extracted_data,
                guidance_notes=notes or "Operator requested re-execution with hint.",
                should_resume_graph=True,
                should_abort=False,
                operator_id=operator_id,
            )

        elif action == HumanActionType.REJECT:
            ticket.status = TicketStatus.REJECTED
            return HumanFeedbackDirective(
                action_type=HumanActionType.REJECT,
                execution_id=ticket.execution_id,
                task_id=ticket.task_id,
                effective_data={},
                guidance_notes=notes or "Rejected by operator as invalid or fraudulent.",
                should_resume_graph=False,
                should_abort=True,
                operator_id=operator_id,
            )

        raise ValueError(f"Unknown HumanActionType: {action}")
