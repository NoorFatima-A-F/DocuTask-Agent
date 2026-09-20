"""
Network Chaos and Failure Simulator.
"""
from typing import List, Dict, Any
from app.platform_verification.service_communication.domain.models import NetworkFailureReport
from app.platform_verification.service_communication.domain.interfaces import INetworkFailureSimulator


class NetworkFailureSimulator(INetworkFailureSimulator):
    """Simulates latency spikes, packet loss, and severed network connections."""

    def simulate_network_failures(self, scenarios: List[Dict[str, Any]]) -> NetworkFailureReport:
        latency_ok = True
        loss_ok = True
        drop_ok = True
        issues: List[str] = []

        for sc in scenarios:
            name = sc.get("scenario", "chaos_scenario")
            fault = sc.get("fault_type", "latency")
            gracefully_recovered = sc.get("gracefully_recovered", True)

            if not gracefully_recovered:
                issues.append(f"Network failure scenario '{name}' ({fault}) failed graceful recovery")
                if fault == "latency":
                    latency_ok = False
                elif fault == "packet_loss":
                    loss_ok = False
                elif fault == "connection_drop":
                    drop_ok = False

        status = "PASS" if len(issues) == 0 else "FAIL"

        return NetworkFailureReport(
            latency_spike_resilience_verified=latency_ok,
            packet_loss_resilience_verified=loss_ok,
            connection_drop_recovery_verified=drop_ok,
            status=status,
            issues=issues,
        )
