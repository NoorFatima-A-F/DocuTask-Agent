"""
Distributed Lock Manager Module.
Prevents concurrent execution of the same document job across worker nodes using advisory locking.
"""

import asyncio
from typing import Dict, Set
from app.core.logging import logger


class DistributedLockManager:
    """Lock manager enforcing mutual exclusion across distributed workers."""

    _active_locks: Set[str] = set()
    _lock_obj = asyncio.Lock()

    @classmethod
    async def acquire_lock(cls, resource_id: str, timeout_seconds: float = 5.0) -> bool:
        """
        Attempts to acquire a distributed lock for resource_id.
        """
        async with cls._lock_obj:
            if resource_id in cls._active_locks:
                logger.warning(f"Lock contention: Resource '{resource_id}' is already locked by another worker.")
                return False
            cls._active_locks.add(resource_id)
            logger.info(f"Acquired distributed lock for resource '{resource_id}'")
            return True

    @classmethod
    async def release_lock(cls, resource_id: str) -> bool:
        """
        Releases lock for resource_id.
        """
        async with cls._lock_obj:
            if resource_id in cls._active_locks:
                cls._active_locks.remove(resource_id)
                logger.info(f"Released distributed lock for resource '{resource_id}'")
                return True
            return False
