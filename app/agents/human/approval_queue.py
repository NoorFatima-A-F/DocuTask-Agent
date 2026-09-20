"""
Approval Queue for Human-In-The-Loop (HITL) Collaboration.
Prioritized queue managing human review tickets, SLA timers, and escalation routing.
"""

from __future__ import annotations

import heapq
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)


class TicketStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MODIFIED = "MODIFIED"
    TIMED_OUT = "TIMED_OUT"


class TicketPriority(int, Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass(order=True)
class HumanTaskTicket:
    """A task requiring human intervention, prioritized in the queue."""

    priority: TicketPriority
    created_at_timestamp: float = field(compare=True)
    ticket_id: UUID = field(default_factory=uuid4, compare=False)
    execution_id: str = field(default="", compare=False)
    task_id: str = field(default="", compare=False)
    reason: str = field(default="", compare=False)
    extracted_data: Dict[str, Any] = field(default_factory=dict, compare=False)
    status: TicketStatus = field(default=TicketStatus.PENDING, compare=False)
    sla_timeout_seconds: float = field(default=300.0, compare=False)
    resolved_at: Optional[datetime] = field(default=None, compare=False)
    operator_id: Optional[str] = field(default=None, compare=False)
    operator_decision: Optional[str] = field(default=None, compare=False)
    corrected_data: Optional[Dict[str, Any]] = field(default=None, compare=False)
    operator_notes: str = field(default="", compare=False)

    def is_expired(self) -> bool:
        if self.status != TicketStatus.PENDING:
            return False
        if self.sla_timeout_seconds is None or self.sla_timeout_seconds <= 0:
            return False
        return (time.time() - self.created_at_timestamp) > self.sla_timeout_seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": str(self.ticket_id),
            "priority": self.priority.name,
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "reason": self.reason,
            "extracted_data": self.extracted_data,
            "status": self.status.value,
            "sla_timeout_seconds": self.sla_timeout_seconds,
            "is_expired": self.is_expired(),
            "operator_id": self.operator_id,
            "operator_decision": self.operator_decision,
            "corrected_data": self.corrected_data,
            "operator_notes": self.operator_notes,
        }


class ApprovalQueue:
    """Thread-safe priority queue holding pending human verification tickets."""

    def __init__(self) -> None:
        self._heap: List[HumanTaskTicket] = []
        self._by_id: Dict[UUID, HumanTaskTicket] = {}

    def submit_ticket(
        self,
        execution_id: str,
        task_id: str,
        reason: str,
        extracted_data: Dict[str, Any],
        priority: TicketPriority = TicketPriority.HIGH,
        sla_timeout_seconds: float = 300.0,
    ) -> HumanTaskTicket:
        """Creates and enqueues a new human review ticket."""
        ticket = HumanTaskTicket(
            priority=priority,
            created_at_timestamp=time.time(),
            execution_id=execution_id,
            task_id=task_id,
            reason=reason,
            extracted_data=extracted_data,
            sla_timeout_seconds=sla_timeout_seconds,
        )
        heapq.heappush(self._heap, ticket)
        self._by_id[ticket.ticket_id] = ticket
        logger.warning(
            "Human review ticket %s enqueued for task %s (priority=%s, reason=%s)",
            ticket.ticket_id,
            task_id,
            priority.name,
            reason,
        )
        return ticket

    def get_next_pending_ticket(self) -> Optional[HumanTaskTicket]:
        """Pops the highest-priority non-expired pending ticket."""
        while self._heap:
            ticket = heapq.heappop(self._heap)
            if ticket.is_expired():
                ticket.status = TicketStatus.TIMED_OUT
                logger.warning("Ticket %s timed out due to SLA expiration", ticket.ticket_id)
                continue
            if ticket.status == TicketStatus.PENDING:
                return ticket
        return None

    def get_ticket(self, ticket_id: UUID) -> Optional[HumanTaskTicket]:
        return self._by_id.get(ticket_id)

    def list_all(self, status: Optional[TicketStatus] = None) -> List[HumanTaskTicket]:
        if status is None:
            return list(self._by_id.values())
        return [t for t in self._by_id.values() if t.status == status]

    def get_tickets_for_execution(self, execution_id: str) -> List[HumanTaskTicket]:
        return [t for t in self._by_id.values() if t.execution_id == execution_id]

    def __len__(self) -> int:
        return sum(1 for t in self._by_id.values() if t.status == TicketStatus.PENDING and not t.is_expired())
