"""Secrets never reach log output."""

from __future__ import annotations

import io
import logging

import pytest

from app.core.config import settings
from app.core.logging import MASK, ScrubbingFormatter, install_secret_scrubbing, scrub

GOOGLE_KEY = "AIza" + "S" * 35
JWT = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.c2lnbmF0dXJlLXZhbHVl"


@pytest.mark.parametrize(
    "line",
    [
        f"calling gemini with key={GOOGLE_KEY}",
        f"headers={{'x-goog-api-key': '{GOOGLE_KEY}'}}",
        f"Authorization: Bearer {JWT}",
        f"token {JWT} rejected",
        "connect postgresql+asyncpg://docutask:s3cr3t-pass@db:5432/docutask",
        'payload {"username": "bob", "password": "Hunter2Hunter2"}',
        "refresh_token=abcdef123456",
    ],
)
def test_generic_secret_shapes_are_masked(line: str) -> None:
    out = scrub(line)
    for secret in (GOOGLE_KEY, JWT, "s3cr3t-pass", "Hunter2Hunter2", "abcdef123456"):
        assert secret not in out
    assert MASK in out


def test_configured_secrets_are_masked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "JWT_SECRET", "a-very-long-configured-jwt-secret-value")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "plain-gemini-key-without-prefix")
    out = scrub("secret a-very-long-configured-jwt-secret-value and plain-gemini-key-without-prefix")
    assert "configured-jwt" not in out and "plain-gemini" not in out


def test_ordinary_text_is_unchanged() -> None:
    line = "Job 1234 finished: COMPLETED in 2.5s for invoice INV-001 total 1,250.00"
    assert scrub(line) == line


def test_tracebacks_are_scrubbed() -> None:
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(ScrubbingFormatter(fmt="%(message)s"))
    log = logging.getLogger("scrub-test")
    log.addHandler(handler)
    try:
        raise RuntimeError(f"upstream said key={GOOGLE_KEY}")
    except RuntimeError:
        log.exception("failed with %s", JWT)
    finally:
        log.removeHandler(handler)
    output = stream.getvalue()
    assert GOOGLE_KEY not in output and JWT not in output and "RuntimeError" in output


def test_third_party_handlers_get_wrapped() -> None:
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    third_party = logging.getLogger("httpx-like")
    third_party.addHandler(handler)
    try:
        install_secret_scrubbing("httpx-like")
        third_party.warning("GET https://example.test/v1?key=%s", GOOGLE_KEY)
    finally:
        third_party.removeHandler(handler)
    assert GOOGLE_KEY not in stream.getvalue()
