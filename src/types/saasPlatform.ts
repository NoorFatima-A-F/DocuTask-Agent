/**
 * Phase 13.19: Enterprise AI Platform & Multi-Tenant SaaS Operating System (EAP-MTSOS)
 * Frontend TypeScript Interfaces & Enums.
 */

export type PlanTier = 'FREE' | 'PRO' | 'BUSINESS' | 'ENTERPRISE';
export type TenantStatus = 'PROVISIONING' | 'ACTIVE' | 'SUSPENDED' | 'ARCHIVED' | 'DELETED';
export type SSOProtocol = 'SAML_2_0' | 'OIDC' | 'SCIM_2_0' | 'OAUTH2';
export type AssetType = 'AGENT_PACK' | 'WORKFLOW_TEMPLATE' | 'PROMPT_PACK' | 'TOOL_PLUGIN' | 'OCR_PIPELINE';
export type ConnectorType =
  | 'GOOGLE_DRIVE'
  | 'MICROSOFT_TEAMS'
  | 'SLACK'
  | 'JIRA'
  | 'SALESFORCE'
  | 'SAP'
  | 'SERVICENOW'
  | 'GITHUB'
  | 'GITLAB'
  | 'SHAREPOINT';

export interface TenantLimits {
  max_organizations: number;
  max_workspaces: number;
  max_concurrent_agents: number;
  max_monthly_tokens: number;
  max_monthly_ocr_pages: number;
  max_storage_gb: number;
  monthly_budget_ceiling_usd: number;
}

export interface TenantConfiguration {
  default_region: string;
  allowed_regions: string[];
  data_residency_enforced: boolean;
  custom_domain?: string | null;
  enforce_sso: boolean;
  mfa_required: boolean;
  allowed_model_families: string[];
}

export interface Tenant {
  tenant_id: string;
  company_name: string;
  slug: string;
  tier: PlanTier;
  status: TenantStatus;
  admin_email: string;
  limits: TenantLimits;
  config: TenantConfiguration;
  created_at: string;
  updated_at: string;
}

export interface OrganizationNode {
  organization_id: string;
  tenant_id: string;
  name: string;
  parent_org_id?: string | null;
  business_unit: string;
  country_code: string;
  created_at: string;
  children?: OrganizationNode[];
}

export interface Workspace {
  workspace_id: string;
  tenant_id: string;
  organization_id: string;
  name: string;
  slug: string;
  owner_email: string;
  allocated_agents_count: number;
  allocated_storage_gb: number;
  created_at: string;
}

export interface Project {
  project_id: string;
  tenant_id: string;
  workspace_id: string;
  name: string;
  description: string;
  active_workflows_count: number;
  created_at: string;
}

export interface SSOProviderConfig {
  provider_id: string;
  tenant_id: string;
  name: string;
  protocol: SSOProtocol;
  issuer_url: string;
  sso_endpoint: string;
  certificate_fingerprint: string;
  enabled: boolean;
}

export interface UserIdentity {
  user_id: string;
  tenant_id: string;
  email: string;
  display_name: string;
  role: string;
  department: string;
  sso_linked: boolean;
  mfa_enabled: boolean;
  last_login_at: string;
}

export interface Subscription {
  subscription_id: string;
  tenant_id: string;
  tier: PlanTier;
  billing_interval: string;
  current_period_start: string;
  current_period_end: string;
  status: string;
  base_price_monthly_usd: number;
  auto_renew: boolean;
}

export interface Invoice {
  invoice_id: string;
  tenant_id: string;
  subscription_id: string;
  amount_due_usd: number;
  amount_paid_usd: number;
  status: 'DRAFT' | 'OPEN' | 'PAID' | 'OVERDUE' | 'VOID';
  billing_period: string;
  created_at: string;
  due_date: string;
}

export interface UsageRecord {
  record_id: string;
  tenant_id: string;
  workspace_id: string;
  metric_name: string;
  quantity: number;
  unit: string;
  unit_cost_usd: number;
  total_cost_usd: number;
  timestamp: string;
}

export interface LicenseKey {
  license_id: string;
  tenant_id: string;
  tier: PlanTier;
  max_seats: number;
  signature_ed25519: string;
  issued_at: string;
  expires_at: string;
  is_airgapped: boolean;
  valid: boolean;
}

export interface MarketplaceAsset {
  asset_id: string;
  title: string;
  asset_type: AssetType;
  publisher_tenant_id: string;
  publisher_name: string;
  version: string;
  description: string;
  downloads_count: number;
  rating: number;
  verified: boolean;
  price_monthly_usd: number;
  tags: string[];
}

export interface ConnectorConfig {
  connector_id: string;
  tenant_id: string;
  connector_type: ConnectorType;
  name: string;
  status: string;
  auth_type: string;
  connected_workspaces: string[];
  last_synced_at: string;
}

export interface TenantPolicy {
  policy_id: string;
  tenant_id: string;
  policy_name: string;
  subject_role: string;
  resource_type: string;
  action: string;
  effect: string;
  conditions: Record<string, any>;
}

export interface AuditEvent {
  audit_id: string;
  tenant_id: string;
  organization_id?: string | null;
  workspace_id?: string | null;
  actor_id: string;
  actor_email: string;
  action: string;
  resource_type: string;
  resource_id: string;
  ip_address: string;
  previous_hash: string;
  event_hash: string;
  timestamp: string;
}

export interface BrandingConfig {
  tenant_id: string;
  custom_cname_domain?: string | null;
  brand_name: string;
  logo_url: string;
  primary_color_hex: string;
  secondary_color_hex: string;
  support_email: string;
  email_footer_text: string;
}

export interface SaaSExecutiveOverview {
  platform_name: string;
  total_tenants: number;
  active_tenants: number;
  total_organizations: number;
  total_workspaces: number;
  monthly_recurring_revenue_usd: number;
  annual_recurring_revenue_usd: number;
  net_mrr_growth_pct: number;
  total_metered_tokens: number;
  total_metered_ocr_pages: number;
  mean_system_sla_compliance_pct: number;
  timestamp: string;
}
