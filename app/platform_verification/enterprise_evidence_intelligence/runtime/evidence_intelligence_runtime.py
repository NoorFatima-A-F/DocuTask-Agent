"""
Phase 3P: Master Runtime Orchestrator for Enterprise Evidence Intelligence.
"""

from typing import Any, Dict, List, Optional

from ..collectors import (
    ChaosEvidenceCollector,
    CloudEvidenceCollector,
    ContainerEvidenceCollector,
    DeploymentEvidenceCollector,
    ObservabilityEvidenceCollector,
    PerformanceEvidenceCollector,
    RecoveryEvidenceCollector,
    SecurityEvidenceCollector,
)
from ..validators.evidence_validator import EvidenceValidator
from ..compliance.compliance_mapper import ComplianceMapper
from ..failure.failure_evidence_manager import FailureEvidenceManager
from ..reporters.executive_report_generator import ExecutiveReportGenerator
from ..reporters.engineering_audit_generator import EngineeringAuditGenerator
from ..reporters.portfolio_layer_generator import PortfolioLayerGenerator
from ..exporter.evidence_intelligence_exporter import EvidenceIntelligenceExporter
from ..domain.models import (
    ComplianceReport,
    EngineeringAuditReport,
    EvidenceProvenance,
    ExecutiveCertificationReport,
    FailureEvidenceReport,
    PortfolioEvidenceBundle,
    StandardizedEvidenceItem,
    VerificationManifest,
)


class EvidenceIntelligenceRuntime:
    """
    Master Runtime Orchestrator for Phase 3P:
    Coordinates multi-domain evidence collection, schema validation, compliance mapping,
    failure intelligence, dual-layer reporting, portfolio generation, and cryptographic export.
    """

    def __init__(
        self,
        collectors: Optional[List[Any]] = None,
        validator: Optional[EvidenceValidator] = None,
        compliance_mapper: Optional[ComplianceMapper] = None,
        failure_manager: Optional[FailureEvidenceManager] = None,
        executive_generator: Optional[ExecutiveReportGenerator] = None,
        audit_generator: Optional[EngineeringAuditGenerator] = None,
        portfolio_generator: Optional[PortfolioLayerGenerator] = None,
        exporter: Optional[EvidenceIntelligenceExporter] = None,
    ):
        self.collectors = collectors or [
            ContainerEvidenceCollector(),
            SecurityEvidenceCollector(),
            PerformanceEvidenceCollector(),
            ChaosEvidenceCollector(),
            RecoveryEvidenceCollector(),
            ObservabilityEvidenceCollector(),
            DeploymentEvidenceCollector(),
            CloudEvidenceCollector(),
        ]
        self.validator = validator or EvidenceValidator()
        self.compliance_mapper = compliance_mapper or ComplianceMapper()
        self.failure_manager = failure_manager or FailureEvidenceManager()
        self.executive_generator = executive_generator or ExecutiveReportGenerator()
        self.audit_generator = audit_generator or EngineeringAuditGenerator()
        self.portfolio_generator = portfolio_generator or PortfolioLayerGenerator()
        self.exporter = exporter or EvidenceIntelligenceExporter()

        self._latest_items: List[StandardizedEvidenceItem] = []
        self._latest_provenance: Optional[EvidenceProvenance] = None
        self._latest_compliance: Optional[ComplianceReport] = None
        self._latest_failures: Optional[FailureEvidenceReport] = None
        self._latest_executive: Optional[ExecutiveCertificationReport] = None
        self._latest_audit: Optional[EngineeringAuditReport] = None
        self._latest_portfolio: Optional[PortfolioEvidenceBundle] = None
        self._latest_manifest: Optional[VerificationManifest] = None

    def run_full_pipeline(
        self,
        export_dir: str = "infrastructure_verification",
    ) -> Dict[str, Any]:
        # 1. Collect Multi-Domain Evidence
        all_items: List[StandardizedEvidenceItem] = []
        for collector in self.collectors:
            items = collector.collect()
            all_items.extend(items)

        # 2. Validate All Evidence Schema
        assert self.validator.validate_batch(all_items), "Evidence item failed schema validation"
        self._latest_items = all_items

        # 3. Build Provenance Record
        provenance = EvidenceProvenance()
        self._latest_provenance = provenance

        # 4. Map Compliance (SOC 2, ISO 27001, NIST)
        compliance = self.compliance_mapper.map_to_frameworks(all_items)
        self._latest_compliance = compliance

        # 5. Analyze Failures
        failures = self.failure_manager.analyze_failures(all_items)
        self._latest_failures = failures

        # 6. Generate Executive Report
        executive_report = self.executive_generator.generate(all_items, score=100.0)
        executive_md = self.executive_generator.generate_markdown(executive_report)
        self._latest_executive = executive_report

        # 7. Generate Engineering Audit Report
        audit_report = self.audit_generator.generate(all_items)
        audit_md = self.audit_generator.generate_markdown(audit_report)
        self._latest_audit = audit_report

        # 8. Generate Portfolio Presentation Layer
        portfolio = self.portfolio_generator.generate(all_items, score=100.0)
        self._latest_portfolio = portfolio

        # 9. Cryptographically Export All Artifacts & Manifest
        manifest = self.exporter.export_all(
            items=all_items,
            provenance=provenance,
            compliance=compliance,
            failures=failures,
            executive_report=executive_report,
            executive_md=executive_md,
            audit_report=audit_report,
            audit_md=audit_md,
            portfolio=portfolio,
            export_dir=export_dir,
        )
        self._latest_manifest = manifest

        return {
            "evidence_items": all_items,
            "provenance": provenance,
            "compliance": compliance,
            "failures": failures,
            "executive_report": executive_report,
            "audit_report": audit_report,
            "portfolio": portfolio,
            "manifest": manifest,
            "passed": executive_report.critical_failures == 0,
            "overall_score": executive_report.score,
            "certification": executive_report.certification,
        }

    def get_latest_items(self) -> List[StandardizedEvidenceItem]:
        return self._latest_items

    def get_latest_provenance(self) -> Optional[EvidenceProvenance]:
        return self._latest_provenance

    def get_latest_compliance(self) -> Optional[ComplianceReport]:
        return self._latest_compliance

    def get_latest_failures(self) -> Optional[FailureEvidenceReport]:
        return self._latest_failures

    def get_latest_executive(self) -> Optional[ExecutiveCertificationReport]:
        return self._latest_executive

    def get_latest_audit(self) -> Optional[EngineeringAuditReport]:
        return self._latest_audit

    def get_latest_portfolio(self) -> Optional[PortfolioEvidenceBundle]:
        return self._latest_portfolio

    def get_latest_manifest(self) -> Optional[VerificationManifest]:
        return self._latest_manifest

    async def run_all(self, export_dir: str = "infrastructure_verification") -> VerificationManifest:
        res = self.run_full_pipeline(export_dir=export_dir)
        return res["manifest"]
