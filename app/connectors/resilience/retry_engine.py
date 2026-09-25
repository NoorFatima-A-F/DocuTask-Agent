"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Retry Framework.
Provides failure classification, exponential backoff with full jitter, retry budgets, and error categorization.
"""

from __future__ import annotations

from enum import Enum
import logging
import random
import time
from typing import Any, Callable, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ConnectorFailureCategory(str, Enum):
    """Categorization of connector and external API failures."""
    TEMPORARY = "TEMPORARY"          # 503, 504, connection reset -> Retryable
    NETWORK = "NETWORK"              # DNS resolution, socket timeout -> Retryable
    RATE_LIMIT = "RATE_LIMIT"        # 429 Too Many Requests -> Retryable with backoff
    AUTHENTICATION = "AUTHENTICATION"# 401, 403, expired token -> Refresh auth / Non-retryable
    VALIDATION = "VALIDATION"        # 400 Bad Request, schema error -> Non-retryable
    PERMANENT = "PERMANENT"          # 404 Not Found, 410 Gone -> Non-retryable
    EXTERNAL_FAILURE = "EXTERNAL_FAILURE" # 500 Internal Error -> Conditionally retryable


class RetryPolicy(BaseModel):
    """Configuration governing retry behavior for an action or connector."""
    max_attempts: int = 3
    initial_interval_seconds: float = 0.5
    backoff_multiplier: float = 2.0
    max_interval_seconds: float = 30.0
    jitter: bool = True
    retryable_categories: List[ConnectorFailureCategory] = Field(
        default_factory=lambda: [
            ConnectorFailureCategory.TEMPORARY,
            ConnectorFailureCategory.NETWORK,
            ConnectorFailureCategory.RATE_LIMIT,
        ]
    )


class ConnectorRetryEngine:
    """
    Classifies connector exceptions and orchestrates backoff calculations.
    """

    def __init__(self, default_policy: Optional[RetryPolicy] = None):
        self._default_policy = default_policy or RetryPolicy()

    def classify_error(self, error: Exception | str) -> ConnectorFailureCategory:
        """Classifies an error string or exception into a standard failure category."""
        msg = str(error).lower()

        if "429" in msg or "rate limit" in msg or "too many requests" in msg:
            return ConnectorFailureCategory.RATE_LIMIT
        elif "401" in msg or "403" in msg or "unauthorized" in msg or "forbidden" in msg or "auth" in msg:
            return ConnectorFailureCategory.AUTHENTICATION
        elif "400" in msg or "validation" in msg or "invalid" in msg or "schema" in msg:
            return ConnectorFailureCategory.VALIDATION
        elif "404" in msg or "not found" in msg or "deprecated" in msg:
            return ConnectorFailureCategory.PERMANENT
        elif "timeout" in msg or "connection refused" in msg or "socket" in msg or "network" in msg or "reset" in msg:
            return ConnectorFailureCategory.NETWORK
        elif "503" in msg or "502" in msg or "504" in msg or "service unavailable" in msg:
            return ConnectorFailureCategory.TEMPORARY
        return ConnectorFailureCategory.EXTERNAL_FAILURE

    def calculate_delay(self, attempt: int, policy: Optional[RetryPolicy] = None) -> float:
        """Calculates backoff delay in seconds for the given attempt index (1-based)."""
        pol = policy or self._default_policy
        delay = pol.initial_interval_seconds * (pol.backoff_multiplier ** (attempt - 1))
        delay = min(delay, pol.max_interval_seconds)

        if pol.jitter:
            delay = random.uniform(delay * 0.5, delay * 1.5)

        return delay

    def should_retry(self, category: ConnectorFailureCategory, attempt: int, policy: Optional[RetryPolicy] = None) -> bool:
        """Determines whether a retry should be attempted."""
        pol = policy or self._default_policy
        if attempt >= pol.max_attempts:
            return False
        return category in pol.retryable_categories

    def execute_with_retry(
        self,
        func: Callable[[], Any],
        policy: Optional[RetryPolicy] = None,
        on_retry: Optional[Callable[[int, Exception, float], None]] = None,
    ) -> Any:
        """Executes a callable with classified backoff retry protection."""
        pol = policy or self._default_policy
        attempt = 1

        while True:
            try:
                return func()
            except Exception as e:
                cat = self.classify_error(e)
                if not self.should_retry(cat, attempt, pol):
                    raise

                delay = self.calculate_delay(attempt, pol)
                logger.warning(f"Connector failure (attempt {attempt}/{pol.max_attempts}, category={cat.value}). Retrying in {delay:.2f}s...")

                if on_retry:
                    on_retry(attempt, e, delay)

                time.sleep(delay)
                attempt += 1
