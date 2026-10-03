"""
Tests for Regional Failover Planning, Traffic Shifting, and Failover Orchestration.
"""

from app.infrastructure.failover.planner import (
    FailoverStatus,
    FailoverType,
    RegionalFailoverPlanner,
)
from app.infrastructure.failover.routing import (
    FailoverRouter,
    RouteTarget,
)
from app.infrastructure.failover.orchestrator import (
    FailoverOrchestrator,
)


def test_regional_failover_planner_preflight_success():
    planner = RegionalFailoverPlanner()
    plan = planner.create_plan(
        plan_id="plan-us-east-failover",
        source_region="us-east-1",
        target_region="us-west-2",
        failover_type=FailoverType.AUTOMATIC,
        affected_services=["api-gateway", "ocr-service"],
        affected_tenants=["tenant-alpha"],
    )

    assert plan.status == FailoverStatus.PROPOSED

    # Run passing preflight checks
    passed = planner.run_preflight_checks(
        plan_id="plan-us-east-failover",
        target_region_healthy=True,
        target_capacity_headroom_percent=40.0,
        data_residency_compliant=True,
        replication_lag_seconds=3.0,
    )

    assert passed
    assert plan.status == FailoverStatus.APPROVED
    assert len(plan.preflight_checks) == 4


def test_regional_failover_planner_preflight_failure():
    planner = RegionalFailoverPlanner()
    plan = planner.create_plan(
        plan_id="plan-eu-failover",
        source_region="eu-west-1",
        target_region="ap-southeast-1",
        affected_tenants=["tenant-gdpr"],
    )

    # Fail on data residency compliance (GDPR violated if moved to AP)
    passed = planner.run_preflight_checks(
        plan_id="plan-eu-failover",
        target_region_healthy=True,
        target_capacity_headroom_percent=50.0,
        data_residency_compliant=False,
    )

    assert not passed
    assert plan.status == FailoverStatus.FAILED


def test_failover_router_traffic_shift():
    router = FailoverRouter()

    t_east = RouteTarget(target_id="target-east", region_id="us-east-1", weight=100.0)
    t_west = RouteTarget(target_id="target-west", region_id="us-west-2", weight=0.0)

    router.register_service_route(service_name="ocr-service", targets=[t_east, t_west])

    # Initial routing points to east
    target = router.route_request("ocr-service")
    assert target.region_id == "us-east-1"

    # Shift 100% traffic to west
    shifted = router.shift_traffic(
        service_name="ocr-service",
        from_region="us-east-1",
        to_region="us-west-2",
        percentage_to_shift=100.0,
    )
    assert shifted
    assert t_east.draining
    assert t_east.weight == 0.0
    assert t_west.weight == 100.0

    # Next request routes to west
    target_after = router.route_request("ocr-service")
    assert target_after.region_id == "us-west-2"


def test_failover_orchestrator_execution():
    planner = RegionalFailoverPlanner()
    router = FailoverRouter()
    orchestrator = FailoverOrchestrator(planner=planner, router=router)

    # Setup routes
    t_east = RouteTarget(target_id="t1", region_id="us-east-1", weight=100.0)
    t_west = RouteTarget(target_id="t2", region_id="us-west-2", weight=0.0)
    router.register_service_route(service_name="workflow-service", targets=[t_east, t_west])

    plan = planner.create_plan(
        plan_id="plan-auto-01",
        source_region="us-east-1",
        target_region="us-west-2",
        affected_services=["workflow-service"],
    )

    revoked_called = []

    def mock_revoke_leases(region_id: str):
        revoked_called.append(region_id)
        return 5

    res = orchestrator.execute_failover(
        plan_id="plan-auto-01",
        revoke_leases_callback=mock_revoke_leases,
    )

    assert res.success
    assert res.status == FailoverStatus.COMPLETED
    assert res.leases_revoked_count == 5
    assert revoked_called == ["us-east-1"]
    assert "workflow-service" in res.services_shifted
    assert plan.status == FailoverStatus.COMPLETED
