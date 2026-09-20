"""
Enterprise Security Audit Unit & Integration Tests.
Verifies weak password rejection, rate limiting, security response headers, and RBAC controls.
"""

import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from app.dependencies.auth import RoleChecker
from app.core.exceptions import AccessDeniedException
from app.models.user import User
from app.schemas.auth import RegisterRequest


def test_password_policy_strict_enforcement():
    """Verifies that weak passwords lacking uppercase, lowercase, numbers, or special chars are rejected."""
    # 1. Missing uppercase
    with pytest.raises(ValidationError) as exc:
        RegisterRequest(email="valid@example.com", username="validuser", password="weakpassword123!")
    assert "uppercase letter" in str(exc.value)

    # 2. Missing lowercase
    with pytest.raises(ValidationError) as exc:
        RegisterRequest(email="valid@example.com", username="validuser", password="WEAKPASSWORD123!")
    assert "lowercase letter" in str(exc.value)

    # 3. Missing digit
    with pytest.raises(ValidationError) as exc:
        RegisterRequest(email="valid@example.com", username="validuser", password="WeakPassword!")
    assert "numeric digit" in str(exc.value)

    # 4. Missing special character
    with pytest.raises(ValidationError) as exc:
        RegisterRequest(email="valid@example.com", username="validuser", password="WeakPassword123")
    assert "special character" in str(exc.value)

    # 5. Too short (< 8 chars)
    with pytest.raises(ValidationError) as exc:
        RegisterRequest(email="valid@example.com", username="validuser", password="W1!")
    assert "at least 8 characters" in str(exc.value)

    # 6. Valid strong password passes
    req = RegisterRequest(email="valid@example.com", username="validuser", password="StrongPassword123!")
    assert req.password == "StrongPassword123!"


@pytest.mark.asyncio
async def test_security_headers_presence(client: AsyncClient):
    """Verifies OWASP security headers attached to every HTTP response."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

    headers = response.headers
    assert "X-Request-ID" in headers
    assert "X-Process-Time" in headers
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Content-Security-Policy" in headers
    assert "Referrer-Policy" in headers


@pytest.mark.asyncio
async def test_rate_limiting_enforcement(client: AsyncClient):
    """Verifies sliding window rate limiting on sensitive POST /login route."""
    login_payload = {
        "username_or_email": "nonexistent_user",
        "password": "WrongPassword123!"
    }

    # Execute 5 allowed login requests
    for _ in range(5):
        res = await client.post("/api/v1/auth/login", json=login_payload)
        assert res.status_code in (401, 429)

    # 6th request should trigger HTTP 429 Too Many Requests
    rate_limited_res = await client.post("/api/v1/auth/login", json=login_payload)
    assert rate_limited_res.status_code == 429
    body = rate_limited_res.json()
    assert body["success"] is False
    assert "Rate limit exceeded" in body["message"]
    assert "Retry-After" in rate_limited_res.headers


def test_rbac_role_checker():
    """Verifies RoleChecker authorization dependency."""
    admin_checker = RoleChecker(["admin"])

    # User role -> AccessDeniedException
    regular_user = User(role="user", is_superuser=False, is_active=True)
    with pytest.raises(AccessDeniedException):
        admin_checker(regular_user)

    # Admin role -> Allowed
    admin_user = User(role="admin", is_superuser=False, is_active=True)
    assert admin_checker(admin_user) == admin_user

    # Superuser -> Allowed
    super_user = User(role="user", is_superuser=True, is_active=True)
    assert admin_checker(super_user) == super_user
