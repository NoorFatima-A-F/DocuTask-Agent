"""Pydantic Request & Response Schemas for Platform Delivery REST APIs."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreateReleaseRequest(BaseModel):
    version: str
    commit_sha: str
    created_by: str = "release-engineer"
    components: List[Dict[str, Any]] = Field(default_factory=list)


class ReleaseResponseSchema(BaseModel):
    release_id: str
    version: str
    commit_sha: str
    status: str
    artifacts: List[str]
    created_at: str


class CreateDeploymentRequest(BaseModel):
    release_id: str
    environment_id: str
    strategy: str = "ROLLING"
    replicas: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DeploymentResponseSchema(BaseModel):
    deployment_id: str
    release_id: str
    environment_id: str
    strategy: str
    status: str
    traffic_weight: float
    created_at: str


class RollbackRequestSchema(BaseModel):
    reason: str
    target_version: str = "1.0.0"


class RollbackResponseSchema(BaseModel):
    incident_id: str
    deployment_id: str
    failed_version: str
    restored_version: str
    reason: str


class PromoteReleaseRequest(BaseModel):
    target_env: str
    source_env: Optional[str] = None
    strategy: str = "ROLLING"


class VerifyArtifactResponseSchema(BaseModel):
    artifact_digest: str
    passed: bool
    denial_reasons: List[str]


class QuarantineRequestSchema(BaseModel):
    reason: str
    reported_by: str = "security_scanner"
