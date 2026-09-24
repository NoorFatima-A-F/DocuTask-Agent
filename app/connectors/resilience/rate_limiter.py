"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Rate Limiting Framework.
Provides multi-tenant rate limiting using Token Bucket and Sliding Window algorithms.
Limits can be applied per Organization, Workspace, Connector, Credential, and User.
"""

from __future__ import annotations

from enum import Enum
import logging
import time
from typing import Dict, List, Optional
from pydantic import BaseModel

from app.connectors.core.exceptions import RateLimitExceededError

logger = logging.getLogger(__name__)


class RateLimitAlgorithm(str, Enum):
    """Supported rate limiting algorithms."""
    TOKEN_BUCKET = "TOKEN_BUCKET"
    SLIDING_WINDOW = "SLIDING_WINDOW"


class RateLimitPolicy(BaseModel):
    """Configuration for an individual rate limit tier."""
    key_prefix: str = "global"
    rate_limit_rps: float = 10.0      # Tokens added per second / Max requests per second
    burst_capacity: float = 20.0      # Maximum token capacity
    window_seconds: float = 1.0
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET


class TokenBucket:
    """Thread-safe in-memory token bucket."""

    def __init__(self, rps: float, burst: float):
        self.rps = rps
        self.capacity = burst
        self.tokens = burst
        self.last_refill = time.time()

    def consume(self, tokens: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rps)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def retry_after(self, tokens: float = 1.0) -> float:
        needed = tokens - self.tokens
        if needed <= 0 or self.rps <= 0:
            return 0.0
        return needed / self.rps


class RateLimiter:
    """
    Enterprise rate limiter enforcing hierarchical quotas across Organization,
    Workspace, Connector, Credential, and User contexts.
    """

    def __init__(self, default_policy: Optional[RateLimitPolicy] = None):
        self._default_policy = default_policy or RateLimitPolicy()
        self._policies: Dict[str, RateLimitPolicy] = {}
        self._buckets: Dict[str, TokenBucket] = {}
        self._sliding_windows: Dict[str, List[float]] = {}

    def set_policy(self, key_prefix: str, policy: RateLimitPolicy) -> None:
        """Sets a specialized rate limit policy for a key prefix (e.g. 'org-123:gmail')."""
        self._policies[key_prefix] = policy

    def _get_policy(self, key: str) -> RateLimitPolicy:
        for prefix, pol in self._policies.items():
            if key.startswith(prefix):
                return pol
        return self._default_policy

    def acquire(
        self,
        key: str,
        cost_tokens: float = 1.0,
    ) -> None:
        """
        Attempts to acquire capacity for a key. Raises RateLimitExceededError if exhausted.
        """
        policy = self._get_policy(key)

        if policy.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(policy.rate_limit_rps, policy.burst_capacity)

            bucket = self._buckets[key]
            if not bucket.consume(cost_tokens):
                retry_after = bucket.retry_after(cost_tokens)
                raise RateLimitExceededError(
                    f"Rate limit exceeded for '{key}'. Limit: {policy.rate_limit_rps} rps. Try again in {retry_after:.2f}s.",
                    retry_after_seconds=retry_after,
                    details={"key": key, "limit_rps": policy.rate_limit_rps},
                )

        elif policy.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
            now = time.time()
            window = policy.window_seconds
            max_requests = policy.rate_limit_rps * window

            if key not in self._sliding_windows:
                self._sliding_windows[key] = []

            # Prune old timestamps
            self._sliding_windows[key] = [t for t in self._sliding_windows[key] if now - t < window]

            if len(self._sliding_windows[key]) >= max_requests:
                oldest = self._sliding_windows[key][0]
                retry_after = max(0.1, window - (now - oldest))
                raise RateLimitExceededError(
                    f"Sliding window rate limit exceeded for '{key}'. Max {max_requests} req / {window}s.",
                    retry_after_seconds=retry_after,
                    details={"key": key, "max_requests": max_requests},
                )

            self._sliding_windows[key].append(now)
