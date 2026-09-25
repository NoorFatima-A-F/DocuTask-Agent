"""
Regional Failover & Dynamic Routing Package.
"""

from app.infrastructure.failover.planner import (
    FailoverPlan,
    FailoverScope,
    FailoverStatus,
    FailoverType,
    PreflightCheckResult,
    RegionalFailoverPlanner,
)
from app.infrastructure.failover.routing import (
    FailoverRouter,
    RouteTarget,
    ServiceRouteTable,
)
from app.infrastructure.failover.orchestrator import (
    FailoverExecutionResult,
    FailoverOrchestrator,
)

__all__ = [
    "FailoverExecutionResult",
    "FailoverOrchestrator",
    "FailoverPlan",
    "FailoverRouter",
    "FailoverScope",
    "FailoverStatus",
    "FailoverType",
    "PreflightCheckResult",
    "RegionalFailoverPlanner",
    "RouteTarget",
    "ServiceRouteTable",
]
