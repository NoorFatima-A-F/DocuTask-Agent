from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

@dataclass(frozen=True)
class RecoveryActionRecord:
    action_type: str
    target_id: str
    initiated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "COMPLETED"

class LifecycleRecoveryManager:
    def __init__(self):
        self._history: List[RecoveryActionRecord] = []

    def trigger_recovery(self, action_type: str, target_id: str) -> RecoveryActionRecord:
        record = RecoveryActionRecord(action_type=action_type, target_id=target_id)
        self._history.append(record)
        return record

    def get_recovery_history(self) -> List[RecoveryActionRecord]:
        return list(self._history)
