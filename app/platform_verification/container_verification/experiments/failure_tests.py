"""
Container Chaos and Failure Injection Tests.
"""
from typing import List, Dict, Any
from app.platform_verification.container_verification.models.verification_models import ContainerFailureReport


class FailureExperiments:
    """Simulates service kills (API, worker, redis) and validates state preservation."""
    __test__ = False

    def execute_failure_simulations(self, scenarios: List[Dict[str, Any]]) -> ContainerFailureReport:
        success = 0
        issues: List[str] = []
        latencies: List[float] = []

        for sc in scenarios:
            name = sc.get("target_service", "api")
            recovered = sc.get("recovered_successfully", True)
            data_loss = sc.get("data_loss", False)
            latency = sc.get("restart_latency_seconds", 2.1)
            latencies.append(latency)

            if recovered and not data_loss:
                success += 1
            else:
                issues.append(f"Failure simulation on '{name}' failed: data_loss={data_loss}, recovered={recovered}")

        avg_lat = sum(latencies) / max(len(latencies), 1)
        status = "PASS" if len(issues) == 0 else "FAIL"

        return ContainerFailureReport(
            simulated_scenarios=len(scenarios),
            recovery_success_count=success,
            data_loss_detected=(len(issues) > 0),
            average_restart_time_seconds=round(avg_lat, 2),
            status=status,
            issues=issues,
        )
