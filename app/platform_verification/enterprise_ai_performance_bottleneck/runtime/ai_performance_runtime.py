"""AI Performance Verification Runtime Orchestrator — Phase 3J.9."""

from typing import Any, Dict, List, Optional

from ..domain.interfaces import (
    IAIPerformanceExporter,
    IAIPerformanceRuntime,
    IAIPerformanceScorer,
    IPerformanceVerifier,
)
from ..domain.models import (
    AIPerformanceVerificationManifest,
    BaseVerificationReport,
    EnterpriseAIPerformanceCertificationReport,
)
from ..exporter.ai_performance_exporter import AIPerformanceExporter
from ..scoring.ai_performance_scorer import AIPerformanceScorer
from ..verifiers import get_all_verifiers


class AIPerformanceRuntime(IAIPerformanceRuntime):

    def __init__(
        self,
        verifiers: Optional[List[IPerformanceVerifier]] = None,
        scorer: Optional[IAIPerformanceScorer] = None,
        exporter: Optional[IAIPerformanceExporter] = None,
    ):
        self.verifiers = verifiers if verifiers is not None else get_all_verifiers()
        self.scorer = scorer or AIPerformanceScorer()
        self.exporter = exporter or AIPerformanceExporter()
        self._latest_certification: Optional[EnterpriseAIPerformanceCertificationReport] = None

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

    def run_full_verification(self, output_dir: str = "performance_ai_verification") -> Dict[str, Any]:
        reports: Dict[str, Any] = {}
        for verifier in self.verifiers:
            report = verifier.verify()
            reports[verifier.verifier_id] = report

        certification = self.scorer.score_reports(reports)
        self._latest_certification = certification

        manifest = self.exporter.export_all(reports, certification, output_dir=output_dir)

        return {
            "reports": reports,
            "certification": certification,
            "manifest": manifest,
            "passed": certification.passed,
            "overall_score": certification.overall_score,
            "tier": certification.certification_tier.value,
        }

    def get_latest_certification(self) -> Optional[EnterpriseAIPerformanceCertificationReport]:
        return self._latest_certification

    async def run_all(self, output_dir: str = "performance_ai_verification") -> AIPerformanceVerificationManifest:
        res = self.run_full_verification(output_dir=output_dir)
        return res["manifest"]
