"""Evidence Attachment Models."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import hashlib
import uuid


class EvidenceAttachment(BaseModel):
    """Raw payload snapshot or binary evidence attachment."""
    attachment_id: str = Field(default_factory=lambda: f"att_{uuid.uuid4().hex[:10]}")
    evidence_id: str
    filename: str
    mime_type: str = "application/json"
    content_text: Optional[str] = None
    checksum: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def compute_checksum(self) -> str:
        data = (self.content_text or "").encode("utf-8")
        self.checksum = hashlib.sha256(data).hexdigest()
        return self.checksum
