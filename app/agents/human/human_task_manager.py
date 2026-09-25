"""
Human Task Manager for Human-In-The-Loop Collaboration.
High-level interface coordinating escalation ticket generation, operator review, and memory feedback.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.agents.human.approval_queue import (
    ApprovalQueue,
    HumanTaskTicket,
    TicketPriority,
    TicketStatus,
)
from app.agents.human.feedback_processor import (
    FeedbackProcessor,
    HumanActionType,
    HumanFeedbackDirective,
)
from app.agents.human.human_feedback_memory import HumanFeedbackMemory
from app.agents.memory.intelligence.episodic_memory import EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticMemory

logger = logging.getLogger(__name__)


class HumanTaskManager:
    """Manages the full lifecycle of human approval requests and continuous feedback learning."""

    def __init__(
        self,
        queue: Optional[ApprovalQueue] = None,
        processor: Optional[FeedbackProcessor] = None,
        feedback_memory: Optional[HumanFeedbackMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None,
        episodic_memory: Optional[EpisodicMemory] = None,
    ) -> None:
        self.queue = queue or ApprovalQueue()
        self.processor = processor or FeedbackProcessor()
        self.feedback_memory = feedback_memory or HumanFeedbackMemory(
            semantic_memory=semantic_memory,
            episodic_memory=episodic_memory,
        )

    def escalate(
        self,
        execution_id: str,
        task_id: str,
        reason: str,
        extracted_data: Dict[str, Any],
        priority: TicketPriority = TicketPriority.HIGH,
        sla_timeout_seconds: float = 300.0,
    ) -> HumanTaskTicket:
        """Escalates an uncertain or policy-breaching execution step to the human review queue."""
        return self.queue.submit_ticket(
            execution_id=execution_id,
            task_id=task_id,
            reason=reason,
            extracted_data=extracted_data,
            priority=priority,
            sla_timeout_seconds=sla_timeout_seconds,
        )

    def submit_operator_decision(
        self,
        ticket_id: UUID,
        action: HumanActionType,
        operator_id: str = "human_operator_1",
        corrected_data: Optional[Dict[str, Any]] = None,
        notes: str = "",
        document_id: str = "",
    ) -> HumanFeedbackDirective:
        """Processes human operator input, updates ticket, and writes permanent memory rules."""
        ticket = self.queue.get_ticket(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found in approval queue.")

        # 1. Process decision into directive
        directive = self.processor.process_decision(
            ticket=ticket,
            action=action,
            operator_id=operator_id,
            corrected_data=corrected_data,
            notes=notes,
        )

        # 2. Learn from feedback
        self.feedback_memory.learn_from_feedback(
            directive=directive,
            document_id=document_id,
        )

        logger.info(
            "HumanTaskManager: Operator '%s' resolved ticket %s with action %s",
            operator_id,
            ticket_id,
            action.value,
        )
        return directive

    def get_pending_tickets(self) -> List[HumanTaskTicket]:
        return self.queue.list_all(status=TicketStatus.PENDING)

    def get_tickets_for_execution(self, execution_id: str) -> List[HumanTaskTicket]:
        return self.queue.get_tickets_for_execution(execution_id)

