"""Evidence Management Engine & Compliance Bundle Packaging."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import hashlib
import json
import uuid
from ..core.events import AuditEvent
from ..storage.repository import AuditRepository
from ..integrity.signatures import AuditSigner
from .artifacts import EvidenceArtifact, EvidenceType
from .attachments import EvidenceAttachment


class EvidenceBundle(BaseModel):
    """Complete, self-contained, signed compliance evidence package."""
    bundle_id: str = Field(default_factory=lambda: f"bnd_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    title: str
    purpose: str
    generated_by: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit_events: List[AuditEvent] = Field(default_factory=list)
    artifacts: List[EvidenceArtifact] = Field(default_factory=list)
    manifest_hash: Optional[str] = None
    signature: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidenceManager:
    """Manages evidence artifact generation, attachment storage, and bundle packaging."""

    def __init__(
        self,
        repository: Optional[AuditRepository] = None,
        signer: Optional[AuditSigner] = None,
    ):
        self.repository = repository or AuditRepository()
        self.signer = signer or AuditSigner()
        self._artifacts: Dict[str, EvidenceArtifact] = {}
        self._attachments: Dict[str, List[EvidenceAttachment]] = {}

    def create_artifact(
        self,
        tenant_id: str,
        name: str,
        evidence_type: EvidenceType,
        source: str,
        content: str,
        related_event_ids: Optional[List[str]] = None,
        classification: str = "CONFIDENTIAL",
        owner: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvidenceArtifact:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        artifact = EvidenceArtifact(
            tenant_id=tenant_id,
            name=name,
            evidence_type=evidence_type,
            source=source,
            related_event_ids=related_event_ids or [],
            content_hash=content_hash,
            classification=classification,
            owner=owner,
            metadata=metadata or {},
        )

        attachment = EvidenceAttachment(
            evidence_id=artifact.evidence_id,
            filename=f"{name.lower().replace(' ', '_')}.json",
            content_text=content,
        )
        attachment.compute_checksum()

        self._artifacts[artifact.evidence_id] = artifact
        self._attachments[artifact.evidence_id] = [attachment]

        return artifact

    def get_artifact(self, evidence_id: str, tenant_id: Optional[str] = None) -> Optional[EvidenceArtifact]:
        art = self._artifacts.get(evidence_id)
        if not art:
            return None
        if tenant_id and art.tenant_id != tenant_id:
            return None
        return art

    def list_artifacts(
        self,
        tenant_id: str,
        evidence_type: Optional[EvidenceType] = None,
    ) -> List[EvidenceArtifact]:
        results = [a for a in self._artifacts.values() if a.tenant_id == tenant_id]
        if evidence_type:
            results = [a for a in results if a.evidence_type == evidence_type]
        return results

    def create_evidence_bundle(
        self,
        tenant_id: str,
        title: str,
        purpose: str,
        generated_by: str = "compliance_officer",
        correlation_id: Optional[str] = None,
        event_ids: Optional[List[str]] = None,
        artifact_ids: Optional[List[str]] = None,
    ) -> EvidenceBundle:
        """Assembles a signed bundle of correlated events and evidence artifacts."""
        selected_events: List[AuditEvent] = []
        if correlation_id:
            selected_events.extend(self.repository.find_by_correlation(correlation_id, tenant_id=tenant_id))
        elif event_ids:
            for eid in event_ids:
                ev = self.repository.get_by_id(eid, tenant_id=tenant_id)
                if ev:
                    selected_events.append(ev)
        else:
            selected_events = self.repository.list_by_tenant(tenant_id)

        selected_artifacts: List[EvidenceArtifact] = []
        if artifact_ids:
            for aid in artifact_ids:
                art = self.get_artifact(aid, tenant_id=tenant_id)
                if art:
                    selected_artifacts.append(art)
        else:
            selected_artifacts = self.list_artifacts(tenant_id)

        bundle = EvidenceBundle(
            tenant_id=tenant_id,
            title=title,
            purpose=purpose,
            generated_by=generated_by,
            audit_events=selected_events,
            artifacts=selected_artifacts,
        )

        # Compute deterministic manifest hash
        manifest_payload = {
            "bundle_id": bundle.bundle_id,
            "tenant_id": bundle.tenant_id,
            "event_hashes": [e.integrity_hash for e in selected_events if e.integrity_hash],
            "artifact_hashes": [a.content_hash for a in selected_artifacts],
            "timestamp": bundle.generated_at.isoformat(),
        }
        manifest_str = json.dumps(manifest_payload, sort_keys=True)
        bundle.manifest_hash = hashlib.sha256(manifest_str.encode("utf-8")).hexdigest()
        bundle.signature = self.signer.sign_hash(bundle.manifest_hash)

        return bundle
