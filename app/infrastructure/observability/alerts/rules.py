"""
Alert Rule Evaluation Engine.

Evaluates metric thresholds, rates-of-change, and anomalies against active AlertRules.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from app.infrastructure.observability.alerts.models import (
    AlertInstance,
    AlertRule,
    AlertStatus,
)

logger = logging.getLogger("infrastructure.observability.alerts.rules")


class AlertRuleEvaluator:
    """
    Evaluates metric values against rule criteria and emits firing or resolved AlertInstances.
    """

    def __init__(self) -> None:
        self._rules: Dict[str, AlertRule] = {}
        self._active_alerts: Dict[str, AlertInstance] = {}  # fingerprint -> AlertInstance

    def register_rule(self, rule: AlertRule) -> None:
        self._rules[rule.rule_id] = rule

    def get_rule(self, rule_id: str) -> Optional[AlertRule]:
        return self._rules.get(rule_id)

    def list_rules(self) -> List[AlertRule]:
        return list(self._rules.values())

    @staticmethod
    def _evaluate_condition(value: float, comparator: str, threshold: float) -> bool:
        if comparator == ">":
            return value > threshold
        elif comparator == ">=":
            return value >= threshold
        elif comparator == "<":
            return value < threshold
        elif comparator == "<=":
            return value <= threshold
        elif comparator in ("==", "="):
            return value == threshold
        return False

    def evaluate(
        self,
        rule_id: str,
        current_value: float,
        service_name: str = "docutask-service",
        region: str = "us-east-1",
        tenant_id: str = "global",
        labels: Optional[Dict[str, str]] = None,
    ) -> Optional[AlertInstance]:
        """
        Evaluate a metric value against a registered rule.
        """
        rule = self._rules.get(rule_id)
        if not rule or not rule.enabled:
            return None

        fingerprint = f"{rule_id}:{service_name}:{region}:{tenant_id}"
        is_breached = self._evaluate_condition(current_value, rule.comparator, rule.threshold_value)

        if is_breached:
            if fingerprint in self._active_alerts:
                # Already firing; update value
                alert = self._active_alerts[fingerprint]
                alert.current_value = current_value
                return alert

            # Create new firing alert
            alert = AlertInstance(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                severity=rule.severity,
                status=AlertStatus.FIRING,
                current_value=current_value,
                threshold_value=rule.threshold_value,
                message=f"Rule '{rule.name}' triggered: {current_value} {rule.comparator} {rule.threshold_value}",
                service_name=service_name,
                region=region,
                tenant_id=tenant_id,
                team=rule.team,
                labels={**rule.labels, **(labels or {})},
                fingerprint=fingerprint,
            )
            self._active_alerts[fingerprint] = alert
            logger.warning(f"ALERT FIRED: [{alert.severity.value}] {alert.message}")
            return alert

        else:
            # If was firing, resolve
            if fingerprint in self._active_alerts:
                alert = self._active_alerts.pop(fingerprint)
                alert.status = AlertStatus.RESOLVED
                logger.info(f"ALERT RESOLVED: {alert.rule_name} on {fingerprint}")
                return alert
            return None

    def list_active_alerts(self) -> List[AlertInstance]:
        return list(self._active_alerts.values())
