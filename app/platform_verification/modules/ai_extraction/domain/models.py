"""
Domain Models & Value Objects for AiExtraction.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field as PydField
import uuid

class AiExtractionEntity(BaseModel):
    id: str = PydField(default_factory=lambda: f"ai_e_{uuid.uuid4().hex[:8]}")
    name: str = "AiExtraction Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = PydField(default_factory=dict)
    created_at: str = PydField(default_factory=lambda: datetime.now(timezone.utc).isoformat())
