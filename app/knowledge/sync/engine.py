"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Synchronization Engine.
Coordinates data sync schedules, webhook-triggered updates, staleness detection, and re-indexing tasks.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.knowledge.core.models import KnowledgeSource, SyncMode

logger = logging.getLogger(__name__)


class SyncStatusRecord(BaseModel):
    """Synchronization telemetry and freshness status for a knowledge source."""
    source_id: str
    last_sync: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_version: str = "1.0.0"
    index_version: str = "1.0.0"
    freshness_score: float = 1.0  # 1.0 = completely up to date, 0.0 = stale
    synced_documents_count: int = 0
    status: str = "COMPLETED"


class KnowledgeSyncEngine:
    """
    Manages synchronization lifecycles across external repositories and internal indices.
    """

    def __init__(self):
        self._sync_records: Dict[str, SyncStatusRecord] = {}

    def record_sync(
        self,
        source: KnowledgeSource,
        documents_count: int,
        source_version: str = "1.0.0",
        index_version: str = "1.0.0",
    ) -> SyncStatusRecord:
        """Updates and records synchronization completion for a source."""
        rec = SyncStatusRecord(
            source_id=source.source_id,
            last_sync=datetime.now(timezone.utc),
            source_version=source_version,
            index_version=index_version,
            freshness_score=1.0,
            synced_documents_count=documents_count,
            status="COMPLETED",
        )
        self._sync_records[source.source_id] = rec
        source.last_sync = rec.last_sync
        logger.info(f"Recorded sync for source '{source.source_id}': {documents_count} docs synced")
        return rec

    def get_sync_status(self, source_id: str) -> Optional[SyncStatusRecord]:
        """Retrieves sync status and freshness for a knowledge source."""
        return self._sync_records.get(source_id)

    def calculate_staleness(self, source_id: str, max_age_hours: float = 24.0) -> float:
        """Calculates freshness score (0.0 to 1.0) based on elapsed time since last sync."""
        rec = self._sync_records.get(source_id)
        if not rec:
            return 0.0
        elapsed_hours = (datetime.now(timezone.utc) - rec.last_sync).total_seconds() / 3600.0
        freshness = max(0.0, 1.0 - (elapsed_hours / max_age_hours))
        rec.freshness_score = freshness
        return freshness
