"""FastAPI Endpoints for Enterprise Deployment Platform."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from ..core.deployment import DeploymentStrategyType
from ..sdk.client import InfrastructureSDK
from .schemas import (
    ApprovePromotionSchema,
    CreateDeploymentRequest,
    CreateFlagRequest,
    CreateReleaseRequest,
    DeploymentResponse,
    EvaluateFlagRequest,
    FlagEvaluationResponse,
    PromotionResponse,
    ReleaseResponse,
    RequestPromotionSchema,
    RollbackRequest,
    RollbackResponse,
)

router = APIRouter(prefix="/api/v1/deployment", tags=["Deployment Platform"])
_sdk = InfrastructureSDK()


def get_sdk() -> InfrastructureSDK:
    """Returns the shared SDK singleton."""
    return _sdk


# --- Releases ---
@router.post("/releases", response_model=ReleaseResponse, status_code=status.HTTP_201_CREATED)
def create_release(req: CreateReleaseRequest):
    try:
        rel = _sdk.create_release(
            version=req.version,
            name=req.name,
            commit_sha=req.commit_sha,
            artifact_ids=req.artifact_ids,
            changelog=req.changelog,
            auto_publish=True,
        )
        return ReleaseResponse(
            release_id=rel.release_id,
            version=rel.version,
            name=rel.name,
            commit_sha=rel.commit_sha,
            artifact_ids=rel.artifact_ids,
            status=rel.status.value,
            created_at=rel.created_at.isoformat(),
            tags=rel.tags,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/releases", response_model=List[ReleaseResponse])
def list_releases():
    releases = _sdk.controller.list_releases()
    return [
        ReleaseResponse(
            release_id=r.release_id,
            version=r.version,
            name=r.name,
            commit_sha=r.commit_sha,
            artifact_ids=r.artifact_ids,
            status=r.status.value,
            created_at=r.created_at.isoformat(),
            tags=r.tags,
        )
        for r in releases
    ]


# --- Deployments ---
@router.post("/deployments", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
def create_deployment(req: CreateDeploymentRequest):
    try:
        strat = DeploymentStrategyType(req.strategy.upper())
        dep = _sdk.deploy(
            release_id=req.release_id,
            target_environment=req.target_environment,
            strategy=strat,
            replicas=req.replicas,
            metadata=req.metadata,
        )
        return DeploymentResponse(
            deployment_id=dep.deployment_id,
            release_id=dep.release_id,
            target_environment=dep.target_environment,
            strategy=dep.strategy.value,
            replicas=dep.replicas,
            status=dep.status.value,
            started_at=dep.started_at.isoformat(),
            traffic_weight=dep.traffic_weight,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/deployments", response_model=List[DeploymentResponse])
def list_deployments(environment: Optional[str] = None):
    deps = _sdk.controller.list_deployments(environment=environment)
    return [
        DeploymentResponse(
            deployment_id=d.deployment_id,
            release_id=d.release_id,
            target_environment=d.target_environment,
            strategy=d.strategy.value,
            replicas=d.replicas,
            status=d.status.value,
            started_at=d.started_at.isoformat(),
            traffic_weight=d.traffic_weight,
        )
        for d in deps
    ]


# --- Rollback ---
@router.post("/rollback", response_model=RollbackResponse)
def execute_rollback(req: RollbackRequest):
    try:
        rec = _sdk.rollback(
            deployment_id=req.deployment_id,
            target_release_id=req.target_release_id,
            reason=req.reason,
        )
        return RollbackResponse(
            rollback_id=rec.rollback_id,
            failed_deployment_id=rec.failed_deployment_id,
            target_release_id=rec.target_release_id,
            environment=rec.environment,
            success=rec.success,
            executed_at=rec.executed_at.isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Promotions ---
@router.post("/promotions", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
def request_promotion(req: RequestPromotionSchema):
    try:
        rec = _sdk.promotions.request_promotion(
            release_id=req.release_id,
            target_env=req.target_env,
            source_env=req.source_env,
            requested_by=req.requested_by,
        )
        return PromotionResponse(
            promotion_id=rec.promotion_id,
            release_id=rec.release_id,
            target_env=rec.target_env,
            status=rec.status.value,
            approved_roles=rec.approved_roles,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/promotions/{promotion_id}/approve", response_model=PromotionResponse)
def approve_promotion(promotion_id: str, req: ApprovePromotionSchema):
    try:
        rec = _sdk.promotions.approve_promotion(
            promotion_id=promotion_id,
            role=req.role,
            approver_identity=req.approver,
        )
        return PromotionResponse(
            promotion_id=rec.promotion_id,
            release_id=rec.release_id,
            target_env=rec.target_env,
            status=rec.status.value,
            approved_roles=rec.approved_roles,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Feature Flags ---
@router.post("/flags", status_code=status.HTTP_201_CREATED)
def create_flag(req: CreateFlagRequest):
    try:
        flag = _sdk.flags.create_flag(
            key=req.key,
            name=req.name,
            description=req.description,
            enabled=req.enabled,
            allowed_tenants=req.allowed_tenants,
            allowed_environments=req.allowed_environments,
            rollout_percentage=req.rollout_percentage,
        )
        return flag.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/flags/evaluate", response_model=FlagEvaluationResponse)
def evaluate_flag(req: EvaluateFlagRequest):
    is_on = _sdk.is_feature_enabled(
        key=req.key,
        tenant_id=req.tenant_id,
        user_id=req.user_id,
        environment=req.environment,
    )
    return FlagEvaluationResponse(key=req.key, enabled=is_on)
