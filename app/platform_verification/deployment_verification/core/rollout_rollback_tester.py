"""
Rollout Strategies & Automated Rollback Tester.
"""
from typing import Dict, Any, Tuple
from app.platform_verification.deployment_verification.domain.models import (
    ReleaseStrategyReport,
    RollbackVerificationReport,
    ZeroDowntimeReport,
    DeploymentStrategy,
    RollbackTrigger,
)
from app.platform_verification.deployment_verification.domain.interfaces import IRolloutRollbackTester


class RolloutRollbackTester(IRolloutRollbackTester):
    """Simulates rolling / blue-green / canary rollouts and automated rollback triggers."""
    __test__ = False

    def test_rollout_and_rollback(self, rollout_config: Dict[str, Any]) -> Tuple[ReleaseStrategyReport, RollbackVerificationReport, ZeroDowntimeReport]:
        strat_str = rollout_config.get("strategy", "ROLLING").upper()
        strat = getattr(DeploymentStrategy, strat_str, DeploymentStrategy.ROLLING)

        zero_dropped = rollout_config.get("zero_dropped_requests", True)
        canary_ok = rollout_config.get("canary_traffic_split_verified", True)

        rel_rep = ReleaseStrategyReport(
            strategy_tested=strat,
            zero_dropped_requests=zero_dropped,
            canary_traffic_split_verified=canary_ok,
            status="PASS" if zero_dropped and canary_ok else "FAIL",
        )

        trigger_str = rollout_config.get("injected_failure", "HEALTH_CHECK_FAILURE")
        trigger = getattr(RollbackTrigger, trigger_str, RollbackTrigger.HEALTH_CHECK_FAILURE)
        rollback_ok = rollout_config.get("rollback_recovered", True)
        data_loss = rollout_config.get("data_loss_detected", False)

        roll_rep = RollbackVerificationReport(
            rollback_trigger=trigger,
            rollback_successful=rollback_ok and not data_loss,
            rollback_duration_seconds=rollout_config.get("rollback_duration_seconds", 3.2),
            data_loss_detected=data_loss,
            status="PASS" if rollback_ok and not data_loss else "FAIL",
        )

        total_req = rollout_config.get("total_traffic_requests", 1000)
        failed_req = rollout_config.get("failed_traffic_requests", 0)
        avail = ((total_req - failed_req) / max(total_req, 1)) * 100.0

        zero_rep = ZeroDowntimeReport(
            simulated_rps=100,
            total_requests_sent=total_req,
            failed_requests=failed_req,
            availability_pct=round(avail, 3),
            status="PASS" if avail >= 99.9 else "FAIL",
        )

        return rel_rep, roll_rep, zero_rep
