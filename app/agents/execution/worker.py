"""
Worker Runtime Model.
Defines Worker representation, capabilities, and health status.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class WorkerStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    DRAINING = "DRAINING"
    DEAD = "DEAD"


class Worker(BaseModel):
    """Execution Worker running atomic tasks."""
    worker_id: str
    capabilities: List[str] = Field(default_factory=lambda: ["DEFAULT"])
    status: WorkerStatus = Field(default=WorkerStatus.IDLE)
    assigned_node_id: Optional[str] = None
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    max_concurrent_tasks: int = Field(default=1, ge=1)
    model_config = {"frozen": True}
