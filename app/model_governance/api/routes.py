"""FastAPI Router for Enterprise Model Registry & Governance (Phase 8C)."""

from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.model_governance.registry.models import Model, ModelLifecycleState
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.registry.service import ModelRegistryService
from app.model_governance.lifecycle.manager import ModelLifecycleManager
from app.model_governance.approval.workflow import ModelApprovalWorkflowEngine
from app.model_governance.selection.selector import (
    ModelSelectionRequest,
    ModelSelectionService,
)
from app.model_governance.risk.scoring import ModelRiskScorer
from app.model_governance.reproducibility.snapshot import ReproducibilityService
from app.model_governance.analytics.usage import ModelUsageTracker
from app.model_governance.analytics.cost import ModelCostCalculator
from app.model_governance.api.schemas import (
    ApprovalReviewRequestDTO,
    LifecycleTransitionRequestDTO,
    ModelRegisterRequestDTO,
    ModelSelectRequestDTO,
    SnapshotCaptureRequestDTO,
)


router = APIRouter(prefix="/api/v1/governance/models", tags=["Model Governance"])

# Singletons / Dependency instances for router
_repo = ModelRegistryRepository()
_registry_service = ModelRegistryService(_repo)
_lifecycle_manager = ModelLifecycleManager(_repo)
_approval_engine = ModelApprovalWorkflowEngine(_repo, _lifecycle_manager)
_selection_service = ModelSelectionService(_repo)
_risk_scorer = ModelRiskScorer()
_reproducibility_service = ReproducibilityService()
_usage_tracker = ModelUsageTracker()
_cost_calc = ModelCostCalculator()


@router.post("", response_model=Model, status_code=status.HTTP_201_CREATED)
def register_model(payload: ModelRegisterRequestDTO, organization_id: str = Query("org_default")):
    model = Model(
        model_id=payload.model_id,
        model_name=payload.model_name,
        organization_id=organization_id,
        family_id=payload.family_id,
        version=payload.version,
        category=payload.category,
        provider=payload.provider,
        deployment_type=payload.deployment_type,
        capabilities=payload.capabilities,
        context_window=payload.context_window,
        max_output_tokens=payload.max_output_tokens,
        input_token_cost_per_1k=payload.input_token_cost_per_1k,
        output_token_cost_per_1k=payload.output_token_cost_per_1k,
        risk_level=payload.risk_level,
        residency_regions=payload.residency_regions,
        metadata=payload.metadata,
    )
    return _registry_service.register_model(model)


@router.get("", response_model=List[Model])
def list_models(
    organization_id: str = Query("org_default"),
    state: Optional[ModelLifecycleState] = None,
):
    return _registry_service.list_models(organization_id=organization_id, status=state)


@router.get("/{model_id}", response_model=Model)
def get_model(model_id: str, organization_id: str = Query("org_default")):
    model = _registry_service.get_model(model_id, organization_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("/{model_id}/lifecycle/transition")
def transition_lifecycle(
    model_id: str,
    payload: LifecycleTransitionRequestDTO,
    organization_id: str = Query("org_default"),
):
    try:
        return _lifecycle_manager.transition(
            model_id=model_id,
            target_state=payload.target_state,
            actor=payload.actor,
            reason=payload.reason,
            organization_id=organization_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{model_id}/approval/submit")
def submit_for_approval(model_id: str, organization_id: str = Query("org_default")):
    try:
        return _approval_engine.initiate_workflow(model_id, organization_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{model_id}/approval/review")
def review_approval_stage(
    model_id: str,
    payload: ApprovalReviewRequestDTO,
    organization_id: str = Query("org_default"),
):
    try:
        return _approval_engine.review_stage(
            model_id=model_id,
            stage_name=payload.stage_name,
            reviewer=payload.reviewer,
            decision=payload.decision,
            comments=payload.comments,
            organization_id=organization_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/select")
def select_model(payload: ModelSelectRequestDTO, organization_id: str = Query("org_default")):
    try:
        req = ModelSelectionRequest(
            task_name=payload.task_name,
            organization_id=organization_id,
            required_capabilities=payload.required_capabilities,
            max_latency_ms=payload.max_latency_ms,
            max_input_cost_per_1k=payload.max_input_cost_per_1k,
            target_region=payload.target_region,
        )
        return _selection_service.select_model(req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/snapshots")
def capture_snapshot(payload: SnapshotCaptureRequestDTO, organization_id: str = Query("org_default")):
    return _reproducibility_service.capture_snapshot(
        snapshot_id=payload.snapshot_id,
        organization_id=organization_id,
        task_name=payload.task_name,
        model_id=payload.model_id,
        model_version=payload.model_version,
        provider=payload.provider,
        prompt_text=payload.prompt_text,
        system_prompt=payload.system_prompt,
        input_data=payload.input_data,
        hyperparameters=payload.hyperparameters,
        workflow_id=payload.workflow_id,
        agent_id=payload.agent_id,
    )


@router.get("/snapshots/{snapshot_id}/verify")
def verify_snapshot(snapshot_id: str):
    is_valid = _reproducibility_service.verify_reproducibility(snapshot_id)
    return {"snapshot_id": snapshot_id, "is_valid": is_valid}
