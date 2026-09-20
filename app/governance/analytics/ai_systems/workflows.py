"""Workflow Intelligence and Governance Bottleneck Analytics."""

from typing import Dict, Any, List, Optional
import collections
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class WorkflowAnalyticsRecord(BaseModel):
    workflow_id: str
    workflow_name: str
    executions_count: int = 0
    failure_rate: float = 0.0
    avg_duration_ms: float = 0.0
    governance_blocks_count: int = 0
    approval_delays_count: int = 0


class WorkflowSystemAnalytics(BaseModel):
    tenant_id: str
    total_workflows: int = 0
    total_executions: int = 0
    workflows: List[WorkflowAnalyticsRecord] = Field(default_factory=list)


class WorkflowAnalyticsEngine:
    """Analyzes workflow execution health, governance delays, and approval bottlenecks."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def analyze_workflows(self, tenant_id: str = "*") -> WorkflowSystemAnalytics:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        executions = self.repo.query_ai_executions(q)
        decisions = self.repo.query_decisions(q)
        approvals = self.repo.query_approvals(q)

        by_wf: Dict[str, List[Any]] = collections.defaultdict(list)
        for e in executions:
            if e.workflow_id:
                by_wf[e.workflow_id].append(e)

        records: List[WorkflowAnalyticsRecord] = []
        total_execs = 0

        for wfid, exec_list in by_wf.items():
            cnt = len(exec_list)
            total_execs += cnt
            succ_cnt = sum(1 for e in exec_list if e.is_success)
            fail_rate = ((cnt - succ_cnt) / cnt) if cnt > 0 else 0.0
            avg_dur = sum(e.latency_ms for e in exec_list) / cnt

            blocks = sum(1 for d in decisions if d.outcome == "BLOCKED")
            delays = sum(1 for a in approvals if a.turnaround_time_seconds > 1800.0)

            records.append(
                WorkflowAnalyticsRecord(
                    workflow_id=wfid,
                    workflow_name=wfid,
                    executions_count=cnt,
                    failure_rate=round(fail_rate, 4),
                    avg_duration_ms=round(avg_dur, 2),
                    governance_blocks_count=blocks,
                    approval_delays_count=delays,
                )
            )

        return WorkflowSystemAnalytics(
            tenant_id=tenant_id,
            total_workflows=len(self.repo.dim_workflows),
            total_executions=total_execs,
            workflows=records,
        )
