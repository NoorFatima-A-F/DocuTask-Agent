"""
Standardized interfaces for Enterprise Verification Evidence Collection, Traceability & Audit System.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact,
    EvidenceCategory,
    AuditEvent,
    EvidenceLineageNode,
    CertificationEvidencePackage,
    AiDecisionEvidence,
    ValidationReport,
    EvidenceRole,
    IntegrityRecord,
)


class IEvidenceStore(ABC):
    @abstractmethod
    def store_artifact(self, execution_id: str, category: EvidenceCategory, content: bytes, metadata: Dict[str, Any]) -> EvidenceArtifact:
        pass

    @abstractmethod
    def retrieve_artifact(self, storage_uri: str) -> bytes:
        pass

    @abstractmethod
    def verify_integrity(self, artifact_id: str) -> IntegrityRecord:
        pass


class IEvidenceCollector(ABC):
    @abstractmethod
    def collect(self, execution_id: str, category: EvidenceCategory, data: Any, metadata: Optional[Dict[str, Any]] = None) -> EvidenceArtifact:
        pass


class IAiEvidenceCollector(ABC):
    @abstractmethod
    def capture_ai_decision(self, execution_id: str, ai_evidence: AiDecisionEvidence) -> EvidenceArtifact:
        pass


class IEvidenceValidator(ABC):
    @abstractmethod
    def validate_artifact(self, artifact: EvidenceArtifact, content: bytes) -> ValidationReport:
        pass


class IEvidenceAccessController(ABC):
    @abstractmethod
    def check_permission(self, role: EvidenceRole, action: str, classification: Any) -> bool:
        pass


class ILineageEngine(ABC):
    @abstractmethod
    def register_node(self, node_id: str, node_type: str, attributes: Dict[str, Any], checksum: str = "") -> EvidenceLineageNode:
        pass

    @abstractmethod
    def link_nodes(self, parent_id: str, child_id: str, relation: str = "derived_from") -> None:
        pass

    @abstractmethod
    def trace_lineage(self, node_id: str) -> Dict[str, Any]:
        pass


class IAuditTrail(ABC):
    @abstractmethod
    def record_event(self, actor: str, action: str, resource: str, details: Dict[str, Any], previous_state: Optional[str] = None, new_state: Optional[str] = None) -> AuditEvent:
        pass

    @abstractmethod
    def get_events_for_resource(self, resource: str) -> List[AuditEvent]:
        pass


class IEvidencePackager(ABC):
    @abstractmethod
    def compile_package(self, execution_id: str, verification_def_id: str, metrics: Dict[str, Any], decision: Dict[str, Any], approvals: Optional[List[Dict[str, Any]]] = None) -> CertificationEvidencePackage:
        pass


# Backward-compatible Interface Aliases
EvidenceStoreInterface = IEvidenceStore
EvidenceCollectorInterface = IEvidenceCollector
LineageEngineInterface = ILineageEngine
AuditLoggerInterface = IAuditTrail
EvidencePackagerInterface = IEvidencePackager
EvidenceAccessControllerInterface = IEvidenceAccessController
EvidenceValidatorInterface = IEvidenceValidator


class EvidenceSearchInterface(ABC):
    @abstractmethod
    def search_artifacts(self, execution_id: Optional[str] = None, category: Optional[Any] = None) -> List[Any]:
        pass
