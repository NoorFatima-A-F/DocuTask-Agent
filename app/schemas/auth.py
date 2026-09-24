"""
Authentication & User Request/Response Schemas.
Utilizes Pydantic v2 validation models.
"""

import re
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.core.config import settings


class RegisterRequest(BaseModel):
    """Payload required to register a new user account."""

    email: EmailStr = Field(..., description="User's valid email address", example="user@example.com")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username", example="johndoe")
    password: str = Field(..., min_length=8, max_length=100, description="Account password", example="SecureP@ss123")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if not v.isalnum() and "_" not in v and "-" not in v:
            raise ValueError("Username can only contain alphanumeric characters, underscores, and hyphens.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if len(v) < settings.MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter (A-Z).")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter (a-z).")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one numeric digit (0-9).")
        if settings.REQUIRE_PASSWORD_SPECIAL_CHAR and not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*...).")
        return v


class LoginRequest(BaseModel):
    """Payload required for user login."""

    username_or_email: str = Field(..., description="Username or Email address", example="johndoe")
    password: str = Field(..., description="Plaintext password", example="SecureP@ss123")


class UserResponse(BaseModel):
    """Public user response model."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    username: str
    role: str = "user"
    is_active: bool
    is_verified: bool = False
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """Authentication token response payload."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiration time in seconds")


class RefreshTokenRequest(BaseModel):
    """Payload required to refresh access tokens."""

    refresh_token: str = Field(..., description="Valid JWT Refresh Token")


class ChangePasswordRequest(BaseModel):
    """Payload required to change password while logged in."""

    old_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return RegisterRequest.validate_password_complexity(v)


class PasswordResetRequest(BaseModel):
    """Payload to initiate a password reset workflow."""

    email: EmailStr = Field(..., description="Registered user email address")


class PasswordResetConfirmRequest(BaseModel):
    """Payload to complete a password reset workflow."""

    token: str = Field(..., description="Password reset verification token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
