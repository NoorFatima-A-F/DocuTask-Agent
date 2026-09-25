from __future__ import annotations
"""
Regional Failover Planner.

Generates and validates automated and manual failover plans, verifying target region
capacity headroom, data residency boundaries, tenant isolation, and dependency readiness.
"""


import enum
import logging
from app.core.security import sanitize_log_input
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.failover.planner")


class FailoverType(str, enum.Enum):
    """Type of failover operation."""
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"
    DRILL = "DRILL"
    PLANNED_MAINTENANCE = "PLANNED_MAINTENANCE"


class FailoverScope(str, enum.Enum):
    """Scope of failure domain to fail over."""
    COMPONENT = "COMPONENT"
    CLUSTER = "CLUSTER"
    ZONE = "ZONE"
    REGION = "REGION"


class FailoverStatus(str, enum.Enum):
    """Lifecycle status of a failover operation."""
    PROPOSED = "PROPOSED"
    VALIDATING = "VALIDATING"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    DRAINING = "DRAINING"
    PROMOTING = "PROMOTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class PreflightCheckResult(BaseModel):
    """Result of pre-flight validation check."""
    check_name: str
    passed: bool
    details: str
    blocking: bool = True


class FailoverPlan(BaseModel):
    """Detailed migration and failover plan."""
    plan_id: str
    failover_type: FailoverType
    scope: FailoverScope
    source_region: str
    target_region: str
    status: FailoverStatus = FailoverStatus.PROPOSED
    affected_services: List[str] = Field(default_factory=list)
    affected_tenants: List[str] = Field(default_factory=list)
    preflight_checks: List[PreflightCheckResult] = Field(default_factory=list)
    estimated_duration_seconds: float = Field(default=60.0)
    allow_data_loss: bool = False
    initiated_by: str = "system"
    reason: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RegionalFailoverPlanner:
    """
    Evaluates candidate target regions, checks compliance & capacity,
    and produces executable FailoverPlans.
    """

    def __init__(self) -> None:
        self._plans: Dict[str, FailoverPlan] = {}

    def create_plan(
        self,
        plan_id: str,
        source_region: str,
        target_region: str,
        failover_type: FailoverType = FailoverType.AUTOMATIC,
        scope: FailoverScope = FailoverScope.REGION,
        affected_services: Optional[List[str]] = None,
        affected_tenants: Optional[List[str]] = None,
        reason: str = "Unhealthy source region",
        initiated_by: str = "system",
        allow_data_loss: bool = False,
    ) -> FailoverPlan:
        """Create a new failover plan."""
        plan = FailoverPlan(
            plan_id=plan_id,
            failover_type=failover_type,
            scope=scope,
            source_region=source_region,
            target_region=target_region,
            status=FailoverStatus.PROPOSED,
            affected_services=affected_services or [],
            affected_tenants=affected_tenants or [],
            reason=reason,
            initiated_by=initiated_by,
            allow_data_loss=allow_data_loss,
        )
        self._plans[plan_id] = plan
        return plan

    def run_preflight_checks(
        self,
        plan_id: str,
        target_region_healthy: bool = True,
        target_capacity_headroom_percent: float = 35.0,
        data_residency_compliant: bool = True,
        replication_lag_seconds: float = 5.0,
        max_acceptable_lag_seconds: float = 30.0,
    ) -> bool:
        """Run pre-flight checks before approving a plan."""
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"Failover plan '{sanitize_log_input(plan_id)}' not found.")

        plan.status = FailoverStatus.VALIDATING
        checks: List[PreflightCheckResult] = []

        # 1. Target region health
        checks.append(
            PreflightCheckResult(
                check_name="target_region_health",
                passed=target_region_healthy,
                details=f"Target region '{plan.target_region}' health is {'OK' if target_region_healthy else 'FAILED'}",
                blocking=True,
            )
        )

        # 2. Target capacity headroom (> 20% required)
        has_capacity = target_capacity_headroom_percent >= 20.0
        checks.append(
            PreflightCheckResult(
                check_name="target_capacity_headroom",
                passed=has_capacity,
                details=f"Target region headroom: {target_capacity_headroom_percent}% (min 20% required)",
                blocking=True,
            )
        )

        # 3. Data residency & compliance
        checks.append(
            PreflightCheckResult(
                check_name="data_residency_compliance",
                passed=data_residency_compliant,
                details=f"Data residency compliance check for tenants {plan.affected_tenants}: {'PASS' if data_residency_compliant else 'FAIL'}",
                blocking=True,
            )
        )

        # 4. Replication lag vs RPO
        lag_ok = replication_lag_seconds <= max_acceptable_lag_seconds or plan.allow_data_loss
        checks.append(
            PreflightCheckResult(
                check_name="replication_lag_within_rpo",
                passed=lag_ok,
                details=f"Replication lag is {replication_lag_seconds}s (max {max_acceptable_lag_seconds}s)",
                blocking=not plan.allow_data_loss,
            )
        )

        plan.preflight_checks = checks
        all_passed = all(c.passed for c in checks if c.blocking)

        if all_passed:
            plan.status = FailoverStatus.APPROVED
            logger.info("Failover plan '%s' passed preflight checks and is APPROVED.", sanitize_log_input(plan_id))
        else:
            plan.status = FailoverStatus.FAILED
            logger.warning("Failover plan '%s' failed preflight checks.", sanitize_log_input(plan_id))

        return all_passed

    def get_plan(self, plan_id: str) -> Optional[FailoverPlan]:
        return self._plans.get(plan_id)

    def list_plans(self) -> List[FailoverPlan]:
        return list(self._plans.values())
