"""
Alert Quality & Actionable Context Validator.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import AlertQualityReport
from app.platform_verification.observability_verification.domain.interfaces import IAlertQualityValidator


class AlertQualityValidator(IAlertQualityValidator):
    """Audits alert rule actionable definitions, symptoms, probable causes, and runbook links."""

    def validate_alerts(self, alert_rules: List[Dict[str, Any]]) -> AlertQualityReport:
        unactionable: List[str] = []
        actionable_count = 0

        for alert in alert_rules:
            name = alert.get("name", "alert")
            symptoms = alert.get("has_symptoms", True)
            cause = alert.get("has_probable_cause", True)
            runbook = alert.get("has_remediation_link", True)

            if symptoms and cause and runbook:
                actionable_count += 1
            else:
                unactionable.append(f"Alert '{name}' lacks symptoms, probable cause, or runbook link")

        total = len(alert_rules)
        score = (actionable_count / max(total, 1)) * 100.0
        score = round(min(100.0, score), 2)
        status = "PASS" if len(unactionable) == 0 else "FAIL"

        return AlertQualityReport(
            total_alert_rules=total,
            actionable_alerts_count=actionable_count,
            unactionable_alerts=unactionable,
            alert_quality_score=score,
            status=status,
        )
