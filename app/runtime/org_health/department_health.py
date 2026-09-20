"""
AMAEOP Pillar 5 - Department Health Scorer
Calculates granular health scores (0-100%) factoring worker utilization, queue congestion, latency variance, and error rates.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from app.runtime.organization.department import Department


@dataclass
class DepartmentHealthBreakdown:
    department_id: str
    department_name: str
    composite_health_score: float  # 0.0 - 100.0
    utilization_penalty: float
    queue_congestion_penalty: float
    error_rate_penalty: float
    sla_breach_risk: float  # 0.0 - 1.0
    burnout_risk_status: str  # NOMINAL | ELEVATED | CRITICAL_BURNOUT
    is_throttling_recommended: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DepartmentHealthScorer:
    """Computes transparent, mathematically grounded health diagnostics per department."""

    @classmethod
    def evaluate_department(cls, dept: Department) -> DepartmentHealthBreakdown:
        # 1. Utilization penalty: penalize > 85% utilization
        util = dept.kpis.resource_utilization_pct
        util_pen = max(0.0, (util - 85.0) * 0.5) if util > 85.0 else 0.0

        # 2. Queue congestion penalty
        queue_ratio = dept.queue_depth / max(1, dept.concurrency_limit)
        queue_pen = min(15.0, queue_ratio * 4.0)

        # 3. Error rate penalty
        err_pen = min(20.0, dept.kpis.error_rate_pct * 3.0)

        # Composite score
        base_score = 100.0 - util_pen - queue_pen - err_pen
        composite = round(max(0.0, min(100.0, base_score)), 1)

        # Burnout risk
        if util > 90.0 and queue_ratio > 1.0:
            burnout = "CRITICAL_BURNOUT"
        elif util > 80.0 or queue_ratio > 0.5:
            burnout = "ELEVATED"
        else:
            burnout = "NOMINAL"

        sla_risk = round(min(1.0, max(0.0, (100.0 - dept.kpis.sla_compliance_pct) / 10.0 + queue_ratio * 0.1)), 2)

        return DepartmentHealthBreakdown(
            department_id=dept.department_id,
            department_name=dept.name,
            composite_health_score=composite,
            utilization_penalty=round(util_pen, 1),
            queue_congestion_penalty=round(queue_pen, 1),
            error_rate_penalty=round(err_pen, 1),
            sla_breach_risk=sla_risk,
            burnout_risk_status=burnout,
            is_throttling_recommended=composite < 80.0,
        )
