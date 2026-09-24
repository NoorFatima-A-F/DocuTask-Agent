"""Data Provenance Source Records (Phase 8B)."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field


class ProvenanceSourceRecord(BaseModel):
    """Immutable record of the primary source and origin of a data asset."""
    source_id: str
    asset_id: str
    original_uri: str
    source_type: str  # FILE_UPLOAD, CONNECTOR_SYNC, USER_INPUT, SYSTEM_EVENT
    checksum_sha256: str
    uploaded_by: str
    organization_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def verify_content(self, content: bytes | str) -> bool:
        """Verify content integrity against SHA-256 checksum."""
        data = content.encode("utf-8") if isinstance(content, str) else content
        return hashlib.sha256(data).hexdigest() == self.checksum_sha256
