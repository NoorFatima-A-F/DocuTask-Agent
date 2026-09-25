"""
State Serializer for Phase 13.4.
Deterministic JSON state serialization for hash computation and disk storage.
"""

from typing import Dict, Any
import json


class StateSerializer:
    """
    Serializes runtime state dictionary into deterministic JSON bytes.
    """

    @staticmethod
    def serialize(state: Dict[str, Any]) -> str:
        return json.dumps(state, sort_keys=True, separators=(",", ":"), default=str)
