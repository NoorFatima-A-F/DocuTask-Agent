"""Policy Usage, Coverage, and Friction Analytics."""

from typing import Dict, Any, List, Optional
import collections
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class PolicyUsageStat(BaseModel):
    policy_id: str
    policy_name: str
    policy_type: str
    invocations_count: int = 0
    violations_count: int = 0
    exceptions_granted_count: int = 0
    friction_index: float = 0.0  # (violations + exceptions) / invocations


class PolicyIntelligenceReport(BaseModel):
    tenant_id: str
    total_policies: int = 0
    active_policies: int = 0
    total_evaluations: int = 0
    total_violations: int = 0
    overall_friction_rate: float = 0.0
    policy_usage_stats: List[PolicyUsageStat] = Field(default_factory=list)


class PolicyAnalyticsEngine:
    """Analyzes policy coverage, utilization, and friction across enterprise pipelines."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def generate_policy_intelligence(self, tenant_id: str = "*") -> PolicyIntelligenceReport:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        decisions = self.repo.query_decisions(q)
        policy_events = self.repo.query_policy_events(q)
        approvals = self.repo.query_approvals(q)

        all_pols = [p for p in self.repo.dim_policies.values() if tenant_id == "*" or p.tenant_id == tenant_id]

        # Calculate per-policy stats
        invocations: Dict[str, int] = collections.Counter(d.policy_id for d in decisions if d.policy_id)
        violations: Dict[str, int] = collections.Counter(pe.policy_id for pe in policy_events if pe.policy_id)

        usage_stats = []
        for pol in all_pols:
            inv_cnt = invocations.get(pol.policy_id, 0)
            viol_cnt = violations.get(pol.policy_id, 0)
            friction = (viol_cnt / inv_cnt) if inv_cnt > 0 else 0.0

            usage_stats.append(
                PolicyUsageStat(
                    policy_id=pol.policy_id,
                    policy_name=pol.policy_name,
                    policy_type=pol.policy_type,
                    invocations_count=inv_cnt,
                    violations_count=viol_cnt,
                    friction_index=round(friction, 4),
                )
            )

        total_evals = len(decisions)
        total_viols = len(policy_events)
        overall_friction = (total_viols / total_evals) if total_evals > 0 else 0.0

        return PolicyIntelligenceReport(
            tenant_id=tenant_id,
            total_policies=len(all_pols),
            active_policies=len(all_pols),
            total_evaluations=total_evals,
            total_violations=total_viols,
            overall_friction_rate=round(overall_friction, 4),
            policy_usage_stats=usage_stats,
        )
