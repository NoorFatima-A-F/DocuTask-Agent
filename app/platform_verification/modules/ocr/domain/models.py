"""
Domain Models & Value Objects for Ocr.
"""
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field as PydField
import uuid

class OcrEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"ocr_{uuid.uuid4().hex[:8]}")
    name: str = "Ocr Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
