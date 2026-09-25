"""
Runtime Serialization Utilities.
Versioned JSON serialization and Google Cloud Pub/Sub message formatting for runtime kernel models.
"""

import json
from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class RuntimeSerializer:
    """Versioned serializer for platform runtime models, state snapshots, and sessions."""

    SCHEMA_VERSION = "23.0"

    @classmethod
    def serialize_to_json(cls, model: BaseModel) -> str:
        """Encodes model into versioned JSON envelope."""
        data = model.model_dump(mode="json")
        envelope = {
            "schema_version": cls.SCHEMA_VERSION,
            "model_class": model.__class__.__name__,
            "payload": data,
        }
        return json.dumps(envelope, default=str)

    @classmethod
    def deserialize_from_json(cls, json_str: str, model_class: Type[T]) -> T:
        """Decodes versioned JSON envelope into target model class."""
        envelope = json.loads(json_str)
        payload = envelope.get("payload", envelope)
        return model_class.model_validate(payload)

    @classmethod
    def to_pubsub_message(cls, model: BaseModel) -> Dict[str, Any]:
        """Encodes model into Cloud Pub/Sub payload format."""
        return {
            "attributes": {
                "schema_version": cls.SCHEMA_VERSION,
                "model_type": model.__class__.__name__,
            },
            "data": cls.serialize_to_json(model).encode("utf-8"),
        }
