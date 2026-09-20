"""Audit Storage Partition Manager."""

from datetime import datetime, timezone
from typing import Optional


class AuditPartitionManager:
    """Manages partition keys for tenant-isolated, time-bucketed audit event storage."""

    @staticmethod
    def get_partition_key(
        tenant_id: str,
        timestamp: Optional[datetime] = None,
        category: Optional[str] = None,
    ) -> str:
        ts = timestamp or datetime.now(timezone.utc)
        month_str = ts.strftime("%Y-%m")
        cat_str = category.upper() if category else "ALL"
        return f"{tenant_id}/{month_str}/{cat_str}"
