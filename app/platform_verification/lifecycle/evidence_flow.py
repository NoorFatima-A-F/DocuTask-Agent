from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Dict, List, Any
import uuid

@dataclass(frozen=True)
class SealedEvidenceArtifact:
    artifact_id: str
    execution_id: str
    step_id: str
    artifact_type: str
    sha256_checksum: str
    size_bytes: int
    payload: Dict[str, Any]
    retention_tier: str = "PRODUCTION_CERTIFIED"
    sealed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class EvidenceLifecycleManager:
    def __init__(self):
        self._store: Dict[str, SealedEvidenceArtifact] = {}

    def collect_and_seal(self, execution_id: str, step_id: str, artifact_type: str, data: Dict[str, Any]) -> SealedEvidenceArtifact:
        serialized = json.dumps(data, sort_keys=True).encode("utf-8")
        checksum = hashlib.sha256(serialized).hexdigest()
        artifact_id = f"evi_{uuid.uuid4().hex[:12]}"

        artifact = SealedEvidenceArtifact(
            artifact_id=artifact_id,
            execution_id=execution_id,
            step_id=step_id,
            artifact_type=artifact_type,
            sha256_checksum=checksum,
            size_bytes=len(serialized),
            payload=data
        )
        self._store[artifact_id] = artifact
        return artifact

    def get_by_id(self, artifact_id: str) -> SealedEvidenceArtifact:
        return self._store[artifact_id]

    def verify_artifact_integrity(self, artifact: SealedEvidenceArtifact) -> bool:
        serialized = json.dumps(artifact.payload, sort_keys=True).encode("utf-8")
        recomputed = hashlib.sha256(serialized).hexdigest()
        return recomputed == artifact.sha256_checksum
