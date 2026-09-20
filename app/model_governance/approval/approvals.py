"""Model Approval Records & Review Evidence (Phase 8C)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.model_governance.registry.models import ApprovalStatus


class StageStatus(str, Enum):
    """Status of an individual review stage."""
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"


class ApprovalStage(BaseModel):
    """Single stage in a multi-stage approval workflow."""
    stage_name: str
    status: StageStatus = StageStatus.PENDING
    reviewer_id: Optional[str] = None
    decision: Optional[StageStatus] = None
    comments: Optional[str] = None
    timestamp: Optional[datetime] = None


class ApprovalDecisionRecord(BaseModel):
    """Single stage review decision."""
    stage_name: str  # TECHNICAL_VALIDATION, SECURITY_REVIEW, etc.
    reviewer_id: str
    decision: str  # APPROVED, REJECTED, CHANGES_REQUESTED
    comments: str = ""
    evidence_uris: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelApprovalRecord(BaseModel):
    """Comprehensive approval history container for an AI model."""
    approval_id: str
    model_id: str
    organization_id: str
    current_status: ApprovalStatus = ApprovalStatus.PENDING_SUBMISSION
    status: ApprovalStatus = ApprovalStatus.PENDING_SUBMISSION
    stages: List[ApprovalStage] = Field(default_factory=list)
    decisions: List[ApprovalDecisionRecord] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    final_approved_at: Optional[datetime] = None
