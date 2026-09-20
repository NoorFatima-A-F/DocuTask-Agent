"""Structured Mesh Access Logging and Audit Events."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MeshAccessLogRecord:
    timestamp: float
    request_id: str
    trace_id: str
    source_service: str
    target_service: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    client_ip: str = "127.0.0.1"
    mtls_authenticated: bool = True
    security_decision: str = "ALLOW"
    applied_policy: Optional[str] = None
    error_message: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


class MeshAccessLogger:
    """Structured access logger collecting zero-trust security and communication audit logs."""

    def __init__(self, max_records: int = 1000):
        self.max_records = max_records
        self._records: List[MeshAccessLogRecord] = []

    def log_access(self, record: MeshAccessLogRecord) -> None:
        self._records.append(record)
        if len(self._records) > self.max_records:
            self._records.pop(0)

    def query_logs(
        self,
        service_name: Optional[str] = None,
        min_status_code: Optional[int] = None,
        limit: int = 100,
    ) -> List[MeshAccessLogRecord]:
        """Query and filter structured access records."""
        results: List[MeshAccessLogRecord] = []
        for rec in reversed(self._records):
            if service_name and rec.target_service != service_name and rec.source_service != service_name:
                continue
            if min_status_code and rec.status_code < min_status_code:
                continue
            results.append(rec)
            if len(results) >= limit:
                break
        return results

    def clear(self) -> None:
        self._records.clear()
