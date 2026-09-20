"""Retry Policy Engine with Exponential Backoff and Jitter."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional, Set

from ..mesh.data_plane import MeshRequest, MeshResponse


class BackoffStrategy(str, Enum):
    FIXED = "FIXED"
    EXPONENTIAL = "EXPONENTIAL"
    FULL_JITTER = "FULL_JITTER"


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_backoff_ms: float = 50.0
    max_backoff_ms: float = 2000.0
    backoff_multiplier: float = 2.0
    retryable_status_codes: Set[int] = field(default_factory=lambda: {429, 502, 503, 504})
    backoff_strategy: BackoffStrategy = BackoffStrategy.FULL_JITTER


class RetryPolicyEngine:
    """Executes calls with configurable retry strategies and jitter calculation."""

    def __init__(self, default_policy: Optional[RetryPolicy] = None):
        self.default_policy = default_policy or RetryPolicy()

    def calculate_backoff(self, attempt: int, policy: Optional[RetryPolicy] = None) -> float:
        """Calculate backoff duration in milliseconds for a given attempt index (1-based)."""
        pol = policy or self.default_policy
        if attempt <= 1:
            base = pol.initial_backoff_ms
        else:
            base = min(pol.max_backoff_ms, pol.initial_backoff_ms * (pol.backoff_multiplier ** (attempt - 1)))

        if pol.backoff_strategy == BackoffStrategy.FIXED:
            return pol.initial_backoff_ms
        elif pol.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            return base
        else:  # FULL_JITTER
            return random.uniform(0, base)

    def execute_with_retry(
        self,
        request: MeshRequest,
        operation_fn: Callable[[MeshRequest], MeshResponse],
        policy: Optional[RetryPolicy] = None,
    ) -> MeshResponse:
        """Execute request and retry on retryable failure status codes."""
        pol = policy or self.default_policy
        attempt = 1
        last_response: Optional[MeshResponse] = None

        while attempt <= pol.max_attempts:
            try:
                response = operation_fn(request)
                last_response = response

                # If status code is not retryable or is successful, return immediately
                if response.status_code not in pol.retryable_status_codes:
                    return response

                # If we reached maximum attempts, break and return last response
                if attempt >= pol.max_attempts:
                    return response

                # Otherwise sleep backoff (or simulate delay)
                delay_ms = self.calculate_backoff(attempt, pol)
                time.sleep(delay_ms / 1000.0)
            except Exception as ex:
                if attempt >= pol.max_attempts:
                    return MeshResponse(
                        status_code=503,
                        error_message=f"Request failed after {attempt} attempts: {str(ex)}",
                        request_id=request.request_id,
                    )
                delay_ms = self.calculate_backoff(attempt, pol)
                time.sleep(delay_ms / 1000.0)

            attempt += 1

        return last_response or MeshResponse(status_code=500, error_message="Retry exhausted", request_id=request.request_id)
