from typing import Dict, Optional
from ..domain.verification_domain import VerificationDefinition

class InMemoryVerificationRepository:
    def __init__(self):
        self._store: Dict[str, VerificationDefinition] = {}

    def save(self, defn: VerificationDefinition) -> None:
        self._store[defn.id] = defn

    def get(self, defn_id: str) -> Optional[VerificationDefinition]:
        return self._store.get(defn_id)
