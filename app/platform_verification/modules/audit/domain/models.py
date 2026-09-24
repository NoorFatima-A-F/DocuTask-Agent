"""
Domain Models & Value Objects for Audit.
"""
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field as PydField
import uuid

class AuditEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"audi_{uuid.uuid4().hex[:8]}")
    name: str = "Audit Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
