"""Review Comments and Auditor Notes."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class ReviewComment(BaseModel):
    """Comment or deliberation note attached to a human review request."""
    comment_id: str = Field(default_factory=lambda: f"cmt_{uuid.uuid4().hex[:8]}")
    review_id: str
    tenant_id: str
    author_id: str
    author_name: str
    author_role: str
    text: str
    is_internal: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
