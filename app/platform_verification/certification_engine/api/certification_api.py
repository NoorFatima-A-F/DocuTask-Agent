"""
REST API Router for Enterprise Verification Quality Gates & Certification (PART 6).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.platform_verification.certification_engine.domain.models import (
    ApprovalAction,
    ApprovalReview,
    CertificationLevel,
    ChangeType,
    ExceptionRequest,
    RiskLevel,
)
from app.platform_verification.certification_engine.runtime.certification_platform_runtime import (
    EnterpriseCertificationPlatformRuntime,
)

router = APIRouter(prefix="/certifications", tags=["Platform Verification Governance & Certification"])
_runtime = EnterpriseCertificationPlatformRuntime()


class EvaluateGateRequest(BaseModel):
    system_id: str
    system_version: str
    model_version: str
    target_level: CertificationLevel = CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED
    metrics: Dict[str, Any]
    gate_ids: List[str]
    policy_ids: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None


class IssueCertificationRequest(BaseModel):
    decision_id: str
    evidence_package_id: str
    approved_by: str
    validity_days: int = 90


class ReviewApprovalRequest(BaseModel):
    reviewer_id: str
    reviewer_role: str
    action: ApprovalAction
    comments: str


class SubmitExceptionRequest(BaseModel):
    system_id: str
    component: str
    gate_id: str
    metric_name: str
    risk_level: RiskLevel
    reason: str
    owner: str
    duration_days: int = 30


class ChangeAnalysisRequest(BaseModel):
    change_type: ChangeType
    changed_entity: str
    version_before: str
    version_after: str
    system_id: str


@router.post("/evaluate", response_model=Dict[str, Any])
def evaluate_quality_gates(req: EvaluateGateRequest):
    """Evaluates quality gates, policies, and risk for release decision."""
    decision = _runtime.decision_engine.make_release_decision(
        system_id=req.system_id,
        system_version=req.system_version,
        model_version=req.model_version,
        target_level=req.target_level,
        metrics=req.metrics,
        gate_ids=req.gate_ids,
        policy_ids=req.policy_ids,
        context=req.context,
    )
    _runtime.record_decision(decision)
    return {
        "decision_id": decision.decision_id,
        "decision": decision.decision.value,
        "total_score": decision.total_score,
        "risk_level": decision.risk_assessment.risk_level.value,
        "requires_human_approval": decision.requires_human_approval,
        "explainable_reasons": decision.explainable_reasons,
    }


@router.post("", response_model=Dict[str, Any])
def issue_certification(req: IssueCertificationRequest):
    """Issues a formal cryptographic certification for an approved decision."""
    decision = _runtime.get_decision(req.decision_id)
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decision '{req.decision_id}' not found.",
        )
    cert = _runtime.cert_engine.issue_certification(
        decision=decision,
        evidence_package_id=req.evidence_package_id,
        approved_by=req.approved_by,
        validity_days=req.validity_days,
    )
    return {
        "certification_id": cert.id,
        "system_id": cert.system_id,
        "level": cert.certification_level.value,
        "status": cert.status.value,
        "signature": cert.signature,
        "expires_at": cert.expires_at,
    }


@router.get("/{cert_id}", response_model=Dict[str, Any])
def get_certification(cert_id: str):
    """Retrieves and validates a certification record by ID."""
    cert = _runtime.cert_engine.get_certification(cert_id)
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certification '{cert_id}' not found.",
        )
    is_valid = _runtime.cert_engine.verify_certification_validity(cert_id)
    return {
        "certification_id": cert.id,
        "system_id": cert.system_id,
        "level": cert.certification_level.value,
        "status": cert.status.value,
        "score": cert.score,
        "is_valid": is_valid,
        "expires_at": cert.expires_at,
    }


@router.post("/{cert_id}/approve", response_model=Dict[str, Any])
def approve_certification(cert_id: str, req: ReviewApprovalRequest):
    """Submits a human review approving or reviewing certification."""
    review = ApprovalReview(
        review_id=f"REV-{cert_id}",
        certification_id=cert_id,
        reviewer_id=req.reviewer_id,
        reviewer_role=req.reviewer_role,
        action=req.action,
        comments=req.comments,
    )
    _runtime.approval_workflow.submit_review(review)
    return {"status": "ReviewRecorded", "certification_id": cert_id, "action": req.action.value}


@router.post("/exceptions", response_model=Dict[str, Any])
def submit_exception(req: SubmitExceptionRequest):
    """Submits a quality gate exception request."""
    exc = ExceptionRequest(
        exception_id="",
        system_id=req.system_id,
        component=req.component,
        gate_id=req.gate_id,
        metric_name=req.metric_name,
        risk_level=req.risk_level,
        reason=req.reason,
        owner=req.owner,
        duration_days=req.duration_days,
    )
    result = _runtime.exception_manager.request_exception(exc)
    return {
        "exception_id": result.exception_id,
        "status": result.status.value,
        "expires_at": result.expires_at,
    }


@router.post("/impact-analysis", response_model=Dict[str, Any])
def analyze_change_impact(req: ChangeAnalysisRequest):
    """Analyzes system change impact and automatically invalidates affected certifications."""
    report = _runtime.change_impact_analyzer.analyze_change(
        change_type=req.change_type,
        changed_entity=req.changed_entity,
        version_before=req.version_before,
        version_after=req.version_after,
        system_id=req.system_id,
    )
    return {
        "change_id": report.change_id,
        "change_type": report.change_type.value,
        "invalidated_certifications": report.invalidated_certifications,
        "required_reverification_suites": report.required_reverification_suites,
    }


@router.get("/dashboard/overview", response_model=Dict[str, Any])
def get_certification_dashboard():
    """Retrieves real-time governance dashboard."""
    view = _runtime.dashboard_engine.build_dashboard_view()
    return {
        "active_certifications_count": view.active_certifications_count,
        "gate_summary": view.gate_summary,
        "risk_summary": view.risk_summary,
        "pending_approvals_count": view.pending_approvals_count,
        "expiring_soon_count": view.expiring_soon_count,
    }
