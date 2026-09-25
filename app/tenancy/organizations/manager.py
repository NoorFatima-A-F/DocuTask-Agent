"""Organization Manager (ESP-MOOS).

Provides CRUD operations, querying, filtering, and lifecycle management for organizations.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional
from app.tenancy.core.models import (
    Organization,
    TenantLifecycleState,
    SubscriptionTier,
    ComplianceProfileType,
    Region,
)
from app.tenancy.core.exceptions import TenantNotFoundError, TenancyError
from app.tenancy.organizations.lifecycle import OrganizationLifecycleManager


class OrganizationManager:
    """Enterprise Organization registry and manager."""

    def __init__(self, lifecycle_manager: Optional[OrganizationLifecycleManager] = None):
        self._organizations: Dict[str, Organization] = {}
        self._slug_index: Dict[str, str] = {}
        self.lifecycle = lifecycle_manager or OrganizationLifecycleManager()

    def _generate_slug(self, name: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
        return slug or "org"

    def create_organization(
        self,
        org_id: str,
        name: str,
        owner_id: str,
        industry: str = "Technology",
        region: Region = Region.US_EAST,
        subscription_plan: SubscriptionTier = SubscriptionTier.FREE,
        compliance_profile: ComplianceProfileType = ComplianceProfileType.STANDARD,
        metadata: Optional[Dict[str, any]] = None,
    ) -> Organization:
        """Register a new organization entity."""
        if org_id in self._organizations:
            raise TenancyError(f"Organization '{org_id}' already exists")

        slug = self._generate_slug(name)
        if slug in self._slug_index:
            slug = f"{slug}-{org_id[:6]}"

        org = Organization(
            id=org_id,
            name=name,
            slug=slug,
            industry=industry,
            region=region,
            status=TenantLifecycleState.REGISTERED,
            subscription_plan=subscription_plan,
            compliance_profile=compliance_profile,
            owner_id=owner_id,
            metadata=metadata or {},
        )
        self._organizations[org_id] = org
        self._slug_index[slug] = org_id
        return org

    def get_organization(self, org_id: str) -> Organization:
        """Retrieve an organization by ID."""
        org = self._organizations.get(org_id)
        if not org:
            raise TenantNotFoundError(f"Organization '{org_id}' not found")
        return org

    def get_by_slug(self, slug: str) -> Organization:
        """Retrieve an organization by unique URL slug."""
        org_id = self._slug_index.get(slug)
        if not org_id:
            raise TenantNotFoundError(f"Organization with slug '{slug}' not found")
        return self.get_organization(org_id)

    def list_organizations(
        self,
        status: Optional[TenantLifecycleState] = None,
        region: Optional[Region] = None,
        subscription_plan: Optional[SubscriptionTier] = None,
    ) -> List[Organization]:
        """List organizations matching optional filter criteria."""
        results = list(self._organizations.values())
        if status:
            results = [o for o in results if o.status == status]
        if region:
            results = [o for o in results if o.region == region]
        if subscription_plan:
            results = [o for o in results if o.subscription_plan == subscription_plan]
        return results

    def update_organization(
        self,
        org_id: str,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        subscription_plan: Optional[SubscriptionTier] = None,
        compliance_profile: Optional[ComplianceProfileType] = None,
        metadata: Optional[Dict[str, any]] = None,
    ) -> Organization:
        """Update organization metadata."""
        org = self.get_organization(org_id)
        if name:
            org.name = name
        if industry:
            org.industry = industry
        if subscription_plan:
            org.subscription_plan = subscription_plan
        if compliance_profile:
            org.compliance_profile = compliance_profile
        if metadata:
            org.metadata.update(metadata)
        return org

    def update_status(
        self,
        org_id: str,
        target_state: TenantLifecycleState,
        actor_id: str = "system",
        reason: str = "Status update",
    ) -> Organization:
        """Transition organization status via lifecycle FSM."""
        org = self.get_organization(org_id)
        return self.lifecycle.transition(org, target_state, actor_id=actor_id, reason=reason)
