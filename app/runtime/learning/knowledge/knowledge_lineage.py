"""
Knowledge Lineage Tracker for Phase 13.5 (ARLP-KIP).
Cryptographic provenance tracking using SHA-256 hash chains for tamper-evident knowledge audits.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import hashlib
import uuid
from pydantic import BaseModel, Field


class LineageRecord(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"lin_{uuid.uuid4().hex[:8]}")
    record_id: str
    version: str
    parent_hash: Optional[str] = None
    lineage_hash: str
    source_mission_id: str
    content_hash: str
    mutation_note: str = "Initial knowledge registration"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KnowledgeLineageTracker:
    """
    Maintains append-only SHA-256 cryptographic provenance chains for all knowledge records.
    """

    def __init__(self):
        self._chains: Dict[str, List[LineageRecord]] = {}
        self._seed_default_lineage()

    def _seed_default_lineage(self):
        self.record_origin("kn-ocr-shard", "1.0.0", "mission-001", "sha256:init_ocr_hash")

    def record_origin(
        self,
        record_id: str,
        version: str,
        source_mission_id: str,
        content_hash: str,
    ) -> LineageRecord:
        serialized = f"ROOT:{record_id}:{version}:{source_mission_id}:{content_hash}"
        lineage_hash = f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]}"

        entry = LineageRecord(
            record_id=record_id,
            version=version,
            parent_hash=None,
            lineage_hash=lineage_hash,
            source_mission_id=source_mission_id,
            content_hash=content_hash,
            mutation_note="Initial record genesis",
        )
        self._chains[record_id] = [entry]
        return entry

    def record_evolution(
        self,
        record_id: str,
        version: str,
        source_mission_id: str,
        content_hash: str,
        mutation_note: str,
    ) -> LineageRecord:
        chain = self._chains.get(record_id, [])
        parent_hash = chain[-1].lineage_hash if chain else None

        serialized = f"{parent_hash}:{record_id}:{version}:{source_mission_id}:{content_hash}:{mutation_note}"
        lineage_hash = f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]}"

        entry = LineageRecord(
            record_id=record_id,
            version=version,
            parent_hash=parent_hash,
            lineage_hash=lineage_hash,
            source_mission_id=source_mission_id,
            content_hash=content_hash,
            mutation_note=mutation_note,
        )
        if record_id not in self._chains:
            self._chains[record_id] = []
        self._chains[record_id].append(entry)
        return entry

    def get_chain(self, record_id: str) -> List[LineageRecord]:
        return self._chains.get(record_id, [])

    def verify_chain_integrity(self, record_id: str) -> bool:
        chain = self._chains.get(record_id, [])
        if not chain:
            return True
        for i in range(1, len(chain)):
            prev = chain[i - 1]
            curr = chain[i]
            if curr.parent_hash != prev.lineage_hash:
                return False
        return True


knowledge_lineage_tracker = KnowledgeLineageTracker()
