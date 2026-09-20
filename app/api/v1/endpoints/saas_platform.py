"""
Phase 13.19: Enterprise AI Platform & Multi-Tenant SaaS Operating System API Endpoints.
Mounted under /api/v1/saas.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query, Body
from app.platform_saas.runtime.saas_master_orchestrator import SaaSMasterOrchestrator
from app.platform_saas.models.schemas import (
    Tenant,
    TenantStatus,
    PlanTier,
    TenantLimits,
    OrganizationNode,
    Workspace,
    Project,
    SSOProviderConfig,
    SSOProtocol,
    UserIdentity,
    Subscription,
    Invoice,
    BillingProvider,
    UsageRecord,
    LicenseKey,
    MarketplaceAsset,
    AssetType,
    ConnectorConfig,
    ConnectorType,
    TenantPolicy,
    AuditEvent,
    BrandingConfig,
    SaaSExecutiveOverview,
)

router = APIRouter()
orchestrator = SaaSMasterOrchestrator()


# 1. Executive Overview & System Diagnostics
@router.get("/overview", response_model=SaaSExecutiveOverview, tags=["Executive Control Plane"])
async def get_executive_overview():
    """Returns platform-wide executive metrics (MRR, ARR, active tenants, usage)."""
    return orchestrator.get_executive_overview()


@router.post("/onboard", tags=["Executive Control Plane"])
async def onboard_enterprise_tenant(payload: Dict[str, Any] = Body(...)):
    """Turnkey onboarding for enterprise tenants (creates tenant, org, workspace, sub, license, audit)."""
    tenant_id = payload.get("tenant_id")
    company_name = payload.get("company_name")
    slug = payload.get("slug")
    admin_email = payload.get("admin_email")
    tier_str = payload.get("tier", "BUSINESS")

    if not all([tenant_id, company_name, slug, admin_email]):
        raise HTTPException(status_code=400, detail="Missing required onboarding fields")

    tier = PlanTier(tier_str) if tier_str in PlanTier.__members__ else PlanTier.BUSINESS
    result = orchestrator.onboard_enterprise_tenant(
        tenant_id=tenant_id,
        company_name=company_name,
        slug=slug,
        admin_email=admin_email,
        tier=tier,
    )
    return result


# 2. Tenant Management
@router.get("/tenants", response_model=List[Tenant], tags=["Tenant Management"])
async def list_tenants():
    return orchestrator.tenants.list_tenants()


@router.post("/tenants", response_model=Tenant, tags=["Tenant Management"])
async def create_tenant(payload: Dict[str, Any] = Body(...)):
    try:
        tier_str = payload.get("tier", "BUSINESS")
        tier = PlanTier(tier_str) if tier_str in PlanTier.__members__ else PlanTier.BUSINESS
        tenant = orchestrator.tenants.provision_tenant(
            tenant_id=payload["tenant_id"],
            company_name=payload["company_name"],
            slug=payload["slug"],
            admin_email=payload["admin_email"],
            tier=tier,
        )
        return tenant
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tenants/{tenant_id}", response_model=Tenant, tags=["Tenant Management"])
async def get_tenant(tenant_id: str):
    tenant = orchestrator.tenants.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/tenants/{tenant_id}/status", response_model=Tenant, tags=["Tenant Management"])
async def update_tenant_status(tenant_id: str, status: TenantStatus = Query(...)):
    try:
        return orchestrator.tenants.update_tenant_status(tenant_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/tenants/{tenant_id}/limits", response_model=Tenant, tags=["Tenant Management"])
async def update_tenant_limits(tenant_id: str, limits: TenantLimits = Body(...)):
    try:
        return orchestrator.tenants.update_limits(tenant_id, limits)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. Organization Hierarchy
@router.get("/organizations", response_model=List[OrganizationNode], tags=["Organization Hierarchy"])
async def list_organizations(tenant_id: Optional[str] = None):
    return orchestrator.organizations.list_organizations(tenant_id)


@router.post("/organizations", response_model=OrganizationNode, tags=["Organization Hierarchy"])
async def create_organization(payload: Dict[str, Any] = Body(...)):
    return orchestrator.organizations.create_organization(
        tenant_id=payload["tenant_id"],
        name=payload["name"],
        business_unit=payload.get("business_unit", "General"),
        country_code=payload.get("country_code", "US"),
        parent_org_id=payload.get("parent_org_id"),
    )


@router.get("/organizations/tree", tags=["Organization Hierarchy"])
async def get_organization_tree(tenant_id: str = Query(...)):
    return orchestrator.organizations.get_organization_tree(tenant_id)


# 4. Workspaces & Projects
@router.get("/workspaces", response_model=List[Workspace], tags=["Workspaces & Projects"])
async def list_workspaces(tenant_id: Optional[str] = None, organization_id: Optional[str] = None):
    return orchestrator.workspaces.list_workspaces(tenant_id, organization_id)


@router.post("/workspaces", response_model=Workspace, tags=["Workspaces & Projects"])
async def create_workspace(payload: Dict[str, Any] = Body(...)):
    return orchestrator.workspaces.create_workspace(
        tenant_id=payload["tenant_id"],
        organization_id=payload["organization_id"],
        name=payload["name"],
        slug=payload["slug"],
        owner_email=payload["owner_email"],
        allocated_agents_count=payload.get("allocated_agents_count", 10),
        allocated_storage_gb=payload.get("allocated_storage_gb", 50),
    )


@router.get("/projects", response_model=List[Project], tags=["Workspaces & Projects"])
async def list_projects(tenant_id: Optional[str] = None, workspace_id: Optional[str] = None):
    return orchestrator.workspaces.list_projects(tenant_id, workspace_id)


@router.post("/projects", response_model=Project, tags=["Workspaces & Projects"])
async def create_project(payload: Dict[str, Any] = Body(...)):
    return orchestrator.workspaces.create_project(
        tenant_id=payload["tenant_id"],
        workspace_id=payload["workspace_id"],
        name=payload["name"],
        description=payload.get("description", ""),
    )


# 5. Enterprise Identity & SSO
@router.get("/identity/sso-configs", response_model=List[SSOProviderConfig], tags=["Enterprise Identity & SSO"])
async def list_sso_configs(tenant_id: Optional[str] = None):
    return orchestrator.identity.list_sso_configs(tenant_id)


@router.post("/identity/sso-configs", response_model=SSOProviderConfig, tags=["Enterprise Identity & SSO"])
async def configure_sso(payload: Dict[str, Any] = Body(...)):
    proto_str = payload.get("protocol", "SAML_2_0")
    protocol = SSOProtocol(proto_str) if proto_str in SSOProtocol.__members__ else SSOProtocol.SAML_2_0
    return orchestrator.identity.configure_sso(
        tenant_id=payload["tenant_id"],
        name=payload["name"],
        protocol=protocol,
        issuer_url=payload["issuer_url"],
        sso_endpoint=payload["sso_endpoint"],
        certificate_fingerprint=payload["certificate_fingerprint"],
    )


@router.get("/identity/users", response_model=List[UserIdentity], tags=["Enterprise Identity & SSO"])
async def list_users(tenant_id: Optional[str] = None):
    return orchestrator.identity.list_users(tenant_id)


@router.post("/identity/users", response_model=UserIdentity, tags=["Enterprise Identity & SSO"])
async def provision_user(payload: Dict[str, Any] = Body(...)):
    return orchestrator.identity.provision_user(
        tenant_id=payload["tenant_id"],
        email=payload["email"],
        display_name=payload["display_name"],
        role=payload.get("role", "AGENT_OPERATOR"),
        department=payload.get("department", "Operations"),
        sso_linked=payload.get("sso_linked", True),
        mfa_enabled=payload.get("mfa_enabled", True),
    )


@router.post("/identity/saml/authenticate", tags=["Enterprise Identity & SSO"])
async def authenticate_saml(payload: Dict[str, Any] = Body(...)):
    return orchestrator.identity.authenticate_saml_assertion(
        tenant_id=payload["tenant_id"],
        saml_response_xml=payload.get("saml_response_xml", "<saml:Response />"),
    )


@router.post("/identity/scim/sync", tags=["Enterprise Identity & SSO"])
async def scim_sync(payload: Dict[str, Any] = Body(...)):
    return orchestrator.identity.scim_sync_users(
        tenant_id=payload["tenant_id"],
        directory_payload=payload.get("users", []),
    )


# 6. Subscriptions & Billing
@router.get("/subscriptions", response_model=List[Subscription], tags=["Subscription & Billing"])
async def list_subscriptions():
    return orchestrator.subscriptions.list_subscriptions()


@router.post("/subscriptions/upgrade", response_model=Subscription, tags=["Subscription & Billing"])
async def upgrade_subscription(payload: Dict[str, Any] = Body(...)):
    tier_str = payload.get("tier", "ENTERPRISE")
    tier = PlanTier(tier_str) if tier_str in PlanTier.__members__ else PlanTier.ENTERPRISE
    return orchestrator.subscriptions.upgrade_tier(payload["tenant_id"], tier)


@router.get("/billing/invoices", response_model=List[Invoice], tags=["Subscription & Billing"])
async def list_invoices(tenant_id: Optional[str] = None):
    return orchestrator.billing.list_invoices(tenant_id)


@router.post("/billing/invoices", response_model=Invoice, tags=["Subscription & Billing"])
async def generate_invoice(payload: Dict[str, Any] = Body(...)):
    return orchestrator.billing.generate_invoice(
        tenant_id=payload["tenant_id"],
        subscription_id=payload["subscription_id"],
        base_amount_usd=payload["base_amount_usd"],
        overage_amount_usd=payload.get("overage_amount_usd", 0.0),
        billing_period=payload.get("billing_period", "2026-09"),
    )


@router.post("/billing/invoices/{invoice_id}/pay", response_model=Invoice, tags=["Subscription & Billing"])
async def pay_invoice(invoice_id: str):
    try:
        return orchestrator.billing.mark_invoice_paid(invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/billing/webhook", tags=["Subscription & Billing"])
async def handle_billing_webhook(payload: Dict[str, Any] = Body(...)):
    prov_str = payload.get("provider", "STRIPE")
    provider = BillingProvider(prov_str) if prov_str in BillingProvider.__members__ else BillingProvider.STRIPE
    return orchestrator.billing.process_webhook_event(provider, payload)


# 7. Usage Metering
@router.get("/usage/records", response_model=List[UsageRecord], tags=["Usage Metering"])
async def list_usage_records(tenant_id: Optional[str] = None):
    return orchestrator.usage.list_records(tenant_id)


@router.post("/usage/records", response_model=UsageRecord, tags=["Usage Metering"])
async def record_usage(payload: Dict[str, Any] = Body(...)):
    return orchestrator.usage.record_usage(
        tenant_id=payload["tenant_id"],
        workspace_id=payload["workspace_id"],
        metric_name=payload["metric_name"],
        quantity=float(payload["quantity"]),
    )


@router.get("/usage/summary/{tenant_id}", tags=["Usage Metering"])
async def get_usage_summary(tenant_id: str):
    return orchestrator.usage.get_tenant_usage_summary(tenant_id)


# 8. Offline Licenses
@router.get("/licenses", response_model=List[LicenseKey], tags=["Licenses & Entitlements"])
async def list_licenses(tenant_id: Optional[str] = None):
    return orchestrator.licenses.list_licenses(tenant_id)


@router.post("/licenses", response_model=LicenseKey, tags=["Licenses & Entitlements"])
async def generate_license(payload: Dict[str, Any] = Body(...)):
    tier_str = payload.get("tier", "ENTERPRISE")
    tier = PlanTier(tier_str) if tier_str in PlanTier.__members__ else PlanTier.ENTERPRISE
    return orchestrator.licenses.generate_license(
        tenant_id=payload["tenant_id"],
        tier=tier,
        max_seats=payload.get("max_seats", 100),
        valid_days=payload.get("valid_days", 365),
        is_airgapped=payload.get("is_airgapped", False),
    )


@router.post("/licenses/{license_id}/validate", tags=["Licenses & Entitlements"])
async def validate_license(license_id: str):
    return orchestrator.licenses.validate_license(license_id)


# 9. AI Marketplace
@router.get("/marketplace/assets", response_model=List[MarketplaceAsset], tags=["AI Marketplace"])
async def list_marketplace_assets(asset_type: Optional[AssetType] = None, tag: Optional[str] = None):
    return orchestrator.marketplace.list_assets(asset_type, tag)


@router.post("/marketplace/assets", response_model=MarketplaceAsset, tags=["AI Marketplace"])
async def publish_marketplace_asset(payload: Dict[str, Any] = Body(...)):
    type_str = payload.get("asset_type", "AGENT_PACK")
    asset_type = AssetType(type_str) if type_str in AssetType.__members__ else AssetType.AGENT_PACK
    return orchestrator.marketplace.publish_asset(
        title=payload["title"],
        asset_type=asset_type,
        publisher_tenant_id=payload["publisher_tenant_id"],
        publisher_name=payload["publisher_name"],
        description=payload["description"],
        version=payload.get("version", "1.0.0"),
        price_monthly_usd=payload.get("price_monthly_usd", 0.0),
        tags=payload.get("tags", []),
    )


@router.post("/marketplace/assets/{asset_id}/install", tags=["AI Marketplace"])
async def install_marketplace_asset(asset_id: str, tenant_id: str = Query(...)):
    try:
        return orchestrator.marketplace.install_asset(tenant_id, asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/marketplace/installed/{tenant_id}", response_model=List[MarketplaceAsset], tags=["AI Marketplace"])
async def list_installed_assets(tenant_id: str):
    return orchestrator.marketplace.list_tenant_installed(tenant_id)


# 10. Integration Hub
@router.get("/integrations", response_model=List[ConnectorConfig], tags=["Integration Hub"])
async def list_integrations(tenant_id: Optional[str] = None):
    return orchestrator.integrations.list_connectors(tenant_id)


@router.post("/integrations", response_model=ConnectorConfig, tags=["Integration Hub"])
async def connect_service(payload: Dict[str, Any] = Body(...)):
    conn_str = payload.get("connector_type", "GOOGLE_DRIVE")
    connector_type = ConnectorType(conn_str) if conn_str in ConnectorType.__members__ else ConnectorType.GOOGLE_DRIVE
    return orchestrator.integrations.connect_service(
        tenant_id=payload["tenant_id"],
        connector_type=connector_type,
        name=payload["name"],
        auth_type=payload.get("auth_type", "OAUTH2"),
        connected_workspaces=payload.get("connected_workspaces", []),
    )


@router.post("/integrations/{connector_id}/test", tags=["Integration Hub"])
async def test_integration_connection(connector_id: str):
    return orchestrator.integrations.test_connection(connector_id)


# 11. Policy & Authorization
@router.get("/policies", response_model=List[TenantPolicy], tags=["Tenant Policies"])
async def list_policies(tenant_id: Optional[str] = None):
    return orchestrator.policies.list_policies(tenant_id)


@router.post("/policies", response_model=TenantPolicy, tags=["Tenant Policies"])
async def create_policy(payload: Dict[str, Any] = Body(...)):
    return orchestrator.policies.create_policy(
        tenant_id=payload["tenant_id"],
        policy_name=payload["policy_name"],
        subject_role=payload["subject_role"],
        resource_type=payload["resource_type"],
        action=payload["action"],
        effect=payload.get("effect", "ALLOW"),
        conditions=payload.get("conditions", {}),
    )


@router.post("/policies/evaluate", tags=["Tenant Policies"])
async def evaluate_policy(payload: Dict[str, Any] = Body(...)):
    return orchestrator.policies.evaluate(
        tenant_id=payload["tenant_id"],
        user_role=payload["user_role"],
        resource_type=payload["resource_type"],
        action=payload["action"],
        context_attributes=payload.get("context_attributes", {}),
    )


# 12. Enterprise Audit Ledger
@router.get("/audit/events", response_model=List[AuditEvent], tags=["Audit & Compliance"])
async def list_audit_events(tenant_id: Optional[str] = None):
    return orchestrator.audit.list_events(tenant_id)


@router.post("/audit/events", response_model=AuditEvent, tags=["Audit & Compliance"])
async def log_audit_event(payload: Dict[str, Any] = Body(...)):
    return orchestrator.audit.log_event(
        tenant_id=payload["tenant_id"],
        actor_id=payload["actor_id"],
        actor_email=payload["actor_email"],
        action=payload["action"],
        resource_type=payload["resource_type"],
        resource_id=payload["resource_id"],
        organization_id=payload.get("organization_id"),
        workspace_id=payload.get("workspace_id"),
        ip_address=payload.get("ip_address", "127.0.0.1"),
    )


@router.get("/audit/verify/{tenant_id}", tags=["Audit & Compliance"])
async def verify_audit_integrity(tenant_id: str):
    return orchestrator.audit.verify_integrity(tenant_id)


# 13. White Labeling & Branding
@router.get("/branding/{tenant_id}", response_model=BrandingConfig, tags=["White Labeling & Branding"])
async def get_tenant_branding(tenant_id: str):
    return orchestrator.branding.get_branding(tenant_id)


@router.put("/branding/{tenant_id}", response_model=BrandingConfig, tags=["White Labeling & Branding"])
async def configure_branding(tenant_id: str, payload: Dict[str, Any] = Body(...)):
    return orchestrator.branding.configure_branding(
        tenant_id=tenant_id,
        brand_name=payload["brand_name"],
        logo_url=payload["logo_url"],
        primary_color_hex=payload.get("primary_color_hex", "#4f46e5"),
        secondary_color_hex=payload.get("secondary_color_hex", "#06b6d4"),
        support_email=payload.get("support_email", "support@example.com"),
        custom_cname_domain=payload.get("custom_cname_domain"),
        email_footer_text=payload.get("email_footer_text", "Powered by Enterprise AI Platform"),
    )
