"""Audit Dashboard Summaries."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from .metrics import AuditMetricsCollector, AuditMetricsSummary


class AuditDashboardSummary(BaseModel):
    tenant_id: str
    metrics: AuditMetricsSummary
    recent_critical_events: List[Dict[str, Any]] = Field(default_factory=list)
    compliance_health_score: float = 100.0


class AuditDashboardService:
    """Provides dashboard aggregations for SecOps and Compliance teams."""

    def __init__(self, metrics_collector: Optional[AuditMetricsCollector] = None):
        self.metrics_collector = metrics_collector or AuditMetricsCollector()

    def get_dashboard(self, tenant_id: str) -> AuditDashboardSummary:
        metrics = self.metrics_collector.get_metrics_summary(tenant_id)
        events = self.metrics_collector.repository.list_by_tenant(tenant_id)
        
        critical_events = [
            e.model_dump(mode="json") for e in events
            if e.severity.value in ["HIGH", "CRITICAL"]
        ][:10]

        # Calculate compliance health score (deducting points for critical errors)
        health = max(0.0, 100.0 - (metrics.critical_severity_count * 15.0) - (metrics.high_severity_count * 5.0))

        return AuditDashboardSummary(
            tenant_id=tenant_id,
            metrics=metrics,
            recent_critical_events=critical_events,
            compliance_health_score=round(health, 1),
        )
