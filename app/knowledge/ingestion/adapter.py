"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Ingestion Framework.
Provides pluggable adapters for batch, incremental, streaming, and event-driven data ingestion.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

from app.knowledge.core.exceptions import IngestionError
from app.knowledge.core.models import (
    KnowledgeDocument,
    KnowledgeObject,
    KnowledgeSource,
    SyncMode,
)

logger = logging.getLogger(__name__)


class KnowledgeSourceAdapter(ABC):
    """
    Abstract contract for source adapters pulling raw data from enterprise systems
    into the knowledge ingestion pipeline.
    """

    def __init__(self, source_model: KnowledgeSource):
        self.source_model = source_model

    @abstractmethod
    def authenticate(self) -> bool:
        """Validates credentials against external source system."""
        pass

    @abstractmethod
    def discover(self) -> List[Dict[str, Any]]:
        """Lists available resources, files, or records from the source."""
        pass

    @abstractmethod
    def fetch(self, resource_id: str) -> KnowledgeDocument:
        """Pulls and creates a KnowledgeDocument from the external resource."""
        pass

    def sync(self, mode: Optional[SyncMode] = None) -> List[KnowledgeDocument]:
        """Executes synchronization loop and returns fetched documents."""
        sync_mode = mode or self.source_model.sync_mode
        resources = self.discover()
        docs: List[KnowledgeDocument] = []
        for r in resources:
            doc = self.fetch(r.get("id", str(uuid.uuid4())))
            docs.append(doc)
        self.source_model.last_sync = datetime.now(timezone.utc)
        logger.info(f"Source adapter '{self.source_model.source_id}' synced {len(docs)} documents ({sync_mode.value})")
        return docs


class BatchFileAdapter(KnowledgeSourceAdapter):
    """Adapter for local files, batch uploads, and directory scans."""

    def __init__(self, source_model: KnowledgeSource, file_records: Optional[List[Dict[str, Any]]] = None):
        super().__init__(source_model)
        self._file_records = file_records or []

    def authenticate(self) -> bool:
        return True

    def discover(self) -> List[Dict[str, Any]]:
        return list(self._file_records)

    def fetch(self, resource_id: str) -> KnowledgeDocument:
        record = next((r for r in self._file_records if r.get("id") == resource_id), None)
        if not record:
            record = {"id": resource_id, "title": "Untitled Document", "content": "", "file_type": "txt"}

        content = record.get("content", "")
        return KnowledgeDocument(
            id=f"kdoc-{uuid.uuid4().hex[:10]}",
            knowledge_id=self.source_model.source_id,
            title=record.get("title", "Batch Document"),
            file_type=record.get("file_type", "txt"),
            raw_content=content,
            normalized_text=content.strip(),
            byte_size=len(content.encode("utf-8")),
            page_count=record.get("page_count", 1),
            metadata=record.get("metadata", {}),
        )


class ConnectorKnowledgeAdapter(KnowledgeSourceAdapter):
    """Adapter bridging Phase 5 Connector Platform instances directly into Knowledge Ingestion."""

    def __init__(self, source_model: KnowledgeSource, connector_runtime: Optional[Any] = None):
        super().__init__(source_model)
        self._connector_runtime = connector_runtime

    def authenticate(self) -> bool:
        return True

    def discover(self) -> List[Dict[str, Any]]:
        return [{"id": "conn-res-1", "title": "External Knowledge Feed", "content": "Sample connector payload"}]

    def fetch(self, resource_id: str) -> KnowledgeDocument:
        return KnowledgeDocument(
            id=f"kdoc-{uuid.uuid4().hex[:10]}",
            knowledge_id=self.source_model.source_id,
            title=f"Resource {resource_id}",
            file_type="json",
            raw_content="{'key': 'value'}",
            normalized_text="key: value",
            byte_size=12,
        )
