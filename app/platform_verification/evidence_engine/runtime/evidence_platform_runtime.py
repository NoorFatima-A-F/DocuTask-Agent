"""
Unified Enterprise Verification Evidence Platform Runtime Facade.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact,
    EvidenceCategory,
    AuditEvent,
    CertificationEvidencePackage,
    AiDecisionEvidence,
    ValidationReport,
    EvidenceRole,
    IntegrityRecord,
    EvidenceContext,
)
from app.platform_verification.evidence_engine.core.store import ContentAddressableStore
from app.platform_verification.evidence_engine.core.collector import EvidenceCollector
from app.platform_verification.evidence_engine.core.middleware import EvidenceCaptureMiddleware
from app.platform_verification.evidence_engine.core.ai_evidence import AiDecisionEvidenceCollector
from app.platform_verification.evidence_engine.core.validator import EvidenceValidationEngine
from app.platform_verification.evidence_engine.core.access_control import EvidenceAccessController
from app.platform_verification.evidence_engine.core.lineage_engine import EvidenceLineageEngine
from app.platform_verification.evidence_engine.core.tracer import OpenTelemetryTracer
from app.platform_verification.evidence_engine.core.audit_trail import ImmutableAuditTrail
from app.platform_verification.evidence_engine.core.search_index import EvidenceSearchIndex
from app.platform_verification.evidence_engine.core.packager import CertificationPackageCompiler
from app.platform_verification.evidence_engine.core.retention import RetentionPolicyManager
from app.platform_verification.evidence_engine.api.evidence_api import EvidenceAPI


class EvidencePlatformRuntime:
    """Top-level enterprise facade for the evidence collection, provenance, and audit system."""

    def __init__(self) -> None:
        self.store = ContentAddressableStore()
        self.audit_trail = ImmutableAuditTrail()
        self.collector = EvidenceCollector(self.store, self.audit_trail)
        self.middleware = EvidenceCaptureMiddleware(self.collector)
        self.ai_collector = AiDecisionEvidenceCollector(self.collector)
        self.validator = EvidenceValidationEngine()
        self.access_control = EvidenceAccessController()
        self.lineage_engine = EvidenceLineageEngine()
        self.tracer = OpenTelemetryTracer()
        self.search_index = EvidenceSearchIndex()
        self.packager = CertificationPackageCompiler(self.store)
        self.retention_manager = RetentionPolicyManager()
        self.api = EvidenceAPI(
            store=self.store,
            collector=self.collector,
            packager=self.packager,
            search_index=self.search_index,
        )

    def collect_evidence(
        self, execution_id: str, category: EvidenceCategory, data: Any, metadata: Optional[Dict[str, Any]] = None
    ) -> EvidenceArtifact:
        art = self.collector.collect(execution_id, category, data, metadata)
        self.search_index.index_artifact(art)
        return art

    def capture_ai_decision(self, execution_id: str, ai_evidence: AiDecisionEvidence) -> EvidenceArtifact:
        art = self.ai_collector.capture_ai_decision(execution_id, ai_evidence)
        self.search_index.index_artifact(art)
        return art

    def validate_artifact(self, artifact_id: str) -> ValidationReport:
        art = self.store.get_artifact(artifact_id)
        if not art:
            raise KeyError(f"Artifact '{artifact_id}' not found.")
        content = self.store.retrieve_artifact(art.storage_uri)
        return self.validator.validate_artifact(art, content)

    def compile_certification_package(
        self, execution_id: str, verification_def_id: str, metrics: Dict[str, Any], decision: Dict[str, Any]
    ) -> CertificationEvidencePackage:
        pkg = self.packager.compile_package(execution_id, verification_def_id, metrics, decision)
        self.audit_trail.record_event(
            actor="CertificationPackageCompiler",
            action="CertificationGenerated",
            resource=pkg.package_id,
            details={"manifest_hash": pkg.package_manifest_hash},
        )
        return pkg
