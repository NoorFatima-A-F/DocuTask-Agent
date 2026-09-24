"""
Execution Serializer Subsystem.
Serializes execution requests, sessions, and snapshots for Pub/Sub, Cloud Tasks, and DB storage.
"""

from typing import Any, Dict


class ExecutionSerializer:
    """Serializes runtime models to JSON string and dictionary representations."""

    @staticmethod
    def to_dict(model: Any) -> Dict[str, Any]:
        return model.model_dump(mode="json")

    @staticmethod
    def to_json(model: Any) -> str:
        return model.model_dump_json()
