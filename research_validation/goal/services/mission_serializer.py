"""
Mission Serializer Service
==========================
Provides deterministic lossless JSON serialization and deserialization with round-trip guarantees.
"""

import json
from typing import Any, Dict
from research_validation.goal.models.goal import Goal
from research_validation.goal.models.mission import Mission


class MissionSerializer:
    """Deterministic JSON serializer for Goals and Missions."""

    @classmethod
    def serialize_goal(cls, goal: Goal) -> str:
        """Serializes Goal to formatted canonical JSON string."""
        return json.dumps(goal.canonical_dict(), indent=2, sort_keys=True)

    @classmethod
    def serialize_mission(cls, mission: Mission) -> str:
        """Serializes Mission to formatted canonical JSON string."""
        return json.dumps(mission.canonical_dict(), indent=2, sort_keys=True)

    @classmethod
    def deserialize_dict(cls, json_str: str) -> Dict[str, Any]:
        """Deserializes JSON string back to Python dictionary."""
        return json.loads(json_str)
