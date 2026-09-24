"""
Platform Kernel Contract Specifications.
Defines base contract interfaces and versioned message/payload schemas.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict
import uuid
from .versioning import SemanticVersion


@dataclass(frozen=True)
class Contract:
    """Base immutable platform data contract."""
    contract_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize contract to dictionary."""
        return {
            "contract_id": self.contract_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True)
class VersionedContract(Contract):
    """Platform contract with explicit semantic versioning and compatibility metadata."""
    schema_version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    schema_name: str = "default.contract"
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize versioned contract with schema headers."""
        base = super().to_dict()
        base.update({
            "schema_version": str(self.schema_version),
            "schema_name": self.schema_name,
            "payload": self.payload,
            "metadata": self.metadata,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VersionedContract":
        """Deserialize from dictionary."""
        semver = SemanticVersion.parse(data.get("schema_version", "1.0.0"))
        return cls(
            contract_id=data.get("contract_id", str(uuid.uuid4())),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(timezone.utc),
            schema_version=semver,
            schema_name=data.get("schema_name", "default.contract"),
            payload=data.get("payload", {}),
            metadata=data.get("metadata", {}),
        )
