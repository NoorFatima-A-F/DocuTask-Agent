"""
Phase 3H.4.12: Observability Audit Certification Runtime
"""
from typing import Dict, Any
from ..verifiers import (
    EvidenceCollectionArchitectureVerifier,
    EvidenceIntegrityVerifier,
    ObservabilityAuditTrailVerifier,
    ProductionReadinessReviewer,
    ObservabilityComplianceValidator,
    ObservabilityCertificationEngine,
    CICDVerificationGate,
)
from ..exporter.observability_certification_exporter import ObservabilityCertificationExporter


class ObservabilityAuditCertificationRuntime:
    def __init__(self):
        self.arch_verifier = EvidenceCollectionArchitectureVerifier()
        self.integrity_verifier = EvidenceIntegrityVerifier()
        self.audit_verifier = ObservabilityAuditTrailVerifier()
        self.prr_reviewer = ProductionReadinessReviewer()
        self.compliance_validator = ObservabilityComplianceValidator()
        self.cert_engine = ObservabilityCertificationEngine()
        self.cicd_gate = CICDVerificationGate()
        self.exporter = ObservabilityCertificationExporter()

    def run_full_audit_and_certification(self, output_dir: str = "observability_certification") -> Dict[str, Any]:
        arch_report = self.arch_verifier.verify_collection_architecture()
        integrity_report = self.integrity_verifier.verify_evidence_integrity([m.model_dump() for m in arch_report.manifests])
        audit_trail_report = self.audit_verifier.generate_audit_trail()
        prr_report = self.prr_reviewer.execute_prr_review()
        compliance_report = self.compliance_validator.validate_compliance()

        certification_report = self.cert_engine.calculate_certification(
            prr_report=prr_report,
            compliance_report=compliance_report,
            integrity_report=integrity_report,
        )

        cicd_gate_report = self.cicd_gate.evaluate_deployment_gate(
            certification_report=certification_report,
        )

        exported_files = self.exporter.export_all_certification_evidence(
            output_dir=output_dir,
            architecture_report=arch_report,
            integrity_report=integrity_report,
            audit_trail_report=audit_trail_report,
            prr_report=prr_report,
            compliance_report=compliance_report,
            certification_report=certification_report,
            cicd_gate_report=cicd_gate_report,
        )

        return {
            "certification_report": certification_report,
            "cicd_gate_report": cicd_gate_report,
            "prr_report": prr_report,
            "compliance_report": compliance_report,
            "integrity_report": integrity_report,
            "audit_trail_report": audit_trail_report,
            "exported_files": exported_files,
            "composite_score": certification_report.composite_score,
            "tier": certification_report.certification_tier.value,
            "decision": cicd_gate_report.gate_decision.value,
        }
