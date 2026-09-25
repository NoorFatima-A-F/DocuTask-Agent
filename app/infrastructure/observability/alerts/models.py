"""
Alert Domain Models & Severity Classifications.

Defines alert severities (INFO, MINOR, MAJOR, CRITICAL, EMERGENCY),
rule definitions, alert states, and routing policies.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from pydantic import BaseModel, Field


class AlertSeverity(str, enum.Enum):
    """Five enterprise alert severity tiers."""
    INFO = "INFO"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class AlertStatus(str, enum.Enum):
    """Lifecycle status of an alert instance."""
    FIRING = "FIRING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    SILENCED = "SILENCED"


class RuleType(str, enum.Enum):
    """Type of alert condition logic."""
    THRESHOLD = "THRESHOLD"
    RATE_OF_CHANGE = "RATE_OF_CHANGE"
    ANOMALY = "ANOMALY"
    COMPOSITE = "COMPOSITE"
    SLO_BURN_RATE = "SLO_BURN_RATE"


class AlertRule(BaseModel):
    """Configurable alert rule specification."""
    rule_id: str
    name: str
    description: str = ""
    rule_type: RuleType = RuleType.THRESHOLD
    severity: AlertSeverity = AlertSeverity.WARNING if hasattr(AlertSeverity, "WARNING") else AlertSeverity.MAJOR
    metric_name: str
    comparator: str = ">"  # >, >=, <, <=, ==
    threshold_value: float
    duration_seconds: float = Field(default=60.0, ge=0.0)
    labels: Dict[str, str] = Field(default_factory=dict)
    team: str = "sre"
    enabled: bool = True


class AlertInstance(BaseModel):
    """Instantiated active or historical alert event."""
    alert_id: str = Field(default_factory=lambda: f"alt-{uuid.uuid4().hex[:12]}")
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.FIRING
    current_value: float
    threshold_value: float
    message: str
    service_name: str = "docutask-service"
    region: str = "us-east-1"
    tenant_id: str = "global"
    team: str = "sre"
    labels: Dict[str, str] = Field(default_factory=dict)
    fingerprint: str = ""
    fired_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
