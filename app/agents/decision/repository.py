"""
Decision Repository Abstraction.
"""

from typing import Dict, Optional
from app.agents.decision.engine import DecisionResult


class DecisionRepository:
    def __init__(self):
        self._store: Dict[str, DecisionResult] = {}

    async def save(self, key: str, result: DecisionResult) -> None:
        self._store[key] = result

    async def get(self, key: str) -> Optional[DecisionResult]:
        return self._store.get(key)
