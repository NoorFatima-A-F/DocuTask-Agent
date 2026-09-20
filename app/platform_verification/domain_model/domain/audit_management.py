"""
Audit Domain: Immutable, Tamper-Evident Hash-Chained Audit Records.
"""
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import hashlib
import json
import uuid


class AuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:8]}")
    entity_type: str
    entity_id: str
    action: str  # CREATE, UPDATE, STATE_CHANGE, CERTIFY, REVOKE
    actor: str = "Enterprise Verification Platform"
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Dict[str, Any]
    previous_hash: str = "0" * 64
    record_hash: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_hash(self) -> str:
        payload = f"{self.audit_id}:{self.entity_type}:{self.entity_id}:{self.action}:{self.previous_hash}:{json.dumps(self.new_state, sort_keys=True)}"
        self.record_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.record_hash
