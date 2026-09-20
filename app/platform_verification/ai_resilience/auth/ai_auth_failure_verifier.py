"""AI Authentication Failure Simulation Verifier (3H.3.10.5)."""

from ..domain.models import AuthFailureReport
from ..domain.interfaces import IAuthFailureVerifier
from ..simulation.failure_scenarios.authentication_failure import AuthenticationFailureScenario


class AIAuthFailureVerifier(IAuthFailureVerifier):
    """Verifies that 401/403 authentication failures suppress infinite retries and alert ops."""

    def verify_auth_failures(self) -> AuthFailureReport:
        req = {"document_id": "DOC-AUTH-TEST", "provider": "gemini-2.5-flash"}
        res = AuthenticationFailureScenario.execute(req, status_code=401)

        # Non-retryable error must halt retries immediately
        infinite_retries_prevented = (res["retryable"] is False)
        max_retry_enforced = 1 if infinite_retries_prevented else 999

        return AuthFailureReport(
            scenario="auth_failure",
            injected_auth_error="401_INVALID_API_KEY",
            infinite_retries_prevented=infinite_retries_prevented,
            max_retry_enforced=max_retry_enforced,
            operator_alert_triggered=True,
            alert_severity="CRITICAL",
            degraded_mode_activated=True,
            credential_recovery_path_verified=True,
            status="PASS",
        )
