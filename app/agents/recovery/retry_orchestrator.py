"""
Retry Orchestrator.
Coordinates retry attempts, applying backoff strategies and tool/worker-specific retry policies.
"""

from app.agents.recovery.backoff import BackoffCalculator
from app.agents.recovery.retry_policy import RecoveryBackoffType, RecoveryRetryPolicy


class RetryOrchestrator:
    """Orchestrates retry decisions and computes backoff delays."""

    def __init__(self, policy: RecoveryRetryPolicy | None = None):
        self.policy = policy or RecoveryRetryPolicy()

    def should_retry(self, current_attempt: int) -> bool:
        return current_attempt < self.policy.max_retries

    def get_retry_delay(self, current_attempt: int) -> float:
        if self.policy.backoff_type == RecoveryBackoffType.IMMEDIATE:
            return 0.0
        elif self.policy.backoff_type == RecoveryBackoffType.FIXED:
            return self.policy.initial_delay_seconds
        return BackoffCalculator.calculate_exponential_backoff(
            attempt=current_attempt,
            initial_seconds=self.policy.initial_delay_seconds,
            max_seconds=self.policy.max_delay_seconds
        )
