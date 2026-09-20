"""
Reflection Serialization Utilities.
Provides versioned JSON serialization and deserialization compatible with Google Cloud Tasks and Pub/Sub.
"""

import json
from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel
from app.agents.reflection.context import ReflectionRequest, ReflectionResult
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.self_critique import SelfCritique

T = TypeVar("T", bound=BaseModel)


class ReflectionSerializer:
    """Handles serialization and deserialization of reflection models with schema versioning."""

    SCHEMA_VERSION = "20.0"

    @classmethod
    def serialize_to_json(cls, model: BaseModel) -> str:
        """Serializes a Pydantic v2 model to JSON string with version metadata."""
        data = model.model_dump(mode="json")
        envelope = {
            "schema_version": cls.SCHEMA_VERSION,
            "model_class": model.__class__.__name__,
            "payload": data
        }
        return json.dumps(envelope, default=str)

    @classmethod
    def deserialize_from_json(cls, json_str: str, model_class: Type[T]) -> T:
        """Deserializes JSON string into target Pydantic model instance."""
        envelope = json.loads(json_str)
        payload = envelope.get("payload", envelope)
        return model_class.model_validate(payload)

    @classmethod
    def to_pubsub_message(cls, model: BaseModel) -> Dict[str, Any]:
        """Encodes model for Google Cloud Pub/Sub publish payload."""
        return {
            "attributes": {
                "schema_version": cls.SCHEMA_VERSION,
                "model_type": model.__class__.__name__
            },
            "data": cls.serialize_to_json(model).encode("utf-8")
        }
