"""
State Deserializer for Phase 13.4.
Deserializes deterministic JSON state snapshots back into dictionary structures.
"""

from typing import Dict, Any
import json


class StateDeserializer:
    """
    Deserializes stored snapshot strings back to memory.
    """

    @staticmethod
    def deserialize(serialized_state: str) -> Dict[str, Any]:
        return json.loads(serialized_state)
