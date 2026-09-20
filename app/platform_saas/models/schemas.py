"""
Phase 13.19: Enterprise AI Platform & Multi-Tenant SaaS Operating System (EAP-MTSOS)
Pydantic Data Models & Schemas.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class TenantStatus(str, Enum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class PlanTier(str, Enum):
    FREE = "FREE"
    PRO = "PRO"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"


class BillingProvider(str, Enum):
    STRIPE = "STRIPE"
    PADDLE = "PADDLE"
    MANUAL_INVOICE = "MANUAL_INVOICE"
    ENTERPRISE_CONTRACT = "ENTERPRISE_CONTRACT"


class InvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    VOID = "VOID"


class SSOProtocol(str, Enum):
    SAML_2_0 = "SAML_2_0"
    OIDC = "OIDC"
    SCIM_2_0 = "SCIM_2_0"
    OAUTH2 = "OAUTH2"


class AssetType(str, Enum):
    AGENT_PACK = "AGENT_PACK"
    WORKFLOW_TEMPLATE = "WORKFLOW_TEMPLATE"
    PROMPT_PACK = "PROMPT_PACK"
    TOOL_PLUGIN = "TOOL_PLUGIN"
    OCR_PIPELINE = "OCR_PIPELINE"


class ConnectorType(str, Enum):
    GOOGLE_DRIVE = "GOOGLE_DRIVE"
    MICROSOFT_TEAMS = "MICROSOFT_TEAMS"
    SLACK = "SLACK"
    JIRA = "JIRA"
    SALESFORCE = "SALESFORCE"
    SAP = "SAP"
    SERVICENOW = "SERVICENOW"
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    SHAREPOINT = "SHAREPOINT"


class TenantLimits(BaseModel):
    max_organizations: int = 5
    max_workspaces: int = 20
    max_concurrent_agents: int = 50
    max_monthly_tokens: int = 100_000_000
    max_monthly_ocr_pages: int = 50_000
    max_storage_gb: int = 500
    monthly_budget_ceiling_usd: float = 10_000.0


class TenantConfiguration(BaseModel):
    default_region: str = "us-east-1"
    allowed_regions: List[str] = Field(default_factory=lambda: ["us-east-1", "eu-central-1", "asia-east-1"])
    data_residency_enforced: bool = True
    custom_domain: Optional[str] = None
    enforce_sso: bool = False
    mfa_required: bool = True
    allowed_model_families: List[str] = Field(default_factory=lambda: ["gemini-pro", "gemini-flash", "claude-3-5", "gpt-4o"])


class Tenant(BaseModel):
    tenant_id: str
    company_name: str
    slug: str
    tier: PlanTier = PlanTier.BUSINESS
    status: TenantStatus = TenantStatus.ACTIVE
    admin_email: str
    limits: TenantLimits = Field(default_factory=TenantLimits)
    config: TenantConfiguration = Field(default_factory=TenantConfiguration)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OrganizationNode(BaseModel):
    organization_id: str
    tenant_id: str
    name: str
    parent_org_id: Optional[str] = None
    business_unit: str = "Global Operations"
    country_code: str = "US"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Workspace(BaseModel):
    workspace_id: str
    tenant_id: str
    organization_id: str
    name: str
    slug: str
    owner_email: str
    allocated_agents_count: int = 10
    allocated_storage_gb: int = 50
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Project(BaseModel):
    project_id: str
    tenant_id: str
    workspace_id: str
    name: str
    description: str = ""
    active_workflows_count: int = 4
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SSOProviderConfig(BaseModel):
    provider_id: str
    tenant_id: str
    name: str  # "Google Workspace", "Okta", "Microsoft Entra ID"
    protocol: SSOProtocol = SSOProtocol.SAML_2_0
    issuer_url: str
    sso_endpoint: str
    certificate_fingerprint: str
    enabled: bool = True


class UserIdentity(BaseModel):
    user_id: str
    tenant_id: str
    email: str
    display_name: str
    role: str = "TENANT_ADMIN"  # SUPER_ADMIN, TENANT_ADMIN, WORKSPACE_MANAGER, AGENT_OPERATOR, VIEWER
    department: str = "Engineering"
    sso_linked: bool = True
    mfa_enabled: bool = True
    last_login_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Subscription(BaseModel):
    subscription_id: str
    tenant_id: str
    tier: PlanTier = PlanTier.BUSINESS
    billing_interval: str = "MONTHLY"  # MONTHLY, ANNUAL
    current_period_start: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_period_end: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "ACTIVE"
    base_price_monthly_usd: float = 2499.0
    auto_renew: bool = True


class Invoice(BaseModel):
    invoice_id: str
    tenant_id: str
    subscription_id: str
    amount_due_usd: float
    amount_paid_usd: float
    status: InvoiceStatus = InvoiceStatus.PAID
    billing_period: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    due_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class UsageRecord(BaseModel):
    record_id: str
    tenant_id: str
    workspace_id: str
    metric_name: str  # "llm_tokens", "ocr_pages", "api_requests", "compute_seconds"
    quantity: float
    unit: str
    unit_cost_usd: float
    total_cost_usd: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LicenseKey(BaseModel):
    license_id: str
    tenant_id: str
    tier: PlanTier
    max_seats: int
    signature_ed25519: str
    issued_at: str
    expires_at: str
    is_airgapped: bool = False
    valid: bool = True


class MarketplaceAsset(BaseModel):
    asset_id: str
    title: str
    asset_type: AssetType
    publisher_tenant_id: str
    publisher_name: str
    version: str = "1.0.0"
    description: str
    downloads_count: int = 0
    rating: float = 5.0
    verified: bool = True
    price_monthly_usd: float = 0.0
    tags: List[str] = Field(default_factory=list)


class ConnectorConfig(BaseModel):
    connector_id: str
    tenant_id: str
    connector_type: ConnectorType
    name: str
    status: str = "CONNECTED"  # CONNECTED, DISCONNECTED, ERROR
    auth_type: str = "OAUTH2"
    connected_workspaces: List[str] = Field(default_factory=list)
    last_synced_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TenantPolicy(BaseModel):
    policy_id: str
    tenant_id: str
    policy_name: str
    subject_role: str
    resource_type: str
    action: str  # READ, EXECUTE, DEPLOY, DELETE, APPROVE
    effect: str = "ALLOW"  # ALLOW, DENY
    conditions: Dict[str, Any] = Field(default_factory=dict)


class AuditEvent(BaseModel):
    audit_id: str
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    actor_id: str
    actor_email: str
    action: str
    resource_type: str
    resource_id: str
    ip_address: str = "127.0.0.1"
    previous_hash: str = "00000000000000000000000000000000"
    event_hash: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BrandingConfig(BaseModel):
    tenant_id: str
    custom_cname_domain: Optional[str] = None
    brand_name: str
    logo_url: str
    primary_color_hex: str = "#4f46e5"
    secondary_color_hex: str = "#06b6d4"
    support_email: str
    email_footer_text: str = "Powered by Enterprise AI Platform"


class SaaSExecutiveOverview(BaseModel):
    platform_name: str = "Enterprise AI Platform & Multi-Tenant SaaS Operating System"
    total_tenants: int
    active_tenants: int
    total_organizations: int
    total_workspaces: int
    monthly_recurring_revenue_usd: float
    annual_recurring_revenue_usd: float
    net_mrr_growth_pct: float
    total_metered_tokens: int
    total_metered_ocr_pages: int
    mean_system_sla_compliance_pct: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
