"""
Memory Lifecycle States for Enterprise Multi-Agent Memory Platform.
Defines MemoryLifecycleState enum tracking memory record lifecycle mutations.
"""

from enum import Enum


class MemoryLifecycleState(str, Enum):
    """Memory record lifecycle states."""
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    SUMMARIZED = "SUMMARIZED"
    COMPRESSED = "COMPRESSED"
    EXPIRED = "EXPIRED"
    PROMOTED = "PROMOTED"
    DEMOTED = "DEMOTED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"
    PURGED = "PURGED"
