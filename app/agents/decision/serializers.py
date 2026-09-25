"""
Decision Serializer Subsystem.
"""

from typing import Any, Dict
from app.agents.decision.engine import DecisionResult


class DecisionSerializer:
    @staticmethod
    def to_dict(result: DecisionResult) -> Dict[str, Any]:
        return result.model_dump(mode="json")

    @staticmethod
    def to_json(result: DecisionResult) -> str:
        return result.model_dump_json()
