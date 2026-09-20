"""Alert Engine with Storm Dampening and Deduplication."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .rules import AlertRule, AlertSeverity, RuleConditionType
from ..metrics.registry import MetricRegistry


class AlertState(str, Enum):
    PENDING = "PENDING"
    FIRING = "FIRING"
    RESOLVED = "RESOLVED"
    SUPPRESSED = "SUPPRESSED"


@dataclass
class ActiveAlert:
    alert_id: str
    rule_id: str
    name: str
    severity: AlertSeverity
    state: AlertState = AlertState.FIRING
    current_value: float = 0.0
    threshold_value: float = 0.0
    triggered_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    description: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None


class AlertEngine:
    """Evaluates rules, manages active alert lifecycle, and prevents alert storms."""

    def __init__(
        self,
        metric_registry: Optional[MetricRegistry] = None,
        storm_threshold_per_minute: int = 20,
    ):
        self.metric_registry = metric_registry or MetricRegistry()
        self.storm_threshold_per_minute = storm_threshold_per_minute
        self._rules: Dict[str, AlertRule] = {}
        self._active_alerts: Dict[str, ActiveAlert] = {}
        self._alert_history: List[ActiveAlert] = []
        self._on_fire_callbacks: List[Callable[[ActiveAlert], None]] = []
        self._on_resolve_callbacks: List[Callable[[ActiveAlert], None]] = []

    def add_rule(self, rule: AlertRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def list_rules(self) -> List[AlertRule]:
        return list(self._rules.values())

    def on_fire(self, callback: Callable[[ActiveAlert], None]) -> None:
        self._on_fire_callbacks.append(callback)

    def on_resolve(self, callback: Callable[[ActiveAlert], None]) -> None:
        self._on_resolve_callbacks.append(callback)

    def evaluate_metrics(self, current_metrics: Optional[Dict[str, float]] = None) -> List[ActiveAlert]:
        """Evaluate all active metric alert rules against current metric values."""
        metrics = current_metrics or {}
        if not metrics:
            snapshot = self.metric_registry.dump_snapshot()
            for k, v in snapshot["counters"].items():
                metrics[k] = v
                metrics[k.split(":")[0]] = v
            for k, v in snapshot["gauges"].items():
                metrics[k] = v
                metrics[k.split(":")[0]] = v

        fired_this_cycle: List[ActiveAlert] = []
        now = time.time()

        for rule in self._rules.values():
            if not rule.enabled or rule.condition_type != RuleConditionType.METRIC_THRESHOLD:
                continue

            current_val = metrics.get(rule.metric_name, 0.0)
            is_breached = rule.evaluate_metric(current_val)

            existing_alert = self._active_alerts.get(rule.rule_id)

            if is_breached:
                if not existing_alert:
                    # New alert firing
                    alert = ActiveAlert(
                        alert_id=f"alt-{uuid.uuid4().hex[:8]}",
                        rule_id=rule.rule_id,
                        name=rule.name,
                        severity=rule.severity,
                        state=AlertState.FIRING,
                        current_value=current_val,
                        threshold_value=rule.threshold_value,
                        triggered_at=now,
                        description=f"{rule.description} (value {current_val} {rule.operator} {rule.threshold_value})",
                        labels=rule.labels,
                    )
                    self._active_alerts[rule.rule_id] = alert
                    fired_this_cycle.append(alert)

                    # Trigger callbacks
                    for cb in self._on_fire_callbacks:
                        try:
                            cb(alert)
                        except Exception:
                            pass
            else:
                if existing_alert and existing_alert.state == AlertState.FIRING:
                    # Alert resolved
                    existing_alert.state = AlertState.RESOLVED
                    existing_alert.resolved_at = now
                    self._alert_history.append(existing_alert)
                    del self._active_alerts[rule.rule_id]

                    for cb in self._on_resolve_callbacks:
                        try:
                            cb(existing_alert)
                        except Exception:
                            pass

        return fired_this_cycle

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        for alert in self._active_alerts.values():
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                return True
        return False

    def list_active_alerts(self, min_severity: Optional[AlertSeverity] = None) -> List[ActiveAlert]:
        return list(self._active_alerts.values())

    def get_alert_history(self, limit: int = 100) -> List[ActiveAlert]:
        return self._alert_history[-limit:]
