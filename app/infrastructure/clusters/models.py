"""Cluster Domain Models, Types, and Lifecycle Status."""

from datetime import datetime, timezone
from enum import Enum
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class ClusterType(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"
    PRIVATE = "PRIVATE"
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    AIR_GAPPED = "AIR_GAPPED"


class ClusterStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    REGISTERING = "REGISTERING"
    REGISTERED = "REGISTERED"
    VALIDATING = "VALIDATING"
    READY = "READY"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    MAINTENANCE = "MAINTENANCE"
    SUSPENDED = "SUSPENDED"
    OFFLINE = "OFFLINE"
    REMOVED = "REMOVED"


class CapacityModel(BaseModel):
    """Compute, Memory, and Storage capacity metrics for a cluster."""

    total_cpu_cores: float = 128.0
    allocatable_cpu_cores: float = 110.0
    utilized_cpu_cores: float = 24.0

    total_memory_gb: float = 512.0
    allocatable_memory_gb: float = 480.0
    utilized_memory_gb: float = 120.0

    total_storage_tb: float = 10.0
    utilized_storage_tb: float = 2.5

    max_pod_capacity: int = 1000
    active_pod_count: int = 150


class ClusterIdentity(BaseModel):
    """Cryptographic and platform identity of a registered cluster."""

    cluster_identity_id: str = Field(default_factory=lambda: f"cid_{secrets.token_hex(8)}")
    workload_identity: str
    provider_identity: str  # e.g. arn:aws:iam::..., gcp-sa@..., spiffe://...
    ownership: str = "docutask-platform-team"
    trust_status: str = "TRUSTED"  # TRUSTED, PROVISIONAL, REVOKED
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClusterLease(BaseModel):
    """Heartbeat lease representing live connectivity."""

    lease_id: str = Field(default_factory=lambda: f"lease_{secrets.token_hex(8)}")
    cluster_id: str
    ttl_seconds: int = 60
    last_renewed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_valid: bool = True


class Cluster(BaseModel):
    """Complete first-class governed Cluster entity."""

    cluster_id: str
    name: str
    provider: str = "kubernetes"  # kubernetes, aws, gcp, azure, local
    region_id: str = "us-east-1"
    environment: str = "PRODUCTION"
    cluster_type: ClusterType = ClusterType.PRODUCTION
    status: ClusterStatus = ClusterStatus.DISCOVERED
    version: str = "1.30.0"
    control_plane_version: str = "3.1.0"
    data_plane_version: str = "3.1.0"
    labels: Dict[str, str] = Field(default_factory=dict)
    capabilities: Set[str] = Field(default_factory=set)
    capacity: CapacityModel = Field(default_factory=CapacityModel)
    tenant_affinity: List[str] = Field(default_factory=list)  # Empty means all allowed unless policy restricted
    compliance_profiles: List[str] = Field(default_factory=lambda: ["SOC2_TYPE_II", "GDPR", "HIPAA"])
    supported_workloads: List[str] = Field(default_factory=lambda: ["ocr", "agent", "workflow", "model_inference"])
    endpoint_metadata: Dict[str, str] = Field(default_factory=dict)
    health_status: str = "HEALTHY"
    identity: Optional[ClusterIdentity] = None
    active_lease: Optional[ClusterLease] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    maintenance_reason: Optional[str] = None
    quarantine_reason: Optional[str] = None
