"""
Unit Tests for AuthService Business Logic.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    DuplicateResourceException,
    InvalidCredentialsException,
    TokenException,
)
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import ChangePasswordRequest, LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_auth_service_full_flow(db_session: AsyncSession):
    """Tests registration, login, token refresh, logout, and password change."""
    user_repo = UserRepository(db_session)
    token_repo = RefreshTokenRepository(db_session)
    auth_service = AuthService(user_repo=user_repo, token_repo=token_repo)

    # 1. Register User
    reg_req = RegisterRequest(
        email="service_test@example.com",
        username="servicetest",
        password="Password123!"
    )
    user_resp = await auth_service.register_user(reg_req)
    assert user_resp.email == "service_test@example.com"
    assert user_resp.username == "servicetest"

    # Duplicate registration attempt
    with pytest.raises(DuplicateResourceException):
        await auth_service.register_user(reg_req)

    # 2. Login
    login_req = LoginRequest(
        username_or_email="servicetest",
        password="Password123!"
    )
    tokens = await auth_service.login(login_req)
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None

    # Invalid login attempt
    bad_login = LoginRequest(
        username_or_email="servicetest",
        password="WrongPassword"
    )
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login(bad_login)

    # 3. Refresh Tokens (Rotation)
    old_refresh_token = tokens.refresh_token
    new_tokens = await auth_service.refresh_tokens(old_refresh_token)
    assert new_tokens.access_token != tokens.access_token
    assert new_tokens.refresh_token != old_refresh_token

    # Re-using old rotated token must fail
    with pytest.raises(TokenException):
        await auth_service.refresh_tokens(old_refresh_token)

    # 4. Logout
    await auth_service.logout(new_tokens.refresh_token)
    with pytest.raises(TokenException):
        await auth_service.refresh_tokens(new_tokens.refresh_token)

    # 5. Change Password
    # Re-login to get active refresh token
    await auth_service.login(login_req)
    change_pwd_req = ChangePasswordRequest(
        old_password="Password123!",
        new_password="NewPassword456!"
    )
    await auth_service.change_password(user_resp.id, change_pwd_req)

    # Old password login should fail now
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login(login_req)

    # New password login succeeds
    new_login_req = LoginRequest(
        username_or_email="servicetest",
        password="NewPassword456!"
    )
    success_login = await auth_service.login(new_login_req)
    assert success_login.access_token is not None
