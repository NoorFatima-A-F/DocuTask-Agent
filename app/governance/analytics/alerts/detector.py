"""Governance Alert Detector evaluating real-time metrics against rules."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

from .rules import AlertRule, AlertSeverity
from ..core.engine import GovernanceMetricsEngine
from ..risk.analyzer import RiskAnalyzer


class AlertEvent(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:10]}")
    rule_id: str
    tenant_id: str
    rule_name: str
    metric: str
    observed_value: float
    threshold_value: float
    severity: AlertSeverity
    message: str
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlertDetector:
    """Evaluates metrics against alert rules to trigger governance incident warnings."""

    DEFAULT_RULES: List[AlertRule] = [
        AlertRule(
            rule_id="rule_high_risk_spike",
            name="High Governance Risk Spike",
            metric="overall_risk_score",
            operator=">=",
            threshold=0.60,
            severity=AlertSeverity.CRITICAL,
        ),
        AlertRule(
            rule_id="rule_high_policy_violations",
            name="Excessive Policy Violations",
            metric="total_policy_violations",
            operator=">=",
            threshold=10.0,
            severity=AlertSeverity.HIGH,
        ),
        AlertRule(
            rule_id="rule_low_governance_score",
            name="Degraded AI Governance Health",
            metric="governance_score",
            operator="<=",
            threshold=70.0,
            severity=AlertSeverity.HIGH,
        ),
        AlertRule(
            rule_id="rule_high_block_rate",
            name="Elevated Decision Block Rate",
            metric="block_rate",
            operator=">=",
            threshold=0.25,
            severity=AlertSeverity.WARNING,
        ),
    ]

    def __init__(
        self,
        rules: Optional[List[AlertRule]] = None,
        metrics_engine: Optional[GovernanceMetricsEngine] = None,
        risk_analyzer: Optional[RiskAnalyzer] = None,
    ):
        self.rules = list(rules or self.DEFAULT_RULES)
        self.metrics = metrics_engine or GovernanceMetricsEngine()
        self.risk = risk_analyzer or RiskAnalyzer(self.metrics.repo)
        self._history: List[AlertEvent] = []

    def add_rule(self, rule: AlertRule) -> AlertRule:
        self.rules.append(rule)
        return rule

    def _eval_op(self, observed: float, op: str, threshold: float) -> bool:
        if op == ">":
            return observed > threshold
        elif op == ">=":
            return observed >= threshold
        elif op == "<":
            return observed < threshold
        elif op == "<=":
            return observed <= threshold
        elif op == "==":
            return observed == threshold
        return False

    def evaluate_alerts(self, tenant_id: str = "*") -> List[AlertEvent]:
        active_alerts: List[AlertEvent] = []

        # Gather metric lookup values
        gov_score = self.metrics.calculate_governance_score(tenant_id)
        dec_metrics = self.metrics.get_decision_metrics(tenant_id)
        pol_metrics = self.metrics.get_policy_metrics(tenant_id)
        risk_summary = self.risk.analyze_risk_posture(tenant_id)

        metric_lookup: Dict[str, float] = {
            "governance_score": gov_score,
            "overall_risk_score": risk_summary.overall_risk_score,
            "total_policy_violations": float(pol_metrics.total_policy_violations),
            "blocked_actions": float(dec_metrics.blocked_actions),
            "block_rate": dec_metrics.block_rate,
            "override_rate": dec_metrics.override_rate,
            "critical_risk_events": float(risk_summary.critical_risk_events_count),
        }

        for rule in self.rules:
            if not rule.is_active:
                continue
            if rule.tenant_id != "*" and rule.tenant_id != tenant_id:
                continue

            observed = metric_lookup.get(rule.metric)
            if observed is not None and self._eval_op(observed, rule.operator, rule.threshold):
                alert = AlertEvent(
                    rule_id=rule.rule_id,
                    tenant_id=tenant_id,
                    rule_name=rule.name,
                    metric=rule.metric,
                    observed_value=observed,
                    threshold_value=rule.threshold,
                    severity=rule.severity,
                    message=f"Alert '{rule.name}' triggered: metric '{rule.metric}' observed value {observed} {rule.operator} threshold {rule.threshold}",
                )
                active_alerts.append(alert)
                self._history.append(alert)

        return active_alerts

    def get_alert_history(self, tenant_id: Optional[str] = None) -> List[AlertEvent]:
        if tenant_id and tenant_id != "*":
            return [a for a in self._history if a.tenant_id == tenant_id]
        return list(self._history)
