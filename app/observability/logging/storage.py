"""Log Storage Backend with Multi-Tenant Partitioning and Search."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LogEntry:
    timestamp: float
    service: str
    level: str
    message: str
    trace_id: str
    tenant_id: str
    record_dict: Dict[str, Any] = field(default_factory=dict)


class LogStorageBackend:
    """Thread-safe multi-tenant indexed log repository."""

    def __init__(self, max_records: int = 10000, retention_seconds: float = 86400.0 * 7):
        self.max_records = max_records
        self.retention_seconds = retention_seconds
        self._logs: List[LogEntry] = []
        self._lock = threading.Lock()

    def write(self, entry: LogEntry) -> None:
        with self._lock:
            self._logs.append(entry)
            if len(self._logs) > self.max_records:
                self._logs.pop(0)

    def search(
        self,
        tenant_id: Optional[str] = None,
        service: Optional[str] = None,
        level: Optional[str] = None,
        trace_id: Optional[str] = None,
        query: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: int = 100,
    ) -> List[LogEntry]:
        """Search structured logs by multiple dimensions and text search."""
        with self._lock:
            results: List[LogEntry] = []
            for entry in reversed(self._logs):
                if tenant_id and entry.tenant_id != tenant_id and entry.tenant_id != "system":
                    continue
                if service and entry.service != service:
                    continue
                if level and entry.level != level.upper():
                    continue
                if trace_id and entry.trace_id != trace_id:
                    continue
                if start_time and entry.timestamp < start_time:
                    continue
                if end_time and entry.timestamp > end_time:
                    continue
                if query and query.lower() not in entry.message.lower():
                    continue

                results.append(entry)
                if len(results) >= limit:
                    break

            return results

    def prune_expired(self, current_time: Optional[float] = None) -> int:
        now = current_time or time.time()
        cutoff = now - self.retention_seconds
        with self._lock:
            initial = len(self._logs)
            self._logs = [l for l in self._logs if l.timestamp >= cutoff]
            return initial - len(self._logs)

    def clear(self) -> None:
        with self._lock:
            self._logs.clear()
