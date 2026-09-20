"""Governance Alert Rules, Conditions, and Severity Classifications."""

from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertCondition(BaseModel):
    metric_name: str
    operator: str   # ">", ">=", "<", "<=", "=="
    threshold: float


class AlertRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: f"alr_rule_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "*"
    name: str
    metric: str
    operator: str = ">"
    threshold: float
    severity: AlertSeverity = AlertSeverity.HIGH
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
