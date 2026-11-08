"""Fixed-window rate limiting.

* Client IP: the TCP peer, unless the peer is in ``TRUSTED_PROXIES``; then the right-most
  ``X-Forwarded-For`` hop that is not a trusted proxy. Left-most XFF values are client-controlled
  and never used, so spoofing the header does not change the bucket.
* Buckets: every ``/api/`` request counts against ``RATE_LIMIT_PER_MINUTE`` per IP. Auth
  endpoints have stricter per-IP limits plus a per-account limit (login), so neither rotating
  usernames from one IP nor spreading attempts on one account across IPs bypasses them.
* Storage: Redis (shared across processes) when ``REDIS_URL`` is set, else a bounded in-process
  LRU. If Redis errors, the in-process store is used for that request and a warning is logged.
"""

from __future__ import annotations

import ipaddress
import json
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Protocol

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import settings
from app.core.logging import logger
from app.schemas.response import APIResponse

API = settings.API_V1_STR


@dataclass(frozen=True)
class Limit:
    requests: int
    window_seconds: int


#: Per-IP limits for auth endpoints (stricter than the general API limit).
AUTH_IP_LIMITS: dict[str, Limit] = {
    f"{API}/auth/login": Limit(10, 60),
    f"{API}/auth/register": Limit(5, 60),
    f"{API}/auth/refresh": Limit(30, 60),
}
#: Per-account limit on login attempts, independent of IP.
LOGIN_ACCOUNT_LIMIT = Limit(5, 60)


class CounterStore(Protocol):
    async def hit(self, key: str, window_seconds: int) -> tuple[int, int]:
        """Count a hit; return ``(count_in_window, seconds_until_reset)``."""


class MemoryStore:
    """Fixed-window counters in a bounded LRU (oldest keys evicted first)."""

    def __init__(self, max_keys: int = 10_000):
        self.max_keys = max_keys
        self._windows: OrderedDict[str, tuple[int, int]] = OrderedDict()

    async def hit(self, key: str, window_seconds: int) -> tuple[int, int]:
        now = int(time.time())
        window = now // window_seconds
        slot = f"{key}:{window}"
        count = self._windows.pop(slot, (0, 0))[0] + 1
        self._windows[slot] = (count, window)
        while len(self._windows) > self.max_keys:
            self._windows.popitem(last=False)
        return count, (window + 1) * window_seconds - now

    def clear(self) -> None:
        self._windows.clear()

    def __len__(self) -> int:
        return len(self._windows)


class RedisStore:
    """Fixed-window counters in Redis (INCR + EXPIRE)."""

    def __init__(self, url: str):
        import redis.asyncio as aioredis

        self._redis = aioredis.Redis.from_url(url, socket_connect_timeout=1, socket_timeout=1)

    async def hit(self, key: str, window_seconds: int) -> tuple[int, int]:
        now = int(time.time())
        window = now // window_seconds
        slot = f"ratelimit:{key}:{window}"
        async with self._redis.pipeline(transaction=True) as pipe:
            pipe.incr(slot)
            pipe.expire(slot, window_seconds + 1)
            count, _ = await pipe.execute()
        return int(count), (window + 1) * window_seconds - now


def _networks(cidrs: list[str]) -> list[ipaddress.IPv4Network | ipaddress.IPv6Network]:
    return [ipaddress.ip_network(c.strip(), strict=False) for c in cidrs if c.strip()]


def _is_trusted(ip: str, trusted: list[ipaddress.IPv4Network | ipaddress.IPv6Network]) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in trusted)


def client_ip(peer: str | None, forwarded_for: str | None, trusted_proxies: list[str]) -> str:
    """Right-most untrusted hop; XFF is only honoured when the peer is a trusted proxy."""
    peer = peer or "unknown"
    trusted = _networks(trusted_proxies)
    if not forwarded_for or not _is_trusted(peer, trusted):
        return peer
    for hop in reversed([h.strip() for h in forwarded_for.split(",") if h.strip()]):
        if not _is_trusted(hop, trusted):
            return hop
    return peer


class RateLimiter:
    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.redis: CounterStore | None = RedisStore(settings.REDIS_URL) if settings.REDIS_URL else None

    async def hit(self, key: str, limit: Limit) -> tuple[bool, int, int]:
        """Return ``(allowed, remaining, retry_after)``."""
        store: CounterStore = self.memory
        if self.redis is not None:
            store = self.redis
        try:
            count, reset = await store.hit(key, limit.window_seconds)
        except Exception as exc:  # Redis down: keep limiting per process rather than not at all
            logger.warning("Rate-limit store error (%s); using in-process counters", type(exc).__name__)
            count, reset = await self.memory.hit(key, limit.window_seconds)
        return count <= limit.requests, max(0, limit.requests - count), max(1, reset)


#: Process-wide limiter (tests reset ``rate_limiter.memory``).
rate_limiter = RateLimiter()


def _too_many(limit: Limit, retry_after: int) -> JSONResponse:
    body = APIResponse.error_response(
        message="Rate limit exceeded. Please try again later.",
        errors={"limit": limit.requests, "window_seconds": limit.window_seconds, "retry_after_seconds": retry_after},
    ).model_dump()
    return JSONResponse(
        status_code=429,
        content=body,
        headers={
            "Retry-After": str(retry_after),
            "X-RateLimit-Limit": str(limit.requests),
            "X-RateLimit-Remaining": "0",
        },
    )


async def _login_account(request: Request) -> str:
    try:
        body = json.loads(await request.body() or b"{}")
    except (ValueError, UnicodeDecodeError):
        return ""
    return str(body.get("username_or_email") or "").strip().lower() if isinstance(body, dict) else ""


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path.rstrip("/")
        if not path.startswith("/api/"):
            return await call_next(request)

        ip = client_ip(
            request.client.host if request.client else None,
            request.headers.get("x-forwarded-for"),
            settings.TRUSTED_PROXIES,
        )
        checks: list[tuple[str, Limit]] = [(f"ip:{ip}", Limit(settings.RATE_LIMIT_PER_MINUTE, 60))]
        if request.method == "POST" and path in AUTH_IP_LIMITS:
            checks.append((f"ip:{ip}:{path}", AUTH_IP_LIMITS[path]))
            if path == f"{API}/auth/login":
                account = await _login_account(request)
                if account:
                    checks.append((f"account:{account}:{path}", LOGIN_ACCOUNT_LIMIT))

        tightest: tuple[Limit, int] | None = None
        for key, limit in checks:
            allowed, remaining, retry_after = await rate_limiter.hit(key, limit)
            if not allowed:
                logger.warning("Rate limit exceeded on %s (%s)", path, key.split(":")[0])
                return _too_many(limit, retry_after)
            if tightest is None or remaining < tightest[1]:
                tightest = (limit, remaining)

        response = await call_next(request)
        if tightest is not None:
            response.headers["X-RateLimit-Limit"] = str(tightest[0].requests)
            response.headers["X-RateLimit-Remaining"] = str(tightest[1])
        return response
