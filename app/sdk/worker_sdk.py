"""Enterprise Agent SDK - Worker Abstractions."""

from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkerTask:
    task_id: str
    capability_name: str
    input_payload: Dict[str, Any]
    sla_timeout_ms: float = 5000.0
    created_at: float = field(default_factory=time.time)


@dataclass
class WorkerResult:
    task_id: str
    status: str  # SUCCESS, FAILED, TIMEOUT
    output_payload: Dict[str, Any]
    latency_ms: float
    cost_usd: float = 0.0
    energy_joules: float = 0.0
    error_message: Optional[str] = None


class BaseWorker(abc.ABC):
    def __init__(self, worker_id: str, capability: str):
        self.worker_id = worker_id
        self.capability = capability

    @abc.abstractmethod
    def process_task(self, task: WorkerTask) -> WorkerResult:
        """Process an assigned capability task."""
        pass

    def probe_health(self) -> Dict[str, Any]:
        return {"worker_id": self.worker_id, "capability": self.capability, "healthy": True}
