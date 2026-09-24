"""Master Runtime Coordinator for Phase 3H.3.12 Readiness Evidence Generation & Audit Framework."""

from typing import Dict, Any
from ..collector.readiness_evidence_collector import ReadinessEvidenceCollector
from ..schema.evidence_schema_normalizer import EvidenceSchemaNormalizer
from ..repository.evidence_repository_manager import EvidenceRepositoryManager
from ..metadata.evidence_metadata_generator import EvidenceMetadataGenerator
from ..integrity.evidence_integrity_verifier import EvidenceIntegrityVerifier
from ..timeline.readiness_timeline_reconstructor import ReadinessTimelineReconstructor
from ..failures.failure_evidence_documenter import FailureEvidenceDocumenter
from ..comparison.evidence_regression_comparator import EvidenceRegressionComparator
from ..observability.operational_dashboard_evidence_builder import OperationalDashboardEvidenceBuilder
from ..cicd.cicd_deployment_gate_evaluator import CICDDeploymentGateEvaluator
from ..scoring.evidence_quality_scorer import EvidenceQualityScorer
from ..package.final_evidence_package_generator import FinalEvidencePackageGenerator


class ReadinessAuditRuntime:
    """Master orchestrator executing the 12-part readiness evidence and audit framework."""

    def __init__(self, export_dir: str = "readiness_evidence"):
        self.collector = ReadinessEvidenceCollector()
        self.normalizer = EvidenceSchemaNormalizer()
        self.repo_manager = EvidenceRepositoryManager(base_dir=export_dir)
        self.metadata_gen = EvidenceMetadataGenerator()
        self.integrity_verifier = EvidenceIntegrityVerifier()
        self.timeline_reconstructor = ReadinessTimelineReconstructor()
        self.failure_documenter = FailureEvidenceDocumenter()
        self.regression_comparator = EvidenceRegressionComparator()
        self.dashboard_builder = OperationalDashboardEvidenceBuilder()
        self.cicd_evaluator = CICDDeploymentGateEvaluator()
        self.scorer = EvidenceQualityScorer()
        self.package_generator = FinalEvidencePackageGenerator()
        self.export_dir = export_dir

    def run_full_audit(self) -> Dict[str, Any]:
        """Runs end-to-end evidence collection, normalization, integrity verification, and packaging."""
        # 1. Collect and normalize records
        raw_evidence = self.collector.collect_raw_evidence()
        normalized_records = self.normalizer.normalize_records(raw_evidence)

        # 2. Generate metadata, timeline, failures, regression
        metadata = self.metadata_gen.generate_metadata()
        timeline_report = self.timeline_reconstructor.reconstruct_timeline()
        failure_report = self.failure_documenter.document_failures()
        regression_report = self.regression_comparator.compare_against_baseline()
        dashboard_evidence = self.dashboard_builder.build_dashboard_evidence()

        # 3. Create run directory
        self.repo_manager.create_run_directory()

        # 4. Preliminary integrity check
        initial_integrity = self.integrity_verifier.compute_and_verify_integrity(self.export_dir)

        # 5. Scorecard calculation
        scorecard = self.scorer.calculate_scorecard(
            integrity_report=initial_integrity,
            timeline_report=timeline_report,
            failure_report=failure_report,
            regression_report=regression_report,
            total_records=len(normalized_records),
        )

        # 6. Package final evidence files in readiness_evidence/
        manifests = self.package_generator.generate_package(
            metadata=metadata,
            integrity_report=initial_integrity,
            timeline_report=timeline_report,
            failure_report=failure_report,
            regression_report=regression_report,
            scorecard=scorecard,
            target_dir=self.export_dir,
        )

        # 7. Re-verify integrity after file emission
        final_integrity = self.integrity_verifier.compute_and_verify_integrity(self.export_dir)

        # 8. Evaluate CI/CD Deployment Gate
        cicd_decision = self.cicd_evaluator.evaluate_gate(scorecard, len(manifests))

        return {
            "metadata": metadata,
            "normalized_records": normalized_records,
            "timeline_report": timeline_report,
            "failure_report": failure_report,
            "regression_report": regression_report,
            "dashboard_evidence": dashboard_evidence,
            "integrity_report": final_integrity,
            "scorecard": scorecard,
            "cicd_decision": cicd_decision,
            "manifests": manifests,
        }
