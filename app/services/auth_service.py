"""
Authentication Service Business Logic Layer.
Handles registration, authentication, refresh token rotation, logout, and password management.
"""

import uuid
from typing import Optional
from app.core.config import settings
from app.core.exceptions import (
    AccessDeniedException,
    DuplicateResourceException,
    InvalidCredentialsException,
    ResourceNotFoundException,
    TokenException,
)
from app.core.logging import logger
from app.core.security import (
    sanitize_log_input,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    """Service providing core user authentication and lifecycle operations."""

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register_user(self, request: RegisterRequest) -> UserResponse:
        """
        Registers a new user account after validating email and username uniqueness.
        """
        # Validate email uniqueness
        if await self.user_repo.exists_email(request.email):
            logger.warning("Registration failed: Email '%s' already exists.", sanitize_log_input(request.email))
            raise DuplicateResourceException("An account with this email address already exists.")

        # Validate username uniqueness
        if await self.user_repo.exists_username(request.username):
            logger.warning("Registration failed: Username '%s' already exists.", sanitize_log_input(request.username))
            raise DuplicateResourceException("An account with this username already exists.")

        # Hash password and persist user
        hashed_pwd = hash_password(request.password)
        user_data = {
            "email": request.email.lower().strip(),
            "username": request.username.strip(),
            "hashed_password": hashed_pwd,
            "is_active": True,
            "is_superuser": False,
        }
        user = await self.user_repo.create(user_data)
        logger.info("User successfully registered: ID=%s, Username=%s", sanitize_log_input(user.id), sanitize_log_input(user.username))
        return UserResponse.model_validate(user)

    async def login(self, request: LoginRequest) -> TokenResponse:
        """
        Authenticates user credentials and generates access and refresh tokens.
        """
        identifier = request.username_or_email.strip()
        user: Optional[User] = None

        # Check if identifier is email or username
        if "@" in identifier:
            user = await self.user_repo.get_by_email(identifier)
        else:
            user = await self.user_repo.get_by_username(identifier)

        if not user or not verify_password(request.password, user.hashed_password):
            logger.warning("Login attempt failed for identifier: '%s'", sanitize_log_input(identifier))
            raise InvalidCredentialsException("Invalid email/username or password.")

        if not user.is_active:
            logger.warning("Login failed: User account '%s' is deactivated.", sanitize_log_input(user.id))
            raise AccessDeniedException("User account is inactive. Please contact support.")

        # Generate tokens
        access_token = create_access_token(subject=str(user.id))
        raw_refresh_token, expires_at = create_refresh_token(subject=str(user.id))

        # Store refresh token hash in DB
        token_h = hash_token(raw_refresh_token)
        await self.token_repo.create({
            "user_id": user.id,
            "token_hash": token_h,
            "expires_at": expires_at,
            "revoked": False
        })

        logger.info("User logged in successfully: ID=%s", sanitize_log_input(user.id))
        return TokenResponse(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def refresh_tokens(self, refresh_token_str: str) -> TokenResponse:
        """
        Refreshes tokens using Refresh Token Rotation mechanism.
        Revokes old token and issues a fresh access & refresh token pair.
        """
        # Decode and validate refresh token JWT structure
        payload = decode_token(refresh_token_str, expected_type="refresh")
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise TokenException("Invalid token payload")

        user_id = uuid.UUID(user_id_str)
        t_hash = hash_token(refresh_token_str)

        # Check database for valid token record
        token_obj = await self.token_repo.get_valid_token(t_hash)
        if not token_obj:
            logger.warning("Token refresh failed: Revoked or invalid token presented for user %s", sanitize_log_input(user_id))
            raise TokenException("Refresh token is invalid, expired, or has been revoked")

        # Verify user active status
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AccessDeniedException("User account associated with token is inactive or deleted")

        # Revoke current refresh token (Rotation)
        await self.token_repo.revoke(token_obj)

        # Issue new token pair
        new_access_token = create_access_token(subject=str(user.id))
        new_raw_refresh_token, new_expires_at = create_refresh_token(subject=str(user.id))
        new_t_hash = hash_token(new_raw_refresh_token)

        await self.token_repo.create({
            "user_id": user.id,
            "token_hash": new_t_hash,
            "expires_at": new_expires_at,
            "revoked": False
        })

        logger.info("Refreshed token successfully for user: ID=%s", sanitize_log_input(user.id))
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_raw_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def logout(self, refresh_token_str: str) -> None:
        """
        Logs out user by revoking the provided refresh token.
        """
        t_hash = hash_token(refresh_token_str)
        token_obj = await self.token_repo.get_valid_token(t_hash)
        if token_obj:
            await self.token_repo.revoke(token_obj)
            logger.info("Successfully revoked refresh token for user %s", sanitize_log_input(token_obj.user_id))

    async def revoke_all_sessions(self, user_id: uuid.UUID) -> None:
        """
        Revokes all active sessions / refresh tokens for a user across all devices.
        """
        await self.token_repo.revoke_all_for_user(user_id)
        logger.info("Revoked all sessions for user %s", sanitize_log_input(user_id))

    async def change_password(self, user_id: uuid.UUID, request: ChangePasswordRequest) -> None:
        """
        Changes user password after validating current password.
        Revokes all existing refresh tokens for security upon password update.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")

        if not verify_password(request.old_password, user.hashed_password):
            raise InvalidCredentialsException("Current password is incorrect")

        new_hashed = hash_password(request.new_password)
        await self.user_repo.update(user, {"hashed_password": new_hashed})

        # Invalidate all user sessions on password change
        await self.token_repo.revoke_all_for_user(user_id)
        logger.info("Password changed successfully for user %s. All active sessions revoked.", sanitize_log_input(user_id))
