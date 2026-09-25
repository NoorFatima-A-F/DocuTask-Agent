"""
3J.4 Master Runtime Orchestrator.

Coordinates execution of all 11 resource and capacity verifiers,
drives 6-category resource quality scoring, and exports reports.
"""

from typing import Any, Dict, List, Optional

from ..domain.interfaces import (
    IResourceExporter,
    IResourceRuntime,
    IResourceScorer,
    IResourceVerifier,
)
from ..domain.models import ResourceCapacityCertificationReport
from ..exporter.resource_capacity_exporter import ResourceCapacityExporter
from ..scoring.resource_capacity_scorer import ResourceCapacityScorer
from ..verifiers import get_all_verifiers


class ResourceCapacityRuntime(IResourceRuntime):
    """Master runtime orchestrator for Resource Utilization & Capacity Engineering."""

    def __init__(
        self,
        verifiers: Optional[List[IResourceVerifier]] = None,
        scorer: Optional[IResourceScorer] = None,
        exporter: Optional[IResourceExporter] = None,
        export_dir: str = "performance_verification",
    ):
        self.verifiers = verifiers or get_all_verifiers()
        self.scorer = scorer or ResourceCapacityScorer()
        self.exporter = exporter or ResourceCapacityExporter(export_dir=export_dir)
        self._latest_reports: Dict[str, Any] = {}
        self._latest_certification: Optional[ResourceCapacityCertificationReport] = None
        self._exported_files: List[str] = []

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes all 11 verifiers, calculates certification score, and exports manifests."""
        reports: Dict[str, Any] = {}

        key_mapping = {
            "VERIFY-3J.4.1-RESOURCE-PROFILING": "resource_profiling",
            "VERIFY-3J.4.2-CONTAINER-POLICY": "container_policy",
            "VERIFY-3J.4.3-CPU-CAPACITY": "cpu_capacity",
            "VERIFY-3J.4.4-MEMORY-LEAK": "memory_leak",
            "VERIFY-3J.4.5-WORKER-CAPACITY": "worker_capacity",
            "VERIFY-3J.4.6-QUEUE-CAPACITY": "queue_capacity",
            "VERIFY-3J.4.7-DATABASE-CAPACITY": "database_capacity",
            "VERIFY-3J.4.8-AI-RESOURCE-PROFILE": "ai_resource_profile",
            "VERIFY-3J.4.9-CAPACITY-MODELING": "capacity_modeling",
            "VERIFY-3J.4.10-AUTOSCALING-READINESS": "autoscaling_readiness",
            "VERIFY-3J.4.11-RESOURCE-ALERTING": "resource_alerting",
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

    def get_latest_certification(self) -> Optional[ResourceCapacityCertificationReport]:
        """Returns the most recent certification report if available."""
        return self._latest_certification
