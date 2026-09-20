"""
Domain Models & Value Objects for Datasets.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field as PydField
import uuid

class DatasetsEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"data_{uuid.uuid4().hex[:8]}")
    name: str = "Datasets Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
