"""
Configuration Domain: Configurations and Immutable Canonical Execution Snapshots.
"""
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import hashlib
import json
import uuid


class ConfigurationSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"cfg_snap_{uuid.uuid4().hex[:8]}")
    configuration_id: str
    canonical_hash_sha256: str
    resolved_values: Dict[str, Any]
    is_frozen: bool = True
    created_by: str = "Enterprise Config Resolver"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Configuration(BaseModel):
    configuration_id: str = Field(default_factory=lambda: f"cfg_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    scope_type: str = "MODULE"
    owner: str = "Platform Engineering"
    version: str = "1.0.0"
    status: str = "ACTIVE"
    raw_parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
