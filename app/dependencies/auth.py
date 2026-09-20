"""
Authentication & Authorization FastAPI Dependencies.
Implements OAuth2 Bearer token extraction, RBAC role enforcement, and security context providers.
"""

import uuid
from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import AccessDeniedException, TokenException
from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.dependencies.db import get_user_repository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=True
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Decodes Bearer access token and fetches current user entity.
    
    :raises TokenException: If token is invalid or user does not exist
    """
    payload = decode_token(token, expected_type="access")
    user_id_str: str = payload.get("sub", "")
    if not user_id_str:
        raise TokenException("Invalid authentication credentials")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise TokenException("Invalid user ID format in token payload")

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise TokenException("User no longer exists in system")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Ensures current authenticated user is active.
    
    :raises AccessDeniedException: If user account is disabled/inactive
    """
    if not current_user.is_active:
        raise AccessDeniedException("User account is inactive")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Ensures current active user possesses administrative superuser privileges.
    
    :raises AccessDeniedException: If user lacks superuser permissions
    """
    if not current_user.is_superuser:
        raise AccessDeniedException("The user does not have sufficient permissions")
    return current_user


class RoleChecker:
    """RBAC dependency checking whether active user possesses required roles."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = [r.lower().strip() for r in allowed_roles]

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        Validates user role against allowed_roles.
        
        :raises AccessDeniedException: If user lacks permission
        """
        if current_user.is_superuser or current_user.role.lower() == "admin":
            return current_user

        if current_user.role.lower() not in self.allowed_roles:
            raise AccessDeniedException(
                f"User role '{current_user.role}' is not authorized to perform this operation"
            )
        return current_user


# Role-specific dependency shortcuts
get_current_admin = RoleChecker(["admin"])
