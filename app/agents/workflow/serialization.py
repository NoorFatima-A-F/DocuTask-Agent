"""
Workflow Serialization Utilities.
Handles versioned JSON serialization and Google Cloud Pub/Sub message encoding for all workflow models.
"""

import json
from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class WorkflowSerializer:
    """Versioned serializer for workflow definitions, instances, and events."""

    SCHEMA_VERSION = "22.0"

    @classmethod
    def serialize_to_json(cls, model: BaseModel) -> str:
        """Serializes a model to JSON string with schema version envelope."""
        data = model.model_dump(mode="json")
        envelope = {
            "schema_version": cls.SCHEMA_VERSION,
            "model_class": model.__class__.__name__,
            "payload": data,
        }
        return json.dumps(envelope, default=str)

    @classmethod
    def deserialize_from_json(cls, json_str: str, model_class: Type[T]) -> T:
        """Deserializes JSON string into target model instance."""
        envelope = json.loads(json_str)
        payload = envelope.get("payload", envelope)
        return model_class.model_validate(payload)

    @classmethod
    def to_pubsub_message(cls, model: BaseModel) -> Dict[str, Any]:
        """Encodes model for Cloud Pub/Sub message payload."""
        return {
            "attributes": {
                "schema_version": cls.SCHEMA_VERSION,
                "model_type": model.__class__.__name__,
            },
            "data": cls.serialize_to_json(model).encode("utf-8"),
        }
