"""
Phase 3H.4.12: Enterprise Observability Evidence, Audit & Certification - Abstract Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    EvidenceCollectionArchitectureReport,
    EvidenceIntegrityReport,
    ObservabilityAuditTrailReport,
    ProductionReadinessReviewReport,
    ObservabilityComplianceReport,
    ObservabilityCertificationReport,
    CICDGateReport,
)


class IEvidenceCollectionArchitectureVerifier(ABC):
    @abstractmethod
    def verify_collection_architecture(self) -> EvidenceCollectionArchitectureReport:
        pass


class IEvidenceIntegrityVerifier(ABC):
    @abstractmethod
    def verify_evidence_integrity(self, manifests: List[Dict[str, Any]]) -> EvidenceIntegrityReport:
        pass


class IObservabilityAuditTrailVerifier(ABC):
    @abstractmethod
    def generate_audit_trail(self) -> ObservabilityAuditTrailReport:
        pass


class IProductionReadinessReviewer(ABC):
    @abstractmethod
    def execute_prr_review(self) -> ProductionReadinessReviewReport:
        pass


class IObservabilityComplianceValidator(ABC):
    @abstractmethod
    def validate_compliance(self) -> ObservabilityComplianceReport:
        pass


class ICertificationEngine(ABC):
    @abstractmethod
    def calculate_certification(
        self,
        prr_report: ProductionReadinessReviewReport,
        compliance_report: ObservabilityComplianceReport,
        integrity_report: EvidenceIntegrityReport,
    ) -> ObservabilityCertificationReport:
        pass


class ICICDVerificationGate(ABC):
    @abstractmethod
    def evaluate_deployment_gate(
        self,
        certification_report: ObservabilityCertificationReport,
    ) -> CICDGateReport:
        pass


class IObservabilityCertificationExporter(ABC):
    @abstractmethod
    def export_all_certification_evidence(
        self,
        output_dir: str,
        architecture_report: EvidenceCollectionArchitectureReport,
        integrity_report: EvidenceIntegrityReport,
        audit_trail_report: ObservabilityAuditTrailReport,
        prr_report: ProductionReadinessReviewReport,
        compliance_report: ObservabilityComplianceReport,
        certification_report: ObservabilityCertificationReport,
        cicd_gate_report: CICDGateReport,
    ) -> List[str]:
        pass
