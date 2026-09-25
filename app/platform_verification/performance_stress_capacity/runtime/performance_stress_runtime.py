"""
Performance Stress Runtime (3J.2.14).

Coordinates execution of all performance stress and capacity boundary verifiers,
drives multi-dimensional scoring, and exports reports.
"""

from typing import Any, Dict, List, Optional

from ..domain.interfaces import (
    IPerformanceExporter,
    IPerformanceRuntime,
    IPerformanceScorer,
    IPerformanceVerifier,
)
from ..domain.models import CertificationReport
from ..exporter.performance_stress_exporter import PerformanceStressExporter
from ..scoring.performance_stress_scorer import PerformanceStressScorer
from ..verifiers import get_all_verifiers


class PerformanceStressRuntime(IPerformanceRuntime):
    """Master orchestrator for the Performance Stress & Capacity Verification subsystem."""

    def __init__(
        self,
        verifiers: Optional[List[IPerformanceVerifier]] = None,
        scorer: Optional[IPerformanceScorer] = None,
        exporter: Optional[IPerformanceExporter] = None,
        export_dir: str = "performance_verification",
    ):
        self.verifiers = verifiers or get_all_verifiers()
        self.scorer = scorer or PerformanceStressScorer()
        self.exporter = exporter or PerformanceStressExporter(export_dir=export_dir)
        self._latest_reports: Dict[str, Any] = {}
        self._latest_certification: Optional[CertificationReport] = None
        self._exported_files: List[str] = []

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes all performance verifiers, calculates certification score, and exports manifests."""
        reports: Dict[str, Any] = {}

        # Key mapping by verifier_id pattern or class
        key_mapping = {
            "VERIFY-3J.2.1-PERF-ENV": "environment_isolation",
            "VERIFY-3J.2.2-BASELINE-STRESS": "baseline_stress",
            "VERIFY-3J.2.3-PROGRESSIVE-LOAD": "progressive_load",
            "VERIFY-3J.2.4-OVERLOAD-STRESS": "overload_stress",
            "VERIFY-3J.2.5-CAPACITY-BOUNDARY": "capacity_boundary",
            "VERIFY-3J.2.7-WORKER-SCALING": "worker_scaling",
            "VERIFY-3J.2.8-DATABASE-STRESS": "database_performance",
            "VERIFY-3J.2.9-AI-PROVIDER-STRESS": "ai_provider_stress",
            "VERIFY-3J.2.10-MEMORY-STABILITY": "memory_stability",
            "VERIFY-3J.2.11-PERFORMANCE-RECOVERY": "recovery",
            "VERIFY-3J.2.13-REGRESSION-GATE": "regression",
        }

        for verifier in self.verifiers:
            report = verifier.verify()
            mapped_key = key_mapping.get(verifier.verifier_id, verifier.verifier_id.lower().replace("-", "_"))
            reports[mapped_key] = report

        # Calculate composite score & certification tier
        certification = self.scorer.score_reports(reports)

        # Export all reports & metadata
        exported_files = self.exporter.export(reports, certification)

        self._latest_reports = reports
        self._latest_certification = certification
        self._exported_files = exported_files

        return {
            "reports": reports,
            "certification": certification,
            "exported_files": exported_files,
            "passed": certification.passed,
            "score": certification.overall_score,
            "tier": certification.certification_tier.value,
        }

    def get_latest_certification(self) -> Optional[CertificationReport]:
        """Returns the most recent certification report if available."""
        return self._latest_certification
