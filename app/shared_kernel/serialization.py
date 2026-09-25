"""
Standardized Serialization Contracts and Encoders.
Supports JSON, YAML, and binary schema serialization contracts.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Type, TypeVar
import json

T = TypeVar("T")

class SerializationFormat(str, Enum):
    JSON = "JSON"
    YAML = "YAML"
    BINARY = "BINARY"

class SerializerContract(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> str:
        pass

    @abstractmethod
    def deserialize(self, payload: str, target_type: Type[T]) -> T:
        pass

class JsonSerializer(SerializerContract):
    def serialize(self, obj: Any) -> str:
        return json.dumps(obj, default=str)

    def deserialize(self, payload: str, target_type: Type[T]) -> T:
        return json.loads(payload)

class SerializationSchemaValidatorContract(ABC):
    @abstractmethod
    def validate_payload(self, payload: str, schema: Dict[str, Any]) -> bool:
        pass
