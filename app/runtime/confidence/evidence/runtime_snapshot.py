"""
Runtime Snapshot for Phase 13.3 (ASCE-CGP).
Immutable container for point-in-time runtime evidence signals.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class RuntimeEvidenceSnapshot(BaseModel):
    mission_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    signals: Dict[str, Any] = Field(default_factory=dict)
    event_ids: List[str] = Field(default_factory=list)
    truth_ledger_hash: str = "hash-default-verified"
    replay_offset: int = 0
    snapshot_hash: str = ""

    def model_post_init(self, __context: Any) -> None:
        if not self.snapshot_hash:
            content = f"{self.mission_id}:{self.timestamp}:{json.dumps(self.signals, sort_keys=True)}"
            self.snapshot_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
