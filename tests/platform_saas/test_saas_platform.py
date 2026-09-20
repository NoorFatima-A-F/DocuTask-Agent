"""
Phase 13.19: Comprehensive Pytest Suite for Multi-Tenant Enterprise AI Platform & SaaS Operating System (EAP-MTSOS).
Tests all services, isolation mechanisms, cryptographic licenses, and API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
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
from app.platform_saas.runtime.saas_master_orchestrator import SaaSMasterOrchestrator
from app.platform_saas.models.schemas import (
    PlanTier,
    TenantStatus,
    TenantLimits,
    SSOProtocol,
    AssetType,
    ConnectorType,
    BillingProvider,
    InvoiceStatus,
)

client = TestClient(app)


# 1. Tenant Lifecycle Tests
def test_tenant_lifecycle():
    tm = TenantManager()
    tenant = tm.provision_tenant(
        tenant_id="tenant_stark_ind",
        company_name="Stark Industries",
        slug="stark-ind",
        admin_email="tony@starkindustries.com",
        tier=PlanTier.ENTERPRISE,
    )
    assert tenant.tenant_id == "tenant_stark_ind"
    assert tenant.status == TenantStatus.ACTIVE
    assert tm.get_tenant("tenant_stark_ind") is not None

    # Update status
    updated = tm.update_tenant_status("tenant_stark_ind", TenantStatus.SUSPENDED)
    assert updated.status == TenantStatus.SUSPENDED

    # Update limits
    new_limits = TenantLimits(max_workspaces=100, max_concurrent_agents=500)
    tm.update_limits("tenant_stark_ind", new_limits)
    assert tm.get_tenant("tenant_stark_ind").limits.max_workspaces == 100


# 2. Enterprise Identity & SSO Tests
def test_enterprise_identity_and_sso():
    identity = EnterpriseIdentityService()
    cfg = identity.configure_sso(
        tenant_id="tenant_stark_ind",
        name="Jarvis ID Provider",
        protocol=SSOProtocol.OIDC,
        issuer_url="https://auth.stark.ai",
        sso_endpoint="https://auth.stark.ai/oauth2/auth",
        certificate_fingerprint="SHA256:11:22:33:44:55",
    )
    assert cfg.provider_id.startswith("sso_")
    assert len(identity.list_sso_configs("tenant_stark_ind")) == 1

    # User provisioning
    user = identity.provision_user(
        tenant_id="tenant_stark_ind",
        email="pepper@stark.ai",
        display_name="Pepper Potts (CEO)",
        role="TENANT_ADMIN",
    )
    assert user.email == "pepper@stark.ai"
    assert user.mfa_enabled is True

    # SAML Auth simulation
    auth_resp = identity.authenticate_saml_assertion("tenant_stark_ind", "<saml:Response>valid</saml:Response>")
    assert auth_resp["authenticated"] is True
    assert "saml_sess_" in auth_resp["session_token"]


# 3. Organization Hierarchy & Workspaces
def test_org_hierarchy_and_workspaces():
    org_svc = OrganizationHierarchyService()
    ws_svc = WorkspaceManager()

    parent_org = org_svc.create_organization(
        tenant_id="tenant_stark_ind",
        name="Stark AI Labs",
        business_unit="Defense & AI",
        country_code="US",
    )
    child_org = org_svc.create_organization(
        tenant_id="tenant_stark_ind",
        name="Arc Reactor Robotics",
        parent_org_id=parent_org.organization_id,
    )
    tree = org_svc.get_organization_tree("tenant_stark_ind")
    assert len(tree) == 1
    assert tree[0]["organization_id"] == parent_org.organization_id
    assert len(tree[0]["children"]) == 1

    # Workspace & Project
    ws = ws_svc.create_workspace(
        tenant_id="tenant_stark_ind",
        organization_id=parent_org.organization_id,
        name="Armor Telemetry Production",
        slug="armor-telemetry",
        owner_email="tony@stark.ai",
    )
    assert ws.workspace_id.startswith("ws_")

    prj = ws_svc.create_project(
        tenant_id="tenant_stark_ind",
        workspace_id=ws.workspace_id,
        name="Mark 85 Autonomous Target Guidance",
    )
    assert prj.project_id.startswith("prj_")


# 4. Subscription & Billing Engine
def test_subscription_and_billing():
    sub_svc = SubscriptionService()
    bill_svc = BillingEngine()

    sub = sub_svc.create_subscription("tenant_stark_ind", tier=PlanTier.PRO)
    assert sub.tier == PlanTier.PRO
    assert sub.base_price_monthly_usd == 499.0

    # Upgrade
    upgraded = sub_svc.upgrade_tier("tenant_stark_ind", PlanTier.ENTERPRISE)
    assert upgraded.tier == PlanTier.ENTERPRISE
    assert upgraded.base_price_monthly_usd == 7999.0

    # Invoice generation & payment
    inv = bill_svc.generate_invoice("tenant_stark_ind", upgraded.subscription_id, 7999.0, overage_amount_usd=250.0)
    assert inv.amount_due_usd == 8249.0
    assert inv.status == InvoiceStatus.OPEN

    paid_inv = bill_svc.mark_invoice_paid(inv.invoice_id)
    assert paid_inv.status == InvoiceStatus.PAID
    assert paid_inv.amount_paid_usd == 8249.0


# 5. Usage Metering
def test_usage_metering():
    usage_svc = UsageMeteringService()
    usage_svc.record_usage("tenant_stark_ind", "ws_01", "llm_tokens", 5_000_000)
    usage_svc.record_usage("tenant_stark_ind", "ws_01", "ocr_pages", 1_200)

    summary = usage_svc.get_tenant_usage_summary("tenant_stark_ind")
    assert summary["total_tokens"] == 5_000_000
    assert summary["total_ocr_pages"] == 1_200
    assert summary["metered_spend_usd"] > 0


# 6. Cryptographic Offline Licenses
def test_offline_license_manager():
    lic_mgr = LicenseManager()
    lic = lic_mgr.generate_license(
        tenant_id="tenant_stark_ind",
        tier=PlanTier.ENTERPRISE,
        max_seats=500,
        valid_days=30,
        is_airgapped=True,
    )
    assert lic.valid is True
    assert "ED25519_SIG_" in lic.signature_ed25519

    validation = lic_mgr.validate_license(lic.license_id)
    assert validation["valid"] is True
    assert validation["max_seats"] == 500


# 7. AI Marketplace
def test_ai_marketplace():
    market = AIMarketplaceService()
    asset = market.publish_asset(
        title="Automated Drone Flight Path OCR",
        asset_type=AssetType.OCR_PIPELINE,
        publisher_tenant_id="tenant_stark_ind",
        publisher_name="Stark Aviation",
        description="Scans flight manifests with sub-second latency",
    )
    assert asset.asset_id.startswith("asset_")

    install_res = market.install_asset("tenant_globex_health", asset.asset_id)
    assert install_res["installed"] is True
    installed_list = market.list_tenant_installed("tenant_globex_health")
    assert any(a.asset_id == asset.asset_id for a in installed_list)


# 8. Integration Hub
def test_integration_hub():
    hub = IntegrationHub()
    conn = hub.connect_service(
        tenant_id="tenant_stark_ind",
        connector_type=ConnectorType.SALESFORCE,
        name="Stark CRM Salesforce Bridge",
    )
    assert conn.status == "CONNECTED"
    test_res = hub.test_connection(conn.connector_id)
    assert test_res["status"] == "HEALTHY"


# 9. Policy Evaluation & Security Isolation
def test_policy_evaluation_and_isolation():
    pol_engine = TenantPolicyEngine()
    pol = pol_engine.create_policy(
        tenant_id="tenant_stark_ind",
        policy_name="Operator Run Only",
        subject_role="AGENT_OPERATOR",
        resource_type="agent_workflow",
        action="EXECUTE",
        effect="ALLOW",
    )
    assert pol.policy_id.startswith("pol_")

    eval_allow = pol_engine.evaluate("tenant_stark_ind", "AGENT_OPERATOR", "agent_workflow", "EXECUTE")
    assert eval_allow["decision"] == "ALLOW"

    eval_deny = pol_engine.evaluate("tenant_stark_ind", "AGENT_OPERATOR", "system_billing", "DELETE")
    assert eval_deny["decision"] == "DENY"

    # Runtime isolation check
    TenantRuntimeIsolation.set_current_context("tenant_acme_corp", role="AGENT_OPERATOR")
    with pytest.raises(PermissionError):
        TenantRuntimeIsolation.assert_tenant_access("tenant_globex_health")

    # Super Admin bypass
    TenantRuntimeIsolation.set_current_context("tenant_acme_corp", role="SUPER_ADMIN")
    TenantRuntimeIsolation.assert_tenant_access("tenant_globex_health")  # Should not raise


# 10. Audit Ledger Cryptographic Hash Chaining
def test_audit_ledger_hash_chain():
    audit = EnterpriseAuditService()
    tenant_id = "tenant_crypto_test"
    audit.log_event(tenant_id, "usr_1", "u1@test.com", "LOGIN", "AUTH", "auth_01")
    audit.log_event(tenant_id, "usr_1", "u1@test.com", "CREATE_AGENT", "AGENT", "agt_01")
    audit.log_event(tenant_id, "usr_1", "u1@test.com", "DEPLOY_WORKFLOW", "WORKFLOW", "wf_01")

    res = audit.verify_integrity(tenant_id)
    assert res["valid"] is True
    assert res["verified_events_count"] == 3


# 11. SaaS Master Orchestrator Turnkey Onboarding
def test_master_orchestrator_onboarding():
    orch = SaaSMasterOrchestrator()
    res = orch.onboard_enterprise_tenant(
        tenant_id="tenant_wayne_ent",
        company_name="Wayne Enterprises",
        slug="wayne-ent",
        admin_email="bruce@wayneenterprises.com",
        tier=PlanTier.ENTERPRISE,
    )
    assert res["status"] == "ONBOARDING_SUCCESSFUL"
    assert res["tenant"].tenant_id == "tenant_wayne_ent"
    assert res["subscription"].tier == PlanTier.ENTERPRISE
    assert res["license"].max_seats == 250

    overview = orch.get_executive_overview()
    assert overview.total_tenants >= 3
    assert overview.monthly_recurring_revenue_usd > 10000.0


# 12. FastAPI HTTP Endpoints
def test_fastapi_saas_endpoints():
    # Executive overview
    res = client.get("/api/v1/saas/overview")
    assert res.status_code == 200
    data = res.json()
    assert "platform_name" in data
    assert "monthly_recurring_revenue_usd" in data

    # Tenants list
    res = client.get("/api/v1/saas/tenants")
    assert res.status_code == 200
    assert len(res.json()) >= 2

    # Organization tree
    res = client.get("/api/v1/saas/organizations/tree?tenant_id=tenant_acme_corp")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Marketplace assets
    res = client.get("/api/v1/saas/marketplace/assets")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # Connectors
    res = client.get("/api/v1/saas/integrations")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # Audit verify
    res = client.get("/api/v1/saas/audit/verify/tenant_acme_corp")
    assert res.status_code == 200
    assert res.json()["valid"] is True
