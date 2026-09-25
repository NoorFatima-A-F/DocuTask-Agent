"""Prompt Regression Testing Framework (Phase 8D).

Compares candidate prompt versions against baseline releases to prevent performance regressions.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptVersion
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.evaluation.runner import PromptEvaluationRunner


class RegressionTestReport(BaseModel):
    """Detailed comparison between baseline and candidate prompt versions."""
    prompt_id: str
    baseline_version_id: str
    candidate_version_id: str
    baseline_composite_score: float
    candidate_composite_score: float
    score_delta: float
    is_regression: bool
    allowed_regression_margin: float = 0.02
    detailed_findings: List[str] = Field(default_factory=list)


class PromptRegressionTester:
    """Executes regression test suites to block degrading prompt releases."""

    def __init__(self, eval_runner: Optional[PromptEvaluationRunner] = None):
        self.runner = eval_runner or PromptEvaluationRunner()

    def test_regression(
        self,
        baseline: PromptVersion,
        candidate: PromptVersion,
        dataset: PromptEvaluationDataset,
        inference_fn: Callable[[str], Any],
        max_allowed_drop: float = 0.02,
    ) -> RegressionTestReport:
        """Run evaluation on both versions and compare quality scores."""
        base_metrics = self.runner.evaluate_prompt(baseline, dataset, inference_fn)
        cand_metrics = self.runner.evaluate_prompt(candidate, dataset, inference_fn)

        delta = round(cand_metrics.composite_score - base_metrics.composite_score, 4)
        is_regression = delta < -max_allowed_drop

        findings = []
        if is_regression:
            findings.append(
                f"Candidate composite score ({cand_metrics.composite_score:.4f}) dropped by {abs(delta):.4f} "
                f"exceeding allowed margin {max_allowed_drop:.4f}"
            )
        else:
            findings.append(
                f"Candidate composite score ({cand_metrics.composite_score:.4f}) is within acceptable tolerance "
                f"compared to baseline ({base_metrics.composite_score:.4f})"
            )

        return RegressionTestReport(
            prompt_id=candidate.prompt_id,
            baseline_version_id=baseline.version_id,
            candidate_version_id=candidate.version_id,
            baseline_composite_score=base_metrics.composite_score,
            candidate_composite_score=cand_metrics.composite_score,
            score_delta=delta,
            is_regression=is_regression,
            allowed_regression_margin=max_allowed_drop,
            detailed_findings=findings,
        )
