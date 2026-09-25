"""
Phase 3L: Runtime Orchestrator for Enterprise Disaster Recovery & Business Continuity.
"""

import time
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IDisasterRecoveryVerifier
from ..domain.models import (
    BaseVerificationReport,
    DisasterRecoveryScorecard,
    VerificationManifest,
)
from ..exporter.disaster_recovery_exporter import DisasterRecoveryExporter
from ..scoring.disaster_recovery_scorer import DisasterRecoveryScorer
from ..verifiers import (
    BackupSecurityVerifier,
    BusinessImpactAnalysisVerifier,
    CompleteSystemRestoreVerifier,
    ConfigurationRecoveryVerifier,
    DatabaseRecoveryVerifier,
    DisasterRecoveryArchitectureVerifier,
    DRAutomationPipelineVerifier,
    DRFailureSimulationVerifier,
    PITRRecoveryVerifier,
    RecoveryObjectivesVerifier,
    RecoveryObservabilityVerifier,
    SecretRecoveryVerifier,
    StorageRecoveryVerifier,
)


class DisasterRecoveryRuntime:
    """
    Coordinates execution of all 13 Phase 3L disaster recovery verifiers,
    computes multi-pillar resilience scoring, and exports signed evidence artifacts.
    """

    def __init__(
        self,
        verifiers: Optional[List[IDisasterRecoveryVerifier]] = None,
        scorer: Optional[DisasterRecoveryScorer] = None,
        exporter: Optional[DisasterRecoveryExporter] = None,
    ):
        if verifiers is not None:
            self.verifiers = verifiers
        else:
            self.verifiers = [
                DisasterRecoveryArchitectureVerifier(),
                BusinessImpactAnalysisVerifier(),
                RecoveryObjectivesVerifier(),
                DatabaseRecoveryVerifier(),
                StorageRecoveryVerifier(),
                ConfigurationRecoveryVerifier(),
                SecretRecoveryVerifier(),
                CompleteSystemRestoreVerifier(),
                PITRRecoveryVerifier(),
                BackupSecurityVerifier(),
                DRAutomationPipelineVerifier(),
                DRFailureSimulationVerifier(),
                RecoveryObservabilityVerifier(),
            ]
        self.scorer = scorer or DisasterRecoveryScorer()
        self.exporter = exporter or DisasterRecoveryExporter()
        self._latest_scorecard: Optional[DisasterRecoveryScorecard] = None
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
        raise ValueError(f"Verifier '{identifier}' not found in registered Phase 3L suite.")

    def run_full_verification(self, export_dir: str = "disaster_recovery_verification") -> Dict[str, Any]:
        """Runs all 13 verifiers, calculates scorecard, and exports signed evidence artifacts."""
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

    def get_latest_scorecard(self) -> Optional[DisasterRecoveryScorecard]:
        return self._latest_scorecard

    def get_latest_manifest(self) -> Optional[VerificationManifest]:
        return self._latest_manifest

    async def run_all(self, export_dir: str = "disaster_recovery_verification") -> VerificationManifest:
        """Async compatibility wrapper for FastAPI routes."""
        res = self.run_full_verification(export_dir=export_dir)
        return res["manifest"]
