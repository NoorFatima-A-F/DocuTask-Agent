"""Webhook Subscription and Endpoint Registry."""

from datetime import datetime, timezone
import secrets
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class WebhookEventType(str):
    DECISION_CREATED = "GovernanceDecisionCreated"
    POLICY_VIOLATION = "PolicyViolation"
    APPROVAL_REQUIRED = "ApprovalRequired"
    RISK_DETECTED = "RiskDetected"
    AUDIT_GENERATED = "AuditGenerated"
    COMPLIANCE_FAILURE = "ComplianceFailure"
    ALL = "*"


class WebhookEndpoint(BaseModel):
    """Configuration record for an outbound webhook endpoint."""

    webhook_id: str
    tenant_id: str
    url: str
    events: List[str] = Field(default_factory=lambda: ["*"])
    secret_key: str
    is_active: bool = True
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WebhookSubscriptionManager:
    """Multi-tenant subscription manager for webhooks."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, WebhookEndpoint] = {}

    def register(
        self,
        tenant_id: str,
        url: str,
        events: Optional[List[str]] = None,
        secret: Optional[str] = None,
        description: Optional[str] = None,
    ) -> WebhookEndpoint:
        """Register a new webhook subscription endpoint."""
        if not url.startswith("https://") and not url.startswith("http://"):
            raise ValueError("Webhook URL must use HTTP or HTTPS scheme.")

        webhook_id = f"wh_{secrets.token_hex(8)}"
        secret_key = secret or f"whsec_{secrets.token_urlsafe(24)}"

        endpoint = WebhookEndpoint(
            webhook_id=webhook_id,
            tenant_id=tenant_id,
            url=url,
            events=events or ["*"],
            secret_key=secret_key,
            description=description,
        )
        self._endpoints[webhook_id] = endpoint
        return endpoint

    def get(self, webhook_id: str) -> Optional[WebhookEndpoint]:
        return self._endpoints.get(webhook_id)

    def list_by_tenant(self, tenant_id: str) -> List[WebhookEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.tenant_id == tenant_id]

    def delete(self, webhook_id: str) -> bool:
        if webhook_id in self._endpoints:
            del self._endpoints[webhook_id]
            return True
        return False
