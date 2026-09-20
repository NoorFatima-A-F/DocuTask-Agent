"""
Phase 13.19: SaaS Master Orchestrator.
Coordinates the entire multi-tenant enterprise operating system lifecycle.
"""

from typing import Dict, List, Optional, Any
from app.platform_saas.tenant.tenant_manager import TenantManager
from app.platform_saas.identity.enterprise_identity_service import EnterpriseIdentityService
from app.platform_saas.organizations.organization_hierarchy_service import OrganizationHierarchyService
from app.platform_saas.workspaces.workspace_manager import WorkspaceManager
from app.platform_saas.subscriptions.subscription_service import SubscriptionService
from app.platform_saas.billing.billing_engine import BillingEngine
from app.platform_saas.usage.usage_metering_service import UsageMeteringService
from app.platform_saas.licenses.license_manager import LicenseManager
from app.platform_saas.marketplace.ai_marketplace_service import AIMarketplaceService
from app.platform_saas.integrations.integration_hub import IntegrationHub
from app.platform_saas.policy.tenant_policy_engine import TenantPolicyEngine
from app.platform_saas.audit.enterprise_audit_service import EnterpriseAuditService
from app.platform_saas.branding.white_label_service import WhiteLabelService
from app.platform_saas.analytics.saas_analytics_engine import SaaSAnalyticsEngine
from app.platform_saas.runtime.tenant_runtime_isolation import TenantRuntimeIsolation
from app.platform_saas.models.schemas import PlanTier, SaaSExecutiveOverview


class SaaSMasterOrchestrator:
    def __init__(self):
        self.tenants = TenantManager()
        self.identity = EnterpriseIdentityService()
        self.organizations = OrganizationHierarchyService()
        self.workspaces = WorkspaceManager()
        self.subscriptions = SubscriptionService()
        self.billing = BillingEngine()
        self.usage = UsageMeteringService()
        self.licenses = LicenseManager()
        self.marketplace = AIMarketplaceService()
        self.integrations = IntegrationHub()
        self.policies = TenantPolicyEngine()
        self.audit = EnterpriseAuditService()
        self.branding = WhiteLabelService()
        self.analytics = SaaSAnalyticsEngine()
        self.runtime = TenantRuntimeIsolation()

    def get_executive_overview(self) -> SaaSExecutiveOverview:
        tenants_list = self.tenants.list_tenants()
        orgs_list = self.organizations.list_organizations()
        workspaces_list = self.workspaces.list_workspaces()
        
        mrr = sum(s.base_price_monthly_usd for s in self.subscriptions.list_subscriptions() if s.status == "ACTIVE")
        records = self.usage.list_records()
        tokens = sum(int(r.quantity) for r in records if r.metric_name == "llm_tokens")
        pages = sum(int(r.quantity) for r in records if r.metric_name == "ocr_pages")

        return self.analytics.compute_executive_overview(
            total_tenants=len(tenants_list),
            active_tenants=len([t for t in tenants_list if t.status == "ACTIVE"]),
            total_organizations=len(orgs_list),
            total_workspaces=len(workspaces_list),
            mrr_usd=mrr,
            metered_tokens=tokens,
            metered_ocr_pages=pages,
        )

    def onboard_enterprise_tenant(
        self,
        tenant_id: str,
        company_name: str,
        slug: str,
        admin_email: str,
        tier: PlanTier = PlanTier.BUSINESS,
    ) -> Dict[str, Any]:
        """Provisions a complete turnkey enterprise SaaS tenant stack."""
        tenant = self.tenants.provision_tenant(
            tenant_id=tenant_id,
            company_name=company_name,
            slug=slug,
            admin_email=admin_email,
            tier=tier,
        )
        org = self.organizations.create_organization(
            tenant_id=tenant_id,
            name=f"{company_name} HQ",
            business_unit="Executive Management",
            country_code="US",
        )
        ws = self.workspaces.create_workspace(
            tenant_id=tenant_id,
            organization_id=org.organization_id,
            name="Default Workspace",
            slug="default-ws",
            owner_email=admin_email,
        )
        sub = self.subscriptions.create_subscription(
            tenant_id=tenant_id,
            tier=tier,
        )
        lic = self.licenses.generate_license(
            tenant_id=tenant_id,
            tier=tier,
            max_seats=50 if tier == PlanTier.BUSINESS else 250,
        )
        self.audit.log_event(
            tenant_id=tenant_id,
            actor_id="usr_system_provisioner",
            actor_email=admin_email,
            action="ENTERPRISE_ONBOARDING_COMPLETED",
            resource_type="TENANT",
            resource_id=tenant_id,
            organization_id=org.organization_id,
            workspace_id=ws.workspace_id,
        )

        return {
            "tenant": tenant,
            "organization": org,
            "workspace": ws,
            "subscription": sub,
            "license": lic,
            "status": "ONBOARDING_SUCCESSFUL",
        }
