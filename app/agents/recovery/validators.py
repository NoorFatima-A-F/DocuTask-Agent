"""
Recovery Fail-Fast Request Validators.
"""

from app.agents.recovery.context import RecoveryRequest
from app.agents.recovery.exceptions import RecoveryException


class RecoveryRequestValidator:
    """Fail-fast validator for recovery requests."""

    @staticmethod
    def validate_request(request: RecoveryRequest) -> None:
        if not request.failure:
            raise RecoveryException("RecoveryRequest must contain a valid Failure entity.")
        if not request.failure.identity.execution_id:
            raise RecoveryException("Failure must specify an associated execution_id.")
