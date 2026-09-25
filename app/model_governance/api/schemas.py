"""FastAPI Pydantic Schemas for Model Governance REST API (Phase 8C)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from app.model_governance.registry.models import (
    DeploymentType,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)
from app.model_governance.approval.approvals import StageStatus


class ModelRegisterRequestDTO(BaseModel):
    model_id: str
    model_name: str
    organization_id: str
    family_id: str
    version: str
    category: ModelCategory
    provider: ModelProvider
    deployment_type: DeploymentType = DeploymentType.MANAGED_CLOUD
    capabilities: Set[str] = Field(default_factory=set)
    context_window: int = 128000
    max_output_tokens: int = 4096
    input_token_cost_per_1k: float = 0.001
    output_token_cost_per_1k: float = 0.002
    risk_level: RiskLevel = RiskLevel.MEDIUM
    residency_regions: List[str] = Field(default_factory=lambda: ["us-east-1"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LifecycleTransitionRequestDTO(BaseModel):
    target_state: ModelLifecycleState
    actor: str
    reason: str


class ApprovalReviewRequestDTO(BaseModel):
    stage_name: str
    reviewer: str
    decision: StageStatus  # APPROVED or REJECTED
    comments: Optional[str] = None


class ModelSelectRequestDTO(BaseModel):
    task_name: str
    required_capabilities: Set[str] = Field(default_factory=set)
    max_latency_ms: Optional[float] = None
    max_input_cost_per_1k: Optional[float] = None
    target_region: str = "us-east-1"


class BenchmarkRunRequestDTO(BaseModel):
    dataset_name: str
    dataset_version: str = "1.0.0"
    domain: str = "general"
    samples: List[Dict[str, Any]] = Field(default_factory=list)


class RiskAssessmentRequestDTO(BaseModel):
    security_eval: float = 0.8
    compliance_eval: float = 0.8
    robustness_eval: float = 0.8
    fairness_eval: float = 0.8
    notes: Optional[str] = None


class SnapshotCaptureRequestDTO(BaseModel):
    snapshot_id: str
    task_name: str
    model_id: str
    model_version: str
    provider: str
    prompt_text: str
    system_prompt: str
    input_data: Any
    hyperparameters: Optional[Dict[str, Any]] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
