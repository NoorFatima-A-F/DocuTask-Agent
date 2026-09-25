"""Central AI Chaos Failure Simulator and Fault Injector (3H.3.10.1)."""

from typing import Dict, Any, List
from ..domain.models import FailureInjectionScenario, ChaosScenarioType
from ..domain.interfaces import IAIFailureSimulator
from .failure_scenarios import (
    ProviderUnavailableScenario,
    LatencyInjectionScenario,
    InvalidResponseScenario,
    QuotaExhaustionScenario,
    AuthenticationFailureScenario,
    NetworkFailureScenario,
    QualityDegradationScenario,
)


class AIFailureSimulator(IAIFailureSimulator):
    """Coordinates and injects controlled faults into AI request pipelines."""

    def __init__(self):
        self._scenarios: List[FailureInjectionScenario] = [
            FailureInjectionScenario(
                scenario_id="SCENARIO-01-OUTAGE",
                scenario_type=ChaosScenarioType.PROVIDER_OUTAGE,
                description="Simulates upstream provider 503 outage and connection refusal",
                injected_fault="HTTP_503",
                target_provider="gemini-2.5-flash",
                duration_seconds=15.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-02-LATENCY",
                scenario_type=ChaosScenarioType.LATENCY_SPIKE,
                description="Simulates extreme inference latency spikes (5s, 10s, 30s)",
                injected_fault="LATENCY_SPIKE_10S",
                target_provider="gemini-2.5-flash",
                duration_seconds=20.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-03-INVALID-SCHEMA",
                scenario_type=ChaosScenarioType.INVALID_RESPONSE,
                description="Simulates broken JSON syntax, missing keys, and plain text responses",
                injected_fault="SYNTAX_ERROR",
                target_provider="gemini-2.5-flash",
                duration_seconds=10.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-04-AUTH-FAILURE",
                scenario_type=ChaosScenarioType.AUTHENTICATION_FAILURE,
                description="Simulates 401 Unauthorized credential invalidation",
                injected_fault="401_INVALID_API_KEY",
                target_provider="gemini-2.5-flash",
                duration_seconds=5.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-05-QUOTA-429",
                scenario_type=ChaosScenarioType.QUOTA_EXHAUSTION,
                description="Simulates 429 Too Many Requests rate limit bursts",
                injected_fault="HTTP_429_RATE_LIMIT",
                target_provider="gemini-2.5-flash",
                duration_seconds=15.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-06-NETWORK-DROP",
                scenario_type=ChaosScenarioType.NETWORK_FAILURE,
                description="Simulates TCP resets and TLS handshake drops",
                injected_fault="TCP_RESET",
                target_provider="gemini-2.5-flash",
                duration_seconds=10.0,
            ),
            FailureInjectionScenario(
                scenario_id="SCENARIO-07-QUALITY-DEGRADE",
                scenario_type=ChaosScenarioType.QUALITY_DEGRADATION,
                description="Simulates low confidence and hallucinated extraction outputs",
                injected_fault="LOW_CONFIDENCE_0.42",
                target_provider="gemini-2.5-flash",
                duration_seconds=15.0,
            ),
        ]

    def list_scenarios(self) -> List[FailureInjectionScenario]:
        """List all available chaos injection scenarios."""
        return self._scenarios

    def inject_fault(self, scenario: FailureInjectionScenario, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Inject the scenario's fault into the given request payload."""
        if scenario.scenario_type == ChaosScenarioType.PROVIDER_OUTAGE:
            fault_mode = scenario.parameters.get("fault_mode", "HTTP_503")
            return ProviderUnavailableScenario.execute(request_payload, fault_mode=fault_mode)

        elif scenario.scenario_type == ChaosScenarioType.LATENCY_SPIKE:
            delay_ms = scenario.parameters.get("delay_ms", 5000.0)
            threshold_ms = scenario.parameters.get("timeout_threshold_ms", 3000.0)
            return LatencyInjectionScenario.execute(
                request_payload, injected_delay_ms=delay_ms, timeout_threshold_ms=threshold_ms
            )

        elif scenario.scenario_type == ChaosScenarioType.INVALID_RESPONSE:
            corruption = scenario.parameters.get("corruption_type", "SYNTAX_ERROR")
            return InvalidResponseScenario.execute(request_payload, corruption_type=corruption)

        elif scenario.scenario_type == ChaosScenarioType.QUOTA_EXHAUSTION:
            retry_after = scenario.parameters.get("retry_after_seconds", 5)
            return QuotaExhaustionScenario.execute(request_payload, retry_after_seconds=retry_after)

        elif scenario.scenario_type == ChaosScenarioType.AUTHENTICATION_FAILURE:
            status_code = scenario.parameters.get("status_code", 401)
            return AuthenticationFailureScenario.execute(request_payload, status_code=status_code)

        elif scenario.scenario_type == ChaosScenarioType.NETWORK_FAILURE:
            fault_type = scenario.parameters.get("fault_type", "TCP_RESET")
            return NetworkFailureScenario.execute(request_payload, fault_type=fault_type)

        elif scenario.scenario_type == ChaosScenarioType.QUALITY_DEGRADATION:
            quality_fault = scenario.parameters.get("quality_fault", "LOW_CONFIDENCE")
            return QualityDegradationScenario.execute(request_payload, quality_fault=quality_fault)

        return {"success": True, "data": "Default fallback execution", "status_code": 200}
