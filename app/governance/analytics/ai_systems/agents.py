"""Agent Intelligence and Performance Analytics."""

from typing import Dict, Any, List, Optional
import collections
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class AgentPerformanceRecord(BaseModel):
    agent_id: str
    agent_name: str
    total_invocations: int = 0
    success_rate: float = 1.0
    failure_rate: float = 0.0
    avg_risk_score: float = 0.0
    human_intervention_rate: float = 0.0
    total_cost_usd: float = 0.0
    avg_latency_ms: float = 0.0


class AgentSystemAnalytics(BaseModel):
    tenant_id: str
    total_agents: int = 0
    active_agents: int = 0
    total_executions: int = 0
    overall_agent_success_rate: float = 1.0
    agent_records: List[AgentPerformanceRecord] = Field(default_factory=list)


class AgentAnalyticsEngine:
    """Calculates agent workforce activity, reliability, and human intervention rates."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def analyze_agents(self, tenant_id: str = "*") -> AgentSystemAnalytics:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        executions = self.repo.query_ai_executions(q)
        approvals = self.repo.query_approvals(q)

        by_agent: Dict[str, List[Any]] = collections.defaultdict(list)
        for e in executions:
            if e.agent_id:
                by_agent[e.agent_id].append(e)

        records: List[AgentPerformanceRecord] = []
        total_execs = 0
        total_successes = 0

        for aid, exec_list in by_agent.items():
            cnt = len(exec_list)
            total_execs += cnt
            success_cnt = sum(1 for e in exec_list if e.is_success)
            total_successes += success_cnt
            fail_cnt = cnt - success_cnt

            succ_rate = (success_cnt / cnt) if cnt > 0 else 1.0
            fail_rate = (fail_cnt / cnt) if cnt > 0 else 0.0
            avg_risk = sum(e.risk_score for e in exec_list) / cnt
            avg_latency = sum(e.latency_ms for e in exec_list) / cnt
            cost = sum(e.cost_usd for e in exec_list)

            # Approvals associated with this tenant/agent
            intv_cnt = sum(1 for a in approvals if a.tenant_id == tenant_id or tenant_id == "*")
            intv_rate = min(1.0, (intv_cnt / cnt)) if cnt > 0 else 0.0

            records.append(
                AgentPerformanceRecord(
                    agent_id=aid,
                    agent_name=aid,
                    total_invocations=cnt,
                    success_rate=round(succ_rate, 4),
                    failure_rate=round(fail_rate, 4),
                    avg_risk_score=round(avg_risk, 4),
                    human_intervention_rate=round(intv_rate, 4),
                    total_cost_usd=round(cost, 4),
                    avg_latency_ms=round(avg_latency, 2),
                )
            )

        overall_succ = (total_successes / total_execs) if total_execs > 0 else 1.0

        return AgentSystemAnalytics(
            tenant_id=tenant_id,
            total_agents=len(self.repo.dim_agents),
            active_agents=len(records),
            total_executions=total_execs,
            overall_agent_success_rate=round(overall_succ, 4),
            agent_records=records,
        )
