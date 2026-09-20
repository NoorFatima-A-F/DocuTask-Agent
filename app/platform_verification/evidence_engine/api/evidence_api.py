"""
Evidence Query and Management REST API Router.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceCategory,
    EvidenceArtifact,
    CertificationEvidencePackage,
    IntegrityRecord,
)
from app.platform_verification.evidence_engine.core.store import ContentAddressableStore
from app.platform_verification.evidence_engine.core.collector import EvidenceCollector
from app.platform_verification.evidence_engine.core.packager import CertificationPackageCompiler
from app.platform_verification.evidence_engine.core.search_index import EvidenceSearchIndex


class EvidenceAPI:
    """In-process REST API endpoints for evidence management."""

    def __init__(
        self,
        store: ContentAddressableStore,
        collector: EvidenceCollector,
        packager: CertificationPackageCompiler,
        search_index: EvidenceSearchIndex,
    ) -> None:
        self.store = store
        self.collector = collector
        self.packager = packager
        self.search_index = search_index

    def post_evidence(self, execution_id: str, category: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST /evidence"""
        cat = EvidenceCategory(category)
        art = self.collector.collect(execution_id=execution_id, category=cat, data=data, metadata=metadata)
        self.search_index.index_artifact(art)
        return {"artifact_id": art.artifact_id, "storage_uri": art.storage_uri, "checksum": art.checksum_sha256}

    def get_evidence(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """GET /evidence/{id}"""
        art = self.store.get_artifact(artifact_id)
        if not art:
            return None
        return art.model_dump() if hasattr(art, "model_dump") else art.dict()

    def search_evidence(self, query: str) -> List[Dict[str, Any]]:
        """GET /evidence/search?q={query}"""
        results = self.search_index.search(query)
        return [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in results]

    def verify_evidence_integrity(self, artifact_id: str) -> Dict[str, Any]:
        """POST /evidence/{id}/verify"""
        rec = self.store.verify_integrity(artifact_id)
        return rec.model_dump() if hasattr(rec, "model_dump") else rec.dict()

    def generate_package(self, execution_id: str, verification_def_id: str, metrics: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
        """POST /evidence/package"""
        pkg = self.packager.compile_package(
            execution_id=execution_id,
            verification_def_id=verification_def_id,
            metrics=metrics,
            decision=decision,
        )
        return pkg.model_dump() if hasattr(pkg, "model_dump") else pkg.dict()
