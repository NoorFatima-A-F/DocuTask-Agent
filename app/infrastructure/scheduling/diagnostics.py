"""Scheduling Diagnostics, Decision Records, and Explainable Placement."""

from datetime import datetime, timezone
import secrets
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.scheduling.scoring import ScoreBreakdown


class SchedulingDecision(BaseModel):
    """Immutable audit record detailing the exact scheduling placement outcome."""

    decision_id: str = Field(default_factory=lambda: f"dec_{secrets.token_hex(8)}")
    workload_id: str
    is_scheduled: bool
    selected_region: Optional[str] = None
    selected_cluster: Optional[str] = None
    selected_worker: Optional[str] = None
    candidate_count: int = 0
    rejected_candidates: Dict[str, List[str]] = Field(default_factory=dict)  # worker_id -> rejection reasons
    rejection_reasons: List[str] = Field(default_factory=list)               # high-level rejection reasons
    score_breakdown: Optional[ScoreBreakdown] = None
    reservation_id: Optional[str] = None
    execution_lease_id: Optional[str] = None
    decision_latency_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SchedulerDiagnosticsReport(BaseModel):
    """Comprehensive diagnostic snapshot explaining scheduling status."""

    workload_id: str
    state: str
    is_scheduled: bool
    selected_placement: Optional[Dict[str, str]] = None
    eligible_regions_count: int = 0
    eligible_clusters_count: int = 0
    candidate_workers_count: int = 0
    rejected_workers_breakdown: Dict[str, List[str]] = Field(default_factory=dict)
    blocking_reasons: List[str] = Field(default_factory=list)
    last_decision: Optional[SchedulingDecision] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SchedulerDiagnosticsService:
    """Produces explainable diagnostic reports for scheduling decisions and backlog items."""

    def __init__(self) -> None:
        self._decisions: Dict[str, List[SchedulingDecision]] = {}  # workload_id -> list of decisions

    def record_decision(self, decision: SchedulingDecision) -> None:
        if decision.workload_id not in self._decisions:
            self._decisions[decision.workload_id] = []
        self._decisions[decision.workload_id].append(decision)

    def get_latest_decision(self, workload_id: str) -> Optional[SchedulingDecision]:
        decisions = self._decisions.get(workload_id, [])
        return decisions[-1] if decisions else None

    def generate_diagnostics_report(
        self,
        workload_id: str,
        state: str,
        eligible_regions_count: int = 0,
        eligible_clusters_count: int = 0,
        candidate_workers_count: int = 0,
        blocking_reasons: Optional[List[str]] = None,
    ) -> SchedulerDiagnosticsReport:
        """Construct an explainable diagnostic report."""
        last_decision = self.get_latest_decision(workload_id)
        selected_placement = None
        if last_decision and last_decision.is_scheduled:
            selected_placement = {
                "region": last_decision.selected_region or "",
                "cluster": last_decision.selected_cluster or "",
                "worker": last_decision.selected_worker or "",
            }

        rejected = last_decision.rejected_candidates if last_decision else {}
        reasons = list(blocking_reasons or [])
        if last_decision and not last_decision.is_scheduled:
            reasons.extend(last_decision.rejection_reasons)

        return SchedulerDiagnosticsReport(
            workload_id=workload_id,
            state=state,
            is_scheduled=last_decision.is_scheduled if last_decision else False,
            selected_placement=selected_placement,
            eligible_regions_count=eligible_regions_count,
            eligible_clusters_count=eligible_clusters_count,
            candidate_workers_count=candidate_workers_count,
            rejected_workers_breakdown=rejected,
            blocking_reasons=reasons,
            last_decision=last_decision,
        )
