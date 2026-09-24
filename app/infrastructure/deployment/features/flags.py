"""Feature Flag Definitions, Targeting Rules, and Percentage Ramp-Up."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class RolloutRule:
    """Targeting rule for feature flag evaluation."""
    target_environments: List[str] = field(default_factory=lambda: ["*"])
    target_tenants: List[str] = field(default_factory=lambda: ["*"])
    target_users: List[str] = field(default_factory=list)
    percentage: float = 100.0  # 0.0 to 100.0


@dataclass
class FeatureFlag:
    """A governed feature flag definition."""
    flag_key: str
    name: str
    description: str = ""
    enabled: bool = False
    rules: List[RolloutRule] = field(default_factory=list)
    kill_switch_active: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
