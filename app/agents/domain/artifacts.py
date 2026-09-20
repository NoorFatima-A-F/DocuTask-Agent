"""
Produced Execution Artifacts Domain Model.
Defines strongly typed artifacts with SHA-256 checksums, producer metadata, location, and MIME types.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.domain.enums import ArtifactType
from app.agents.domain.value_objects import ArtifactID


class ExecutionArtifact(BaseModel):
    """Execution artifact produced by agent task execution."""

    artifact_id: ArtifactID = Field(default_factory=ArtifactID)
    artifact_type: ArtifactType
    version: str = Field(default="v1.0")
    sha256_checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    producer_component: str = Field(default="DocumentAgent")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    storage_location_uri: str = Field(default="")
    size_bytes: int = Field(default=0, ge=0)
    mime_type: str = Field(default="application/json")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    content_payload: Optional[Any] = Field(default=None)

    model_config = {"frozen": True}
