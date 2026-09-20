"""Pydantic Schemas for Deployment Platform REST API."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Release Schemas ---
class CreateReleaseRequest(BaseModel):
    version: str
    name: str
    commit_sha: str
    artifact_ids: List[str] = Field(default_factory=list)
    changelog: str = ""
    created_by: str = "api-user"
    tags: List[str] = Field(default_factory=list)


class ReleaseResponse(BaseModel):
    release_id: str
    version: str
    name: str
    commit_sha: str
    artifact_ids: List[str]
    status: str
    created_at: str
    tags: List[str]


# --- Deployment Schemas ---
class CreateDeploymentRequest(BaseModel):
    release_id: str
    target_environment: str
    strategy: str = "ROLLING"
    replicas: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DeploymentResponse(BaseModel):
    deployment_id: str
    release_id: str
    target_environment: str
    strategy: str
    replicas: int
    status: str
    started_at: str
    traffic_weight: float


# --- Rollback Schemas ---
class RollbackRequest(BaseModel):
    deployment_id: str
    target_release_id: Optional[str] = None
    reason: str = "API requested rollback"


class RollbackResponse(BaseModel):
    rollback_id: str
    failed_deployment_id: str
    target_release_id: str
    environment: str
    success: bool
    executed_at: str


# --- Promotion Schemas ---
class RequestPromotionSchema(BaseModel):
    release_id: str
    target_env: str
    source_env: Optional[str] = None
    requested_by: str = "api-user"


class ApprovePromotionSchema(BaseModel):
    role: str
    approver: str


class PromotionResponse(BaseModel):
    promotion_id: str
    release_id: str
    target_env: str
    status: str
    approved_roles: List[str]


# --- Feature Flag Schemas ---
class CreateFlagRequest(BaseModel):
    key: str
    name: str
    description: str = ""
    enabled: bool = False
    rollout_percentage: int = 100
    allowed_tenants: List[str] = Field(default_factory=list)
    allowed_environments: List[str] = Field(default_factory=list)


class EvaluateFlagRequest(BaseModel):
    key: str
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    environment: str = "prod"


class FlagEvaluationResponse(BaseModel):
    key: str
    enabled: bool
