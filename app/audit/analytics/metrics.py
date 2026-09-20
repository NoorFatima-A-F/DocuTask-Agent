"""Audit Metrics Collector."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..core.events import AuditEvent, OutcomeType, AuditSeverity
from ..storage.repository import AuditRepository


class AuditMetricsSummary(BaseModel):
    tenant_id: str
    total_events: int
    success_count: int
    failure_count: int
    error_rate: float
    high_severity_count: int
    critical_severity_count: int
    category_breakdown: Dict[str, int] = Field(default_factory=dict)
    average_risk_score: float = 0.0


class AuditMetricsCollector:
    """Aggregates audit events to compute metrics on system usage, failure spikes, and risk."""

    def __init__(self, repository: Optional[AuditRepository] = None):
        self.repository = repository or AuditRepository()

    def get_metrics_summary(self, tenant_id: str) -> AuditMetricsSummary:
        events = self.repository.list_by_tenant(tenant_id)
        if not events:
            return AuditMetricsSummary(
                tenant_id=tenant_id,
                total_events=0,
                success_count=0,
                failure_count=0,
                error_rate=0.0,
                high_severity_count=0,
                critical_severity_count=0,
            )

        total = len(events)
        successes = 0
        failures = 0
        high_sev = 0
        crit_sev = 0
        categories: Dict[str, int] = {}
        total_risk = 0.0

        for ev in events:
            # Outcome
            if ev.outcome == OutcomeType.SUCCESS:
                successes += 1
            else:
                failures += 1

            # Severity
            if ev.severity == AuditSeverity.HIGH:
                high_sev += 1
            elif ev.severity == AuditSeverity.CRITICAL:
                crit_sev += 1

            # Category
            cat_name = ev.category.value if hasattr(ev.category, "value") else str(ev.category)
            categories[cat_name] = categories.get(cat_name, 0) + 1

            total_risk += ev.risk_score

        error_rate = failures / total if total > 0 else 0.0
        avg_risk = total_risk / total if total > 0 else 0.0

        return AuditMetricsSummary(
            tenant_id=tenant_id,
            total_events=total,
            success_count=successes,
            failure_count=failures,
            error_rate=round(error_rate, 4),
            high_severity_count=high_sev,
            critical_severity_count=crit_sev,
            category_breakdown=categories,
            average_risk_score=round(avg_risk, 3),
        )
