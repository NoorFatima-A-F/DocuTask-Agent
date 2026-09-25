"""FastAPI Pydantic Schemas for Prompt Governance API (Phase 8D)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptCategory, PromptLifecycleState, RiskLevel
from app.prompts.approvals.workflow import ApprovalStageStatus
from app.prompts.deployment.publisher import DeploymentEnvironment


class PromptCreateRequestDTO(BaseModel):
    prompt_id: str
    name: str
    owner: str
    category: PromptCategory = PromptCategory.TASK_PROMPT
    description: str = ""
    purpose: str = ""
    initial_template: str = ""
    variables: List[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    tags: Set[str] = Field(default_factory=set)


class PromptVersionCreateRequestDTO(BaseModel):
    template_text: str
    version_number: str
    author: str
    change_reason: str
    variables: List[str] = Field(default_factory=list)
    expected_output_schema: Optional[Dict[str, Any]] = None


class PromptLifecycleTransitionRequestDTO(BaseModel):
    target_state: PromptLifecycleState
    actor: str
    reason: str


class PromptApprovalReviewRequestDTO(BaseModel):
    stage_name: str
    reviewer: str
    decision: ApprovalStageStatus
    comments: Optional[str] = None


class PromptDeployRequestDTO(BaseModel):
    version_id: str
    environment: DeploymentEnvironment = DeploymentEnvironment.PRODUCTION
    deployed_by: str
    traffic_percentage: float = 100.0


class PromptRenderRequestDTO(BaseModel):
    variables: Dict[str, Any] = Field(default_factory=dict)
    version_id: Optional[str] = None
