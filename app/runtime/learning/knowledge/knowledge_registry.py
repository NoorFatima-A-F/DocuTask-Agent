"""
Knowledge Registry for Phase 13.5 (ARLP-KIP).
Central repository for version-controlled, evidence-backed knowledge artifacts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib
import json
import uuid
from pydantic import BaseModel, Field


class KnowledgeRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"kn_{uuid.uuid4().hex[:8]}")
    title: str
    category: str = "EXECUTION_RULE"
    source_mission_id: str = "mission-001"
    confidence_score: float = 0.95
    validation_status: str = "VERIFIED"
    version: str = "1.0.0"
    content_hash: str = ""
    content: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    replaced_by: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KnowledgeRegistry:
    """
    Manages institutional knowledge records with full lifecycle and version history.
    """

    def __init__(self):
        self._records: Dict[str, KnowledgeRecord] = {}
        self._seed_default_records()

    def _seed_default_records(self):
        self.register_record(
            title="Parallel Wavefront Sharding for Large Document Sets",
            category="EXECUTION_RULE",
            source_mission_id="mission-001",
            confidence_score=0.965,
            content={"shard_size": 4, "parallelism": 6, "speedup_pct": 34.2},
            tags=["ocr", "sharding", "performance", "wavefront"],
        )
        self.register_record(
            title="Dynamic SMT Verification on Ambiguous Entity Extractions",
            category="VALIDATION_STRATEGY",
            source_mission_id="mission-001",
            confidence_score=0.942,
            content={"confidence_floor": 0.88, "smt_timeout_ms": 120},
            tags=["smt", "verification", "confidence", "truth"],
        )
        self.register_record(
            title="Exponential Jitter Backoff on OCR Throttling",
            category="RESILIENCE_STRATEGY",
            source_mission_id="mission-001",
            confidence_score=0.978,
            content={"base_delay_ms": 250, "max_retries": 3, "jitter": True},
            tags=["resilience", "retry", "throttling"],
        )

    def register_record(
        self,
        title: str,
        category: str = "EXECUTION_RULE",
        source_mission_id: str = "mission-001",
        confidence_score: float = 0.95,
        validation_status: str = "VERIFIED",
        version: str = "1.0.0",
        content: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> KnowledgeRecord:
        content_dict = content or {}
        tags_list = tags or []
        serialized = json.dumps({"title": title, "category": category, "content": content_dict}, sort_keys=True)
        content_hash = f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]}"
        rec_id = f"kn_{uuid.uuid4().hex[:8]}"

        rec = KnowledgeRecord(
            record_id=rec_id,
            title=title,
            category=category,
            source_mission_id=source_mission_id,
            confidence_score=confidence_score,
            validation_status=validation_status,
            version=version,
            content_hash=content_hash,
            content=content_dict,
            tags=tags_list,
        )
        self._records[rec_id] = rec
        return rec

    def get_record(self, record_id: str) -> Optional[KnowledgeRecord]:
        return self._records.get(record_id)

    def list_records(self, category: Optional[str] = None) -> List[KnowledgeRecord]:
        records = list(self._records.values())
        if category:
            records = [r for r in records if r.category == category]
        return records

    def deprecate_record(self, record_id: str, superseded_by: Optional[str] = None) -> Optional[KnowledgeRecord]:
        rec = self._records.get(record_id)
        if rec:
            rec.validation_status = "DEPRECATED"
            rec.replaced_by = superseded_by
            rec.updated_at = datetime.now(timezone.utc).isoformat()
        return rec


knowledge_registry = KnowledgeRegistry()
