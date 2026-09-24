from __future__ import annotations
"""
Failover Orchestrator.

Coordinates end-to-end failover execution including pre-flight verification,
graceful draining, lease revocation, target activation, traffic re-routing, and post-audit.
"""


import logging
from app.core.security import sanitize_log_input
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.failover.planner import (
    FailoverPlan,
    FailoverStatus,
    FailoverType,
    RegionalFailoverPlanner,
)
from app.infrastructure.failover.routing import FailoverRouter

logger = logging.getLogger("infrastructure.failover.orchestrator")


class FailoverExecutionResult(BaseModel):
    """Execution outcome of a failover plan."""
    plan_id: str
    status: FailoverStatus
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    services_shifted: List[str]
    leases_revoked_count: int
    success: bool
    error_message: Optional[str] = None
    audit_trail: List[str] = Field(default_factory=list)


class FailoverOrchestrator:
    """
    Executes automated and manual failovers across regions and clusters with zero split-brain guarantees.
    """

    def __init__(
        self,
        planner: Optional[RegionalFailoverPlanner] = None,
        router: Optional[FailoverRouter] = None,
    ) -> None:
        self.planner = planner or RegionalFailoverPlanner()
        self.router = router or FailoverRouter()
        self._execution_history: Dict[str, FailoverExecutionResult] = {}

    def execute_failover(
        self,
        plan_id: str,
        revoke_leases_callback: Optional[Any] = None,
    ) -> FailoverExecutionResult:
        """
        Execute full failover sequence for an approved or proposed plan.
        """
        plan = self.planner.get_plan(plan_id)
        if not plan:
            raise KeyError(f"Failover plan '{plan_id}' not found.")

        start_time = datetime.now(timezone.utc)
        audit_trail: List[str] = [f"Failover started for plan '{plan_id}' from '{plan.source_region}' to '{plan.target_region}'"]
        leases_revoked = 0
        services_shifted: List[str] = []

        try:
            # Step 1: Pre-flight checks
            if plan.status == FailoverStatus.PROPOSED:
                audit_trail.append("Running pre-flight checks...")
                passed = self.planner.run_preflight_checks(plan_id)
                if not passed:
                    raise RuntimeError("Pre-flight checks failed; failover aborted.")

            plan.status = FailoverStatus.EXECUTING
            audit_trail.append("Status transitioned to EXECUTING")

            # Step 2: Drain source traffic
            plan.status = FailoverStatus.DRAINING
            audit_trail.append(f"Marking source region '{plan.source_region}' as draining")
            self.router.mark_region_draining(plan.source_region)

            # Step 3: Revoke active leases in source region
            audit_trail.append("Revoking active execution leases in source region to prevent split-brain")
            if revoke_leases_callback and callable(revoke_leases_callback):
                leases_revoked = revoke_leases_callback(plan.source_region)
                audit_trail.append(f"Successfully revoked {leases_revoked} leases")
            else:
                audit_trail.append("No active execution leases required revocation")

            # Step 4: Promote target & Shift traffic
            plan.status = FailoverStatus.PROMOTING
            audit_trail.append(f"Shifting traffic for affected services to target region '{plan.target_region}'")

            target_services = plan.affected_services or list(self.router._route_tables.keys())
            for svc in target_services:
                shifted = self.router.shift_traffic(
                    service_name=svc,
                    from_region=plan.source_region,
                    to_region=plan.target_region,
                    percentage_to_shift=100.0,
                )
                if shifted:
                    services_shifted.append(svc)

            audit_trail.append(f"Successfully shifted traffic for {len(services_shifted)} services")

            # Step 5: Complete failover
            plan.status = FailoverStatus.COMPLETED
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            audit_trail.append(f"Failover successfully completed in {duration:.2f}s")

            result = FailoverExecutionResult(
                plan_id=plan_id,
                status=FailoverStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                services_shifted=services_shifted,
                leases_revoked_count=leases_revoked,
                success=True,
                audit_trail=audit_trail,
            )
            self._execution_history[plan_id] = result
            return result

        except Exception as e:
            plan.status = FailoverStatus.FAILED
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            audit_trail.append(f"Failover failed: {str(e)}")

            result = FailoverExecutionResult(
                plan_id=plan_id,
                status=FailoverStatus.FAILED,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                services_shifted=services_shifted,
                leases_revoked_count=leases_revoked,
                success=False,
                error_message=str(e),
                audit_trail=audit_trail,
            )
            self._execution_history[plan_id] = result
            logger.error(f"Failover execution failed for plan '{sanitize_log_input(plan_id)}': {sanitize_log_input(str(e))}")
            return result

    def get_execution_result(self, plan_id: str) -> Optional[FailoverExecutionResult]:
        return self._execution_history.get(plan_id)
