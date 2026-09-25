"""Enterprise Model Registry & Lifecycle Domain Models (Phase 8C)."""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator


class ModelLifecycleState(str, enum.Enum):
    """9-state Model Lifecycle FSM."""
    REGISTERED = "REGISTERED"
    EVALUATING = "EVALUATING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    RESTRICTED = "RESTRICTED"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"
    ARCHIVED = "ARCHIVED"


class ModelCategory(str, enum.Enum):
    """Supported model functional categories."""
    LLM = "LLM"
    FOUNDATION_LLM = "FOUNDATION_LLM"
    REASONING_LLM = "REASONING_LLM"
    EMBEDDING = "EMBEDDING"
    VISION = "VISION"
    SPEECH = "SPEECH"
    OCR = "OCR"
    CLASSIFICATION = "CLASSIFICATION"
    RERANKING = "RERANKING"
    TRANSLATION = "TRANSLATION"
    CODE = "CODE"
    REASONING = "REASONING"
    LOCAL = "LOCAL"
    CUSTOM = "CUSTOM"


class ModelProvider(str, enum.Enum):
    """Supported AI model providers."""
    GOOGLE = "GOOGLE"
    GOOGLE_GEMINI = "GOOGLE_GEMINI"
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    ANTHROPIC_CLAUDE = "ANTHROPIC_CLAUDE"
    AZURE_OPENAI = "AZURE_OPENAI"
    AWS_BEDROCK = "AWS_BEDROCK"
    VERTEX_AI = "VERTEX_AI"
    COHERE = "COHERE"
    MISTRAL = "MISTRAL"
    OLLAMA = "OLLAMA"
    HUGGINGFACE = "HUGGINGFACE"
    SELF_HOSTED = "SELF_HOSTED"
    CUSTOM = "CUSTOM"


class DeploymentType(str, enum.Enum):
    """Model deployment hosting architectures."""
    CLOUD_SaaS = "CLOUD_SaaS"
    MANAGED_CLOUD = "MANAGED_CLOUD"
    DEDICATED_ENDPOINT = "DEDICATED_ENDPOINT"
    ON_PREMISES = "ON_PREMISES"
    LOCAL_DEVICE = "LOCAL_DEVICE"
    VPC_PRIVATE = "VPC_PRIVATE"


class RiskLevel(str, enum.Enum):
    """Risk tiers for AI models."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ApprovalStatus(str, enum.Enum):
    """Multi-stage approval status."""
    PENDING_SUBMISSION = "PENDING_SUBMISSION"
    UNDER_TECHNICAL_REVIEW = "UNDER_TECHNICAL_REVIEW"
    UNDER_SECURITY_REVIEW = "UNDER_SECURITY_REVIEW"
    UNDER_COMPLIANCE_REVIEW = "UNDER_COMPLIANCE_REVIEW"
    UNDER_BUSINESS_APPROVAL = "UNDER_BUSINESS_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Model(BaseModel):
    """Canonical Governed AI Model Entity."""
    model_id: str
    name: Optional[str] = None
    model_name: Optional[str] = None
    provider: ModelProvider
    organization_id: str
    workspace_id: str = "default"
    owner_id: str = "system"
    family_id: str = ""
    category: ModelCategory = ModelCategory.LLM
    version: str = "1.0.0"
    status: ModelLifecycleState = ModelLifecycleState.REGISTERED
    lifecycle_state: ModelLifecycleState = ModelLifecycleState.REGISTERED
    approval_status: ApprovalStatus = ApprovalStatus.PENDING_SUBMISSION
    capabilities: Set[str] = Field(default_factory=set)
    deployment_type: DeploymentType = DeploymentType.MANAGED_CLOUD
    region: str = "us-east-1"
    residency_regions: List[str] = Field(default_factory=lambda: ["us-east-1"])
    license: str = "Commercial API"
    risk_level: RiskLevel = RiskLevel.MEDIUM
    context_window: int = 128000
    max_output_tokens: int = 4096
    input_token_cost_per_1k: float = 0.00015
    output_token_cost_per_1k: float = 0.00060
    replacement_model_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "lifecycle_state" and hasattr(self, "status"):
            super().__setattr__("status", value)
        elif name == "status" and hasattr(self, "lifecycle_state"):
            super().__setattr__("lifecycle_state", value)
        elif name == "name" and hasattr(self, "model_name"):
            super().__setattr__("model_name", value)
        elif name == "model_name" and hasattr(self, "name"):
            super().__setattr__("name", value)

    @model_validator(mode="before")
    @classmethod
    def sync_name_and_status_before(cls, values: Any) -> Any:
        if isinstance(values, dict):
            # Sync name <-> model_name
            if "name" in values and not values.get("model_name"):
                values["model_name"] = values["name"]
            elif "model_name" in values and not values.get("name"):
                values["name"] = values["model_name"]

            # Sync status <-> lifecycle_state
            if "lifecycle_state" in values and "status" not in values:
                values["status"] = values["lifecycle_state"]
            elif "status" in values and "lifecycle_state" not in values:
                values["lifecycle_state"] = values["status"]

        return values

    @model_validator(mode="after")
    def sync_name_and_status_after(self) -> Model:
        if self.name and not self.model_name:
            self.model_name = self.name
        elif self.model_name and not self.name:
            self.name = self.model_name

        if self.lifecycle_state != self.status:
            self.status = self.lifecycle_state
        return self
