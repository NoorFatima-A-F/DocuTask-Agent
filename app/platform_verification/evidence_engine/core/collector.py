"""
Automated Multi-Source Evidence Collection Engine.
Captures workflow states, inputs, runtime traces, outputs, AI decisions, and metrics.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact,
    EvidenceCategory,
    EvidenceLifecycleState,
    EvidenceClassification,
)
from app.platform_verification.evidence_engine.domain.interfaces import IEvidenceCollector
from app.platform_verification.evidence_engine.core.store import ContentAddressableStore
from app.platform_verification.evidence_engine.core.audit_trail import ImmutableAuditTrail


class EvidenceCollector(IEvidenceCollector):
    """Multi-source evidence collector with automatic CAS storage and audit logging."""

    def __init__(
        self,
        store: Optional[ContentAddressableStore] = None,
        audit_trail: Optional[ImmutableAuditTrail] = None,
    ) -> None:
        self.store = store or ContentAddressableStore()
        self.audit_trail = audit_trail

    def collect(
        self,
        execution_id: str,
        category: EvidenceCategory,
        data: Any,
        metadata: Optional[Dict[str, Any]] = None,
        classification: EvidenceClassification = EvidenceClassification.INTERNAL,
    ) -> EvidenceArtifact:
        if isinstance(data, (dict, list)):
            content = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        elif isinstance(data, str):
            content = data.encode("utf-8")
        elif isinstance(data, bytes):
            content = data
        else:
            content = str(data).encode("utf-8")

        artifact = self.store.store_artifact(
            execution_id=execution_id,
            category=category,
            content=content,
            metadata=metadata,
            classification=classification,
        )

        if self.audit_trail:
            self.audit_trail.record_event(
                actor="EvidenceCollector",
                action="EvidenceCreated",
                resource=artifact.artifact_id,
                details={"category": category.value, "checksum": artifact.checksum_sha256},
            )

        return artifact

    def collect_artifact(
        self,
        execution_id: str,
        category: EvidenceCategory,
        data: bytes,
        content_type: str = "application/json",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvidenceArtifact:
        meta = metadata or {}
        meta["content_type"] = content_type
        return self.collect(execution_id, category, data, meta)

    def collect_json_evidence(
        self,
        execution_id: str,
        category: EvidenceCategory,
        payload: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvidenceArtifact:
        return self.collect(execution_id, category, payload, metadata)

    def get_artifact(self, artifact_id: str) -> Optional[EvidenceArtifact]:
        return self.store.get_artifact(artifact_id)


# Aliases
EvidenceCollectorInterface = IEvidenceCollector
AutomatedEvidenceCollector = EvidenceCollector
evidence_collector = EvidenceCollector()
