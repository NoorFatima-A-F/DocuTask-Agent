"""
API package for Backup Architecture Verification.
"""
from app.platform_verification.backup_architecture_verification.api.backup_architecture_api import (
    router as backup_architecture_router,
)

__all__ = ["backup_architecture_router"]
