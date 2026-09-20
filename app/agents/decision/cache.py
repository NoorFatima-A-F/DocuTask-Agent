"""
Decision Cache Subsystem.
"""

from typing import Dict, Optional
from app.agents.decision.engine import DecisionResult


class DecisionCache:
    def __init__(self):
        self._cache: Dict[str, DecisionResult] = {}

    def get(self, key: str) -> Optional[DecisionResult]:
        return self._cache.get(key)

    def set(self, key: str, result: DecisionResult) -> None:
        self._cache[key] = result
