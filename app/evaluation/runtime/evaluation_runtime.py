"""Synchronous Evaluation Runtime for Phase 6 AI System Evaluation & Certification."""

from datetime import datetime, timezone
import os
from typing import Any, Dict, List, Optional
import uuid

from ..agent_evaluation.agent_evaluator import AgentEvaluator
from ..benchmarks.ai_capability_benchmarker import AICapabilityBenchmarker
from ..cost_intelligence.cost_business_evaluator import CostBusinessEvaluator
from ..domain.interfaces import IBaseEvaluator, IEvaluationRuntime
from ..domain.models import (
    EvaluationStatus,
    PlatformCertificationScore,
    PortfolioShowcaseReport,
)
from ..explainability.explainability_evaluator import ExplainabilityEvaluator
from ..human_experience.human_experience_evaluator import HumanExperienceEvaluator
from ..llm_evaluation.llm_evaluator import LLMEvaluator
from ..performance.performance_benchmarker import PerformanceBenchmarker
from ..rag_evaluation.rag_evaluator import RAGEvaluator
from ..reliability.reliability_evaluator import ReliabilityEvaluator
from ..reporting.portfolio_evidence_generator import PortfolioEvidenceGenerator
from ..scoring.portfolio_certification_scorer import PortfolioCertificationScorer
from ..security.security_evaluator import SecurityEvaluator


class EvaluationRuntime(IEvaluationRuntime):
    """Executes all 10 evaluators synchronously, calculates weighted certification scores, and exports evidence."""

    def __init__(
        self,
        scorer: Optional[PortfolioCertificationScorer] = None,
        evidence_generator: Optional[PortfolioEvidenceGenerator] = None,
    ):
        self.scorer = scorer or PortfolioCertificationScorer()
        self.evidence_generator = evidence_generator or PortfolioEvidenceGenerator()
        self.evaluators: Dict[str, IBaseEvaluator] = {
            "ai_capability": AICapabilityBenchmarker(),
            "llm_evaluation": LLMEvaluator(),
            "agent_evaluation": AgentEvaluator(),
            "rag_evaluation": RAGEvaluator(),
            "performance": PerformanceBenchmarker(),
            "cost_business": CostBusinessEvaluator(),
            "reliability": ReliabilityEvaluator(),
            "security": SecurityEvaluator(),
            "explainability": ExplainabilityEvaluator(),
            "human_experience": HumanExperienceEvaluator(),
        }

    def execute_all(self, output_dir: Optional[str] = None) -> PortfolioShowcaseReport:
        evaluation_id = f"EVAL-RUN-{uuid.uuid4().hex[:8].upper()}"
        executed_reports: Dict[str, Any] = {}

        # 1. Execute all 10 evaluation modules
        for key, evaluator in self.evaluators.items():
            report = evaluator.evaluate()
            executed_reports[key] = report

        # 2. Compute 6-pillar certification score
        score: PlatformCertificationScore = self.scorer.calculate_score(executed_reports)

        # 3. Build summary markdown
        summary_md = self._generate_summary_markdown(score)

        # 4. Construct showcase report
        showcase_report = PortfolioShowcaseReport(
            project_name="DocuTask Agent",
            phase="Phase 6 - AI System Evaluation, Benchmarking & Portfolio Certification",
            evaluation_id=evaluation_id,
            status=score.evaluation_status,
            score=score,
            reports=executed_reports,
            summary_markdown=summary_md,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # 5. Export all evidence files and SHA-256 manifests
        self.evidence_generator.export(showcase_report, output_dir=output_dir)

        return showcase_report

    def _generate_summary_markdown(self, score: PlatformCertificationScore) -> str:
        lines = [
            f"# DocuTask Agent Portfolio Certification Summary",
            f"",
            f"**Overall Score**: {score.overall_score:.1f}/100",
            f"**Tier**: {score.certification_tier.value}",
            f"**Status**: {score.evaluation_status.value}",
            f"",
            f"## Pillar Breakdown",
            f"| Pillar | Weight | Score | Weighted Score | Checks Passed |",
            f"| :--- | :--- | :--- | :--- | :--- |",
        ]
        for cat in score.categories:
            lines.append(
                f"| {cat.name} | {cat.weight*100:.0f}% | {cat.score:.1f}% | {cat.weighted_score:.2f} | {cat.checks_passed}/{cat.checks_total} |"
            )
        return "\n".join(lines)
