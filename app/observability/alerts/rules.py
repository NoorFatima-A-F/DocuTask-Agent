"""Alert Rule Definitions and Evaluation Conditions."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class RuleConditionType(str, Enum):
    METRIC_THRESHOLD = "METRIC_THRESHOLD"
    EVENT_MATCH = "EVENT_MATCH"
    ANOMALY_SPIKE = "ANOMALY_SPIKE"


@dataclass
class AlertRule:
    rule_id: str
    name: str
    severity: AlertSeverity = AlertSeverity.WARNING
    condition_type: RuleConditionType = RuleConditionType.METRIC_THRESHOLD
    metric_name: str = ""
    operator: str = ">"  # ">", "<", ">=", "<=", "=="
    threshold_value: float = 0.0
    duration_seconds: float = 0.0
    description: str = ""
    enabled: bool = True
    labels: Dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def evaluate_metric(self, current_value: float) -> bool:
        if not self.enabled:
            return False
        if self.operator == ">":
            return current_value > self.threshold_value
        elif self.operator == ">=":
            return current_value >= self.threshold_value
        elif self.operator == "<":
            return current_value < self.threshold_value
        elif self.operator == "<=":
            return current_value <= self.threshold_value
        elif self.operator == "==":
            return current_value == self.threshold_value
        return False
