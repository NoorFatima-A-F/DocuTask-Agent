"""
API Integration Tests for Authentication Endpoints.
Verifies all routes return standardized APIResponse JSON format.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    """Verifies health check endpoint returns 200 and standard success envelope."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "System operating normally"
    assert data["data"]["status"] == "healthy"
    assert data["errors"] is None


@pytest.mark.asyncio
async def test_auth_api_full_workflow(client: AsyncClient):
    """Verifies complete authentication HTTP API workflow."""

    # 1. Register User
    reg_payload = {
        "email": "api_user@example.com",
        "username": "apiuser",
        "password": "SecurePassword123!"
    }
    response = await client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "api_user@example.com"
    assert body["data"]["username"] == "apiuser"

    # Duplicate Register Attempt -> 409
    response_dup = await client.post("/api/v1/auth/register", json=reg_payload)
    assert response_dup.status_code == 409
    body_dup = response_dup.json()
    assert body_dup["success"] is False
    assert "already exists" in body_dup["message"]

    # 2. Login
    login_payload = {
        "username_or_email": "apiuser",
        "password": "SecurePassword123!"
    }
    login_res = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    
    tokens = login_res.json()["data"]
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # Bad Login Attempt -> 401
    bad_login_res = await client.post("/api/v1/auth/login", json={
        "username_or_email": "apiuser",
        "password": "WrongPassword"
    })
    assert bad_login_res.status_code == 401
    assert bad_login_res.json()["success"] is False

    # 3. GET /me (Authenticated)
    headers = {"Authorization": f"Bearer {access_token}"}
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["data"]["username"] == "apiuser"

    # GET /me (Unauthenticated) -> 401
    me_unauth = await client.get("/api/v1/auth/me")
    assert me_unauth.status_code == 401

    # 4. Refresh Token
    refresh_res = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()["data"]
    new_access_token = new_tokens["access_token"]
    new_refresh_token = new_tokens["refresh_token"]

    # 5. Change Password
    new_headers = {"Authorization": f"Bearer {new_access_token}"}
    change_pwd_payload = {
        "old_password": "SecurePassword123!",
        "new_password": "NewSecurePassword456!"
    }
    pwd_res = await client.post("/api/v1/auth/change-password", json=change_pwd_payload, headers=new_headers)
    assert pwd_res.status_code == 200
    assert pwd_res.json()["success"] is True

    # Login with new password
    login_new_pwd = await client.post("/api/v1/auth/login", json={
        "username_or_email": "api_user@example.com",
        "password": "NewSecurePassword456!"
    })
    assert login_new_pwd.status_code == 200
    latest_tokens = login_new_pwd.json()["data"]

    # 6. Logout
    logout_res = await client.post("/api/v1/auth/logout", json={"refresh_token": latest_tokens["refresh_token"]})
    assert logout_res.status_code == 200

    # 7. Logout All Sessions
    latest_headers = {"Authorization": f"Bearer {latest_tokens['access_token']}"}
    logout_all_res = await client.post("/api/v1/auth/logout-all", headers=latest_headers)
    assert logout_all_res.status_code == 200
