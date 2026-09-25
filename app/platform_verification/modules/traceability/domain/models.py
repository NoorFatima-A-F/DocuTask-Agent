"""
Domain Models & Value Objects for Traceability.
"""
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field as PydField
import uuid

class TraceabilityEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"trac_{uuid.uuid4().hex[:8]}")
    name: str = "Traceability Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
