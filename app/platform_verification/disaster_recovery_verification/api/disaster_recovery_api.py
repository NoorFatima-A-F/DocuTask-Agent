"""
In-process REST API Router for Disaster Recovery Architecture Verification.
"""
from typing import Dict, Any
from app.platform_verification.disaster_recovery_verification.runtime.disaster_recovery_runtime import (
    DisasterRecoveryVerificationRuntime,
)
from app.platform_verification.disaster_recovery_verification.domain.models import DRScenarioType


class DisasterRecoveryApiRouter:
    """REST API endpoint handler for DR verification operations."""

    def __init__(self, runtime: DisasterRecoveryVerificationRuntime):
        self.runtime = runtime

    def handle_run_full_dr_verification(self) -> Dict[str, Any]:
        result = self.runtime.execute_full_dr_verification()
        scorecard = result["scorecard"]
        return {
            "status": "SUCCESS",
            "certification": {
                "composite_score": scorecard.composite_score,
                "tier": scorecard.certification_tier.value,
                "maturity_level": scorecard.maturity_level.value,
                "passed": scorecard.passed,
            },
            "scenarios_executed": len(result["scenarios"]),
            "artifacts_generated": list(result["evidence"].keys()),
        }

    def handle_simulate_scenario(self, scenario_str: str) -> Dict[str, Any]:
        scenario = DRScenarioType(scenario_str)
        sim_res = self.runtime.test_harness.execute_scenario(scenario)
        return {
            "scenario": sim_res.scenario.value,
            "rto_seconds": sim_res.rto_seconds,
            "rpo_seconds": sim_res.rpo_seconds,
            "data_loss_detected": sim_res.data_loss_detected,
            "status": sim_res.status,
        }
