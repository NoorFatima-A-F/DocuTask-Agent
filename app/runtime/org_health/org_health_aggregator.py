"""
AMAEOP Pillar 5 - Organization Health Intelligence Aggregator
Aggregates enterprise-wide health metrics, identifies systemic bottlenecks, and projects organizational risk.
"""

from typing import Dict, List, Any
from app.runtime.organization.organizational_state import org_state_manager
from app.runtime.org_health.department_health import DepartmentHealthScorer, DepartmentHealthBreakdown


class OrgHealthAggregator:
    """Computes enterprise-level health matrix and identifies organizational bottlenecks."""

    @classmethod
    def get_organization_health_report(cls) -> Dict[str, Any]:
        depts = org_state_manager._departments.values()
        breakdowns: List[DepartmentHealthBreakdown] = [DepartmentHealthScorer.evaluate_department(d) for d in depts]

        avg_health = sum(b.composite_health_score for b in breakdowns) / len(breakdowns)
        critical_depts = [b.department_id for b in breakdowns if b.composite_health_score < 80.0]
        elevated_burnout = [b.department_id for b in breakdowns if b.burnout_risk_status != "NOMINAL"]

        # Identify primary bottleneck department
        bottleneck = max(breakdowns, key=lambda b: b.queue_congestion_penalty + b.utilization_penalty)

        return {
            "organization_health_score": round(avg_health, 1),
            "organization_health_tier": "OPTIMAL_RESILIENT" if avg_health >= 95.0 else ("STABLE" if avg_health >= 85.0 else "AT_RISK"),
            "primary_bottleneck_department": bottleneck.department_id,
            "primary_bottleneck_name": bottleneck.department_name,
            "departments_with_elevated_burnout": elevated_burnout,
            "critical_departments_count": len(critical_depts),
            "department_breakdowns": [b.to_dict() for b in breakdowns],
            "formula_documentation": "Health = 100 - UtilizationPenalty(>85%) - QueueCongestionPenalty - (ErrorRate * 20)",
        }
