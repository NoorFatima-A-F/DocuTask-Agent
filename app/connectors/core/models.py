"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Domain Models.
Defines first-class connector entities, lifecycle states, authentication types,
capabilities, descriptors, normalized events, and execution contracts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class ConnectorCategory(str, Enum):
    """Broad functional categories for technology-independent capability discovery."""
    COMMUNICATION = "communication"
    STORAGE = "storage"
    SEARCH = "search"
    CRM = "crm"
    FINANCE = "finance"
    CALENDAR = "calendar"
    AI = "ai"
    DATABASE = "database"
    AUTOMATION = "automation"
    DOCUMENTS = "documents"
    DEV_TOOLS = "dev_tools"
    PRODUCTIVITY = "productivity"
    CUSTOM = "custom"


class ConnectorStatus(str, Enum):
    """10-state connector lifecycle specification."""
    DISCOVERED = "DISCOVERED"
    INSTALLED = "INSTALLED"
    CONFIGURED = "CONFIGURED"
    AUTHENTICATED = "AUTHENTICATED"
    VALIDATED = "VALIDATED"
    READY = "READY"
    ACTIVE = "ACTIVE"
    UPDATING = "UPDATING"
    DISABLED = "DISABLED"
    REMOVED = "REMOVED"


class ConnectorHealth(str, Enum):
    """Health indicator of a connector and its external backend dependencies."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class AuthType(str, Enum):
    """Supported authentication mechanisms across the universal connector framework."""
    OAUTH2 = "OAUTH2"
    OAUTH2_PKCE = "OAUTH2_PKCE"
    API_KEY = "API_KEY"
    JWT = "JWT"
    BEARER = "BEARER"
    BASIC = "BASIC"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    OIDC = "OIDC"
    SAML = "SAML"
    MTLS = "MTLS"
    NONE = "NONE"


class TriggerType(str, Enum):
    """Supported trigger types for external event ingestion."""
    WEBHOOK = "WEBHOOK"
    SCHEDULE = "SCHEDULE"
    POLLING = "POLLING"
    EVENT_STREAM = "EVENT_STREAM"
    DATABASE_EVENT = "DATABASE_EVENT"
    CLOUD_EVENT = "CLOUD_EVENT"
    MANUAL = "MANUAL"


class CapabilityDescriptor(BaseModel):
    """Technology-independent capability descriptor (e.g., email.send, message.send)."""
    name: str  # e.g., "email.send"
    category: ConnectorCategory = ConnectorCategory.COMMUNICATION
    description: str = ""
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class ActionDescriptor(BaseModel):
    """Contract and metadata for an executable connector action."""
    id: str = Field(default_factory=lambda: f"act-{uuid.uuid4().hex[:8]}")
    name: str  # e.g., "send_email"
    connector_id: str
    capability: str  # e.g., "email.send"
    description: str = ""
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)
    timeout_seconds: float = 30.0
    retry_policy: Dict[str, Any] = Field(default_factory=dict)
    cost_usd: float = 0.001
    idempotent: bool = False


class TriggerDescriptor(BaseModel):
    """Specification for an external event trigger."""
    id: str = Field(default_factory=lambda: f"trig-{uuid.uuid4().hex[:8]}")
    name: str  # e.g., "new_email_received"
    connector_id: str
    trigger_type: TriggerType = TriggerType.WEBHOOK
    description: str = ""
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    polling_interval_seconds: int = 60


class NormalizedEvent(BaseModel):
    """Canonical cross-platform event structure for all ingested vendor triggers."""
    id: str = Field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:12]}")
    type: str  # e.g., "email.received"
    source: str  # e.g., "connector.gmail"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    organization: str = "org-default"
    workspace_id: str = "ws-default"
    correlation_id: str = Field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:8]}")
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CredentialMetadata(BaseModel):
    """Tenant-isolated credential metadata (secrets stored in SecretProvider)."""
    id: str = Field(default_factory=lambda: f"cred-{uuid.uuid4().hex[:8]}")
    connector: str
    organization: str = "org-default"
    workspace: str = "ws-default"
    owner: str = "system"
    auth_type: AuthType = AuthType.API_KEY
    permissions: List[str] = Field(default_factory=list)
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires: Optional[datetime] = None
    rotation_policy: str = "90_days"
    secret_key_ref: str = ""
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionResult(BaseModel):
    """Result of an action execution through the connector runtime."""
    execution_id: str = Field(default_factory=lambda: f"exec-{uuid.uuid4().hex[:10]}")
    connector_id: str
    action_name: str
    status: str = "SUCCESS"  # SUCCESS, FAILED, TIMED_OUT, POLICY_REJECTED
    output: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    cached: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConnectorPolicyRule(BaseModel):
    """Governance and security policy governing connector invocation."""
    id: str = Field(default_factory=lambda: f"cpol-{uuid.uuid4().hex[:8]}")
    name: str = "default_policy"
    allowed_connectors: Optional[List[str]] = None  # None = all allowed
    disallowed_connectors: List[str] = Field(default_factory=list)
    allowed_regions: Optional[List[str]] = None
    disallowed_data_tags: List[str] = Field(default_factory=list)
    max_cost_per_call_usd: float = 1.0
    require_approval_above_cost_usd: float = 0.50
    pii_redaction_required: bool = True
    max_concurrency: int = 50


class Connector(BaseModel):
    """
    First-class platform resource representing an installable integration provider.
    """
    id: str
    name: str
    vendor: str
    version: str = "1.0.0"
    category: ConnectorCategory = ConnectorCategory.CUSTOM
    capabilities: List[str] = Field(default_factory=list)
    authentication_types: List[AuthType] = Field(default_factory=lambda: [AuthType.API_KEY])
    supported_regions: List[str] = Field(default_factory=lambda: ["global", "us-east-1", "eu-west-1"])
    api_versions: List[str] = Field(default_factory=lambda: ["v1"])
    status: ConnectorStatus = ConnectorStatus.DISCOVERED
    owner: str = "system"
    health: ConnectorHealth = ConnectorHealth.HEALTHY
    documentation: str = ""
    license: str = "Apache-2.0"
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
