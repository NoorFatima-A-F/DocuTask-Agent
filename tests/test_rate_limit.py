"""Rate limiting: trusted-proxy IP resolution, per-IP and per-account auth buckets, bounded memory."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app
from app.middleware.rate_limit import MemoryStore, RateLimiter, client_ip, rate_limiter

LOGIN = f"{settings.API_V1_STR}/auth/login"
REGISTER = f"{settings.API_V1_STR}/auth/register"


def test_xff_ignored_when_peer_is_not_a_trusted_proxy() -> None:
    assert client_ip("203.0.113.9", "1.2.3.4", trusted_proxies=[]) == "203.0.113.9"
    assert client_ip("203.0.113.9", "1.2.3.4", trusted_proxies=["10.0.0.0/8"]) == "203.0.113.9"


def test_rightmost_untrusted_hop_is_used_behind_trusted_proxies() -> None:
    # client spoofs "6.6.6.6"; the real client 198.51.100.7 was appended by our proxy chain
    xff = "6.6.6.6, 198.51.100.7, 10.0.0.5"
    assert client_ip("10.0.0.1", xff, trusted_proxies=["10.0.0.0/8"]) == "198.51.100.7"


def test_all_hops_trusted_falls_back_to_peer() -> None:
    assert client_ip("10.0.0.1", "10.0.0.2", trusted_proxies=["10.0.0.0/8"]) == "10.0.0.1"


def test_garbage_xff_hop_counts_as_untrusted_client() -> None:
    assert client_ip("10.0.0.1", "not-an-ip", trusted_proxies=["10.0.0.0/8"]) == "not-an-ip"


async def test_memory_store_is_bounded() -> None:
    store = MemoryStore(max_keys=100)
    for i in range(1000):
        await store.hit(f"k{i}", 60)
    assert len(store) == 100


async def test_redis_failure_falls_back_to_memory_limits() -> None:
    class Broken:
        async def hit(self, key: str, window_seconds: int) -> tuple[int, int]:
            raise ConnectionError("down")

    limiter = RateLimiter()
    limiter.redis = Broken()
    from app.middleware.rate_limit import Limit

    results = [(await limiter.hit("k", Limit(2, 60)))[0] for _ in range(3)]
    assert results == [True, True, False]


async def _client(peer: str) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app, client=(peer, 1234)), base_url="http://test")


async def test_spoofed_xff_does_not_reset_the_login_bucket(client: AsyncClient) -> None:
    payload = {"username_or_email": "victim", "password": "WrongPassword123!"}
    async with await _client("203.0.113.10") as c:
        codes = [
            (await c.post(LOGIN, json=payload, headers={"X-Forwarded-For": f"1.1.1.{i}"})).status_code for i in range(6)
        ]
    assert codes[:5] == [401] * 5 and codes[5] == 429


async def test_account_limit_holds_across_ips(client: AsyncClient) -> None:
    payload = {"username_or_email": "Victim@Example.com", "password": "WrongPassword123!"}
    codes = []
    for i in range(6):
        async with await _client(f"198.51.100.{i}") as c:
            codes.append((await c.post(LOGIN, json=payload)).status_code)
    assert codes[5] == 429


async def test_ip_limit_holds_across_usernames(client: AsyncClient) -> None:
    async with await _client("203.0.113.11") as c:
        codes = [
            (await c.post(LOGIN, json={"username_or_email": f"user{i}", "password": "x"})).status_code
            for i in range(11)
        ]
    assert 429 not in codes[:10] and codes[10] == 429


async def test_general_api_limit_per_ip(client: AsyncClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 3)
    async with await _client("203.0.113.12") as c:
        codes = [(await c.get(f"{settings.API_V1_STR}/documents")).status_code for _ in range(4)]
    assert codes == [401, 401, 401, 429]


async def test_health_probes_are_not_rate_limited(client: AsyncClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 1)
    async with await _client("203.0.113.13") as c:
        assert {(await c.get("/healthz")).status_code for _ in range(5)} == {200}


def test_limiter_singleton_uses_memory_in_tests() -> None:
    assert rate_limiter.redis is None
