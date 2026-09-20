from typing import List, Optional
import hashlib
from ..domain.evidence_domain import EvidenceAggregate, EvidenceCaptured
from app.shared_kernel import Result, Ok, get_event_bus

class EvidenceService:
    def __init__(self, repo, cas_store):
        self.repo = repo
        self.cas_store = cas_store

    async def record_evidence(self, evidence_id: str, run_id: str, payload: bytes, tier: str = "WARM", tags: Optional[List[str]] = None) -> Result[EvidenceAggregate, str]:
        h = self.cas_store.put(payload)
        agg = EvidenceAggregate(id=evidence_id, run_id=run_id, retention_tier=tier, cas_hash=h, size_bytes=len(payload), tags=tags or [])
        self.repo.save(agg)
        await get_event_bus().publish(EvidenceCaptured(evidence_id=evidence_id, cas_hash=h))
        return Ok(agg)
