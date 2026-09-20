"""
Platform Resource Management Models.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ResourceType(str, Enum):
    CPU_CORES = "CPU_CORES"
    MEMORY_MB = "MEMORY_MB"
    WORKER_SLOTS = "WORKER_SLOTS"
    DB_CONNECTIONS = "DB_CONNECTIONS"
    AI_TOKENS = "AI_TOKENS"
    API_CALLS_PER_MIN = "API_CALLS_PER_MIN"
    STORAGE_MB = "STORAGE_MB"
    QUEUE_DEPTH = "QUEUE_DEPTH"


@dataclass
class ResourceQuota:
    """Resource quota for a tenant or workspace."""
    tenant_id: str
    resource_type: ResourceType
    limit: float
    reserved: float = 0.0
    burst_allowed: bool = False
    burst_limit: float = 0.0


@dataclass
class ResourceUsage:
    """Current resource consumption."""
    tenant_id: str
    resource_type: ResourceType
    current_usage: float = 0.0
    peak_usage: float = 0.0
