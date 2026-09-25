"""
Phase 3M: Runtime Orchestrator for Enterprise Cloud Readiness Verification.
"""

import time
from typing import Any, Dict, List, Optional

from ..domain.interfaces import ICloudReadinessVerifier
from ..domain.models import (
    BaseVerificationReport,
    CloudReadinessScorecard,
    VerificationManifest,
)
from ..exporter.cloud_readiness_exporter import CloudReadinessExporter
from ..scoring.cloud_readiness_scorer import CloudReadinessScorer
from ..verifiers import (
    AutoScalingReadinessVerifier,
    CloudArchitectureAssessmentVerifier,
    CloudComputeResourceVerifier,
    CloudMigrationSimulationVerifier,
    CloudNetworkingVerifier,
    CloudObservabilityCompatibilityVerifier,
    CloudQueueWorkerScalabilityVerifier,
    CloudSecretManagementVerifier,
    CloudSecurityVerifier,
    CloudStorageCompatibilityVerifier,
    ContainerCloudCompatibilityVerifier,
    InfrastructureAsCodeVerifier,
    KubernetesReadinessVerifier,
    ManagedDatabaseReadinessVerifier,
    MultiCloudPortabilityVerifier,
)


class CloudReadinessRuntime:
    """
    Coordinates execution of all 15 Phase 3M cloud readiness verifiers,
    computes multi-pillar cloud scoring, and exports signed evidence artifacts.
    """

    def __init__(
        self,
        verifiers: Optional[List[ICloudReadinessVerifier]] = None,
        scorer: Optional[CloudReadinessScorer] = None,
        exporter: Optional[CloudReadinessExporter] = None,
    ):
        if verifiers is not None:
            self.verifiers = verifiers
        else:
            self.verifiers = [
                CloudArchitectureAssessmentVerifier(),
                ContainerCloudCompatibilityVerifier(),
                CloudComputeResourceVerifier(),
                CloudNetworkingVerifier(),
                CloudStorageCompatibilityVerifier(),
                ManagedDatabaseReadinessVerifier(),
                CloudQueueWorkerScalabilityVerifier(),
                AutoScalingReadinessVerifier(),
                CloudSecretManagementVerifier(),
                CloudObservabilityCompatibilityVerifier(),
                InfrastructureAsCodeVerifier(),
                KubernetesReadinessVerifier(),
                CloudSecurityVerifier(),
                MultiCloudPortabilityVerifier(),
                CloudMigrationSimulationVerifier(),
            ]
        self.scorer = scorer or CloudReadinessScorer()
        self.exporter = exporter or CloudReadinessExporter()
        self._latest_scorecard: Optional[CloudReadinessScorecard] = None
        self._latest_manifest: Optional[VerificationManifest] = None
        self._latest_reports: List[BaseVerificationReport] = []

    def execute_verifier(self, identifier: str) -> BaseVerificationReport:
        """Find and execute a single verifier by ID, phase, or partial name."""
        id_clean = identifier.lower()
        for v in self.verifiers:
            if (
                v.verifier_id.lower() == id_clean
                or (hasattr(v, "phase_id") and v.phase_id.lower() == id_clean)
                or id_clean in v.verifier_id.lower()
                or id_clean in v.name.lower()
            ):
                return v.verify()
        raise ValueError(f"Verifier '{identifier}' not found in registered Phase 3M suite.")

    def run_full_verification(self, export_dir: str = "cloud_readiness_verification") -> Dict[str, Any]:
        """Runs all 15 verifiers, calculates scorecard, and exports signed evidence artifacts."""
        start_time = time.time()
        reports: List[BaseVerificationReport] = []

        for verifier in self.verifiers:
            report = verifier.verify()
            reports.append(report)

        elapsed = time.time() - start_time
        self._latest_reports = reports

        # Compute Scorecard
        scorecard = self.scorer.score(reports, execution_time_seconds=elapsed)
        self._latest_scorecard = scorecard

        # Configure exporter directory
        self.exporter.export_dir = self.exporter.export_dir.__class__(export_dir)
        self.exporter.export_dir.mkdir(parents=True, exist_ok=True)

        # Export all reports & scorecard
        for report in reports:
            self.exporter.export_report(report)
        self.exporter.export_scorecard(scorecard)

        # Generate Manifest & Metadata
        manifest = self.exporter.generate_manifest(scorecard, reports)
        self._latest_manifest = manifest

        return {
            "reports": reports,
            "scorecard": scorecard,
            "manifest": manifest,
            "passed": scorecard.status.value == "PASSED",
            "overall_score": scorecard.overall_score,
            "tier": scorecard.certification_tier.value,
        }

    def get_latest_scorecard(self) -> Optional[CloudReadinessScorecard]:
        return self._latest_scorecard

    def get_latest_manifest(self) -> Optional[VerificationManifest]:
        return self._latest_manifest

    async def run_all(self, export_dir: str = "cloud_readiness_verification") -> VerificationManifest:
        """Async compatibility wrapper for FastAPI routes."""
        res = self.run_full_verification(export_dir=export_dir)
        return res["manifest"]
