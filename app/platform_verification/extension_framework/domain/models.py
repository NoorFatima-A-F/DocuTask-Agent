"""
Domain Models for Enterprise Verification Extension Framework & Plugin Architecture.
"""
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class PluginCategory(str, Enum):
    VERIFICATION = "VERIFICATION"
    EXECUTION = "EXECUTION"
    DATASET = "DATASET"
    METRIC = "METRIC"
    AI_PROVIDER = "AI_PROVIDER"
    STORAGE = "STORAGE"
    NOTIFICATION = "NOTIFICATION"
    COMPLIANCE = "COMPLIANCE"


class PluginLifecycleState(str, Enum):
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    INSTALLED = "INSTALLED"
    REGISTERED = "REGISTERED"
    INITIALIZED = "INITIALIZED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"
    FAILED = "FAILED"
    DEPRECATED = "DEPRECATED"
    REMOVED = "REMOVED"


class PluginHealthState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    QUARANTINED = "QUARANTINED"
    DISABLED = "DISABLED"


class PluginPermission(str, Enum):
    READ_DATASET = "READ_DATASET"
    WRITE_EVIDENCE = "WRITE_EVIDENCE"
    ACCESS_MODEL = "ACCESS_MODEL"
    ACCESS_NETWORK = "ACCESS_NETWORK"
    ACCESS_STORAGE = "ACCESS_STORAGE"
    EXECUTE_CODE = "EXECUTE_CODE"
    EMIT_CUSTOM_METRICS = "EMIT_CUSTOM_METRICS"
    KMS_SIGN = "KMS_SIGN"


class SecurityClassification(str, Enum):
    INTERNAL = "INTERNAL"
    COMMUNITY = "COMMUNITY"
    VERIFIED_PARTNER = "VERIFIED_PARTNER"
    ENTERPRISE_CERTIFIED = "ENTERPRISE_CERTIFIED"
    SANDBOXED_UNTRUSTED = "SANDBOXED_UNTRUSTED"


class PluginDependencyDeclaration(BaseModel):
    name: str
    min_version: str = "1.0.0"
    max_version: Optional[str] = None
    is_optional: bool = False
    dependency_type: str = "PLUGIN"  # PLUGIN, PYTHON_PACKAGE, SERVICE, AI_MODEL


class PluginMetadata(BaseModel):
    plugin_id: str
    name: str
    version: str = "1.0.0"
    category: PluginCategory = PluginCategory.VERIFICATION
    author: str = "DocuTask Verification Squad"
    owner: str = "Enterprise Architecture"
    description: str
    capabilities: List[str] = Field(default_factory=list)
    supported_verification_levels: List[str] = Field(default_factory=lambda: ["UNIT", "INTEGRATION", "E2E", "CANARY", "CHAOS"])
    dependencies: List[PluginDependencyDeclaration] = Field(default_factory=list)
    min_platform_version: str = "2.0.0"
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    security_classification: SecurityClassification = SecurityClassification.INTERNAL
    granted_permissions: List[PluginPermission] = Field(default_factory=list)
    license: str = "Apache-2.0"
    api_version: str = "1.0.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginManifest(BaseModel):
    manifest_id: str = Field(default_factory=lambda: f"mnf_{uuid.uuid4().hex[:8]}")
    name: str
    version: str
    category: PluginCategory
    runtime_python: str = ">=3.12"
    interfaces: List[str] = Field(default_factory=list)
    required_permissions: List[PluginPermission] = Field(default_factory=list)
    manifest_hash_sha256: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_hash(self) -> str:
        payload = f"{self.name}:{self.version}:{self.category.value}:{self.runtime_python}:{','.join(self.interfaces)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def __init__(self, **data):
        super().__init__(**data)
        if not self.manifest_hash_sha256:
            self.manifest_hash_sha256 = self.compute_hash()


class PluginMarketplaceEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: f"mkt_{uuid.uuid4().hex[:8]}")
    plugin_id: str
    version: str
    category: PluginCategory
    author: str
    certification_level: SecurityClassification = SecurityClassification.COMMUNITY
    download_count: int = 0
    rating: float = 5.0
    digital_signature: str = ""
    is_published: bool = True
    published_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginQuarantineRecord(BaseModel):
    quarantine_id: str = Field(default_factory=lambda: f"qrt_{uuid.uuid4().hex[:8]}")
    plugin_id: str
    quarantined_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reason: str
    consecutive_failures: int
    is_active: bool = True


class PluginSecurityContext(BaseModel):
    caller_identity: str
    permissions: List[PluginPermission] = Field(default_factory=list)
    is_sandboxed: bool = True
    max_memory_mb: int = 1024
    max_execution_time_seconds: int = 60
    allow_network_hosts: List[str] = Field(default_factory=list)


class PluginExecutionContext(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:8]}")
    verification_id: str
    dataset_reference: Dict[str, Any] = Field(default_factory=dict)
    configuration_snapshot: Dict[str, Any] = Field(default_factory=dict)
    environment_metadata: Dict[str, Any] = Field(default_factory=dict)
    security_context: PluginSecurityContext
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginExecutionResult(BaseModel):
    execution_id: str
    plugin_id: str
    is_success: bool
    metrics: List[Dict[str, Any]] = Field(default_factory=list)
    raw_evidence: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    logs: List[str] = Field(default_factory=list)
    completed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginHealthMetrics(BaseModel):
    plugin_id: str
    state: PluginHealthState = PluginHealthState.HEALTHY
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    last_error: Optional[str] = None
    last_health_check: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    plugin_id: str
    plugin_version: str
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_id: Optional[str] = None
    correlation_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0.0"
