"""Request DTOs for the Public and Internal Governance Platform APIs."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PolicyCreateRequest(BaseModel):
    """Payload to create a new governance policy."""

    name: str = Field(..., min_length=3, max_length=128)
    description: str = Field(..., max_length=1024)
    policy_type: str = Field("operational", description="security, compliance, privacy, operational, or model")
    severity: str = Field("HIGH", description="LOW, MEDIUM, HIGH, CRITICAL")
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    enforcement_action: str = Field("DENY", description="DENY, APPROVAL_REQUIRED, AUDIT_ONLY, WARN")
    tags: List[str] = Field(default_factory=list)


class PolicyPublishRequest(BaseModel):
    """Payload to publish or activate an existing policy version."""

    version: Optional[str] = None
    changelog: Optional[str] = "Publishing governance policy"


class DecisionEvaluationRequest(BaseModel):
    """Payload to evaluate an action against active governance policies."""

    action: str = Field(..., description="E.g., agent.execute, model.invoke, tool.execute, data.access")
    resource: str = Field(..., description="E.g., invoice_agent, gpt4_client, sql_db")
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ApprovalDecisionRequest(BaseModel):
    """Payload to record a human approval intervention."""

    reviewer_id: str
    decision: str = Field("APPROVED", description="APPROVED or REJECTED")
    comments: Optional[str] = "Approved via developer API"
    override_reason: Optional[str] = None


class WebhookCreateRequest(BaseModel):
    """Payload to register a new webhook subscription."""

    url: str
    events: List[str] = Field(default_factory=lambda: ["*"])
    description: Optional[str] = None
    secret: Optional[str] = None


class PluginRegisterRequest(BaseModel):
    """Payload to register a new governance plugin."""

    name: str
    version: str
    owner: str
    description: str = ""
    capabilities: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
