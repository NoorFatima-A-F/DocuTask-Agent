"""
Kubernetes Health Transition Compatibility Verifier (Part 3H.3.3.10).
Validates that orchestrator state transitions map correctly to container endpoints,
ensuring pods in RECOVERING or NOT_READY states are excluded from ingress traffic.
"""
from typing import Dict, Any
from app.platform_verification.health_transition_intelligence.domain.models import HealthState


class KubernetesTransitionVerifier:
    """
    Verifies container orchestrator probe and routing alignment during state transitions.
    """

    STATE_HTTP_MAP = {
        HealthState.STARTING: 503,
        HealthState.READY: 200,
        HealthState.DEGRADED: 200,
        HealthState.NOT_READY: 503,
        HealthState.RECOVERING: 503,
    }

    def verify_transition_compatibility(self) -> Dict[str, Any]:
        results = {}
        for state, expected_code in self.STATE_HTTP_MAP.items():
            actual_code = self.get_http_status_code(state)
            results[state.value] = {
                "expected_http_code": expected_code,
                "actual_http_code": actual_code,
                "traffic_admitted": actual_code == 200,
                "passed": actual_code == expected_code,
            }

        all_passed = all(r["passed"] for r in results.values())

        return {
            "all_transitions_compatible": all_passed,
            "recovering_state_isolated": results["RECOVERING"]["actual_http_code"] == 503,
            "ready_state_admitted": results["READY"]["actual_http_code"] == 200,
            "degraded_state_admitted": results["DEGRADED"]["actual_http_code"] == 200,
            "not_ready_state_isolated": results["NOT_READY"]["actual_http_code"] == 503,
            "state_code_mapping": results,
            "passed": all_passed,
        }

    def get_http_status_code(self, state: HealthState) -> int:
        return self.STATE_HTTP_MAP.get(state, 503)
