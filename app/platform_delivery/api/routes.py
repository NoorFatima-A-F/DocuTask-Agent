"""FastAPI Endpoints for Platform Delivery Operating System (Req 63, 64, 65, 66)."""
from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status

from ..sdk.client import InfrastructureSDK
from .schemas import (
    CreateDeploymentRequest,
    CreateReleaseRequest,
    DeploymentResponseSchema,
    PromoteReleaseRequest,
    QuarantineRequestSchema,
    ReleaseResponseSchema,
    RollbackRequestSchema,
    RollbackResponseSchema,
    VerifyArtifactResponseSchema,
)

router = APIRouter(prefix="/api/v1/platform", tags=["Platform Delivery Control Plane"])
_sdk = InfrastructureSDK()


def get_delivery_sdk() -> InfrastructureSDK:
    return _sdk


# --- Releases ---
@router.post("/releases", response_model=ReleaseResponseSchema, status_code=status.HTTP_201_CREATED)
def create_release(req: CreateReleaseRequest):
    try:
        rel = _sdk.release(version=req.version, commit_sha=req.commit_sha)
        return ReleaseResponseSchema(
            release_id=rel.release_id,
            version=rel.version,
            commit_sha=rel.commit_sha,
            status=rel.status.value,
            artifacts=rel.artifacts,
            created_at=rel.created_at.isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/releases/{id}", response_model=ReleaseResponseSchema)
def get_release(id: str):
    rel = _sdk.release_manager.get_release(id)
    if not rel:
        raise HTTPException(status_code=404, detail="Release not found")
    return ReleaseResponseSchema(
        release_id=rel.release_id,
        version=rel.version,
        commit_sha=rel.commit_sha,
        status=rel.status.value,
        artifacts=rel.artifacts,
        created_at=rel.created_at.isoformat(),
    )


@router.post("/releases/{id}/promote", response_model=DeploymentResponseSchema)
def promote_release(id: str, req: PromoteReleaseRequest):
    try:
        dep = _sdk.promote(release_id=id, target_env=req.target_env, source_env=req.source_env, strategy=req.strategy)
        return DeploymentResponseSchema(
            deployment_id=dep.deployment_id,
            release_id=dep.release_id,
            environment_id=dep.environment_id,
            strategy=dep.strategy,
            status=dep.status.value,
            traffic_weight=dep.traffic_weight,
            created_at=dep.created_at.isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Deployments ---
@router.post("/deployments", response_model=DeploymentResponseSchema, status_code=status.HTTP_201_CREATED)
def create_deployment(
    req: CreateDeploymentRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    try:
        dep = _sdk.deploy(
            release_id=req.release_id,
            environment_id=req.environment_id,
            strategy=req.strategy,
            replicas=req.replicas,
            idempotency_key=idempotency_key,
        )
        return DeploymentResponseSchema(
            deployment_id=dep.deployment_id,
            release_id=dep.release_id,
            environment_id=dep.environment_id,
            strategy=dep.strategy,
            status=dep.status.value,
            traffic_weight=dep.traffic_weight,
            created_at=dep.created_at.isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/deployments/{id}", response_model=DeploymentResponseSchema)
def get_deployment(id: str):
    dep = _sdk.control_plane.get_deployment(type("Query", (), {"deployment_id": id})())
    if not dep:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return DeploymentResponseSchema(
        deployment_id=dep.deployment_id,
        release_id=dep.release_id,
        environment_id=dep.environment_id,
        strategy=dep.strategy,
        status=dep.status.value,
        traffic_weight=dep.traffic_weight,
        created_at=dep.created_at.isoformat(),
    )


@router.post("/deployments/{id}/rollback", response_model=RollbackResponseSchema)
def rollback_deployment(id: str, req: RollbackRequestSchema):
    try:
        inc = _sdk.rollback(deployment_id=id, reason=req.reason, target_version=req.target_version)
        return RollbackResponseSchema(
            incident_id=inc.incident_id,
            deployment_id=inc.deployment_id,
            failed_version=inc.failed_version,
            restored_version=inc.restored_version,
            reason=inc.reason,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Artifacts ---
@router.post("/artifacts/{digest}/verify", response_model=VerifyArtifactResponseSchema)
def verify_artifact(digest: str):
    report = _sdk.verify_artifact(artifact_digest=digest)
    return VerifyArtifactResponseSchema(
        artifact_digest=report.artifact_digest,
        passed=report.passed,
        denial_reasons=report.denial_reasons,
    )


@router.post("/artifacts/{digest}/quarantine")
def quarantine_artifact(digest: str, req: QuarantineRequestSchema):
    try:
        art = _sdk.artifact_registry.quarantine_artifact(digest=digest, reason=req.reason)
        return {"status": "QUARANTINED", "digest": art.digest, "reason": art.quarantine_reason}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
