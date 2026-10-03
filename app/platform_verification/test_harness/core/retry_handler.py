"""
Enterprise Retry Handler with Exponential Backoff and Failed Execution Preservation.
"""
from __future__ import annotations
import time
from typing import Callable
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    VerificationContext,
    HarnessExecutionResult,
)


class RetryHandler:
    """Executes operations with retry and exponential backoff, preserving failure context."""

    @staticmethod
    def execute_with_retry(
        runner_fn: Callable[[VerificationTestSpec, VerificationContext], HarnessExecutionResult],
        spec: VerificationTestSpec,
        context: VerificationContext,
    ) -> HarnessExecutionResult:
        policy = spec.retry_policy
        attempts = 0
        current_delay = policy.initial_delay_ms / 1000.0

        last_result: HarnessExecutionResult = runner_fn(spec, context)
        while not last_result.passed and attempts < policy.max_retries:
            attempts += 1
            time.sleep(current_delay)
            current_delay = min(policy.max_delay_ms / 1000.0, current_delay * policy.backoff_factor)
            last_result = runner_fn(spec, context)

        last_result.retry_attempts = attempts
        return last_result
