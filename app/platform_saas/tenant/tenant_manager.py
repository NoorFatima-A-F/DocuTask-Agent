"""
Phase 13.19: Tenant Management Platform.
Handles full lifecycle provisioning, configuration, limits, and status updates for multi-tenant organizations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.platform_saas.models.schemas import (
    Tenant,
    TenantStatus,
    PlanTier,
    TenantLimits,
    TenantConfiguration,
)


class TenantManager:
    def __init__(self):
        self._tenants: Dict[str, Tenant] = {}
        self._seed_default_tenants()

    def _seed_default_tenants(self) -> None:
        """Seeds default multi-tenant enterprise accounts."""
        t1 = Tenant(
            tenant_id="tenant_acme_corp",
            company_name="Acme Corporation Global",
            slug="acme-corp",
            tier=PlanTier.ENTERPRISE,
            status=TenantStatus.ACTIVE,
            admin_email="admin@acmecorp.com",
            limits=TenantLimits(
                max_organizations=10,
                max_workspaces=50,
                max_concurrent_agents=100,
                max_monthly_tokens=500_000_000,
                max_monthly_ocr_pages=200_000,
                max_storage_gb=2000,
                monthly_budget_ceiling_usd=25000.0,
            ),
            config=TenantConfiguration(
                default_region="us-east-1",
                allowed_regions=["us-east-1", "eu-central-1"],
                custom_domain="ai.acmecorp.com",
                enforce_sso=True,
                mfa_required=True,
            ),
        )

        t2 = Tenant(
            tenant_id="tenant_globex_health",
            company_name="Globex Healthcare Systems",
            slug="globex-health",
            tier=PlanTier.BUSINESS,
            status=TenantStatus.ACTIVE,
            admin_email="compliance@globexhealth.com",
            limits=TenantLimits(
                max_organizations=5,
                max_workspaces=15,
                max_concurrent_agents=30,
                max_monthly_tokens=150_000_000,
                max_monthly_ocr_pages=80_000,
                max_storage_gb=500,
                monthly_budget_ceiling_usd=10000.0,
            ),
            config=TenantConfiguration(
                default_region="eu-central-1",
                allowed_regions=["eu-central-1"],
                data_residency_enforced=True,
                enforce_sso=True,
            ),
        )

        self._tenants[t1.tenant_id] = t1
        self._tenants[t2.tenant_id] = t2

    def provision_tenant(
        self,
        tenant_id: str,
        company_name: str,
        slug: str,
        admin_email: str,
        tier: PlanTier = PlanTier.BUSINESS,
    ) -> Tenant:
        """Provisions a new tenant with isolated runtime parameters."""
        if tenant_id in self._tenants:
            raise ValueError(f"Tenant {tenant_id} already exists")

        tenant = Tenant(
            tenant_id=tenant_id,
            company_name=company_name,
            slug=slug,
            tier=tier,
            status=TenantStatus.ACTIVE,
            admin_email=admin_email,
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._tenants[tenant_id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self._tenants.get(tenant_id)

    def list_tenants(self) -> List[Tenant]:
        return list(self._tenants.values())

    def update_tenant_status(self, tenant_id: str, status: TenantStatus) -> Tenant:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        tenant.status = status
        tenant.updated_at = datetime.now(timezone.utc).isoformat()
        return tenant

    def update_limits(self, tenant_id: str, limits: TenantLimits) -> Tenant:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        tenant.limits = limits
        tenant.updated_at = datetime.now(timezone.utc).isoformat()
        return tenant
