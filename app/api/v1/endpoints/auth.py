"""
Authentication API Endpoints Router.
Receives HTTP requests, validates payloads via Pydantic, delegates to AuthService, and returns standard APIResponse envelopes.
"""

from fastapi import APIRouter, Depends, status
from app.dependencies.auth import get_current_active_user
from app.dependencies.db import get_auth_service
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.response import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
    description="Registers a new user account with unique email and username."
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[UserResponse]:
    """Handles new user registration."""
    user_response = await auth_service.register_user(request)
    return APIResponse.success_response(
        data=user_response,
        message="User account created successfully"
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate user login",
    description="Authenticates credentials and issues access and refresh JWT tokens."
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[TokenResponse]:
    """Handles user login authentication."""
    tokens = await auth_service.login(request)
    return APIResponse.success_response(
        data=tokens,
        message="Authentication successful"
    )


@router.post(
    "/refresh",
    response_model=APIResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Refresh access tokens",
    description="Rotates refresh token and issues a new pair of access and refresh tokens."
)
async def refresh_tokens(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[TokenResponse]:
    """Handles refresh token rotation."""
    tokens = await auth_service.refresh_tokens(request.refresh_token)
    return APIResponse.success_response(
        data=tokens,
        message="Tokens refreshed successfully"
    )


@router.post(
    "/logout",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="User logout",
    description="Revokes the provided refresh token session."
)
async def logout(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[dict]:
    """Handles single session logout."""
    await auth_service.logout(request.refresh_token)
    return APIResponse.success_response(
        data={},
        message="Successfully logged out"
    )


@router.post(
    "/logout-all",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Logout all active sessions",
    description="Revokes all active refresh tokens for the current user across all devices."
)
async def logout_all(
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[dict]:
    """Handles multi-device session invalidation."""
    await auth_service.revoke_all_sessions(current_user.id)
    return APIResponse.success_response(
        data={},
        message="All sessions successfully revoked"
    )


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Returns the profile information of the currently authenticated user."
)
async def get_me(
    current_user: User = Depends(get_current_active_user)
) -> APIResponse[UserResponse]:
    """Retrieves authenticated user profile."""
    user_response = UserResponse.model_validate(current_user)
    return APIResponse.success_response(
        data=user_response,
        message="User profile retrieved successfully"
    )


@router.post(
    "/change-password",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Change user password",
    description="Changes current user password and invalidates all existing active sessions."
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> APIResponse[dict]:
    """Handles user password update."""
    await auth_service.change_password(current_user.id, request)
    return APIResponse.success_response(
        data={},
        message="Password updated successfully. Please log in with your new password."
    )
