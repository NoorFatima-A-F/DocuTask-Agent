"""
API package for Database Backup Verification.
"""
from app.platform_verification.database_backup_verification.api.database_backup_api import (
    router as database_backup_router,
)

__all__ = ["database_backup_router"]
