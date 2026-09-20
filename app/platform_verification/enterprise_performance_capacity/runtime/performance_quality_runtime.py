"""Performance Quality Runtime Orchestrator - Phase 3J.5."""

import os
from typing import Any, Dict, List, Optional

from ..domain.interfaces import (
    IPerformanceExporter,
    IPerformanceRuntime,
    IPerformanceScorer,
    IPerformanceVerifier,
)
from ..domain.models import (
    BaseVerificationReport,
    EnterprisePerformanceCertificationReport,
    PerformanceVerificationManifest,
)
from ..exporter.performance_quality_exporter import PerformanceQualityExporter
from ..scoring.performance_quality_scorer import PerformanceQualityScorer
from ..verifiers import get_all_verifiers


class PerformanceQualityRuntime(IPerformanceRuntime):
    """Coordinates execution of all 15 verifiers, calculates certification score, and exports evidence."""

    def __init__(
        self,
        verifiers: Optional[List[IPerformanceVerifier]] = None,
        scorer: Optional[IPerformanceScorer] = None,
        exporter: Optional[IPerformanceExporter] = None,
    ):
        self.verifiers = verifiers if verifiers is not None else get_all_verifiers()
        self.scorer = scorer or PerformanceQualityScorer()
        self.exporter = exporter or PerformanceQualityExporter()
        self._latest_certification: Optional[EnterprisePerformanceCertificationReport] = None
        self._latest_manifest: Optional[PerformanceVerificationManifest] = None

    def execute_verifier(self, identifier: str) -> BaseVerificationReport:
        id_clean = identifier.lower()
        for v in self.verifiers:
            if (
                v.verifier_id.lower() == id_clean
                or (hasattr(v, "phase_id") and v.phase_id.lower() == id_clean)
                or identifier in v.verifier_id
                or identifier in v.name
            ):
                return v.verify()
        raise ValueError(f"Verifier '{identifier}' not found in registered suite.")

    def run_full_verification(self, output_dir: str = "performance_verification") -> Dict[str, Any]:
        reports: Dict[str, Any] = {}
        for verifier in self.verifiers:
            report = verifier.verify()
            reports[verifier.verifier_id] = report

        certification = self.scorer.score_reports(reports)
        self._latest_certification = certification

        manifest = self.exporter.export_all(reports, certification, output_dir=output_dir)
        self._latest_manifest = manifest

        return {
            "reports": reports,
            "certification": certification,
            "manifest": manifest,
            "passed": certification.passed,
            "overall_score": certification.overall_score,
            "tier": certification.certification_tier.value,
        }

    def get_latest_certification(self) -> Optional[EnterprisePerformanceCertificationReport]:
        return self._latest_certification

    # Async compatibility helper for async routes
    async def run_all(self, output_dir: str = "performance_verification") -> PerformanceVerificationManifest:
        res = self.run_full_verification(output_dir=output_dir)
        return res["manifest"]
