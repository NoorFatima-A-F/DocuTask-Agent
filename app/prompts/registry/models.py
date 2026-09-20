"""Enterprise Prompt Domain Models (Phase 8D).

Treats prompts as first-class, versioned, evaluated, and governed enterprise software assets.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator


class PromptLifecycleState(str, enum.Enum):
    """10-state Prompt Lifecycle FSM."""
    DRAFT = "DRAFT"
    VALIDATION = "VALIDATION"
    TESTING = "TESTING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    EXPERIMENTAL = "EXPERIMENTAL"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class PromptCategory(str, enum.Enum):
    """Supported prompt functional categories."""
    SYSTEM_PROMPT = "SYSTEM_PROMPT"
    TASK_PROMPT = "TASK_PROMPT"
    AGENT_PROMPT = "AGENT_PROMPT"
    CHAIN_PROMPT = "CHAIN_PROMPT"
    RAG_PROMPT = "RAG_PROMPT"
    TOOL_PROMPT = "TOOL_PROMPT"
    CLASSIFICATION_PROMPT = "CLASSIFICATION_PROMPT"
    EXTRACTION_PROMPT = "EXTRACTION_PROMPT"
    SUMMARIZATION_PROMPT = "SUMMARIZATION_PROMPT"
    REASONING_PROMPT = "REASONING_PROMPT"
    CUSTOM = "CUSTOM"


class RiskLevel(str, enum.Enum):
    """Risk classification for prompt assets."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PromptApprovalStatus(str, enum.Enum):
    """Approval gate status."""
    NOT_SUBMITTED = "NOT_SUBMITTED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PromptVersion(BaseModel):
    """Immutable version snapshot of an enterprise prompt."""
    version_id: str
    prompt_id: str
    version_number: str = "1.0.0"
    content_hash: str
    prompt_template: str
    variables: List[str] = Field(default_factory=list)
    model_compatibility: List[str] = Field(default_factory=lambda: ["*"])
    expected_output_schema: Optional[Dict[str, Any]] = None
    change_reason: str = "Initial version"
    created_by: str = "system"
    approval_status: PromptApprovalStatus = PromptApprovalStatus.NOT_SUBMITTED
    evaluation_score: Optional[float] = None
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Prompt(BaseModel):
    """Canonical Governed Enterprise Prompt Entity."""
    prompt_id: str
    name: str
    description: str = ""
    purpose: str = ""
    category: PromptCategory = PromptCategory.TASK_PROMPT
    organization_id: str
    workspace_id: str = "default"
    owner: str
    department: str = "AI Engineering"
    risk_level: RiskLevel = RiskLevel.MEDIUM
    status: PromptLifecycleState = PromptLifecycleState.DRAFT
    lifecycle_state: PromptLifecycleState = PromptLifecycleState.DRAFT
    current_version: str = "1.0.0"
    active_version_id: Optional[str] = None
    tags: Set[str] = Field(default_factory=set)
    allowed_models: List[str] = Field(default_factory=lambda: ["*"])
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_by: str = "system"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "lifecycle_state" and hasattr(self, "status"):
            super().__setattr__("status", value)
        elif name == "status" and hasattr(self, "lifecycle_state"):
            super().__setattr__("lifecycle_state", value)

    @model_validator(mode="before")
    @classmethod
    def sync_status_before(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "lifecycle_state" in values and "status" not in values:
                values["status"] = values["lifecycle_state"]
            elif "status" in values and "lifecycle_state" not in values:
                values["lifecycle_state"] = values["status"]
        return values

    @model_validator(mode="after")
    def sync_status_after(self) -> Prompt:
        if self.lifecycle_state != self.status:
            self.status = self.lifecycle_state
        return self
