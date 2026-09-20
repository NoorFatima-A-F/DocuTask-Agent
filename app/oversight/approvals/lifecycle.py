"""Approval Lifecycle State Machine Definitions."""

from enum import Enum


class ApprovalLifecycleState(str, Enum):
    """10-State Lifecycle FSM for Human Reviews & Approvals."""
    CREATED = "CREATED"
    PENDING_REVIEW = "PENDING_REVIEW"
    ASSIGNED = "ASSIGNED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"
