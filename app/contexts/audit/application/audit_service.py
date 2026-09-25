from typing import Dict, Any
import hashlib
import json
from ..domain.audit_domain import AuditRecordAggregate, AuditRecordAppended
from app.shared_kernel import Result, Ok, get_event_bus

class AuditLedgerService:
    def __init__(self, repo):
        self.repo = repo

    async def log_action(self, event_type: str, actor: str, payload: Dict[str, Any]) -> Result[AuditRecordAggregate, str]:
        last = self.repo.get_latest()
        prev_h = last.record_hash if last else "0" * 64
        seq = (last.sequence + 1) if last else 1
        raw = f"{seq}:{event_type}:{actor}:{prev_h}:{json.dumps(payload, sort_keys=True)}"
        rec_h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        rec_id = f"aud_{seq:06d}"
        agg = AuditRecordAggregate(id=rec_id, sequence=seq, event_type=event_type, actor=actor, prev_hash=prev_h, record_hash=rec_h, details=payload)
        self.repo.save(agg)
        await get_event_bus().publish(AuditRecordAppended(record_id=rec_id, event_type=event_type))
        return Ok(agg)

    def verify_integrity(self) -> bool:
        records = self.repo.list_all()
        for i, r in enumerate(records):
            prev = ("0" * 64) if i == 0 else records[i-1].record_hash
            if r.prev_hash != prev:
                return False
        return True
