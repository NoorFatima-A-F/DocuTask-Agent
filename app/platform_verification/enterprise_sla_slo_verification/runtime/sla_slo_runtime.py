"""
Phase 3J.10: Enterprise SLA/SLO Verification Runtime Orchestrator.
"""

import time
from typing import Any, Dict, List, Optional

from ..domain.interfaces import ISLASLOVerifier
from ..domain.models import (
    BaseVerificationReport,
    SLASLOScorecard,
    VerificationManifest,
)
from ..exporter.sla_slo_exporter import SLASLOExporter
from ..scoring.sla_slo_scorer import SLASLOScorer
from ..verifiers import (
    CICDPerformancePipelineVerifier,
    ContinuousMonitoringVerifier,
    DashboardValidationVerifier,
    ErrorBudgetVerifier,
    LongRunningReliabilityVerifier,
    PerformanceAlertVerifier,
    PerformanceGovernanceVerifier,
    PerformanceIncidentVerifier,
    PerformanceRecoveryVerifier,
    PerformanceRegressionVerifier,
    SLADefinitionVerifier,
    SLOImplementationVerifier,
)


class SLASLORuntime:
    """Orchestrates synchronous execution of all 12 SLA/SLO verification engines."""

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        export_dir: Optional[str] = None,
    ):
        self.config = config or {}
        self.export_dir = export_dir or "sla_slo_verification"
        self.exporter = SLASLOExporter(export_dir=self.export_dir)
        self.scorer = SLASLOScorer()

        # Instantiate all 12 verifiers
        self.verifiers: List[ISLASLOVerifier] = [
            SLADefinitionVerifier(self.config),
            SLOImplementationVerifier(self.config),
            ErrorBudgetVerifier(self.config),
            ContinuousMonitoringVerifier(self.config),
            PerformanceRegressionVerifier(self.config),
            LongRunningReliabilityVerifier(self.config),
            PerformanceAlertVerifier(self.config),
            PerformanceIncidentVerifier(self.config),
            PerformanceRecoveryVerifier(self.config),
            DashboardValidationVerifier(self.config),
            PerformanceGovernanceVerifier(self.config),
            CICDPerformancePipelineVerifier(self.config),
        ]

    def run_all(self) -> Dict[str, Any]:
        start_time = time.time()
        reports: List[BaseVerificationReport] = []

        for verifier in self.verifiers:
            report = verifier.verify()
            reports.append(report)
            self.exporter.export_report(report)

        execution_time = time.time() - start_time
        scorecard: SLASLOScorecard = self.scorer.score(reports, execution_time_seconds=round(execution_time, 3))
        self.exporter.export_scorecard(scorecard)

        manifest: VerificationManifest = self.exporter.generate_manifest(scorecard, reports)

        return {
            "status": scorecard.status.value,
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value,
            "scorecard": scorecard,
            "reports": reports,
            "manifest": manifest,
            "export_dir": str(self.export_dir),
            "execution_time_seconds": round(execution_time, 3),
        }

    def run_verifier(self, verifier_id: str) -> Optional[BaseVerificationReport]:
        for verifier in self.verifiers:
            if (
                verifier.verifier_id.lower() == verifier_id.lower()
                or verifier.phase_id.lower() == verifier_id.lower()
            ):
                report = verifier.verify()
                self.exporter.export_report(report)
                return report
        return None
