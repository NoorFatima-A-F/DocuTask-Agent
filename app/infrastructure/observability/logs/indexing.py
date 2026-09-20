"""
Log Search Index.

Provides multi-field inverted indexing and querying for structured log records
by tenant, service, trace_id, severity level, time window, and text substring.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from app.infrastructure.observability.logs.models import LogLevel, LogRecord

logger = logging.getLogger("infrastructure.observability.logs.indexing")


class LogIndex:
    """
    Inverted search index for platform log records.
    """

    def __init__(self, max_records: int = 10000) -> None:
        self.max_records = max_records
        self._records: Dict[str, LogRecord] = {}  # log_id -> LogRecord
        self._by_tenant: Dict[str, Set[str]] = {}  # tenant_id -> set of log_ids
        self._by_service: Dict[str, Set[str]] = {}  # service_name -> set of log_ids
        self._by_trace: Dict[str, Set[str]] = {}  # trace_id -> set of log_ids
        self._by_level: Dict[LogLevel, Set[str]] = {}  # level -> set of log_ids

    def index(self, record: LogRecord) -> None:
        """Add a log record to the inverted index."""
        if len(self._records) >= self.max_records:
            # Evict oldest
            oldest_id = next(iter(self._records))
            self.remove(oldest_id)

        self._records[record.log_id] = record

        self._by_tenant.setdefault(record.tenant_id, set()).add(record.log_id)
        self._by_service.setdefault(record.service_name, set()).add(record.log_id)
        self._by_level.setdefault(record.level, set()).add(record.log_id)

        if record.trace_id:
            self._by_trace.setdefault(record.trace_id, set()).add(record.log_id)

    def index_batch(self, records: List[LogRecord]) -> None:
        for r in records:
            self.index(r)

    def search(
        self,
        tenant_id: Optional[str] = None,
        service_name: Optional[str] = None,
        trace_id: Optional[str] = None,
        level: Optional[LogLevel] = None,
        min_level: Optional[LogLevel] = None,
        keyword: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[LogRecord]:
        """
        Query indexed logs matching multiple filtering criteria.
        """
        candidate_ids: Optional[Set[str]] = None

        if tenant_id and tenant_id != "all":
            ids = self._by_tenant.get(tenant_id, set())
            candidate_ids = ids if candidate_ids is None else candidate_ids.intersection(ids)

        if service_name:
            ids = self._by_service.get(service_name, set())
            candidate_ids = ids if candidate_ids is None else candidate_ids.intersection(ids)

        if trace_id:
            ids = self._by_trace.get(trace_id, set())
            candidate_ids = ids if candidate_ids is None else candidate_ids.intersection(ids)

        if level:
            ids = self._by_level.get(level, set())
            candidate_ids = ids if candidate_ids is None else candidate_ids.intersection(ids)

        matching_ids = candidate_ids if candidate_ids is not None else set(self._records.keys())

        level_order = [
            LogLevel.TRACE,
            LogLevel.DEBUG,
            LogLevel.INFO,
            LogLevel.NOTICE,
            LogLevel.WARNING,
            LogLevel.ERROR,
            LogLevel.CRITICAL,
            LogLevel.FATAL,
        ]
        min_level_idx = level_order.index(min_level) if min_level else 0

        results: List[LogRecord] = []
        kw_lower = keyword.lower() if keyword else None

        for lid in matching_ids:
            record = self._records.get(lid)
            if not record:
                continue

            if min_level and level_order.index(record.level) < min_level_idx:
                continue

            if start_time and record.timestamp < start_time:
                continue

            if end_time and record.timestamp > end_time:
                continue

            if kw_lower and kw_lower not in record.message.lower() and (not record.exception or kw_lower not in record.exception.lower()):
                continue

            results.append(record)

        # Sort descending by timestamp
        results.sort(key=lambda r: r.timestamp, reverse=True)
        return results[:limit]

    def remove(self, log_id: str) -> None:
        rec = self._records.pop(log_id, None)
        if not rec:
            return
        if rec.tenant_id in self._by_tenant:
            self._by_tenant[rec.tenant_id].discard(log_id)
        if rec.service_name in self._by_service:
            self._by_service[rec.service_name].discard(log_id)
        if rec.level in self._by_level:
            self._by_level[rec.level].discard(log_id)
        if rec.trace_id and rec.trace_id in self._by_trace:
            self._by_trace[rec.trace_id].discard(log_id)
