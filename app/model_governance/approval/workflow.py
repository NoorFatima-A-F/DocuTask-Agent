"""Model Approval Multi-Stage Workflow Engine (Phase 8C).

Governs:
Submission -> Technical Validation -> Security Review -> Compliance Audit -> Business Approval -> Final Gate.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.model_governance.registry.models import Model, ApprovalStatus, ModelLifecycleState
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.lifecycle.manager import ModelLifecycleManager
from app.model_governance.approval.approvals import (
    ApprovalDecisionRecord,
    ApprovalStage,
    ModelApprovalRecord,
    StageStatus,
)


class ModelApprovalWorkflowEngine:
    """Manages the formal review and multi-stage signoff required before model activation."""

    STAGE_NAMES = [
        "TECHNICAL_VALIDATION",
        "SECURITY_REVIEW",
        "COMPLIANCE_AUDIT",
        "BUSINESS_APPROVAL",
        "FINAL_GATE",
    ]

    def __init__(
        self,
        repository: Optional[ModelRegistryRepository] = None,
        lifecycle_manager: Optional[ModelLifecycleManager] = None,
    ):
        self.repository = repository
        self.lifecycle_manager = lifecycle_manager
        # (model_id, org_id) -> ModelApprovalRecord
        self._approvals: Dict[str, ModelApprovalRecord] = {}

    def _get_key(self, model_id: str, organization_id: str) -> str:
        return f"{organization_id}:{model_id}"

    def initiate_workflow(self, model_id: str, organization_id: str = "org_default") -> ModelApprovalRecord:
        """Initiates the 5-stage approval workflow for a model."""
        stages = [ApprovalStage(stage_name=name) for name in self.STAGE_NAMES]
        record = ModelApprovalRecord(
            approval_id=f"appr_{uuid.uuid4().hex[:10]}",
            model_id=model_id,
            organization_id=organization_id,
            current_status=ApprovalStatus.UNDER_TECHNICAL_REVIEW,
            status=ApprovalStatus.UNDER_TECHNICAL_REVIEW,
            stages=stages,
        )
        self._approvals[self._get_key(model_id, organization_id)] = record

        if self.repository:
            model = self.repository.get_model(model_id, organization_id)
            if model:
                model.approval_status = ApprovalStatus.UNDER_TECHNICAL_REVIEW
                self.repository.save_model(model)

        return record

    def submit_for_review(self, model: Model, submitter_id: str) -> ModelApprovalRecord:
        """Alias for submitting model."""
        return self.initiate_workflow(model.model_id, model.organization_id)

    def review_stage(
        self,
        model_id: str,
        stage_name: str,
        reviewer: str,
        decision: StageStatus | str,
        comments: Optional[str] = None,
        organization_id: str = "org_default",
        evidence_uris: Optional[List[str]] = None,
    ) -> ModelApprovalRecord:
        """Review and record decision for a specific approval stage."""
        key = self._get_key(model_id, organization_id)
        record = self._approvals.get(key)
        if not record:
            record = self.initiate_workflow(model_id, organization_id)

        decision_str = decision.value if isinstance(decision, StageStatus) else str(decision)
        stage_status = StageStatus.APPROVED if decision_str == "APPROVED" else StageStatus.REJECTED

        for stg in record.stages:
            if stg.stage_name.upper() == stage_name.upper():
                stg.status = stage_status
                stg.reviewer_id = reviewer
                stg.decision = stage_status
                stg.comments = comments
                stg.timestamp = datetime.now(timezone.utc)
                break

        record.decisions.append(
            ApprovalDecisionRecord(
                stage_name=stage_name,
                reviewer_id=reviewer,
                decision=decision_str,
                comments=comments or "",
                evidence_uris=evidence_uris or [],
            )
        )

        model = self.repository.get_model(model_id, organization_id) if self.repository else None

        if stage_status == StageStatus.REJECTED:
            record.current_status = ApprovalStatus.REJECTED
            record.status = ApprovalStatus.REJECTED
            if model:
                model.approval_status = ApprovalStatus.REJECTED
                model.lifecycle_state = ModelLifecycleState.RESTRICTED
                self.repository.save_model(model)
            return record

        # Check if all stages approved
        all_approved = all(stg.status == StageStatus.APPROVED for stg in record.stages)
        if all_approved:
            record.current_status = ApprovalStatus.APPROVED
            record.status = ApprovalStatus.APPROVED
            record.final_approved_at = datetime.now(timezone.utc)
            if model:
                model.approval_status = ApprovalStatus.APPROVED
                model.lifecycle_state = ModelLifecycleState.APPROVED
                self.repository.save_model(model)
        else:
            # Advance to next stage status
            stage_map = {
                "TECHNICAL_VALIDATION": ApprovalStatus.UNDER_SECURITY_REVIEW,
                "SECURITY_REVIEW": ApprovalStatus.UNDER_COMPLIANCE_REVIEW,
                "COMPLIANCE_AUDIT": ApprovalStatus.UNDER_BUSINESS_APPROVAL,
                "BUSINESS_APPROVAL": ApprovalStatus.UNDER_TECHNICAL_REVIEW,
                "FINAL_GATE": ApprovalStatus.APPROVED,
            }
            next_stat = stage_map.get(stage_name.upper(), ApprovalStatus.UNDER_TECHNICAL_REVIEW)
            record.current_status = next_stat
            record.status = next_stat
            if model:
                model.approval_status = next_stat
                self.repository.save_model(model)

        return record

    def record_decision(
        self,
        model: Model,
        stage_name: str,
        reviewer_id: str,
        decision: str,
        comments: str = "",
        evidence_uris: Optional[List[str]] = None,
    ) -> ModelApprovalRecord:
        return self.review_stage(
            model_id=model.model_id,
            stage_name=stage_name,
            reviewer=reviewer_id,
            decision=decision,
            comments=comments,
            organization_id=model.organization_id,
            evidence_uris=evidence_uris,
        )

    def get_approval_record(self, model_id: str, organization_id: str = "org_default") -> Optional[ModelApprovalRecord]:
        return self._approvals.get(self._get_key(model_id, organization_id))
