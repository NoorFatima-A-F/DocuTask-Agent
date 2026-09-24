"""Prompt Approval Multi-Stage Workflow Engine (Phase 8D).

Governs:
DRAFT -> SECURITY_SCAN -> EVALUATION_TESTS -> HUMAN_REVIEW -> GOVERNANCE_SIGN_OFF -> APPROVED
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptApprovalStatus, PromptLifecycleState
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.lifecycle.manager import PromptLifecycleManager


class ApprovalStageStatus(str, Enum):
    """Status of an approval stage."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PromptApprovalStage(BaseModel):
    """Single stage in a prompt approval review pipeline."""
    stage_name: str
    status: ApprovalStageStatus = ApprovalStageStatus.PENDING
    reviewer: Optional[str] = None
    comments: Optional[str] = None
    timestamp: Optional[datetime] = None


class PromptApprovalWorkflowRecord(BaseModel):
    """Container for complete approval workflow history."""
    workflow_id: str
    prompt_id: str
    version_id: str
    organization_id: str
    overall_status: PromptApprovalStatus = PromptApprovalStatus.PENDING_REVIEW
    stages: List[PromptApprovalStage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finalized_at: Optional[datetime] = None


class PromptApprovalWorkflowEngine:
    """Manages multi-tier prompt review and promotion."""

    STAGE_NAMES = [
        "SECURITY_SCAN",
        "EVALUATION_TESTS",
        "HUMAN_REVIEW",
        "GOVERNANCE_SIGN_OFF",
    ]

    def __init__(
        self,
        repository: Optional[PromptRegistryRepository] = None,
        lifecycle_manager: Optional[PromptLifecycleManager] = None,
    ):
        self.repository = repository
        self.lifecycle_manager = lifecycle_manager
        # (org_id, prompt_id, version_id) -> PromptApprovalWorkflowRecord
        self._workflows: Dict[tuple[str, str, str], PromptApprovalWorkflowRecord] = {}

    def initiate_workflow(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
    ) -> PromptApprovalWorkflowRecord:
        """Create and start a new approval workflow."""
        stages = [PromptApprovalStage(stage_name=name) for name in self.STAGE_NAMES]
        wf = PromptApprovalWorkflowRecord(
            workflow_id=f"wf_appr_{uuid.uuid4().hex[:8]}",
            prompt_id=prompt_id,
            version_id=version_id,
            organization_id=organization_id,
            overall_status=PromptApprovalStatus.PENDING_REVIEW,
            stages=stages,
        )
        self._workflows[(organization_id, prompt_id, version_id)] = wf

        if self.repository:
            version = self.repository.get_version(prompt_id, version_id, organization_id)
            if version:
                version.approval_status = PromptApprovalStatus.PENDING_REVIEW
                self.repository.save_version(organization_id, version)

        return wf

    def review_stage(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        stage_name: str,
        reviewer: str,
        decision: ApprovalStageStatus,
        comments: Optional[str] = None,
    ) -> PromptApprovalWorkflowRecord:
        """Record reviewer decision on a specific approval stage."""
        key = (organization_id, prompt_id, version_id)
        wf = self._workflows.get(key)
        if not wf:
            wf = self.initiate_workflow(prompt_id, version_id, organization_id)

        for stg in wf.stages:
            if stg.stage_name.upper() == stage_name.upper():
                stg.status = decision
                stg.reviewer = reviewer
                stg.comments = comments
                stg.timestamp = datetime.now(timezone.utc)
                break

        if decision == ApprovalStageStatus.REJECTED:
            wf.overall_status = PromptApprovalStatus.REJECTED
            wf.finalized_at = datetime.now(timezone.utc)
            if self.repository:
                version = self.repository.get_version(prompt_id, version_id, organization_id)
                if version:
                    version.approval_status = PromptApprovalStatus.REJECTED
                    self.repository.save_version(organization_id, version)
            return wf

        all_approved = all(s.status == ApprovalStageStatus.APPROVED for s in wf.stages)
        if all_approved:
            wf.overall_status = PromptApprovalStatus.APPROVED
            wf.finalized_at = datetime.now(timezone.utc)
            if self.repository:
                version = self.repository.get_version(prompt_id, version_id, organization_id)
                if version:
                    version.approval_status = PromptApprovalStatus.APPROVED
                    self.repository.save_version(organization_id, version)
                prompt = self.repository.get_prompt(prompt_id, organization_id)
                if prompt:
                    prompt.status = PromptLifecycleState.APPROVED
                    prompt.lifecycle_state = PromptLifecycleState.APPROVED
                    self.repository.save_prompt(prompt)

        return wf

    def get_workflow(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
    ) -> Optional[PromptApprovalWorkflowRecord]:
        """Retrieve workflow record."""
        return self._workflows.get((organization_id, prompt_id, version_id))
