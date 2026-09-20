"""
3J.3 Master Runtime Orchestrator.

Coordinates execution of all 12 performance baseline and capacity boundary verifiers,
drives 6-category quality scoring, and exports reports.
"""

from typing import Any, Dict, List, Optional

from ..domain.interfaces import (
    IPerformanceExporter,
    IPerformanceRuntime,
    IPerformanceScorer,
    IPerformanceVerifier,
)
from ..domain.models import PerformanceQualityCertificationReport
from ..exporter.performance_baseline_exporter import PerformanceBaselineExporter
from ..scoring.performance_baseline_scorer import PerformanceBaselineScorer
from ..verifiers import get_all_verifiers


class PerformanceBaselineRuntime(IPerformanceRuntime):
    """Master runtime orchestrator for the Performance Baseline & Capacity Verification subsystem."""

    def __init__(
        self,
        verifiers: Optional[List[IPerformanceVerifier]] = None,
        scorer: Optional[IPerformanceScorer] = None,
        exporter: Optional[IPerformanceExporter] = None,
        export_dir: str = "performance_verification",
    ):
        self.verifiers = verifiers or get_all_verifiers()
        self.scorer = scorer or PerformanceBaselineScorer()
        self.exporter = exporter or PerformanceBaselineExporter(export_dir=export_dir)
        self._latest_reports: Dict[str, Any] = {}
        self._latest_certification: Optional[PerformanceQualityCertificationReport] = None
        self._exported_files: List[str] = []

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes all 12 performance verifiers, calculates certification score, and exports manifests."""
        reports: Dict[str, Any] = {}

        key_mapping = {
            "VERIFY-3J.3.1-PERF-ARCHITECTURE": "performance_architecture",
            "VERIFY-3J.3.2-BASELINE-PERFORMANCE": "baseline_performance",
            "VERIFY-3J.3.3-AI-PIPELINE-PERFORMANCE": "ai_pipeline_performance",
            "VERIFY-3J.3.4-CONCURRENT-LOAD": "concurrent_load",
            "VERIFY-3J.3.5-CAPACITY-MODEL": "capacity_model",
            "VERIFY-3J.3.6-LATENCY-DISTRIBUTION": "latency_distribution",
            "VERIFY-3J.3.7-RESOURCE-UTILIZATION": "resource_utilization",
            "VERIFY-3J.3.8-DATABASE-PERFORMANCE": "database_performance",
            "VERIFY-3J.3.9-QUEUE-PERFORMANCE": "queue_capacity",
            "VERIFY-3J.3.10-WORKER-SCALING": "worker_scaling",
            "VERIFY-3J.3.11-PERF-FAILURE": "performance_failure",
            "VERIFY-3J.3.12-PERF-REGRESSION": "performance_regression",
        }

        for verifier in self.verifiers:
            report = verifier.verify()
            mapped_key = key_mapping.get(verifier.verifier_id, verifier.verifier_id.lower().replace("-", "_"))
            reports[mapped_key] = report

        certification = self.scorer.score_reports(reports)
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

    def get_latest_certification(self) -> Optional[PerformanceQualityCertificationReport]:
        """Returns the most recent certification report if available."""
        return self._latest_certification
