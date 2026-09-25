"""
Planner Serializer Subsystem.
"""

from typing import Any, Dict


class PlannerSerializer:
    """Serializes CandidatePlan and PlanningTrace models."""

    @staticmethod
    def to_dict(model: Any) -> Dict[str, Any]:
        return model.model_dump(mode="json")

    @staticmethod
    def to_json(model: Any) -> str:
        return model.model_dump_json()
