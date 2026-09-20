"""Model Intelligence and Usage Telemetry Analytics."""

from typing import Dict, Any, List, Optional
import collections
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class ModelUsageRecord(BaseModel):
    model_id: str
    invocations_count: int = 0
    failure_rate: float = 0.0
    avg_latency_ms: float = 0.0
    avg_risk_score: float = 0.0
    total_cost_usd: float = 0.0
    drift_signals: int = 0
    compliance_status: str = "APPROVED"


class ModelSystemAnalytics(BaseModel):
    tenant_id: str
    total_models_tracked: int = 0
    total_invocations: int = 0
    total_cost_usd: float = 0.0
    models: List[ModelUsageRecord] = Field(default_factory=list)


class ModelAnalyticsEngine:
    """Analyzes model telemetry, cost, drift, and performance across deployments."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def analyze_models(self, tenant_id: str = "*") -> ModelSystemAnalytics:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        executions = self.repo.query_ai_executions(q)

        by_model: Dict[str, List[Any]] = collections.defaultdict(list)
        for e in executions:
            if e.model_id:
                by_model[e.model_id].append(e)

        records: List[ModelUsageRecord] = []
        total_inv = 0
        total_cost = 0.0

        for mid, exec_list in by_model.items():
            cnt = len(exec_list)
            total_inv += cnt
            succ_cnt = sum(1 for e in exec_list if e.is_success)
            fail_rate = ((cnt - succ_cnt) / cnt) if cnt > 0 else 0.0
            avg_lat = sum(e.latency_ms for e in exec_list) / cnt
            avg_risk = sum(e.risk_score for e in exec_list) / cnt
            cost = sum(e.cost_usd for e in exec_list)
            total_cost += cost

            drift_cnt = sum(1 for e in exec_list if e.risk_score > 0.8 or e.latency_ms > 4000.0)

            records.append(
                ModelUsageRecord(
                    model_id=mid,
                    invocations_count=cnt,
                    failure_rate=round(fail_rate, 4),
                    avg_latency_ms=round(avg_lat, 2),
                    avg_risk_score=round(avg_risk, 4),
                    total_cost_usd=round(cost, 4),
                    drift_signals=drift_cnt,
                    compliance_status="APPROVED" if avg_risk < 0.7 else "RESTRICTED",
                )
            )

        return ModelSystemAnalytics(
            tenant_id=tenant_id,
            total_models_tracked=len(self.repo.dim_models),
            total_invocations=total_inv,
            total_cost_usd=round(total_cost, 4),
            models=records,
        )
