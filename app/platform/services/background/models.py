"""
Background Service Definitions and Scheduling Models.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid


class ServicePriority(int, Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 20


@dataclass
class ServiceDefinition:
    """Specification of a background service task."""
    name: str
    handler: Callable[..., Any]
    service_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    schedule_cron: Optional[str] = None  # e.g., "*/5 * * * *"
    interval_seconds: Optional[int] = None
    priority: ServicePriority = ServicePriority.NORMAL
    timeout_seconds: int = 60
    max_retries: int = 3
    concurrency_limit: int = 1
    dependencies: List[str] = field(default_factory=list)
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
