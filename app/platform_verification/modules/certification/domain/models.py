"""
Domain Models & Value Objects for Certification.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field as PydField
import uuid

class CertificationEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"cert_{uuid.uuid4().hex[:8]}")
    name: str = "Certification Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
