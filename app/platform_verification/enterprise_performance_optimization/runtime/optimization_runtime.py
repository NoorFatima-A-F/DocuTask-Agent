"""
Phase 3J.11: Intelligent Performance Optimization Verification Runtime Orchestrator.
"""

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IOptimizationVerifier
from ..domain.models import (
    BaseVerificationReport,
    OptimizationScorecard,
    VerificationManifest,
)
from ..exporter.optimization_exporter import OptimizationExporter
from ..scoring.optimization_scorer import OptimizationScorer
from ..verifiers import (
    AIPipelineOptimizationVerifier,
    AutomatedRemediationVerifier,
    BottleneckRootCauseVerifier,
    CICDOptimizationPipelineVerifier,
    ContinuousOptimizationLoopVerifier,
    DatabaseOptimizationVerifier,
    IntelligentAutoscalingVerifier,
    OptimizationRecommendationVerifier,
    OptimizationSafetyVerifier,
    PerformanceAnomalyVerifier,
    PerformanceIntelligenceArchitectureVerifier,
    PredictiveCapacityPlanningVerifier,
)


class OptimizationRuntime:
    """Orchestrates synchronous execution of all 12 intelligent performance optimization verifiers."""

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        export_dir: Optional[str] = None,
    ):
        self.config = config or {}
        self.export_dir = export_dir or "performance_optimization_verification"
        self.exporter = OptimizationExporter(export_dir=self.export_dir)
        self.scorer = OptimizationScorer()

        # Instantiate all 12 verifiers
        self.verifiers: List[IOptimizationVerifier] = [
            PerformanceIntelligenceArchitectureVerifier(self.config),
            BottleneckRootCauseVerifier(self.config),
            OptimizationRecommendationVerifier(self.config),
            IntelligentAutoscalingVerifier(self.config),
            DatabaseOptimizationVerifier(self.config),
            AIPipelineOptimizationVerifier(self.config),
            PredictiveCapacityPlanningVerifier(self.config),
            PerformanceAnomalyVerifier(self.config),
            AutomatedRemediationVerifier(self.config),
            OptimizationSafetyVerifier(self.config),
            ContinuousOptimizationLoopVerifier(self.config),
            CICDOptimizationPipelineVerifier(self.config),
        ]

    def run_all(self) -> Dict[str, Any]:
        start_time = time.time()
        reports: List[BaseVerificationReport] = []

        for verifier in self.verifiers:
            report = verifier.verify()
            reports.append(report)
            self.exporter.export_report(report)

        execution_time = time.time() - start_time
        scorecard: OptimizationScorecard = self.scorer.score(reports, execution_time_seconds=round(execution_time, 3))
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
