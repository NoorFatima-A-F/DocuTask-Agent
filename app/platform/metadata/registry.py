"""
Enterprise Metadata Framework.
Registers, indexes, and queries metadata across all platform entities.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from ..kernel.versioning import SemanticVersion


class MetadataType(str, Enum):
    AGENT = "AGENT"
    WORKFLOW = "WORKFLOW"
    PLUGIN = "PLUGIN"
    CONNECTOR = "CONNECTOR"
    MODULE = "MODULE"
    PROMPT = "PROMPT"
    MODEL = "MODEL"


@dataclass
class PlatformEntityMetadata:
    """Universal platform metadata envelope."""
    entity_id: str
    entity_type: MetadataType
    name: str
    version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    description: str = ""
    author: str = "DocuTask Enterprise"
    tags: List[str] = field(default_factory=list)
    schema_definition: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "name": self.name,
            "version": str(self.version),
            "description": self.description,
            "author": self.author,
            "tags": self.tags,
            "schema_definition": self.schema_definition,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class MetadataRegistry:
    """Central registry and search engine for platform metadata."""

    def __init__(self):
        self._entries: Dict[str, PlatformEntityMetadata] = {}

    def register(self, metadata: PlatformEntityMetadata) -> None:
        """Register entity metadata."""
        self._entries[metadata.entity_id] = metadata

    def get(self, entity_id: str) -> Optional[PlatformEntityMetadata]:
        """Retrieve metadata by entity ID."""
        return self._entries.get(entity_id)

    def find_by_type(self, entity_type: MetadataType) -> List[PlatformEntityMetadata]:
        """Filter metadata by entity type."""
        return [m for m in self._entries.values() if m.entity_type == entity_type]

    def find_by_tag(self, tag: str) -> List[PlatformEntityMetadata]:
        """Filter metadata entries having a specific tag."""
        return [m for m in self._entries.values() if tag in m.tags]

    def search(self, query: str) -> List[PlatformEntityMetadata]:
        """Search across name, description, and tags."""
        q = query.lower()
        return [
            m for m in self._entries.values()
            if q in m.name.lower() or q in m.description.lower() or any(q in t.lower() for t in m.tags)
        ]

    def list_all(self) -> List[PlatformEntityMetadata]:
        """List all registered metadata entries."""
        return list(self._entries.values())
