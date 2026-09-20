"""Retention Policy Models & Definitions."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class RetentionAction(str, Enum):
    DELETE_AFTER_PERIOD = "DELETE_AFTER_PERIOD"
    ARCHIVE = "ARCHIVE"
    LEGAL_HOLD = "LEGAL_HOLD"
    PERMANENT_RETENTION = "PERMANENT_RETENTION"


class RetentionPolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"ret_pol_{uuid.uuid4().hex[:8]}")
    tenant_id: str
    name: str
    description: Optional[str] = None
    action: RetentionAction = RetentionAction.ARCHIVE
    retention_days: int = 365  # Default 1 year (e.g. 2555 days = 7 years for financial)
    applies_to_categories: List[str] = Field(default_factory=lambda: ["*"])
    applies_to_classifications: List[str] = Field(default_factory=lambda: ["*"])
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
