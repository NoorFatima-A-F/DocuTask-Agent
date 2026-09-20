"""
Environment Domain: Tier Provisioning, Snapshots, Hardware Profiles, and Runtime Fingerprints.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class EnvironmentType(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION_SHADOW = "PRODUCTION_SHADOW"
    CHAOS = "CHAOS"
    SECURITY_LAB = "SECURITY_LAB"


class HardwareProfile(BaseModel):
    cpu_cores: int = 8
    ram_gb: float = 32.0
    gpu_type: Optional[str] = "NVIDIA-A100-80GB"
    gpu_count: int = 1
    storage_type: str = "NVMe-SSD"


class EnvironmentSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"env_snap_{uuid.uuid4().hex[:8]}")
    environment_id: str
    tier: EnvironmentType
    operating_system: str = "Ubuntu 24.04 LTS / Linux 6.8"
    runtime_version: str = "Python 3.14.0"
    container_image_digest: str = "sha256:d41d8cd98f00b204e9800998ecf8427e"
    infrastructure_version: str = "k8s-v1.30.2"
    hardware_profile: HardwareProfile = Field(default_factory=HardwareProfile)
    network_configuration: Dict[str, str] = Field(default_factory=lambda: {"vpc": "verification-vpc-01", "egress": "RESTRICTED"})
    dependency_fingerprint_sha256: str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    git_commit_sha: str = "main-e9f8a12b"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Environment(BaseModel):
    environment_id: str = Field(default_factory=lambda: f"env_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    tier: EnvironmentType = EnvironmentType.INTEGRATION
    owner: str = "Platform SRE Team"
    purpose: str = "Integration & Verification Benchmarking"
    status: str = "READY"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
