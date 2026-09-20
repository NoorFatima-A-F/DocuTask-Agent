"""
Domain Models & Value Objects for Rag.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field as PydField
import uuid

class RagEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"rag_{uuid.uuid4().hex[:8]}")
    name: str = "Rag Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
