"""Content-Addressable Artifact Registry.

Stores runtime artifacts, intermediate outputs, and schemas indexed strictly
by their SHA-256 cryptographic digest.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StoredArtifact:
    sha256: str
    artifact_name: str
    content_type: str
    size_bytes: int
    data: Any
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sha256": self.sha256,
            "artifact_name": self.artifact_name,
            "content_type": self.content_type,
            "size_bytes": self.size_bytes,
            "created_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.created_at)),
            "metadata": self.metadata,
        }


class ArtifactRegistry:
    def __init__(self):
        self._artifacts: Dict[str, StoredArtifact] = {}

    def register(
        self,
        name: str,
        content: Any,
        content_type: str = "application/json",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StoredArtifact:
        if isinstance(content, (dict, list)):
            serialized = json.dumps(content, sort_keys=True)
            raw_bytes = serialized.encode("utf-8")
        elif isinstance(content, str):
            raw_bytes = content.encode("utf-8")
        elif isinstance(content, bytes):
            raw_bytes = content
        else:
            raw_bytes = str(content).encode("utf-8")

        digest = hashlib.sha256(raw_bytes).hexdigest()
        artifact = StoredArtifact(
            sha256=digest,
            artifact_name=name,
            content_type=content_type,
            size_bytes=len(raw_bytes),
            data=content,
            metadata=metadata or {},
        )
        self._artifacts[digest] = artifact
        return artifact

    def get(self, sha256: str) -> Optional[StoredArtifact]:
        return self._artifacts.get(sha256)

    def contains(self, sha256: str) -> bool:
        return sha256 in self._artifacts

    def list_artifacts(self) -> List[Dict[str, Any]]:
        return [art.to_dict() for art in self._artifacts.values()]

    def count(self) -> int:
        return len(self._artifacts)

    def clear(self) -> None:
        self._artifacts.clear()


global_artifact_registry = ArtifactRegistry()
