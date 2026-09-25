"""FastAPI REST routes for Deployment Control Plane, Releases, GitOps, and Artifacts."""

from dataclasses import asdict
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..sdk.deployment_sdk import DeploymentSDK
from ..control_plane.state import DeploymentStrategyType
from ..rollback.executor import RollbackTriggerType

router = APIRouter(prefix="/deployments", tags=["Enterprise Deployment & Release Engineering"])

# Global singleton SDK
_deployment_sdk: Optional[DeploymentSDK] = None


def get_deployment_sdk() -> DeploymentSDK:
    """Get singleton DeploymentSDK."""
    global _deployment_sdk
    if _deployment_sdk is None:
        _deployment_sdk = DeploymentSDK()
    return _deployment_sdk


# --- Pydantic Request Models ---
class DeploymentCreateRequest(BaseModel):
    service_name: str
    target_environment: str
    target_version: str
    release_id: Optional[str] = None
    strategy: str = "rolling"


class RollbackTriggerRequest(BaseModel):
    reason: str = "Operator rollback"
    trigger_type: str = "manual"


class ReleaseCreateRequest(BaseModel):
    version: str
    components_changed: List[str]
    artifact_ids: List[str]
    changelog: str = ""
    target_environments: List[str] = Field(default_factory=lambda: ["staging", "prod"])


class PipelineRunRequest(BaseModel):
    pipeline_name: str
    commit_sha: str


class PromoteRequest(BaseModel):
    from_env: str
    to_env: str
    release_id: str
    artifact_id: str
    approvers: List[str] = Field(default_factory=list)


class FeatureFlagCreateRequest(BaseModel):
    flag_key: str
    percentage: float = 100.0


# --- Endpoints ---
@router.get("")
def list_deployments(service_name: Optional[str] = None, environment: Optional[str] = None) -> Dict[str, Any]:
    """List deployments."""
    sdk = get_deployment_sdk()
    deps = sdk.control_plane.list_deployments(service_name=service_name, environment=environment)
    return {
        "deployments_count": len(deps),
        "deployments": [asdict(d) for d in deps],
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def trigger_deployment(req: DeploymentCreateRequest) -> Dict[str, Any]:
    """Trigger a new deployment."""
    sdk = get_deployment_sdk()
    strat = DeploymentStrategyType(req.strategy.lower()) if req.strategy.lower() in [s.value for s in DeploymentStrategyType] else DeploymentStrategyType.ROLLING

    try:
        record = sdk.deploy(
            service_name=req.service_name,
            target_environment=req.target_environment,
            target_version=req.target_version,
            release_id=req.release_id,
            strategy=strat,
        )
        return asdict(record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{deployment_id}")
def get_deployment(deployment_id: str) -> Dict[str, Any]:
    """Get deployment details by ID."""
    sdk = get_deployment_sdk()
    dep = sdk.control_plane.get_deployment(deployment_id)
    if not dep:
        raise HTTPException(status_code=404, detail=f"Deployment '{deployment_id}' not found")
    return asdict(dep)


@router.post("/{deployment_id}/rollback")
def rollback_deployment(deployment_id: str, req: RollbackTriggerRequest) -> Dict[str, Any]:
    """Trigger rollback for a deployment."""
    sdk = get_deployment_sdk()
    tt = RollbackTriggerType(req.trigger_type.lower()) if req.trigger_type.lower() in [t.value for t in RollbackTriggerType] else RollbackTriggerType.MANUAL
    try:
        rca = sdk.rollback(deployment_id=deployment_id, reason=req.reason, trigger_type=tt)
        return asdict(rca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/releases/list")
def list_releases() -> Dict[str, Any]:
    """List all releases."""
    sdk = get_deployment_sdk()
    rels = sdk.release_manager.list_releases()
    return {
        "releases_count": len(rels),
        "releases": [asdict(r) for r in rels],
    }


@router.post("/releases/create", status_code=status.HTTP_201_CREATED)
def create_release(req: ReleaseCreateRequest) -> Dict[str, Any]:
    """Create a new release metadata record."""
    sdk = get_deployment_sdk()
    try:
        rel = sdk.create_release(
            version=req.version,
            components_changed=req.components_changed,
            artifact_ids=req.artifact_ids,
            changelog=req.changelog,
            target_environments=req.target_environments,
        )
        return asdict(rel)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pipelines/list")
def list_pipelines() -> Dict[str, Any]:
    """List CI/CD pipeline runs."""
    sdk = get_deployment_sdk()
    runs = sdk.pipeline_engine.list_runs()
    return {
        "runs_count": len(runs),
        "runs": [asdict(r) for r in runs],
    }


@router.post("/pipelines/run")
def run_pipeline(req: PipelineRunRequest) -> Dict[str, Any]:
    """Execute a CI/CD pipeline."""
    sdk = get_deployment_sdk()
    run = sdk.run_pipeline(pipeline_name=req.pipeline_name, commit_sha=req.commit_sha)
    return asdict(run)


@router.get("/artifacts/list")
def list_artifacts(name: Optional[str] = None) -> Dict[str, Any]:
    """List registered artifacts."""
    sdk = get_deployment_sdk()
    arts = sdk.artifact_registry.list_artifacts(name=name)
    return {
        "artifacts_count": len(arts),
        "artifacts": [asdict(a) for a in arts],
    }


@router.post("/promote")
def promote_artifact(req: PromoteRequest) -> Dict[str, Any]:
    """Promote artifact across environments."""
    sdk = get_deployment_sdk()
    try:
        chk = sdk.promote(
            from_env=req.from_env,
            to_env=req.to_env,
            release_id=req.release_id,
            artifact_id=req.artifact_id,
            approvers=req.approvers,
        )
        return asdict(chk)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/features")
def create_or_enable_feature(req: FeatureFlagCreateRequest) -> Dict[str, Any]:
    """Enable or create a feature flag."""
    sdk = get_deployment_sdk()
    flag = sdk.enable_feature(req.flag_key, percentage=req.percentage)
    return asdict(flag)
