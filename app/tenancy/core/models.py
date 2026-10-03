"""Enterprise SaaS Multi-Tenancy Core Domain Models (ESP-MOOS).

Defines first-class tenant resources: Organizations, Workspaces, Environments,
Projects, Teams, Memberships, Invitations, ResourceIdentity, TenantContext,
Subscription Tiers, Quotas, Metering Events, Branding, Domains, and Backups.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class TenantLifecycleState(str, enum.Enum):
    """Organization 7-state lifecycle state machine."""
    REGISTERED = "REGISTERED"
    PROVISIONING = "PROVISIONING"
    INITIALIZED = "INITIALIZED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class EnvironmentType(str, enum.Enum):
    """Execution environment types."""
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    QA = "QA"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    SANDBOX = "SANDBOX"


class MembershipRole(str, enum.Enum):
    """RBAC roles for workspace and organization membership."""
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"
    GUEST = "GUEST"
    AUDITOR = "AUDITOR"


class InvitationState(str, enum.Enum):
    """5-state invitation lifecycle."""
    CREATED = "CREATED"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class QuotaState(str, enum.Enum):
    """Resource quota states."""
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    LIMITED = "LIMITED"
    EXCEEDED = "EXCEEDED"
    SUSPENDED = "SUSPENDED"


class SubscriptionTier(str, enum.Enum):
    """SaaS commercial subscription tiers."""
    FREE = "FREE"
    DEVELOPER = "DEVELOPER"
    PROFESSIONAL = "PROFESSIONAL"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"
    CUSTOM = "CUSTOM"


class ComplianceProfileType(str, enum.Enum):
    """Compliance framework profiles."""
    STANDARD = "STANDARD"
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    PCI_DSS = "PCI_DSS"


class Region(str, enum.Enum):
    """Supported geographical deployment and data residency regions."""
    US_EAST = "us-east-1"
    US_WEST = "us-west-2"
    EU_WEST = "eu-west-1"
    EU_CENTRAL = "eu-central-1"
    ASIA_PACIFIC = "ap-southeast-1"
    MIDDLE_EAST = "me-central-1"
    PRIVATE_CLOUD = "private-cloud"


class ResourceType(str, enum.Enum):
    """Platform resource types governed by tenant ownership."""
    WORKFLOW = "WORKFLOW"
    AGENT = "AGENT"
    KNOWLEDGE = "KNOWLEDGE"
    CONNECTOR = "CONNECTOR"
    SECRET = "SECRET"
    PROMPT = "PROMPT"
    TEMPLATE = "TEMPLATE"
    EXECUTION = "EXECUTION"
    DATASET = "DATASET"
    MODEL = "MODEL"


class ResourceIdentity(BaseModel):
    """Canonical ownership metadata stamped on all platform entities."""
    resource_id: str
    resource_type: ResourceType
    organization_id: str
    workspace_id: str
    environment_id: str = "default"
    project_id: str = "default"
    owner_id: str
    creator_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags: Dict[str, str] = Field(default_factory=dict)


class TenantContext(BaseModel):
    """Unified tenant context passed with all requests and worker jobs."""
    organization_id: str
    workspace_id: str
    environment_id: str = "default"
    project_id: str = "default"
    user_id: str
    role_ids: List[str] = Field(default_factory=list)
    permissions: Set[str] = Field(default_factory=set)
    region: Region = Region.US_EAST
    compliance_profile: ComplianceProfileType = ComplianceProfileType.STANDARD
    subscription_plan: SubscriptionTier = SubscriptionTier.FREE
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    is_admin_delegated: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Organization(BaseModel):
    """Tenant organization entity."""
    id: str
    name: str
    slug: str
    industry: str = "Technology"
    region: Region = Region.US_EAST
    timezone: str = "UTC"
    status: TenantLifecycleState = TenantLifecycleState.REGISTERED
    subscription_id: str = "sub_free"
    subscription_plan: SubscriptionTier = SubscriptionTier.FREE
    compliance_profile: ComplianceProfileType = ComplianceProfileType.STANDARD
    branding_id: Optional[str] = None
    owner_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Workspace(BaseModel):
    """Workspace boundary within an organization."""
    workspace_id: str
    organization_id: str
    name: str
    description: str = ""
    department: str = "General"
    region: Region = Region.US_EAST
    status: str = "ACTIVE"
    policies: Dict[str, Any] = Field(default_factory=dict)
    configuration: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Environment(BaseModel):
    """Execution environment partition within a workspace."""
    environment_id: str
    workspace_id: str
    organization_id: str
    name: str
    env_type: EnvironmentType = EnvironmentType.DEVELOPMENT
    variables: Dict[str, str] = Field(default_factory=dict)
    secrets: Dict[str, str] = Field(default_factory=dict)
    connectors: List[str] = Field(default_factory=list)
    workflow_versions: Dict[str, str] = Field(default_factory=dict)
    agent_configs: Dict[str, Any] = Field(default_factory=dict)
    knowledge_snapshot_id: Optional[str] = None
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    is_locked: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Project(BaseModel):
    """Project deployment boundary within a workspace."""
    project_id: str
    workspace_id: str
    organization_id: str
    name: str
    description: str = ""
    workflows: List[str] = Field(default_factory=list)
    agents: List[str] = Field(default_factory=list)
    knowledge_spaces: List[str] = Field(default_factory=list)
    connectors: List[str] = Field(default_factory=list)
    policies: Dict[str, Any] = Field(default_factory=dict)
    variables: Dict[str, str] = Field(default_factory=dict)
    resources: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Team(BaseModel):
    """Team grouping within an organization."""
    team_id: str
    organization_id: str
    name: str
    department: str
    description: str = ""
    member_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Membership(BaseModel):
    """User membership in an organization or workspace."""
    membership_id: str
    user_id: str
    organization_id: str
    workspace_id: Optional[str] = None
    role: MembershipRole = MembershipRole.MEMBER
    permissions: Set[str] = Field(default_factory=set)
    status: str = "ACTIVE"
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Invitation(BaseModel):
    """User invitation to join organization or workspace."""
    invitation_id: str
    email: str
    organization_id: str
    workspace_id: Optional[str] = None
    role: MembershipRole = MembershipRole.MEMBER
    inviter_user_id: str
    status: InvitationState = InvitationState.CREATED
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuotaLimit(BaseModel):
    """Quota limit and current usage for a single resource."""
    resource_name: str
    limit_value: int
    current_usage: int = 0
    warning_threshold: float = 0.8
    hard_limit: bool = True
    quota_state: QuotaState = QuotaState.NORMAL


class MeteringEvent(BaseModel):
    """Granular usage metering event for billing and analytics."""
    event_id: str
    organization_id: str
    workspace_id: str
    resource_type: str
    quantity: float
    unit: str
    cost_usd: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Subscription(BaseModel):
    """Subscription configuration and entitlement contract."""
    subscription_id: str
    organization_id: str
    tier: SubscriptionTier
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True
    features: Dict[str, bool] = Field(default_factory=dict)
    quotas: Dict[str, int] = Field(default_factory=dict)
    billing_interval: str = "MONTHLY"
    amount_usd: float = 0.0


class BrandingProfile(BaseModel):
    """White-label organization visual branding."""
    branding_id: str
    organization_id: str
    logo_url: str = ""
    favicon_url: str = ""
    primary_color: str = "#0052CC"
    secondary_color: str = "#172B4D"
    font_family: str = "Inter, sans-serif"
    email_footer_text: str = ""
    custom_login_title: str = "DocuTask Enterprise"
    css_overrides: str = ""


class CustomDomain(BaseModel):
    """Custom domain routing and SSL metadata."""
    domain_id: str
    organization_id: str
    domain_name: str
    is_verified: bool = False
    verification_token: str
    ssl_active: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BackupSnapshot(BaseModel):
    """Tenant backup archive representation."""
    snapshot_id: str
    organization_id: str
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    scope: str = "FULL_ORGANIZATION"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = Field(default_factory=dict)
    size_bytes: int = 0
    checksum: str = ""
