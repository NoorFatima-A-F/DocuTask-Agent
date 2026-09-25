"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Human Escalation Engine.
Manages policy-driven human-in-the-loop intervention for autonomous agent systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class EscalationReason(str, Enum):
    """Triggers mandating human intervention."""
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    SECURITY_RISK = "SECURITY_RISK"
    COMPLIANCE_ISSUE = "COMPLIANCE_ISSUE"
    HIGH_FINANCIAL_IMPACT = "HIGH_FINANCIAL_IMPACT"
    MODEL_DISAGREEMENT = "MODEL_DISAGREEMENT"
    REPEATED_FAILURE = "REPEATED_FAILURE"
    POLICY_REQUIREMENT = "POLICY_REQUIREMENT"


class EscalationStatus(str, Enum):
    """Lifecycle states of an escalation ticket."""
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


@dataclass
class EscalationRecord:
    """Audit and operational record for human escalation."""
    id: str = field(default_factory=lambda: f"esc-{uuid.uuid4().hex[:12]}")
    reason: EscalationReason | str = EscalationReason.LOW_CONFIDENCE
    priority: str = "HIGH"  # CRITICAL, HIGH, NORMAL, LOW
    status: EscalationStatus = EscalationStatus.PENDING
    agent_id: str = ""
    task_id: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    assigned_reviewer: Optional[str] = None
    reviewer_comments: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "reason": self.reason.value if isinstance(self.reason, Enum) else str(self.reason),
            "priority": self.priority,
            "status": self.status.value if isinstance(self.status, Enum) else str(self.status),
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "description": self.description,
            "metadata": self.metadata,
            "assigned_reviewer": self.assigned_reviewer,
            "reviewer_comments": self.reviewer_comments,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


class HumanEscalationEngine:
    """
    Evaluates execution parameters and manages policy-driven escalation
    tickets for human operators and reviewers.
    """

    def __init__(self):
        self._records: Dict[str, EscalationRecord] = {}

    def should_escalate(
        self,
        confidence_score: float = 1.0,
        risk_score: float = 0.0,
        has_security_violation: bool = False,
        financial_amount: float = 0.0,
        financial_threshold: float = 10000.0,
        retry_count: int = 0,
        max_retries: int = 3,
    ) -> Optional[EscalationReason]:
        """
        Determines whether human escalation is triggered by any policy boundary.
        """
        if has_security_violation:
            return EscalationReason.SECURITY_RISK

        if financial_amount >= financial_threshold:
            return EscalationReason.HIGH_FINANCIAL_IMPACT

        if retry_count >= max_retries:
            return EscalationReason.REPEATED_FAILURE

        if confidence_score < 0.75:
            return EscalationReason.LOW_CONFIDENCE

        if risk_score >= 0.50:
            return EscalationReason.SECURITY_RISK

        return None

    def create_escalation(
        self,
        agent_id: str,
        task_id: str,
        reason: EscalationReason | str,
        description: str,
        priority: str = "HIGH",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EscalationRecord:
        """Creates and indexes a new human escalation record."""
        record = EscalationRecord(
            id=f"esc-{uuid.uuid4().hex[:12]}",
            reason=reason,
            priority=priority,
            status=EscalationStatus.PENDING,
            agent_id=agent_id,
            task_id=task_id,
            description=description,
            metadata=metadata or {},
        )
        self._records[record.id] = record
        logger.info(f"Created Human Escalation {record.id} [Reason: {record.reason}, Priority: {priority}]")
        return record

    def resolve(
        self,
        escalation_id: str,
        approved: bool,
        reviewer_id: str,
        comments: str = "",
    ) -> EscalationRecord:
        """Resolves an active escalation ticket with approval or rejection."""
        record = self._records.get(escalation_id)
        if not record:
            raise KeyError(f"Escalation record {escalation_id} not found.")

        record.status = EscalationStatus.APPROVED if approved else EscalationStatus.REJECTED
        record.assigned_reviewer = reviewer_id
        record.reviewer_comments = comments
        record.resolved_at = datetime.now(timezone.utc)

        logger.info(f"Resolved Escalation {escalation_id}: Status={record.status.value} by {reviewer_id}")
        return record

    def get(self, escalation_id: str) -> Optional[EscalationRecord]:
        """Retrieves an escalation record by ID."""
        return self._records.get(escalation_id)

    def list_pending(self) -> List[EscalationRecord]:
        """Lists all open pending escalation records."""
        return [r for r in self._records.values() if r.status == EscalationStatus.PENDING]
