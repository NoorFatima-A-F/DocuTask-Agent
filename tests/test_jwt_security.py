"""JWT hardening: refuse weak secrets outside dev/test; require exp/iat; reject refresh tokens as access."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt
import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from app.core.config import DEFAULT_JWT_SECRET, Settings, settings
from app.core.exceptions import TokenException
from app.core.security import create_access_token, create_refresh_token, decode_token

REPO = Path(__file__).resolve().parent.parent
STRONG = "f" * 64


@pytest.mark.parametrize("env", ["production", "staging", "prod"])
def test_default_secret_refused_outside_dev(env: str) -> None:
    with pytest.raises(ValidationError, match="JWT_SECRET"):
        Settings(ENVIRONMENT=env, JWT_SECRET=DEFAULT_JWT_SECRET, _env_file=None)


def test_short_secret_refused_in_production() -> None:
    with pytest.raises(ValidationError, match="32 bytes"):
        Settings(ENVIRONMENT="production", JWT_SECRET="x" * 31, _env_file=None)


def test_strong_secret_accepted_in_production() -> None:
    assert Settings(ENVIRONMENT="production", JWT_SECRET=STRONG, _env_file=None).JWT_SECRET == STRONG


@pytest.mark.parametrize("env", ["development", "test"])
def test_default_secret_tolerated_in_dev_and_test(env: str) -> None:
    Settings(ENVIRONMENT=env, JWT_SECRET=DEFAULT_JWT_SECRET, _env_file=None)


def test_app_refuses_to_start_in_production_with_default_secret(tmp_path: Path) -> None:
    env = {k: v for k, v in os.environ.items() if k not in {"JWT_SECRET"}}
    env.update({"ENVIRONMENT": "production", "JWT_SECRET": DEFAULT_JWT_SECRET, "PYTHONPATH": str(REPO)})
    # Run from an empty dir so the developer's .env is not picked up.
    proc = subprocess.run(
        [sys.executable, "-c", "import app.core.config"], cwd=tmp_path, env=env, capture_output=True, text=True
    )
    assert proc.returncode != 0
    assert "JWT_SECRET" in proc.stderr


def _token(**claims: object) -> str:
    return jwt.encode(claims, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def test_token_without_exp_rejected() -> None:
    with pytest.raises(TokenException):
        decode_token(_token(sub="u", type="access", iat=datetime.now(UTC)))


def test_token_without_iat_rejected() -> None:
    with pytest.raises(TokenException):
        decode_token(_token(sub="u", type="access", exp=datetime.now(UTC) + timedelta(minutes=5)))


def test_expired_token_rejected() -> None:
    with pytest.raises(TokenException):
        decode_token(create_access_token("u", expires_delta=timedelta(seconds=-5)))


def test_refresh_token_is_not_an_access_token() -> None:
    refresh, _ = create_refresh_token("u")
    with pytest.raises(TokenException):
        decode_token(refresh, expected_type="access")
    assert decode_token(create_access_token("u"))["type"] == "access"


def test_token_signed_with_other_secret_rejected() -> None:
    forged = jwt.encode(
        {
            "sub": "u",
            "type": "access",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "attacker-secret-" + "x" * 32,
        algorithm="HS256",
    )
    with pytest.raises(TokenException):
        decode_token(forged)


async def test_refresh_token_rejected_on_protected_route(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register", json={"email": "jwt@example.com", "username": "jwtuser", "password": "Password123!"}
    )
    login = await client.post("/api/v1/auth/login", json={"username_or_email": "jwtuser", "password": "Password123!"})
    tokens = login.json()["data"]
    ok = await client.get("/api/v1/documents", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert ok.status_code == 200
    bad = await client.get("/api/v1/documents", headers={"Authorization": f"Bearer {tokens['refresh_token']}"})
    assert bad.status_code == 401
