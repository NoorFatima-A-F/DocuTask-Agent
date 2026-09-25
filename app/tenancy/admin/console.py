"""SaaS Administration Console & Audited Support Delegation (ESP-MOOS).

Provides platform-level administrative capabilities:
- Tenant Search & Fleet Overview
- Health & Operational Status Inspection
- Feature Flag Control
- Explicit, Time-Limited, Audited Support Mode Delegation
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.tenancy.core.models import TenantContext, TenantLifecycleState
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.metering.engine import UsageMeteringPlatform
from app.tenancy.quotas.manager import QuotaManager


class SupportDelegationSession(BaseModel):
    """Time-limited, audited administrator delegation session."""
    session_id: str
    admin_user_id: str
    target_organization_id: str
    reason: str
    ticket_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime
    is_active: bool = True


class SaaSAdminConsole:
    """Platform administration console for managing tenant fleet."""

    def __init__(
        self,
        org_manager: OrganizationManager,
        metering_platform: UsageMeteringPlatform,
        quota_manager: QuotaManager,
    ):
        self.org_manager = org_manager
        self.metering_platform = metering_platform
        self.quota_manager = quota_manager
        self._support_sessions: Dict[str, SupportDelegationSession] = {}

    def search_tenants(self, query: str) -> List[Dict[str, Any]]:
        """Search organizations by name or slug."""
        q = query.lower()
        results = []
        for org in self.org_manager.list_organizations():
            if q in org.name.lower() or q in org.slug.lower() or q in org.id.lower():
                results.append({
                    "id": org.id,
                    "name": org.name,
                    "slug": org.slug,
                    "status": org.status.value,
                    "region": org.region.value,
                    "plan": org.subscription_plan.value,
                })
        return results

    def get_tenant_diagnostic(self, organization_id: str) -> Dict[str, Any]:
        """Compile a full diagnostic report for a tenant."""
        org = self.org_manager.get_organization(organization_id)
        quotas = self.quota_manager.list_quotas(organization_id)
        usage = self.metering_platform.get_usage_summary(organization_id)
        total_spend = self.metering_platform.get_total_spend(organization_id)

        return {
            "organization": org.model_dump(mode="json"),
            "total_spend_usd": total_spend,
            "usage_breakdown": usage,
            "quotas": [q.model_dump(mode="json") for q in quotas],
            "is_healthy": org.status == TenantLifecycleState.ACTIVE,
        }

    def create_support_session(
        self,
        admin_user_id: str,
        target_organization_id: str,
        reason: str,
        ticket_id: str,
        duration_minutes: int = 60,
    ) -> SupportDelegationSession:
        """Issue a time-limited, audited support session into a tenant organization."""
        session = SupportDelegationSession(
            session_id=f"supp_{uuid.uuid4().hex[:10]}",
            admin_user_id=admin_user_id,
            target_organization_id=target_organization_id,
            reason=reason,
            ticket_id=ticket_id,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=duration_minutes),
            is_active=True,
        )
        self._support_sessions[session.session_id] = session
        return session

    def build_delegated_context(self, session_id: str) -> TenantContext:
        """Create a delegated TenantContext with audit markings."""
        session = self._support_sessions.get(session_id)
        if not session or not session.is_active:
            raise ValueError("Support session invalid or expired")
        if datetime.now(timezone.utc) > session.expires_at:
            session.is_active = False
            raise ValueError("Support session has expired")

        return TenantContext(
            organization_id=session.target_organization_id,
            workspace_id="default_workspace",
            user_id=session.admin_user_id,
            is_admin_delegated=True,
            metadata={
                "support_session_id": session.session_id,
                "support_ticket_id": session.ticket_id,
                "support_reason": session.reason,
            },
        )
