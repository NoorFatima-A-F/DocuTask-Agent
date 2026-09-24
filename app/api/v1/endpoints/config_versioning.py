"""
FastAPI REST Gateway for Enterprise Configuration, Versioning & Dependency Management.
Part 1.1E of the Enterprise Verification Platform.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.platform_verification.config_versioning.domain.models import (
    ConfigurationSnapshot,
    ConfigurationDiff,
    DependencyItem,
    SBOMManifest,
    DriftReport,
    ChangeRequest,
    RollbackRecord,
    EnvironmentFingerprint,
    EnvironmentTier,
    PromptTemplateVersion,
)
from app.platform_verification.config_versioning.runtime.config_versioning_runtime import (
    EnterpriseConfigVersioningRuntime,
    config_versioning_runtime,
)

router = APIRouter(tags=["Verification Configuration & Versioning"])

def get_config_runtime() -> EnterpriseConfigVersioningRuntime:
    return config_versioning_runtime


class ResolveSnapshotRequest(BaseModel):
    environment: EnvironmentTier = EnvironmentTier.INTEGRATION
    module_name: Optional[str] = None
    overrides: Optional[Dict[str, Any]] = None
    creator: str = "Enterprise Platform Engineer"


class DiffRequest(BaseModel):
    snapshot_a_id: str
    snapshot_b_id: str


class DriftDetectRequest(BaseModel):
    baseline_snapshot_id: str
    environment: EnvironmentTier = EnvironmentTier.INTEGRATION
    module_name: Optional[str] = None
    live_overrides: Optional[Dict[str, Any]] = None


class SubmitChangeRequest(BaseModel):
    target_environment: EnvironmentTier
    title: str
    description: str
    requested_by: str
    target_snapshot_id: str
    previous_snapshot_id: Optional[str] = None


class ApproveChangeRequest(BaseModel):
    approver: str


class RollbackExecutionRequest(BaseModel):
    executed_by: str
    reason: str


# 1. Resolution & Snapshot Management
@router.post("/resolve-and-snapshot", response_model=ConfigurationSnapshot)
def resolve_and_snapshot(
    request: ResolveSnapshotRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    try:
        return runtime.resolve_and_snapshot(
            environment=request.environment,
            module_name=request.module_name,
            overrides=request.overrides,
            creator=request.creator,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/snapshots", response_model=List[ConfigurationSnapshot])
def list_snapshots(
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.snapshots.list_snapshots()


@router.get("/snapshots/{snapshot_id}", response_model=ConfigurationSnapshot)
def get_snapshot(
    snapshot_id: str,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    snapshot = runtime.snapshots.get_snapshot(snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail=f"Snapshot {snapshot_id} not found")
    return snapshot


# 2. Configuration Diff Engine
@router.post("/diff", response_model=ConfigurationDiff)
def compare_snapshots(
    request: DiffRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    try:
        return runtime.diff.compare(request.snapshot_a_id, request.snapshot_b_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. SBOM & Dependency Management
@router.get("/sbom/cyclonedx", response_model=SBOMManifest)
def get_cyclonedx_sbom(
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.sbom.generate_cyclonedx_sbom()


@router.get("/sbom/spdx", response_model=SBOMManifest)
def get_spdx_sbom(
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.sbom.generate_spdx_sbom()


@router.get("/dependencies", response_model=List[DependencyItem])
def list_dependencies(
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.dependencies.get_all_dependencies()


# 4. Environment Fingerprinting
@router.get("/fingerprint", response_model=EnvironmentFingerprint)
def get_environment_fingerprint(
    tier: EnvironmentTier = EnvironmentTier.INTEGRATION,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.fingerprint.capture_fingerprint(tier=tier)


# 5. Drift Detection
@router.post("/drift/detect", response_model=DriftReport)
def detect_configuration_drift(
    request: DriftDetectRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    baseline = runtime.snapshots.get_snapshot(request.baseline_snapshot_id)
    if not baseline:
        raise HTTPException(
            status_code=404,
            detail=f"Baseline snapshot {request.baseline_snapshot_id} not found",
        )

    live_config = runtime.resolver.resolve(
        environment=request.environment,
        module_name=request.module_name,
        experiment_override=request.live_overrides,
    )
    return runtime.drift.detect_drift(baseline, live_config)


# 6. Change Management & Rollback
@router.post("/changes/submit", response_model=ChangeRequest)
def submit_change(
    request: SubmitChangeRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.changes.submit_change_request(
        target_environment=request.target_environment,
        title=request.title,
        description=request.description,
        requested_by=request.requested_by,
        target_snapshot_id=request.target_snapshot_id,
        previous_snapshot_id=request.previous_snapshot_id,
    )


@router.post("/changes/{change_id}/approve", response_model=ChangeRequest)
def approve_change(
    change_id: str,
    request: ApproveChangeRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    try:
        return runtime.changes.approve_change_request(change_id, request.approver)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/changes/{change_id}/rollback", response_model=RollbackRecord)
def execute_rollback(
    change_id: str,
    request: RollbackExecutionRequest,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    try:
        return runtime.changes.execute_rollback(
            change_id=change_id,
            executed_by=request.executed_by,
            reason=request.reason,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 7. AI Artifacts Version Management
@router.get("/ai-artifacts/prompts", response_model=List[PromptTemplateVersion])
def list_prompts(
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.ai_artifacts.list_prompts()


@router.post("/ai-artifacts/prompts", response_model=PromptTemplateVersion)
def register_prompt_version(
    prompt: PromptTemplateVersion,
    runtime: EnterpriseConfigVersioningRuntime = Depends(get_config_runtime),
):
    return runtime.ai_artifacts.register_prompt_version(prompt)
