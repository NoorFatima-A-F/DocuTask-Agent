"""
Enterprise Workflow Retry Engine.
Supports Fixed, Linear, Exponential backoff with jitter, retry budgets, and error categorization.
"""

import math
import random
from typing import Any, Dict, Optional
from ..domain.exceptions import WorkflowValidationException


class RetryEngine:
    """Calculates backoff delays and decides if an error is retryable."""

    NON_RETRYABLE_ERROR_CODES = {
        "VALIDATION_FAILED",
        "PERMISSION_DENIED",
        "INVALID_INPUT",
        "UNAUTHORIZED",
        "QUOTA_EXCEEDED",
    }

    @classmethod
    def is_retryable(cls, error: Exception, error_code: Optional[str] = None) -> bool:
        """Check if an error qualifies for automated retry."""
        code = error_code or getattr(error, "error_code", None)
        if code and code in cls.NON_RETRYABLE_ERROR_CODES:
            return False
        return True

    @classmethod
    def calculate_delay(
        cls,
        attempt: int,
        policy: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Calculate delay in seconds for next retry attempt."""
        pol = policy or {}
        strategy = pol.get("backoff", "exponential")
        base_delay = float(pol.get("base_delay_seconds", 1.0))
        max_delay = float(pol.get("max_delay_seconds", 60.0))
        jitter = bool(pol.get("jitter", True))

        if strategy == "fixed":
            delay = base_delay
        elif strategy == "linear":
            delay = base_delay * attempt
        else:  # exponential
            delay = base_delay * (2 ** (attempt - 1))

        delay = min(delay, max_delay)

        if jitter:
            delay = delay * (0.5 + random.random() * 0.5)

        return round(delay, 3)
