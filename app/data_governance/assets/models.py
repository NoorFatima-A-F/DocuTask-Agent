"""Asset Versioning & Metadata Domain Models (Phase 8B)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.data_governance.registry.models import DataAsset, AssetLifecycleState, ClassificationLevel


class DataAssetVersion(BaseModel):
    """Immutable snapshot record of an asset version."""
    version_id: str
    asset_id: str
    version_number: int
    checksum_sha256: str
    size_bytes: int
    classification: ClassificationLevel
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    change_summary: str = ""
    snapshot_payload: Dict[str, Any] = Field(default_factory=dict)


class AssetTag(BaseModel):
    """Governed metadata tag attached to an asset."""
    tag_name: str
    tag_value: str
    assigned_by: str
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
