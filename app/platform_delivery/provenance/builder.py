"""SLSA v1.0 and in-toto Software Provenance Builder (Req 21)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class SLSAProvenanceStatement:
    """Standardized SLSA v1.0 Provenance Attestation."""
    statement_id: str
    artifact_name: str
    artifact_digest: str
    builder_id: str
    build_type: str
    source_repo: str
    source_commit: str
    build_invocation_id: str
    materials: List[Dict[str, str]] = field(default_factory=list)
    build_started_on: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    build_finished_on: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    slsa_level: int = 3

    def to_in_toto_statement(self) -> Dict[str, Any]:
        return {
            "_type": "https://in-toto.io/Statement/v1",
            "subject": [
                {
                    "name": self.artifact_name,
                    "digest": {"sha256": self.artifact_digest.replace("sha256:", "")},
                }
            ],
            "predicateType": "https://slsa.dev/provenance/v1",
            "predicate": {
                "buildDefinition": {
                    "buildType": self.build_type,
                    "externalParameters": {
                        "repository": self.source_repo,
                        "commit": self.source_commit,
                    },
                    "internalParameters": {
                        "builder": self.builder_id,
                        "invocationId": self.build_invocation_id,
                    },
                },
                "runDetails": {
                    "builder": {"id": self.builder_id},
                    "metadata": {
                        "invocationId": self.build_invocation_id,
                        "startedOn": self.build_started_on.isoformat(),
                        "finishedOn": self.build_finished_on.isoformat(),
                    },
                },
            },
        }


class ProvenanceManager:
    """Builds and stores supply chain provenance attestations."""

    def __init__(self):
        self._provenances: Dict[str, SLSAProvenanceStatement] = {}  # artifact_digest -> statement

    def record_provenance(
        self,
        artifact_name: str,
        artifact_digest: str,
        source_repo: str,
        source_commit: str,
        builder_id: str = "https://github.com/docutask/actions/runner@v1",
        build_type: str = "https://docutask.io/build/container@v1",
    ) -> SLSAProvenanceStatement:
        stmt = SLSAProvenanceStatement(
            statement_id=f"prov-{uuid.uuid4().hex[:8]}",
            artifact_name=artifact_name,
            artifact_digest=artifact_digest,
            builder_id=builder_id,
            build_type=build_type,
            source_repo=source_repo,
            source_commit=source_commit,
            build_invocation_id=f"inv-{uuid.uuid4().hex[:12]}",
        )
        self._provenances[artifact_digest] = stmt
        return stmt

    def get_provenance(self, artifact_digest: str) -> Optional[SLSAProvenanceStatement]:
        return self._provenances.get(artifact_digest)
