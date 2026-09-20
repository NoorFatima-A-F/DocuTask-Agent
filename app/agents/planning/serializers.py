"""
Plan Serializer Subsystem.
Serializes Plan aggregates for JSON, Pub/Sub, and Cloud Tasks payloads.
"""

from typing import Any, Dict
from app.agents.planning.contracts import Plan


class PlanSerializer:
    """Serializer converting Plan models to JSON string / dictionary payloads."""

    @staticmethod
    def to_dict(plan: Plan) -> Dict[str, Any]:
        return plan.model_dump(mode="json")

    @staticmethod
    def to_json(plan: Plan) -> str:
        return plan.model_dump_json()
