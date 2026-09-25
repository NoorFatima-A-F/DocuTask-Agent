"""
Feature Vector Cache for Phase 13.3 (ASCE-CGP).
Thread-safe in-memory cache for extracted and normalized feature vectors.
"""

from typing import Dict, Optional


class FeatureCache:
    """
    Caches extracted feature vectors per mission for ultra-fast confidence evaluations.
    """

    _cache: Dict[str, Dict[str, float]] = {}

    @classmethod
    def set(cls, mission_id: str, features: Dict[str, float]):
        cls._cache[mission_id] = features.copy()

    @classmethod
    def get(cls, mission_id: str) -> Optional[Dict[str, float]]:
        return cls._cache.get(mission_id)

    @classmethod
    def clear(cls, mission_id: Optional[str] = None):
        if mission_id:
            cls._cache.pop(mission_id, None)
        else:
            cls._cache.clear()
