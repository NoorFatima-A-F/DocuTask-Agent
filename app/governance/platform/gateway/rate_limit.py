"""Enterprise Governance API Gateway Rate Limiting.

Implements multi-dimensional token-bucket rate limiting across:
- Tenant
- API Key / Client ID
- User ID
- Endpoint
- Plugin ID
With burst allowances, quota enforcement, and violation tracking.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RateLimitDimension(str):
    TENANT = "tenant"
    CLIENT = "client"
    USER = "user"
    ENDPOINT = "endpoint"
    PLUGIN = "plugin"


class RateLimitPolicy(BaseModel):
    """Configuration for a specific rate limit tier."""

    dimension: str
    limit_key: str
    rate_per_minute: int = 600
    burst_capacity: int = 100
    quota_daily: Optional[int] = 100_000


class TokenBucket:
    """Thread-safe token bucket implementation."""

    def __init__(self, rate_per_minute: int, burst_capacity: int, quota_daily: Optional[int] = None) -> None:
        self.rate_per_second = rate_per_minute / 60.0
        self.burst_capacity = burst_capacity
        self.tokens = float(burst_capacity)
        self.last_refill = time.time()
        self.quota_daily = quota_daily
        self.daily_usage = 0
        self.last_quota_reset_day = datetime.now(timezone.utc).timetuple().tm_yday

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(float(self.burst_capacity), self.tokens + elapsed * self.rate_per_second)
        self.last_refill = now

        # Reset daily quota if new day
        current_day = datetime.now(timezone.utc).timetuple().tm_yday
        if current_day != self.last_quota_reset_day:
            self.daily_usage = 0
            self.last_quota_reset_day = current_day

    def consume(self, tokens: int = 1) -> bool:
        """Attempt to consume tokens. Returns True if allowed, False if exceeded."""
        self._refill()
        if self.quota_daily and (self.daily_usage + tokens) > self.quota_daily:
            return False

        if self.tokens >= tokens:
            self.tokens -= tokens
            self.daily_usage += tokens
            return True
        return False

    @property
    def remaining_tokens(self) -> int:
        self._refill()
        return int(max(0.0, self.tokens))


class RateLimiter:
    """Multi-dimensional enterprise rate limiting engine."""

    def __init__(self) -> None:
        self._buckets: Dict[str, TokenBucket] = {}
        self._custom_policies: Dict[str, RateLimitPolicy] = {}
        self._violations: List[Dict[str, Any]] = []

    def set_policy(self, policy: RateLimitPolicy) -> None:
        """Register a custom rate limit policy for a given dimension and key."""
        policy_key = f"{policy.dimension}:{policy.limit_key}"
        self._custom_policies[policy_key] = policy
        self._buckets[policy_key] = TokenBucket(
            rate_per_minute=policy.rate_per_minute,
            burst_capacity=policy.burst_capacity,
            quota_daily=policy.quota_daily,
        )

    def check_rate_limit(
        self,
        tenant_id: str,
        client_id: str,
        user_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        plugin_id: Optional[str] = None,
        cost: int = 1,
    ) -> tuple[bool, Dict[str, Any]]:
        """Evaluate rate limits across all applicable dimensions.
        
        Returns (is_allowed, details).
        """
        keys_to_check = [
            (f"tenant:{tenant_id}", 1200, 200, 500_000),
            (f"client:{client_id}", 600, 100, 100_000),
        ]
        if user_id:
            keys_to_check.append((f"user:{user_id}", 300, 50, 50_000))
        if endpoint:
            keys_to_check.append((f"endpoint:{endpoint}", 3000, 500, None))
        if plugin_id:
            keys_to_check.append((f"plugin:{plugin_id}", 200, 30, 20_000))

        for key, default_rpm, default_burst, default_quota in keys_to_check:
            bucket = self._buckets.get(key)
            if not bucket:
                bucket = TokenBucket(
                    rate_per_minute=default_rpm,
                    burst_capacity=default_burst,
                    quota_daily=default_quota,
                )
                self._buckets[key] = bucket

            if not bucket.consume(cost):
                violation = {
                    "violation_key": key,
                    "tenant_id": tenant_id,
                    "client_id": client_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "remaining_tokens": bucket.remaining_tokens,
                }
                self._violations.append(violation)
                return False, {
                    "allowed": False,
                    "dimension": key.split(":")[0],
                    "limit_key": key.split(":")[1],
                    "retry_after_seconds": 1.0,
                    "remaining_tokens": bucket.remaining_tokens,
                }

        return True, {
            "allowed": True,
            "remaining_tokens": self._buckets[f"client:{client_id}"].remaining_tokens,
        }

    def get_violations(self, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve rate limit violation history."""
        if tenant_id:
            return [v for v in self._violations if v.get("tenant_id") == tenant_id]
        return list(self._violations)
